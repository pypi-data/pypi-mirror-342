"""Helpers to read/write gtlf/glb files."""

from typing import Callable, Dict, List, Optional, Tuple, Type
import pprint

from jax.numpy import float32

try:
    from dataclasses import dataclass, field

    import jax
    import jax.numpy as jnp
    from jax.tree_util import Partial

    import pygltflib
    from pygltflib.validator import summary

    from sfx.helpers.math import (
        get_quaternion_from_frames,
        vectors_to_quaternion,
        rescale,
        # create_voronoi_from_miller_indices,
        # generate_gaussian_on_sphere,
        get_quaternion_from_axis,
        get_rotation_axis,
    )

    _einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)
except ImportError as e:
    __all__ = []
    raise e
else:
    __all__ = [
        "data_to_glb",
        "vectors_to_glb",
        "pointclouds_to_glb",
    ]
finally:
    pass


@dataclass(kw_only=True)
class _GLTFAnimation:
    samplers: List = field(default_factory=list)
    channels: List = field(default_factory=list)


@dataclass(kw_only=True)
class _NewData:
    data: jax.Array
    count: int
    min: List[float]
    max: List[float]
    type: str | int
    component_type: str | int
    target: int
    buffer: int = 0
    name: str | None = None
    accessor_extensions: Dict = field(default_factory=dict)
    accessor_extras: Dict = field(default_factory=dict)
    bufferview_extensions: Dict = field(default_factory=dict)
    bufferview_extras: Dict = field(default_factory=dict)


@dataclass(kw_only=True)
class _GLTFState:
    binary_blob: bytes = field(default_factory=bytes)
    gltf: pygltflib.GLTF2 = field(default_factory=pygltflib.GLTF2)
    bufferView_idx: int = 0
    accessor_idx: int = 0
    animation: _GLTFAnimation = field(default_factory=_GLTFAnimation)

    def update_data(self, new_data: _NewData):
        new_binary_blob = new_data.data.tobytes()

        if not len(self.binary_blob):
            _len_binary_blob = 0
        else:
            _len_binary_blob = len(self.binary_blob)

        _len_new_binary_blob = len(new_binary_blob)

        if not len(self.gltf.bufferViews):
            self.gltf.bufferViews = [
                pygltflib.BufferView(
                    buffer=new_data.buffer,
                    # 0 if bufferview_index is None else bufferview_index,
                    byteOffset=_len_binary_blob,
                    byteLength=_len_new_binary_blob,
                    target=new_data.target,
                    extensions=new_data.bufferview_extensions,
                    extras=new_data.bufferview_extras,
                )
            ]
            self.bufferView_idx = 0
        else:
            self.gltf.bufferViews += [
                pygltflib.BufferView(
                    buffer=new_data.buffer,
                    # 0 if bufferview_index is None else bufferview_index,
                    byteOffset=_len_binary_blob,
                    byteLength=_len_new_binary_blob,
                    target=new_data.target,
                    extensions=new_data.bufferview_extensions,
                    extras=new_data.bufferview_extras,
                )
            ]
            self.bufferView_idx += 1

        if not len(self.gltf.accessors):
            self.gltf.accessors = [
                pygltflib.Accessor(
                    bufferView=self.bufferView_idx,
                    componentType=new_data.component_type,
                    count=new_data.count,
                    type=new_data.type,
                    min=new_data.min,
                    max=new_data.max,
                    name=new_data.name,
                    extensions=new_data.accessor_extensions,
                    extras=new_data.accessor_extras,
                )
            ]
            self.accessor_idx = 0
        else:
            self.gltf.accessors += [
                pygltflib.Accessor(
                    bufferView=self.bufferView_idx,
                    componentType=new_data.component_type,
                    count=new_data.count,
                    type=new_data.type,
                    min=new_data.min,
                    max=new_data.max,
                    name=new_data.name,
                    extensions=new_data.accessor_extensions,
                    extras=new_data.accessor_extras,
                )
            ]
            self.accessor_idx += 1

        self.binary_blob += new_binary_blob
        return None

    def update_animation_data(
        self,
        mapped,
        path,
        set_input_nb: Optional[Callable] = None,  # lambda nb: nb,
        set_output_nb: Optional[Callable] = None,  # lambda nb: nb,
        set_sampler_nb: Callable = lambda nb: nb,
        set_node_nb: Callable = lambda nb: nb,
        interpolation="STEP",
        sampler_extensions: Dict = {},
        sampler_extras: Dict = {},
        channel_extensions: Dict = {},
        channel_extras: Dict = {},
    ):
        if set_input_nb and set_output_nb:
            self.animation.samplers.extend(
                [
                    pygltflib.AnimationSampler(
                        input=set_input_nb(i),
                        output=set_output_nb(i),
                        interpolation=interpolation,
                        extensions=sampler_extensions,
                        extras=sampler_extras,
                    )
                    for i in mapped
                ]
            )

        self.animation.channels.extend(
            [
                pygltflib.AnimationChannel(
                    sampler=set_sampler_nb(i),
                    target=pygltflib.AnimationChannelTarget(
                        node=set_node_nb(i),
                        path=path,
                    ),
                    extensions=channel_extensions,
                    extras=channel_extras,
                )
                for i in mapped
            ]
        )

    def update_buffers(self):
        self.gltf.buffers.extend(
            [
                pygltflib.Buffer(byteLength=len(self.binary_blob)),
            ]
        )

    def update_animations(self, name: str = "animation"):
        self.gltf.animations.extend(
            [
                pygltflib.Animation(
                    name=name,
                    samplers=self.animation.samplers,
                    channels=self.animation.channels,
                )
            ]
        )

    def update_binary_blob(self):
        self.gltf.set_binary_blob(self.binary_blob)

    def update_nodes(self, nodes):
        self.gltf.nodes.extend(nodes)

    def update_meshes(self, meshes):
        self.gltf.meshes.extend(meshes)

    def update_scenes(self, scenes):
        self.gltf.scenes.extend(scenes)

    def update_materials(self, materials):
        self.gltf.materials.extend(materials)


def create_trajectory(
    data,
    gltf_state,
):
    total_length = len(data)
    mesh_offset = len(gltf_state.gltf.meshes)
    node_offset = len(gltf_state.gltf.nodes)

    # Trajectory meshes
    gltf_state.update_meshes(
        [
            pygltflib.Mesh(
                name=f"Trajectory Mesh {i}",
                primitives=[
                    pygltflib.Primitive(
                        attributes=pygltflib.Attributes(
                            POSITION=gltf_state.accessor_idx + i + 1,
                        ),
                        indices=gltf_state.accessor_idx + 1,
                        mode=pygltflib.LINES,
                    )
                ],
            )
            for i in range(1, data.coordinates.nbparticles + 1)
        ]
    )

    line_total_length = 2 * total_length

    ## Trajectory indices
    trajectory_indices = jnp.arange(0, line_total_length, dtype=jnp.uint32)
    gltf_state.update_data(
        _NewData(
            data=trajectory_indices,
            component_type=pygltflib.UNSIGNED_INT,
            count=line_total_length,
            type=pygltflib.SCALAR,
            max=[int(trajectory_indices.max())],
            min=[int(trajectory_indices.min())],
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
        )
    )

    for i in range(data.coordinates.nbparticles):
        trajectory = jnp.nan_to_num(
            jnp.stack(
                [
                    data.coordinates.position[:, i, :],
                    data.coordinates.position[:, i, :]
                    + data.future_motions.position[:, i, :],
                ],
                axis=-2,
            ).astype(jnp.float32)
        )

        gltf_state.update_data(
            _NewData(
                data=trajectory,
                component_type=pygltflib.FLOAT,
                count=line_total_length,
                type=pygltflib.VEC3,
                max=trajectory.max(axis=(0, 1)).tolist(),
                min=trajectory.min(axis=(0, 1)).tolist(),
                target=pygltflib.ARRAY_BUFFER,
            )
        )

    _nb_trajectories = data.coordinates.nbparticles
    _nbdigit = len(str(_nb_trajectories))
    node_list = list(range(1 + node_offset, 1 + node_offset + _nb_trajectories))
    mesh_list = list(range(mesh_offset, mesh_offset + _nb_trajectories))

    gltf_state.update_nodes([pygltflib.Node(name="Trajectories", children=node_list)])
    gltf_state.update_nodes(
        [
            pygltflib.Node(
                name=f"Trajectory Particle {{n:0>{_nbdigit}d}}".format(n=i),
                mesh=m,
            )
            for i, m in enumerate(mesh_list, start=1)
        ]
    )

    return


def data_to_glb(data, filename):
    _points = jnp.asarray(
        [
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
        ],
        dtype=jnp.float32,
    )
    _triangles = jnp.asarray(
        [
            [0, 1, 2],
            [3, 2, 1],
            [1, 0, 4],
            [5, 4, 0],
            [3, 1, 6],
            [4, 6, 1],
            [2, 3, 7],
            [6, 7, 3],
            [0, 2, 5],
            [7, 5, 2],
            [5, 7, 4],
            [6, 4, 7],
        ],
        dtype=jnp.uint8,
    )

    _nbdigit = len(str(data.coordinates.nbparticles))
    _ref_frame = jnp.eye(3)
    node_list = list(range(data.coordinates.nbparticles + 1))

    gltf_state = _GLTFState()
    gltf_state.update_data(
        _NewData(
            data=_triangles.flatten(),
            count=_triangles.size,
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
            component_type=pygltflib.UNSIGNED_BYTE,
            type=pygltflib.SCALAR,
            max=[int(_triangles.max())],
            min=[int(_triangles.min())],
        ),
    )

    gltf_state.update_data(
        _NewData(
            data=_points,
            component_type=pygltflib.FLOAT,
            count=len(_points),
            type=pygltflib.VEC3,
            max=_points.max(axis=0).tolist(),
            min=_points.min(axis=0).tolist(),
            target=pygltflib.ARRAY_BUFFER,
        )
    )

    # Add Scene
    gltf_state.update_scenes([pygltflib.Scene(nodes=node_list[:1])])

    # Add Particles Meshes
    gltf_state.update_meshes(
        [
            pygltflib.Mesh(
                name="Particle Mesh",
                primitives=[
                    pygltflib.Primitive(
                        attributes=pygltflib.Attributes(POSITION=1),
                        indices=0,
                    )
                ],
            )
        ]
    )

    # Add Default Material
    # gltf_state.update_materials([pygltflib.Material()])
    def _get_quaternion(before: jax.Array, after: jax.Array) -> jax.Array:

        return get_quaternion_from_axis(get_rotation_axis(before, after))

    def _create_initial_quaternions(coordinates):

        if hasattr(coordinates, "orientation"):
            if coordinates.orientation.ndim == 4:
                output = (
                    jnp.nan_to_num(
                        # jax.vmap(get_quaternion_from_frames, in_axes=(None, 0))(
                        jax.vmap(_get_quaternion, in_axes=(None, 0))(
                            jnp.eye(coordinates.orientation.shape[-1]),
                            coordinates.orientation[0],
                        )
                    )
                    .astype(jnp.float32)
                    .tolist()
                )
            elif coordinates.orientation.ndim == 3:
                output = (
                    jnp.nan_to_num(
                        jax.vmap(vectors_to_quaternion, in_axes=(None, 0))(
                            jnp.zeros(coordinates.orientation.shape[-1]).at[1].set(1.0),
                            coordinates.orientation[0],
                        )
                    )
                    .astype(jnp.float32)
                    .tolist()
                )

        else:
            output = (
                jnp.zeros((*coordinates.position[0].shape[:-1], 4))
                .at[..., -1]
                .set(1.0)
                .astype(jnp.float32)
                .tolist()
            )
        return output

    # Add the 'System' parent node, containing all the particle nodes
    gltf_state.update_nodes([pygltflib.Node(name="System", children=node_list[1:])])
    gltf_state.update_nodes(
        [
            pygltflib.Node(
                name=f"Particle {{n:0>{_nbdigit}d}}".format(n=n),
                mesh=m,
                translation=position,
                rotation=rotation,
            )
            for n, m, position, rotation in zip(
                node_list[1:],
                # Mesh index points to the same default mesh
                [0] * data.coordinates.nbparticles,
                jnp.nan_to_num(data.coordinates.position[0])
                .astype(jnp.float32)
                .tolist(),
                _create_initial_quaternions(data.coordinates),
            )
        ]
    )

    if len(data.time) > 1:
        total_length = len(data.time)

        time = jnp.true_divide(
            jnp.arange(1, 1 + total_length, dtype=jnp.float32),
            24,
        )

        gltf_state.update_data(
            _NewData(
                data=time,
                component_type=pygltflib.FLOAT,
                count=len(time),
                type=pygltflib.SCALAR,
                min=[float(time[0])],
                max=[float(time[-1])],
                target=pygltflib.ARRAY_BUFFER,
            ),
        )

        time_accessor_index = gltf_state.accessor_idx
        sampler_accessor_index = gltf_state.accessor_idx

        _translations = jnp.nan_to_num(
            data.coordinates.position.transpose(1, 0, 2)
        ).astype(jnp.float32)

        for i in range(data.coordinates.nbparticles):
            gltf_state.update_data(
                _NewData(
                    data=_translations[i],
                    component_type=pygltflib.FLOAT,
                    count=total_length,
                    type=pygltflib.VEC3,
                    min=_translations[i].min(axis=0).tolist(),
                    max=_translations[i].max(axis=0).tolist(),
                    target=pygltflib.ARRAY_BUFFER,
                ),
            )

        gltf_state.update_animation_data(
            mapped=range(data.coordinates.nbparticles),
            path="translation",
            set_input_nb=lambda _: time_accessor_index,
            set_output_nb=lambda nb: sampler_accessor_index + nb + 1,
            set_sampler_nb=lambda nb: nb,
            set_node_nb=lambda nb: nb + 1,
        )

        if "orientation" in data.coordinates:

            def _create_quaternions(coordinates, total_length):

                if coordinates.orientation.ndim == 4:
                    output = jax.vmap(
                        jax.vmap(
                            lambda ref, rot: jax.lax.cond(
                                jnp.all(jnp.isnan(rot)),
                                lambda: _get_quaternion(ref, ref),
                                lambda: _get_quaternion(ref, rot),
                                # lambda: get_quaternion_from_frames(ref, ref),
                                # lambda: get_quaternion_from_frames(ref, rot),
                            ),
                            in_axes=(None, 0),
                        ),
                        in_axes=(None, 0),
                    )(
                        jnp.eye(coordinates.orientation.shape[-1]),
                        coordinates.orientation.transpose(1, 0, 2, 3).reshape(
                            coordinates.nbparticles,
                            total_length,
                            *coordinates.orientation.shape[-2:],
                        ),
                    ).astype(
                        jnp.float32
                    )
                elif coordinates.orientation.ndim == 3:
                    rot_dof = data.coordinates.orientation.shape[-1]
                    output = (
                        vectors_to_quaternion(
                            jnp.zeros(rot_dof).at[1].set(1.0),
                            coordinates.orientation.transpose(1, 0, 2).reshape(
                                -1, rot_dof
                            ),
                        )
                        .reshape(coordinates.nbparticles, total_length, 4)
                        .astype(jnp.float32)
                    )

                return jnp.nan_to_num(output)

            _rotations = _create_quaternions(data.coordinates, total_length)

            for i in range(data.coordinates.nbparticles):
                gltf_state.update_data(
                    _NewData(
                        data=_rotations[i],
                        component_type=pygltflib.FLOAT,
                        count=total_length,
                        type=pygltflib.VEC4,
                        min=_rotations[i].min(axis=0).tolist(),
                        max=_rotations[i].max(axis=0).tolist(),
                        target=pygltflib.ARRAY_BUFFER,
                    ),
                )

            gltf_state.update_animation_data(
                mapped=node_list[1:],
                path="rotation",
                set_input_nb=lambda _: time_accessor_index,
                set_output_nb=lambda nb: time_accessor_index
                + data.coordinates.nbparticles
                + nb,
                set_sampler_nb=lambda nb: data.coordinates.nbparticles + nb - 1,
                set_node_nb=lambda nb: nb,
            )

        gltf_state.update_animations(name="dof_animations")
        create_trajectory(data, gltf_state)

    gltf_state.update_buffers()
    gltf_state.update_binary_blob()

    summary(gltf_state.gltf)
    gltf_state.gltf.save(f"{filename}.glb")
    return


def vectors_to_glb(
    *vectors, positions=None, names=None, filename="vectors", **attributes
):
    """"""

    def flatten_list(x):
        return jax.tree_util.tree_flatten(
            x, is_leaf=lambda y: not isinstance(y, (list, tuple))
        )[0]

    _nb_vector_types = len(vectors)
    _nb_vectors = vectors[0].shape[-2]

    _nbTypeDigit = len(str(_nb_vector_types))
    _nbdigit = len(str(_nb_vectors))

    if not names:
        names = [f"{t:>0{_nbTypeDigit}d}" for t in range(_nb_vector_types)]

    node_names = [
        [
            f"vectors_{name}_{{n:>0{_nbdigit}d}}".format(name=name, n=n)
            for n in range(_nb_vectors)
        ]
        for name in names
    ]

    node_groups = [t + 1 for t in range(_nb_vector_types)]
    node_list = [
        [node_groups[-1] + t * _nb_vectors + n + 1 for n in range(_nb_vectors)]
        for t in range(_nb_vector_types)
    ]

    _mesh_points = (
        jnp.zeros((2, vectors[0].shape[-1]), dtype=jnp.float32).at[-1, -2].set(1.0)
    )
    _mesh_indices = jnp.arange(2, dtype=jnp.uint8)

    gltf_state = _GLTFState()
    gltf_state.update_data(
        _NewData(
            data=_mesh_indices.flatten(),
            count=_mesh_indices.size,
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
            component_type=pygltflib.UNSIGNED_BYTE,
            type=pygltflib.SCALAR,
            max=[int(_mesh_indices.max())],
            min=[int(_mesh_indices.min())],
        ),
    )

    gltf_state.update_data(
        _NewData(
            data=_mesh_points,
            component_type=pygltflib.FLOAT,
            count=len(_mesh_points),
            type=pygltflib.VEC3,
            max=_mesh_points.max(axis=0).tolist(),
            min=_mesh_points.min(axis=0).tolist(),
            target=pygltflib.ARRAY_BUFFER,
        )
    )

    # Add Scene
    gltf_state.update_scenes([pygltflib.Scene(nodes=[0])])

    # Add main node
    gltf_state.update_nodes([pygltflib.Node(name=f"Vectors", children=node_groups)])

    # Add Particles Meshes
    gltf_state.update_meshes(
        [
            pygltflib.Mesh(
                name=f"vector",
                primitives=[
                    pygltflib.Primitive(
                        indices=0,
                        attributes=pygltflib.Attributes(POSITION=1, **attributes),
                        mode=pygltflib.LINES,
                        # targets=pygltflib.Targets(POSITION=_mult * i + 2, **attributes)
                    )
                ],
            )
        ]
    )

    # Add Default Material
    # gltf_state.update_materials([pygltflib.Material()])

    def _create_initial_quaternions(vectors):

        output = (
            jnp.nan_to_num(
                jax.vmap(
                    lambda vFrom, vTo: vectors_to_quaternion(
                        vFrom, vTo, is_normalized=False
                    ),
                    in_axes=(None, 0),
                )(
                    jnp.zeros(vectors.shape[-1]).at[-2].set(1.0),
                    vectors,
                )
            )
            .astype(jnp.float32)
            .tolist()
        )

        return output

    gltf_state.update_nodes(
        [
            pygltflib.Node(name=f"{name}", children=node_list[i])
            for i, name in enumerate(names)
        ]
    )

    if positions is not None:
        gltf_state.update_nodes(
            [
                pygltflib.Node(
                    name=f"{name}",
                    mesh=0,
                    translation=position,
                    rotation=rotation,
                    extras={
                        "index": i,
                    },
                )
                for names, vector in zip(node_names, vectors)
                for i, (name, position, rotation) in enumerate(
                    zip(
                        names,
                        jnp.nan_to_num(positions[0]).astype(jnp.float32).tolist(),
                        _create_initial_quaternions(vector[0]),
                    )
                )
            ]
        )
    else:
        gltf_state.update_nodes(
            [
                pygltflib.Node(
                    name=f"{name}",
                    mesh=0,
                    translation=[0.0, 0.0, 0.0],
                    rotation=rotation,
                    extras={
                        "index": i,
                    },
                )
                for names, vector in zip(node_names, vectors)
                for i, (name, rotation) in enumerate(
                    zip(
                        names,
                        _create_initial_quaternions(vector[0]),
                    )
                )
            ]
        )

    if len(vectors[0]) > 1:
        total_length = len(vectors[0])

        time = jnp.true_divide(
            jnp.arange(1, 1 + total_length, dtype=jnp.float32),
            24,
        )

        gltf_state.update_data(
            _NewData(
                data=time,
                component_type=pygltflib.FLOAT,
                count=len(time),
                type=pygltflib.SCALAR,
                min=[float(time[0])],
                max=[float(time[-1])],
                target=pygltflib.ARRAY_BUFFER,
            ),
        )

        time_accessor_index = gltf_state.accessor_idx
        sampler_accessor_index = gltf_state.accessor_idx

        _offset = 0
        if positions is not None:
            _translations = jnp.nan_to_num(positions.transpose(1, 0, 2)).astype(
                jnp.float32
            )

            for _trans in _translations:
                gltf_state.update_data(
                    _NewData(
                        data=_trans,
                        component_type=pygltflib.FLOAT,
                        count=total_length,
                        type=pygltflib.VEC3,
                        min=_trans.min(axis=0).tolist(),
                        max=_trans.max(axis=0).tolist(),
                        target=pygltflib.ARRAY_BUFFER,
                    ),
                )

            for n, nodes in enumerate(node_list):
                if n == 0:
                    gltf_state.update_animation_data(
                        mapped=range(len(nodes)),
                        path="translation",
                        set_input_nb=lambda _: time_accessor_index,
                        set_output_nb=lambda nb: sampler_accessor_index + nb + 1,
                        set_sampler_nb=lambda nb: nb,
                        set_node_nb=lambda nb: nodes[nb],
                    )
                else:
                    gltf_state.update_animation_data(
                        mapped=range(len(nodes)),
                        path="translation",
                        set_sampler_nb=lambda nb: nb,
                        set_node_nb=lambda nb: nodes[nb],
                    )
            _offset = _nb_vectors
        else:
            pass

        def _create_quaternions(vectors):
            nbsteps, nbpoints, nbdof = vectors.shape
            output = (
                vectors_to_quaternion(
                    jnp.zeros(nbdof).at[1].set(1.0),
                    vectors.transpose(1, 0, 2).reshape(-1, nbdof),
                    is_normalized=False,
                )
                .reshape(nbpoints, nbsteps, 4)
                .astype(jnp.float32)
            )

            return jnp.nan_to_num(output)

        _rotations = jax.tree_util.tree_map(_create_quaternions, vectors)

        for i, (rots, nodes) in enumerate(zip(_rotations, node_list)):
            _sampler_accessor_index = gltf_state.accessor_idx

            for rot in rots:
                gltf_state.update_data(
                    _NewData(
                        data=rot,
                        component_type=pygltflib.FLOAT,
                        count=total_length,
                        type=pygltflib.VEC4,
                        min=rot.min(axis=0).tolist(),
                        max=rot.max(axis=0).tolist(),
                        target=pygltflib.ARRAY_BUFFER,
                    ),
                )

            gltf_state.update_animation_data(
                mapped=range(len(nodes)),
                path="rotation",
                set_input_nb=lambda _: time_accessor_index,
                set_output_nb=lambda nb: _sampler_accessor_index + nb + 1,
                set_sampler_nb=lambda nb: (i + 1) * _offset + nb,
                set_node_nb=lambda nb: nodes[nb],
            )

        gltf_state.update_animations(name="vectors_animations")

    gltf_state.update_buffers()
    gltf_state.update_binary_blob()

    summary(gltf_state.gltf)
    gltf_state.gltf.save(f"{filename}.glb")

    return


def pointclouds_to_glb(
    *pointclouds: jax.Array,
    attributes: Optional[List[Dict[str, Dict]]] = None,
    positions: Optional[jax.Array] = None,
    names: Optional[List[str]] = None,
    filename: str = "pointclouds",
):
    """"""

    def _create_ptp(amin, amax):

        _ptp = amax - amin
        ptp = jax.lax.cond(
            jnp.sum(_ptp),
            lambda: jnp.where(_ptp, _ptp, amax),
            lambda: jnp.where(amax, amax, 1.0),
        )
        return ptp

    def _rescale(
        array: jax.Array,
        amin: Optional[jax.Array] = None,
        amax: Optional[jax.Array] = None,
    ):

        if amin is None:
            amin = jnp.nanmin(array, axis=0)

        if amax is None:
            amax = jnp.nanmax(array, axis=0)

        return jnp.true_divide(array, _create_ptp(amin, amax))

    _nb_vector_types = len(pointclouds)
    _nb_pointclouds = pointclouds[0].shape[1]

    _nbTypeDigit = len(str(_nb_vector_types))
    _nbdigit = len(str(_nb_pointclouds))

    if not names:
        names = [f"{t:>0{_nbTypeDigit}d}" for t in range(1, _nb_vector_types + 1)]

    node_names = [
        [
            f"pointcloud_{name}_{{n:>0{_nbdigit}d}}".format(name=name, n=n)
            for n in range(1, _nb_pointclouds + 1)
        ]
        for name in names
    ]

    node_groups = [t + 1 for t in range(_nb_vector_types)]
    node_list = [
        [node_groups[-1] + t * _nb_pointclouds + n + 1 for n in range(_nb_pointclouds)]
        for t in range(_nb_vector_types)
    ]

    _mesh_pointclouds = tuple(
        jnp.zeros(pc.shape[-2:], dtype=jnp.float32) for pc in pointclouds
    )
    _mesh_indices = [pc.shape[-2] for pc in pointclouds]

    gltf_state = _GLTFState()

    # Target vectors
    _minmax = []
    _targets_accessor = []
    for pc in pointclouds:
        _nbsteps, _nbnode, _nbpoints, _dim = pc.shape
        _pc = pc.reshape(_nbsteps * _nbnode, _nbpoints, _dim)

        _pc_min = jnp.nanmin(_pc, axis=0)
        _pc_max = jnp.nanmax(_pc, axis=0)

        _minmax.append((_pc_min, _pc_max))
        _ptp = _create_ptp(_pc_min, _pc_max)
        _basis_vectors = _einsum(
            "ij,j->ij",
            jnp.eye(_nbpoints * _dim),
            _ptp.flatten(),
        ).astype(jnp.float32)

        __targets_accessor = []
        for b in _basis_vectors:
            gltf_state.update_data(
                _NewData(
                    data=b,
                    component_type=pygltflib.FLOAT,
                    count=_nbpoints,
                    type=pygltflib.VEC3,
                    min=_ptp.min(axis=0).astype(jnp.float32).tolist(),
                    max=_ptp.max(axis=0).astype(jnp.float32).tolist(),
                    target=pygltflib.ARRAY_BUFFER,
                ),
            )
            __targets_accessor.append(gltf_state.accessor_idx)
        _targets_accessor.append(__targets_accessor)

    _minmax = tuple(_minmax)

    # Indices
    _indices_accessor = []
    for mi in _mesh_indices:
        _indices = jnp.arange(mi, dtype=jnp.uint8)
        gltf_state.update_data(
            _NewData(
                data=_indices.flatten(),
                count=_indices.size,
                target=pygltflib.ELEMENT_ARRAY_BUFFER,
                component_type=pygltflib.UNSIGNED_BYTE,
                type=pygltflib.SCALAR,
                max=[int(_indices.max())],
                min=[int(_indices.min())],
            ),
        )
        _indices_accessor.append(gltf_state.accessor_idx)

    _positions_accessor = []
    for mpc in _mesh_pointclouds:
        gltf_state.update_data(
            _NewData(
                data=mpc.flatten(),
                component_type=pygltflib.FLOAT,
                count=len(mpc),
                type=pygltflib.VEC3,
                max=mpc.max(axis=0).tolist(),
                min=mpc.min(axis=0).tolist(),
                target=pygltflib.ARRAY_BUFFER,
            )
        )
        _positions_accessor.append(gltf_state.accessor_idx)

    _attributes_accessor: List[Dict] = []
    if attributes is not None:
        for attrs in attributes:
            for attr_name, attr in attrs.items():
                _attr = attr["data"].astype(jnp.float32)
                _max = _attr.max(axis=0).tolist() if _attr.ndim else _attr.max()
                _min = _attr.min(axis=0).tolist() if _attr.ndim else _attr.min()

                gltf_state.update_data(
                    _NewData(
                        data=_attr.flatten(),
                        component_type=attr["component_type"],
                        count=len(_attr),
                        type=attr["type"],
                        max=_max,
                        min=_min,
                        target=pygltflib.ARRAY_BUFFER,
                    )
                )

                _name = attr_name  # if attr_name.startswith("_") else f"_{attr_name}"
                _attributes_accessor.append({_name: gltf_state.accessor_idx})
    else:
        _attributes_accessor += [{}] * len(_positions_accessor)

    # Add Scene
    gltf_state.gltf.scene = 0
    gltf_state.update_scenes([pygltflib.Scene(nodes=[0])])

    # Add main node
    gltf_state.update_nodes([pygltflib.Node(name=f"pointclouds", children=node_groups)])
    # assert False, ""

    # Add Particles Meshes
    gltf_state.update_meshes(
        [
            pygltflib.Mesh(
                name=f"point_{m}",
                primitives=[
                    pygltflib.Primitive(
                        indices=i,
                        attributes=pygltflib.Attributes(POSITION=pos, **attrs),
                        mode=pygltflib.POINTS,
                        targets=[pygltflib.Attributes(POSITION=tt) for tt in t],
                    )
                ],
                weights=(
                    [-1.0] * len(ppc.flatten())
                    if len(pc) > 1
                    else _rescale(ppc, mnmx[0], mnmx[1])
                    .flatten()
                    .astype(jnp.float32)
                    .tolist()
                ),
            )
            for m, (i, pos, attrs, t, mnmx, pc) in enumerate(
                zip(
                    _indices_accessor,
                    _positions_accessor,
                    _attributes_accessor,
                    _targets_accessor,
                    _minmax,
                    pointclouds,
                )
            )
            for ppc in pc[0]
        ]
    )

    # Add Default Material
    # gltf_state.update_materials([pygltflib.Material()])

    gltf_state.update_nodes(
        [
            pygltflib.Node(name=f"{name}", children=node_list[i])
            for i, name in enumerate(names)
        ]
    )

    if positions is not None:
        gltf_state.update_nodes(
            [
                pygltflib.Node(
                    name=f"{name}",
                    mesh=t * len(names) + i,
                    translation=position,
                    extras={
                        "index": i,
                    },
                )
                for t, names in enumerate(node_names)
                for i, (name, position) in enumerate(
                    zip(
                        names, jnp.nan_to_num(positions[0]).astype(jnp.float32).tolist()
                    )
                )
            ]
        )
    else:
        gltf_state.update_nodes(
            [
                pygltflib.Node(
                    name=f"{name}",
                    mesh=t * len(names) + i,
                    translation=[0.0, 0.0, 0.0],
                    extras={
                        "index": i,
                    },
                )
                for t, names in enumerate(node_names)
                for i, name in enumerate(names)
            ]
        )

    if len(pointclouds[0]) > 1:
        total_length = len(pointclouds[0])

        time = jnp.true_divide(
            jnp.arange(1, 1 + total_length, dtype=jnp.float32),
            24,
        )

        gltf_state.update_data(
            _NewData(
                data=time,
                component_type=pygltflib.FLOAT,
                count=len(time),
                type=pygltflib.SCALAR,
                min=[float(time[0])],
                max=[float(time[-1])],
                target=pygltflib.ARRAY_BUFFER,
            ),
        )

        time_accessor_index = gltf_state.accessor_idx
        sampler_accessor_index = gltf_state.accessor_idx

        _offset = 0
        if positions is not None:
            _translations = jnp.nan_to_num(positions.transpose(1, 0, 2)).astype(
                jnp.float32
            )

            for _trans in _translations:
                gltf_state.update_data(
                    _NewData(
                        data=_trans,
                        component_type=pygltflib.FLOAT,
                        count=total_length,
                        type=pygltflib.VEC3,
                        min=_trans.min(axis=0).tolist(),
                        max=_trans.max(axis=0).tolist(),
                        target=pygltflib.ARRAY_BUFFER,
                    ),
                )

            for n, nodes in enumerate(node_list):
                if n == 0:
                    gltf_state.update_animation_data(
                        mapped=range(len(nodes)),
                        path="translation",
                        set_input_nb=lambda _: time_accessor_index,
                        set_output_nb=lambda nb: sampler_accessor_index + nb + 1,
                        set_sampler_nb=lambda nb: nb,
                        set_node_nb=lambda nb: nodes[nb],
                    )
                else:
                    gltf_state.update_animation_data(
                        mapped=range(len(nodes)),
                        path="translation",
                        set_sampler_nb=lambda nb: nb,
                        set_node_nb=lambda nb: nodes[nb],
                    )
            _offset = _nb_pointclouds
        else:
            pass

        def _create_weights(pointclouds, minmax):
            nbsteps, nbparticles, nbpoints, nbdof = pointclouds.shape
            output = (
                _rescale(
                    pointclouds,
                    amin=minmax[0],
                    amax=minmax[-1],
                )
                .reshape(nbsteps, nbparticles, -1)
                .transpose(1, 0, 2)
            )

            return jnp.nan_to_num(output).astype(jnp.float32)

        _weights = jax.tree_util.tree_map(_create_weights, pointclouds, _minmax)

        for i, (wghts, nodes) in enumerate(zip(_weights, node_list)):
            _sampler_accessor_index = gltf_state.accessor_idx
            nbparticles, nbsteps, nbpoints = wghts.shape

            for wght in wghts:
                gltf_state.update_data(
                    _NewData(
                        data=wght.flatten(),
                        component_type=pygltflib.FLOAT,
                        count=nbsteps * nbpoints,
                        type=pygltflib.SCALAR,
                        min=[-1.0],  # float(wght.min())],
                        max=[1.0],  # float(wght.max())],
                        target=pygltflib.ARRAY_BUFFER,
                    ),
                )

            gltf_state.update_animation_data(
                mapped=range(nbparticles),
                path="weights",
                set_input_nb=lambda _: time_accessor_index,
                set_output_nb=lambda nb: _sampler_accessor_index + nb + 1,
                set_sampler_nb=lambda nb: _offset + i * nbparticles + nb,
                set_node_nb=lambda nb: nodes[nb],
            )

        gltf_state.update_animations(name="pointclouds_animations")

    gltf_state.update_buffers()
    gltf_state.update_binary_blob()

    summary(gltf_state.gltf)
    gltf_state.gltf.save(f"{filename}.glb")

    return


if __name__ == "__main__":
    pass
