"""Helpers for mathematical functions."""

__all__ = [
    "b_spline",
    "multivariate_b_spline",
    "bessel_first_kind",
    "bessel_second_kind",
    "bessel_first_kind_spherical",
    "bessel_second_kind_spherical",
    "create_kronecker_delta",
    "create_levi_civita_symbol",
    "create_mask",
    "create_b_spline_knots",
    "fix_pbc",
    "fix_pbc_lattice",
    "find_pattern_index",
    "get_force",
    "generate_gaussian_on_sphere",
    "generate_uv_sphere",
    "group_iterative_mgs",
    "group_iterative_mgs_orthogonalizer",
    "iterative_mgs",
    "multiply_functions",
    "sum_functions",
    "compose_functions",
    "split_matrix",
    "recombine_matrix",
    "sqrtm",
    "rotate_vector_around_axis",
    "unwrap",
    "unwrap_lattice",
    "compute_gridmapped_function",
    "compute_blocked_function",
    "particle_mesh_ewald",
    "compute_nearest_image_lattice",
    "compute_combinations",
    "compute_rotation_matrix_angle_axis",
    "create_member_set",
    "binomial_coefficient",
    "get_rotation_matrix",
    "get_rotation_axis",
    "get_quaternion_from_axis",
    "get_quaternion_from_frames",
    "vectors_to_quaternion",
    "create_voronoi_from_miller_indices",
    "automatic_broadcast",
    "homogeneous_multiplication",
    "normalize",
    "rescale",
]

from functools import wraps
from typing import Callable, Dict, List, Optional

import jax
import jax.numpy as jnp
import jax.random as jrnd
import jax.scipy as jsp
import numpy as np
from jax.tree_util import Partial
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.special import jv, yv

_einsum = Partial(jnp.einsum, precision=jax.lax.Precision.HIGHEST)


def normalize(vectors: jax.Array):
    """Normalize vectors along the last axis."""
    return jnp.true_divide(vectors, jnp.linalg.norm(vectors, axis=-1))


def rescale(
    array: jax.Array,
    mapmin: Optional[jax.Array] = None,
    mapmax: Optional[jax.Array] = None,
    amin: Optional[jax.Array] = None,
    amax: Optional[jax.Array] = None,
):
    if mapmin is None:
        mapmin = jnp.asarray(0.0)

    if mapmax is None:
        mapmax = jnp.asarray(1.0)

    if amin is None:
        amin = jnp.nanmin(array, axis=0)

    if amax is None:
        amax = jnp.nanmax(array, axis=0)

    _ptp = amax - amin
    amin, ptp = jax.lax.cond(
        jnp.sum(_ptp),
        # lambda: (amin, jnp.where(jnp.logical_or(_ptp, amax), amax, 1.0)),
        lambda: (amin, jnp.where(_ptp, _ptp, amax)),
        lambda: (jnp.zeros_like(amin), jnp.where(amax, amax, 1.0)),
    )

    print(_ptp, ptp)
    normalized = jnp.true_divide(array - amin, ptp)

    return mapmin + mapmax * normalized


def multiply_functions(*funcs):
    """Multiply functions"""

    @Partial
    def wrapper(*args, **kwargs):
        output = funcs[0](*args, **kwargs)
        for f in funcs[1:]:
            output = output * f(*args, **kwargs)
        return output

    return wrapper


def sum_functions(*funcs):
    """Sum functions"""

    @Partial
    def wrapper(*args, **kwargs):
        output = funcs[0](*args, **kwargs)
        for f in funcs[1:]:
            output = output + f(*args, **kwargs)
        return output

    return wrapper


def compose_functions(func, *funcs, parameters=List[Dict]):
    """Compose functions where the inner-most function is the first argument
    and the outer-most the last arguments.
    """

    @wraps(funcs[-1])
    @Partial
    def wrapper(*args, **kwargs):
        _func = func
        for f, p in zip(funcs, parameters):
            _func = f(_func, **p)
        return _func(*args, **kwargs)

    return wrapper


def create_kronecker_delta(*shape):
    """Creates the kronecker delta tensor from an arbitrary shape."""
    rank = len(shape)

    # Simply check that all indices are equal by computing the sum
    # of difference between each pair of indices.
    func = lambda *args: jnp.sum(jnp.diff(jnp.stack(args))) == 0

    for j in range(rank):
        in_axes = [0 if k == j else None for k in reversed(range(rank))]

        func = jax.vmap(func, in_axes=in_axes)

    return func(*[jnp.arange(s) for s in shape])


def create_levi_civita_symbol(dimension: int):
    """Creates the Levi-Cevita tensor for an arbitrary dimension."""

    interaction = _permutation_sign

    for j in range(dimension):
        in_axes = [0 if k == j else None for k in reversed(range(dimension))]
        interaction = jax.vmap(interaction, in_axes=in_axes)

    return interaction(
        *jnp.repeat(
            jnp.arange(dimension)[jnp.newaxis, :],
            dimension,
            axis=0,
        )
    )


def get_force(potential, gradkw={}):
    @wraps(potential)
    @Partial
    def wrapper(*args, **kwargs):
        return -jax.grad(potential, **gradkw)(*args, **kwargs)

    return wrapper


@Partial
def unwrap(coordinates, pbc):
    coordinates.position = jax.vmap(
        lambda coordinates, pbc: (
            coordinates.position
            - jnp.rint((coordinates.position - pbc.min) / pbc.max) * pbc.max
        ),
        in_axes=(0, 0),
        out_axes=0,
    )(coordinates, pbc)
    return coordinates


@Partial
def unwrap_lattice(coordinates, pbc):
    coordinates.position = jax.vmap(
        lambda coordinates, pbc: compute_nearest_image_lattice(
            coordinates.position,
            pbc,
        ),
        in_axes=(0, 0),
        out_axes=0,
    )(coordinates, pbc)
    return coordinates


@Partial
def _permutation_sign(*indices):
    """Computes the permutation sign of an array."""
    value = 1.0

    for i in range(len(indices)):
        for j in range(0, i):
            value = value * jnp.sign(indices[i] - indices[j])

    return value


@Partial
def rotate_vector_around_axis(vector, axis):
    """axis should represent the rotation increment vector."""
    if vector.shape[-1] == 2:
        cos_angle = jnp.cos(axis)
        sin_angle = jnp.sin(axis)
        rotated_vector = (
            jnp.block(
                [
                    [cos_angle, -sin_angle],
                    [sin_angle, cos_angle],
                ]
            )
            @ vector
        )

    elif vector.shape[-1] == 3:
        angle = jnp.linalg.norm(axis)
        cos_angle = jnp.cos(angle)
        sin_angle = jnp.sin(angle)
        unit_axis = jnp.divide(axis, angle)
        # rotated_vector = (
        #     cos_angle * vector
        #     + jnp.cross(unit_axis, vector) * sin_angle
        #     + unit_axis * jnp.dot(unit_axis, vector) * (1 - cos_angle)
        # )

        rotated_vector = (
            cos_angle * vector
            + jnp.cross(unit_axis, vector) * sin_angle
            + jnp.outer(
                jnp.sum(unit_axis * vector, axis=-1),
                unit_axis,
            )
            * (1 - cos_angle)
        )

    else:
        K = jnp.cross(axis, jnp.eye(vector.shape[0]))
        R = jsp.linalg.expm(K)
        rotated_vector = R @ vector

    return rotated_vector


def get_rotation_matrix(before: jax.Array, after: jax.Array):
    """Computes the rotation matrix that takes vector before to vector after (only 3D for now)."""

    if before.shape[0] == before.shape[1] - 1:
        before = jnp.append(
            before,
            jnp.cross(before[0], before[1])[jnp.newaxis, ...],
            axis=0,
        ).T

    if after.shape[0] == after.shape[1] - 1:
        after = jnp.append(
            after,
            jnp.cross(after[0], after[1])[jnp.newaxis, ...],
            axis=0,
        ).T
    return after @ jnp.linalg.inv(before)


# def get_rotation_axis(before: jax.Array, after: jax.Array):
#     R = get_rotation_matrix(before, after)
#     cosangle = 0.5 * (jnp.trace(R) - 1)
#     angle = jnp.arccos(cosangle)
#     denum = jnp.sqrt(
#         jnp.true_divide(
#             -1,
#             (1 + R[0, 0] - R[1, 1] - R[2, 2]) * cosangle
#             - R[0, 0]
#             + R[1, 1]
#             + R[2, 2]
#             - 1,
#         )
#     )
#     axis = jnp.asarray(
#         [
#             -jnp.true_divide(jnp.sqrt(0.5), denum * (cosangle - 1)),
#             jnp.sqrt(0.5) * (R[0, 1] + R[1, 0]) * denum,
#             jnp.sqrt(0.5) * (R[0, 2] + R[2, 0]) * denum,
#         ]
#     )
#     return angle * axis


@jax.jit
def compute_rotation_matrix_angle_axis(angle: float | jax.Array, axis: jax.Array):
    """Computes the rotation matrix from the angle-axis representation."""
    dim = axis.shape[-1]
    levi_civita = create_levi_civita_symbol(dim)

    K = _einsum("ijk,k", levi_civita, axis)
    R = jnp.eye(dim) + jnp.sin(angle) * K + (1 - jnp.cos(angle)) * K @ K

    return R


@jax.jit
def get_rotation_axis(before: jax.Array, after: jax.Array):
    """Get the axis-angle representation of the rotation matrix
    that transforms vector 'before' into vector 'after'.
    """
    rotation_matrix = get_rotation_matrix(before, after)
    cosangle = 0.5 * (jnp.trace(rotation_matrix) - 1)

    def _get_rotation_axis(cosangle, rotation_matrix):
        dim = rotation_matrix.shape[-1]
        eigv, eigV = jnp.linalg.eig(rotation_matrix)
        eigV_idx = jnp.sum(
            jnp.where(
                jnp.logical_and(
                    jnp.isclose(jnp.real(eigv), 1.0),
                    jnp.logical_not(jnp.imag(eigv)),
                ),
                jnp.arange(dim),
                0,
            )
        )
        axis = jnp.real(eigV[:, eigV_idx])
        angle = jnp.arccos(cosangle)
        return jax.lax.cond(
            jnp.allclose(
                compute_rotation_matrix_angle_axis(angle, axis), rotation_matrix
            ),
            lambda: angle * axis,
            lambda: -angle * axis,
        )

    return jax.lax.cond(
        cosangle == 1,
        lambda _, rotation_matrix: jnp.zeros(rotation_matrix.shape[-1]),
        _get_rotation_axis,
        cosangle,
        rotation_matrix,
    )


def get_quaternion_from_axis(axis):
    angle = jnp.linalg.norm(axis)
    normalized_axis = jnp.true_divide(axis, angle)
    sin_angle = jnp.sin(0.5 * angle)
    cos_angle = jnp.cos(0.5 * angle)
    return (
        jnp.zeros(axis.shape[-1] + 1)
        .at[0]
        .set(normalized_axis[0] * sin_angle)
        .at[1]
        .set(normalized_axis[1] * sin_angle)
        .at[2]
        .set(normalized_axis[2] * sin_angle)
        .at[3]
        .set(cos_angle)
    )


def get_quaternion_from_frames(reference, current):
    """
    From Scipy implementation.
    https://github.com/scipy/scipy/blob/1d59ab9813f052d442f5ae460f016b05aaad20a2/scipy/spatial/transform/_rotation.pyx#L1003
    """
    R = jax.lax.cond(
        jnp.all(reference == jnp.eye(reference.shape[-1])),
        lambda: current,
        lambda: get_rotation_matrix(reference, current),
    )
    decision = (
        jnp.empty(4)
        .at[0]
        .set(R[0, 0])
        .at[1]
        .set(R[1, 1])
        .at[2]
        .set(R[2, 2])
        .at[3]
        .set(jnp.trace(R))
    )

    choice = jnp.argmax(decision)

    def _cond_true():
        i = choice
        j = (i + 1) % 3
        k = (j + 1) % 3

        return (
            jnp.empty(4)
            .at[i]
            .set(1 - decision[3] + 2 * R[i, i])
            .at[j]
            .set(R[j, i] + R[i, j])
            .at[k]
            .set(R[k, i] + R[i, k])
            .at[3]
            .set(R[k, j] + R[j, k])
        )

    def _cond_false():
        return (
            jnp.empty(4)
            .at[0]
            .set(R[2, 1] + R[1, 2])
            .at[1]
            .set(R[0, 2] + R[2, 0])
            .at[2]
            .set(R[1, 0] + R[0, 1])
            .at[3]
            .set(1 + decision[3])
        )

    quat = jax.lax.cond(choice != 3, _cond_true, _cond_false)
    # R =
    #
    # t = jnp.trace(R)
    # r = jnp.sqrt(1 + t)
    # s = 0.5 * jnp.reciprocal(r)
    #
    # R11 = R[0,0]
    # R22 = R[1,1]
    # R33 = R[2,2]
    #
    # _am = (R[2, 1] - R[1, 2]) * s
    # _bm = (R[0, 2] - R[2, 0]) * s
    # _cm = (R[1, 0] - R[0, 1]) * s
    #
    # _ap = (R[2, 1] + R[1, 2]) * s
    # _bp = (R[0, 2] + R[2, 0]) * s
    # _cp = (R[1, 0] + R[0, 1]) * s
    #
    # _d = 0.5 * r
    #
    # index = (
    #     0 * ((R22 > -R33) & (R11 > -R22) & (R11 > -R33))
    #     + 1 * ((R22 < -R33) & (R11 > R22) & (R11 > R33))
    #     + 2 * ((R22 > R33) & (R11 < R22) & (R11 < -R33))
    #     + 3 * ((R22 < R33) & (R11 < -R22) & (R11 < R33))
    # )
    #
    # return jax.lax.switch(
    #     index,
    #     [
    #         lambda: jnp.asarray([_d, _am, _bm, _cm]),
    #         lambda: jnp.asarray([_bm, _d, _cp, _ap]),
    #         lambda: jnp.asarray([_bm, _cp, _d, _am]),
    #         lambda: jnp.asarray([_cm, _bp, _ap, _d]),
    #     ],
    # )
    return normalize(quat)


def vectors_to_quaternion(vFrom, vTo, is_normalized=True):
    """Adapted from THREEjs Quaternion.js"""

    vFrom, vTo = jax.lax.cond(
        is_normalized,
        lambda: (vFrom, vTo),
        lambda: (
            jnp.true_divide(
                vFrom,
                jnp.linalg.norm(vFrom, axis=-1)[..., jnp.newaxis],
            ),
            jnp.true_divide(
                vTo,
                jnp.linalg.norm(vTo, axis=-1)[..., jnp.newaxis],
            ),
        ),
    )

    def _condition(vFrom, vTo):
        w = 1 + jnp.dot(vFrom, vTo)

        return jax.lax.cond(
            w < jnp.finfo(0.0).eps,
            lambda: jax.lax.cond(
                jnp.abs(vFrom[0]) > jnp.abs(vFrom[-1]),
                lambda: jnp.asarray(
                    [
                        -vFrom[1],
                        vFrom[0],
                        0.0,
                        0.0,
                    ]
                ),
                lambda: jnp.asarray(
                    [
                        0.0,
                        -vFrom[-1],
                        vFrom[1],
                        0.0,
                    ]
                ),
            ),
            lambda: jnp.append(jnp.cross(vFrom, vTo), w),
        )

    if vFrom.ndim > 1 or vTo.ndim > 1:
        vmapvFrom = 0 if vFrom.ndim > 1 else None
        vmapvTo = 0 if vTo.ndim > 1 else None

        output = jax.vmap(
            _condition,
            in_axes=(vmapvFrom, vmapvTo),
        )(vFrom, vTo)
    else:
        output = _condition(vFrom, vTo)

    return jnp.true_divide(
        output,
        jnp.linalg.norm(output, axis=-1)[..., jnp.newaxis],
    )


@Partial
def fix_pbc(coordinates, pbc):
    length = pbc.max - pbc.min
    return coordinates - jnp.nan_to_num(
        jnp.floor((coordinates - pbc.min) / length) * length
    )


@Partial
def fix_pbc_lattice(coordinates, pbc):
    # _A = pbc.direct_lattice
    # _B = pbc.reciprocal_lattice
    # _frac_coord = _B @ coordinates
    # _restrict = _frac_coord - jnp.floor(_frac_coord)
    #
    # return (
    #     jnp.where(jnp.isinf(_A), 0.0, _A) @ _restrict
    #     + jnp.where(jnp.isinf(_A), 1.0, 0.0) @ coordinates
    # )
    _A = pbc.direct_lattice
    _B = pbc.reciprocal_lattice
    # _frac_coord = _B @ vector
    _frac_coord = jnp.tensordot(_B, coordinates.T, axes=1).T
    _restrict = _frac_coord - jnp.floor(_frac_coord)

    # return (
    #     jnp.where(jnp.isinf(_A), 0.0, _A) @ _restrict
    #     + jnp.where(jnp.isinf(_A), 1.0, 0.0) @ vector
    # )
    return (
        jnp.tensordot(
            jnp.where(jnp.isinf(_A), 0.0, _A),
            _restrict.T,
            axes=1,
        ).T
        + jnp.tensordot(
            jnp.where(jnp.isinf(_A), 1.0, 0.0),
            coordinates.T,
            axes=1,
        ).T
    )


def create_mask(shape, lower, upper):
    """Creates a mask for each axis specified in `shape` following
    the lower and upper selection.
    """
    mask = (jnp.arange(shape[0]) % upper[0]) > (lower[0] - 1)

    for i, s in enumerate(shape[1:], start=1):
        mask = jnp.outer(mask, (jnp.arange(s) % upper[i]) > (lower[i] - 1))

    return mask


def create_mask_kronecker_product(array_list):
    """Creates a mask by taking the kronecker product of the arrays in `array_list`.
    The product is incremental in that it takes product of the previous product
    with the current array.
    """
    mask = array_list[0]
    for array in array_list[1:]:
        mask = jnp.kron(mask, array).reshape(list(mask.shape) + list(array.shape))
    return mask


def split_matrix(matrix, nbrows, nbcols):
    """Split a matrix of dimension (`dim1`, `dim2`) in sub-matrices of dimension (`nbrows`,`nbcols`).

    :param matrix: The matrix to split.
    :param nbrows: The number of rows for the sub-matrices.
    :param nbcols: The number of columns for the sub-matrices.

    :return: An array of shape (`dim1//nbrows`, `dim2//nbcols`, `nbrows`, `nbcols`)
    """

    dim1, dim2 = matrix.shape
    return matrix.reshape(dim1 // nbrows, nbrows, dim2 // nbcols, nbcols).swapaxes(1, 2)


def recombine_matrix(splitted_matrix):
    """Recombine a splitted matrix."""
    nblock1, nblock2, nbrows, nbcols = splitted_matrix.shape
    return splitted_matrix.transpose(0, 2, 1, 3).reshape(
        nblock1 * nbrows, nblock2 * nbcols
    )


# Custom Jacobian-Vector Product (JVP) definition for the jsp.linalg.sqrtm
# function
@jax.custom_jvp
def sqrtm(matrix):
    """Computes the square-root of matrix.

    :param matrix: The input matrix

    :return: The square-root of the input matrix.
    """
    return jsp.linalg.sqrtm(matrix)


@sqrtm.defjvp
def sqrtm_jvp(primals, tangents):
    """Computes the Jacobian Vector Product (JVP) of the matrix square-root function.
    :param primals: The input matrix
    :param tangents: The input tangent vector.

    :return: A double with the value of the square-root matrix and
    the output tagent.
    """
    (matrix,) = primals
    dim = matrix.shape[0]

    output_primals = sqrtm(matrix)

    output_tangents = jnp.matmul(
        jnp.linalg.pinv(
            jnp.kron(jnp.eye(dim), sqrtm(matrix))
            + jnp.kron(sqrtm(matrix).T, jnp.eye(dim))
        ),
        tangents[0].flatten(order="F"),
    ).reshape(matrix.shape, order="F")

    return output_primals, output_tangents


# Custom  Jacobian-Vector Product (JVP) definition for 1st kind Bessel
@jax.custom_jvp
def bessel_first_kind(x, v):
    return jax.pure_callback(
        lambda vx: jv(*vx),
        x,
        (v, x),
        vectorized=True,
    )


@bessel_first_kind.defjvp
def bessel_first_kind_jvp(primals, tangents):
    x, v = primals
    dx, dv = tangents
    primal_out = bessel_first_kind(x, v)

    # https://dlmf.nist.gov/10.6 formula 10.6.1
    tangents_out = jax.lax.cond(
        v == 0,
        lambda: -bessel_first_kind(x, v + 1),
        lambda: 0.5 * (bessel_first_kind(x, v - 1) - bessel_first_kind(x, v + 1)),
    )

    return primal_out, tangents_out * dx


# Custom Jacobian-Vector Product (JVP) definition for 2nd kind Bessel
@jax.custom_jvp
def bessel_second_kind(x, v):
    return jax.pure_callback(
        lambda vx: yv(*vx),
        x,
        (v, x),
        vectorized=True,
    )


@bessel_second_kind.defjvp
def bessel_second_kind_jvp(primals, tangents):
    x, v = primals
    dx, dv = tangents
    primal_out = bessel_second_kind(x, v)

    # https://dlmf.nist.gov/10.6 formula 10.6.1
    tangents_out = jax.lax.cond(
        v == 0,
        lambda: -bessel_second_kind(x, v + 1),
        lambda: 0.5 * (bessel_second_kind(x, v - 1) - bessel_second_kind(x, v + 1)),
    )

    return primal_out, tangents_out * dx


# # Custom Jacobian-Vector Product (JVP) definition for Bessel 1st kind Spherical
# def bessel_first_kind_spherical(x, v):
#     return bessel_first_kind(x, v + 0.5) * jnp.sqrt(jnp.pi / (2 * x))
#
#
# # Custom Jacobian-Vector Product (JVP) definition for Bessel 2nd kind Spherical
# def bessel_second_kind_spherical(x, v):
#     return bessel_second_kind(x, v + 0.5) * jnp.sqrt(jnp.pi / (2 * x))


@Partial(jnp.vectorize, excluded=(1,))
def _a(k, n: int):
    """
    https://dlmf.nist.gov/10.49.E1
    """
    return jax.lax.cond(
        k < n + 1,
        lambda: jnp.divide(
            jsp.special.gamma(n + k + 1),
            (2**k * jsp.special.gamma(k + 1) * jsp.special.gamma(n - k + 1)),
        ),
        lambda: jnp.zeros_like(k, dtype=jnp.float_),
    )


@Partial(jnp.vectorize, excluded=(1,))
def bessel_first_kind_spherical(x, n: int):
    """
    Spherical Bessel First Kind.
    https://dlmf.nist.gov/10.49.E2

    """
    sum1 = jax.lax.fori_loop(
        0,
        jnp.floor_divide(n, 2) + 1,
        lambda k, v: v
        + jnp.divide(
            (-1) ** k * _a(2 * k, n),
            x ** (2 * k + 1),
        ),
        0,
    )

    sum2 = jax.lax.fori_loop(
        0,
        jnp.floor_divide(n - 1, 2) + 1,
        lambda k, v: v
        + jnp.divide(
            (-1) ** k * _a(2 * k + 1, n),
            x ** (2 * k + 2),
        ),
        0,
    )
    first_term = jnp.sin(x - 0.5 * jnp.pi * n) * sum1
    second_term = jnp.cos(x - 0.5 * jnp.pi * n) * sum2

    return first_term + second_term


@Partial(jnp.vectorize, excluded=(1,))
def bessel_second_kind_spherical(x, n: int):
    """
    Spherical Bessel Second Kind.
    https://dlmf.nist.gov/10.49.E2

    """
    sum1 = jax.lax.fori_loop(
        0,
        jnp.floor_divide(n, 2) + 1,
        lambda k, v: v
        + jnp.divide(
            (-1) ** k * _a(2 * k, n),
            x ** (2 * k + 1),
        ),
        0,
    )

    sum2 = jax.lax.fori_loop(
        0,
        jnp.floor_divide(n - 1, 2) + 1,
        lambda k, v: v
        + jnp.divide(
            (-1) ** k * _a(2 * k + 1, n),
            x ** (2 * k + 2),
        ),
        0,
    )
    first_term = -jnp.cos(x - 0.5 * jnp.pi * n) * sum1
    second_term = jnp.sin(x - 0.5 * jnp.pi * n) * sum2

    return first_term + second_term


@Partial(jnp.vectorize)
def characteristic_function(x, lower, upper):
    return jax.lax.cond(
        jnp.logical_and(lower <= x, x < upper),
        lambda: 1.0,
        lambda: 0.0,
    )


@Partial(jnp.vectorize, excluded=(1, 2, 3))
def _gamma_(x, index, order, knot_sequence):
    return jnp.nan_to_num(
        jnp.divide(
            x - knot_sequence[index],
            knot_sequence[index + order] - knot_sequence[index],
        ),
        posinf=0.0,
        neginf=0.0,
    )


@Partial
def _inner_(x, index, order, degree, splines, knot_sequence):
    # Example for order=1, degree=0, index=0
    # For a given order 'n', intermediate order 'd' (degree) and
    # index 'k'. The splines necessary to compute b^n_k are;
    #   -| b^{d}_i for d in [0, 1, ..., n - 1]
    # such that for a fixed d:
    #   -| i in [k, k+1, ..., k + n - d]

    lower_spline_nb = index
    upper_spline_nb = lower_spline_nb + order - degree + 1

    return jax.lax.fori_loop(
        lower_spline_nb,
        upper_spline_nb,
        lambda i, val: val.at[i].set(
            _gamma_(x, i, degree + 1, knot_sequence) * splines[i]
            + (1 - _gamma_(x, i + 1, degree + 1, knot_sequence)) * splines[i + 1]
        ),
        jnp.zeros_like(splines),
    )


# @Partial(jnp.vectorize, excluded=(1, 2, 3))
@Partial(jax.custom_jvp, nondiff_argnums=(1, 2, 3))
def b_spline(x, index, order, knot_sequence):
    indication = characteristic_function(
        x, knot_sequence[:-1], jnp.roll(knot_sequence, -1)[:-1]
    )
    return jax.lax.fori_loop(
        0,
        order,
        lambda degree, splines: _inner_(
            x,
            index,
            order,
            degree,
            splines,
            knot_sequence,
        ),
        indication,
    )[index]


@b_spline.defjvp
def b_spline_jvp(index, order, knot_sequence, primals, _):
    """"""
    (x,) = primals

    alpha_i = jnp.nan_to_num(
        jnp.divide(order, knot_sequence[index + order] - knot_sequence[index]),
        posinf=0.0,
        neginf=0.0,
    )

    alpha_ip = jnp.nan_to_num(
        jnp.divide(
            order,
            knot_sequence[index + order + 1] - knot_sequence[index + 1],
        ),
        posinf=0.0,
        neginf=0.0,
    )

    output_primals = b_spline(x, index, order, knot_sequence)
    output_tangents = alpha_i * b_spline(
        x, index, order - 1, knot_sequence
    ) - alpha_ip * b_spline(x, index + 1, order - 1, knot_sequence)

    return output_primals, output_tangents


@Partial
def multivariate_b_spline(coordinates, indices, orders, knots):
    # This is a reduce with the multiplication operation
    if coordinates.ndim < 2:
        coordinates = coordinates[jnp.newaxis, ...]
        slc = 0
    else:
        slc = slice(None, None, None)

    return jax.lax.scan(
        lambda _, coord: (
            None,
            jax.lax.scan(
                lambda c, x: (c * b_spline(*x), None),
                1.0,
                (coord, indices, orders, knots),
            )[0],
        ),
        None,
        coordinates,
    )[-1][slc]


def create_b_spline_knots(
    knots,
    order,
    startpoint: int | None = None,
    endpoint: int | None = None,
    periodic: tuple | None = None,
):
    """
    For periodic, startpoint=1, endpoint=1:
    The start- and end-point are shifted to preserve sum = 1
    """
    _eps = 0.0  # 1e-6
    start_knot = 0
    extra_endknots = 0
    nbknots = len(knots)

    period = knots.ptp()
    if order and startpoint is not None:
        knots = jnp.append(jnp.full(order - startpoint, knots.min()), knots)

        if startpoint == 0:
            start_knot += 1
        elif startpoint == 1:
            knots = jnp.append(knots[0] - _eps, knots)

    if order and endpoint is not None:
        knots = jnp.append(knots, jnp.full(order - endpoint, knots.max()))

        if endpoint == 1:
            extra_endknots += order - endpoint
            knots = jnp.append(knots, knots[-1] + _eps)

    indices = jnp.arange(
        start_knot,
        knots.shape[0] - 2 * order + extra_endknots,
    )

    if order == 0:
        indices = indices[:-1]

    if periodic:
        nb_aperiodic = len(indices)

        knots = jax.vmap(
            lambda shift, k, _: (shift * period + k),
            in_axes=(0, None, None),
        )(
            jnp.arange(periodic[0], periodic[1] + 1),
            knots,
            period,
        ).flatten()
        knot_distance = periodic[1] - periodic[0]
        period_add = jnp.arange(knot_distance + 1) * (
            nbknots + order * (startpoint is not None) + order * (endpoint is not None)
        )

        indices = jax.vmap(lambda p, i: p + i, in_axes=(0, None))(
            period_add, indices
        ).flatten()

        if startpoint == 1 and startpoint == endpoint:
            modify = jnp.arange(0, len(indices), nb_aperiodic)[1:]
            sel1 = indices[modify - 1] + order
            sel2 = indices[modify] + order
            low_right = knots[sel1] - _eps
            high_left = knots[sel2] + _eps
            knots = knots.at[sel1].set(low_right).at[sel2].set(high_left)

    return indices, knots


def compute_gridmapped_function(
    independent,
    input_knots,
    dependent=None,
    function: None | Callable = None,
):
    """Computes a function on a grid defined by independent and/or input_knots."""

    def is_callable(knots):
        # knots is None or isinstance(knots, (int, jax.Array, str))
        return isinstance(knots, Callable)

    def is_one_dimensional(array):
        return isinstance(array, jax.Array) and array.ndim == 1

    dimensional_case = {
        True: {
            "function": {
                True: lambda indep, knots, dep: jnp.histogram(
                    indep,
                    bins=knots,
                    weights=dep,
                )[0],
                False: function,
            },
            "knots": lambda indep, knots: (
                jnp.asarray(np.histogram_bin_edges(indep, bins=knots(indep)))
                if is_callable(knots)
                else jnp.asarray(np.histogram_bin_edges(indep, bins=knots))
            ),
        },
        False: {
            "function": {
                True: lambda indep, knots, dep: jnp.histogramdd(
                    jnp.asarray(indep).T,
                    knots,
                    weights=dep,
                )[0],
                False: function,
            },
            "knots": lambda indep, knots: (
                [
                    (
                        jnp.asarray(np.histogram_bin_edges(v, bins=k(indep)))
                        if is_callable(k)
                        else jnp.asarray(np.histogram_bin_edges(v, bins=k))
                    )
                    for v, k in zip(indep, knots)
                ]
            ),
        },
    }

    get_func, get_knots = dimensional_case[is_one_dimensional(independent)].values()
    knots = get_knots(independent, input_knots)
    output = get_func[function is None](independent, knots, dependent)

    return output, knots


def compute_blocked_function(
    independent_variables,
    knots,
    dependent_variables,
    average=False,
):
    """Computes sum/average per N-dimensional-blocks."""

    def get_flat_shape(knots):
        out = 1
        for k in knots:
            out *= k.shape[0]
        return out

    def block_sum(carry, x):
        i, count, val = x
        return (carry.at[i].set(jnp.nan_to_num(carry[i]) + val), None)

    def block_average(carry, x):
        i, count, val = x
        return (
            carry.at[i].set(jnp.nan_to_num(carry[i]) + val / count),
            None,
        )

    flat_shape = get_flat_shape(knots)

    digitized = jnp.stack(
        [
            jnp.digitize(independent_variables[i], knots[i])
            for i in range(independent_variables.ndim)
        ]
    ).T

    # Initialize to nan since some blocks can be empty
    init_output = jnp.full(flat_shape, jnp.nan)

    _, inverse, counts = jnp.unique(
        digitized, return_inverse=True, return_counts=True, axis=0
    )

    # print(digitized.shape, inverse, counts[inverse].shape, dependent_variables.shape, sep="\n")

    output = jax.lax.scan(
        block_average if average else block_sum,
        init_output,
        (inverse, counts[inverse], dependent_variables),
    )[0]

    # print(output)

    return output.reshape(*[x.shape[0] for x in knots])


@Partial
def find_pattern_index(arr1, arr2):
    """Returns the index where arr2 matches arr1"""
    return jnp.where(
        (jax.scipy.signal.convolve(arr1, arr2[::-1], mode="valid") == jnp.sum(arr2**2))
    )[0]


@Partial(jnp.vectorize, excluded=(1, 2))
def laguerre_polynomial(x, alpha, order):
    return jax.lax.fori_loop(
        2,
        order + 1,
        lambda i, val: val.at[i].set(
            jnp.divide(
                (2 * (i - 1) + 1 + alpha - x) * val[i - 1]
                - (i - 1 + alpha) * val[i - 2],
                (i - 1) + 1,
            )
        ),
        jnp.ones(2 + order).at[1].set(1.0 + alpha - x),
    )[order]


@Partial
def orthonormalized_laguerre(x, alpha, order, degree):
    return jnp.sqrt(
        jnp.divide(
            jnp.exp(-x) * jnp.power(x, alpha) * jsp.special.gamma(degree + 1),
            jsp.special.gamma(degree + alpha + 1),
        )
    ) * laguerre_polynomial(x, alpha, order)


def particle_mesh_ewald(direct_func, reciprocal_func):
    @wraps(direct_func)
    @Partial
    def wrapper(vector, parameters, *args, **kwargs):
        def _sum_term(cell_vector, direct_lattice, reciprocal_lattice):
            v_n = vector + jnp.dot(direct_lattice, cell_vector)
            v_n_norm = jnp.linalg.norm(v_n)
            k_n = 2 * jnp.pi * jnp.dot(cell_vector, reciprocal_lattice)
            k_n2 = jnp.dot(k_n, k_n)
            # jax.experimental.host_callback.id_print((v_n, v_n_norm, k_n, k_n2))

            return jax.lax.cond(
                jnp.any(cell_vector),
                lambda v_n_norm, v_n, k_n2, k_n: direct_func(
                    v_n_norm,
                    v_n,
                    *(*args, parameters),
                    **kwargs,
                )
                + reciprocal_func(
                    k_n2,
                    k_n,
                    *(*args, parameters),
                    **kwargs,
                ),
                lambda v_n_norm, v_n, *_: direct_func(
                    v_n_norm,
                    v_n,
                    *(*args, parameters),
                    **kwargs,
                ),
                v_n_norm,
                jnp.true_divide(v_n, v_n_norm),
                k_n2,
                jnp.true_divide(k_n, jnp.sqrt(k_n2)),
            )

        return jnp.sum(
            jax.vmap(_sum_term, in_axes=(0, None, None))(
                parameters.cell_vectors,
                parameters.pbc.direct_lattice,
                parameters.pbc.reciprocal_lattice,
            ),
            axis=0,
        )

    return wrapper


@Partial
def compute_nearest_image_lattice(vector, pbc):
    _A = pbc.direct_lattice
    _B = pbc.reciprocal_lattice
    # _frac_coord = _B @ vector
    _frac_coord = jnp.tensordot(_B, vector.T, axes=1).T
    _restrict = _frac_coord - jnp.rint(_frac_coord)

    # return (
    #     jnp.where(jnp.isinf(_A), 0.0, _A) @ _restrict
    #     + jnp.where(jnp.isinf(_A), 1.0, 0.0) @ vector
    # )
    return (
        jnp.tensordot(
            jnp.where(jnp.isinf(_A), 0.0, _A),
            _restrict.T,
            axes=1,
        ).T
        + jnp.tensordot(
            jnp.where(jnp.isinf(_A), 1.0, 0.0),
            vector.T,
            axes=1,
        ).T
    )


def compute_combinations(indices, max_distance=jnp.inf):
    combinations = jnp.asarray(jnp.meshgrid(*indices)).T.reshape(-1, 3)
    distance = jnp.linalg.norm(combinations, axis=-1)
    mask = distance <= max_distance
    return combinations[jnp.where(mask)][distance[jnp.where(mask)].argsort()]


@Partial
def iterative_mgs(vector, basis, max_iteration=2, do_normalize=True):
    if do_normalize:
        basis = basis / jnp.linalg.norm(basis, axis=-1)[..., jnp.newaxis]

    def _cond_iteractive_mgs(val):
        k, vector, r, norm = val
        return k < max_iteration

    def _mgs(i, val):
        vector, h = val

        h = basis[i].T @ vector
        new_vector = vector - h * basis[i]
        return (new_vector, h)

    def _iterative_mgs(val):
        k, vector, r, norm = val
        new_vector, h = jax.lax.fori_loop(
            0,
            basis.shape[0],
            _mgs,
            (vector, 0.0),
        )
        r = r + h
        norm = jnp.linalg.norm(new_vector)

        return (k + 1, new_vector, r, norm)

    return jax.lax.while_loop(
        _cond_iteractive_mgs,
        _iterative_mgs,
        (0, vector, 0.0, 0.0),
    )


_full_iterative_mgs_vmap = jax.vmap(
    jax.vmap(
        iterative_mgs,
        in_axes=(0, None),
    ),
    in_axes=(0, 0),
)


def _full_iterative_mgs(basis, orthogonalizer):
    return jax.lax.cond(
        jnp.any(orthogonalizer),
        lambda: _full_iterative_mgs_vmap(basis, orthogonalizer)[1],
        lambda: basis,
    )


@Partial
def group_iterative_mgs(basis):
    nbtype = len(basis)
    # shapes = jnp.asarray([b.shape for b in basis])
    # full_iterative_mgs = jax.vmap(
    #     jax.vmap(
    #         iterative_mgs,
    #         in_axes=(0, None),
    #     ),
    #     in_axes=(0, 0),
    # )

    new_basis = basis.array
    _offset = 0
    for i in range(nbtype):
        _length = basis[i].shape[0]
        for j in range(nbtype):
            if i != j:
                _new_basis = _full_iterative_mgs(
                    new_basis[_offset : _offset + _length].transpose(1, 0, 2),
                    basis[j].array.transpose(1, 0, 2),
                )

                new_basis = new_basis.at[_offset : _offset + _length].set(
                    # (_new_basis / norm[..., jnp.newaxis]).transpose(1, 0, 2)
                    _new_basis.transpose(1, 0, 2)
                )
                _offset += basis[i].shape[0]
        _offset += _length
    # for i in range(nbtype - 1):
    #     for j in range(i + 1, nbtype):
    #         _offset += basis[i].shape[0]
    #         _length = basis[j].shape[0]
    #
    #         _, _new_basis, _, _ = full_iterative_mgs(
    #             basis[j].array.transpose(1, 0, 2),
    #             basis[i].array.transpose(1, 0, 2),
    #         )
    #
    #         new_basis = new_basis.at[_offset : _offset + _length].set(
    #             # (_new_basis / norm[..., jnp.newaxis]).transpose(1, 0, 2)
    #             _new_basis.transpose(1, 0, 2)
    #         )
    #     _offset = basis[i].shape[0]

    return basis.regroup(new_basis)


@Partial
def group_iterative_mgs_orthogonalizer(basis, orthogonalizer):
    nbtype = len(basis)
    # shapes = jnp.asarray([b.shape for b in basis])

    new_basis = basis.array
    _offset = 0
    for i in range(nbtype):
        _length = basis[i].shape[0]
        _new_basis = _full_iterative_mgs(
            new_basis[_offset : _offset + _length].transpose(1, 0, 2),
            orthogonalizer[i].array.transpose(1, 0, 2),
        )

        new_basis = new_basis.at[_offset : _offset + _length].set(
            _new_basis.transpose(1, 0, 2)
        )
        _offset += _length

    return basis.regroup(new_basis)


@Partial
def create_member_set(elements, number, pad=None):
    """Sorts the permutations such that the member set hierarchy is respected."""
    permutations = jnp.asarray(jnp.meshgrid(*([elements] * number))).T.reshape(
        -1, number
    )
    nbfunctions = jnp.count_nonzero(permutations, axis=-1)
    sorting = nbfunctions.argsort()

    sorted_permutations = jnp.flip(permutations[sorting], axis=-1)

    if isinstance(pad, int):
        sorted_permutations = jax.vmap(
            lambda arr: jnp.pad(
                arr,
                (0, pad),
                mode="constant",
                constant_values=(0, 0),
            ),
            in_axes=(0,),
        )(sorted_permutations)

    return sorted_permutations, jnp.sum(sorted_permutations, axis=-1).astype(jnp.int_)


def binomial_coefficient(n, k):
    return jnp.divide(
        jsp.special.gamma(1 + n),
        jsp.special.gamma(1 + n - k) * jsp.special.gamma(1 + k),
    ).astype(jnp.int_)


def create_voronoi_from_miller_indices(basis, k=1):
    dim = basis.shape[-1]
    indices = jnp.arange(-k, k + 1, 1)

    # hkl... miller indices from the indices in the discrete interval [-k, k]
    miller_indices = jnp.asarray(
        jnp.meshgrid(*[indices for d in range(dim)])
    ).T.reshape(-1, dim)[jnp.arange((2 * k + 1) ** dim) != (2 * k + 1) ** dim // 2]

    inside_zone = jnp.ones((len(miller_indices),), dtype=bool)
    lattice_vectors = jnp.einsum("ij,jn", miller_indices, basis)

    distance_to_center = jnp.linalg.norm(0.5 * lattice_vectors, axis=-1)

    # Find which planes form the boundary of the zone
    for i, d1 in enumerate(distance_to_center):
        for j, _ in enumerate(distance_to_center):
            if (
                i != j
                and jnp.linalg.norm(0.5 * lattice_vectors[i] - lattice_vectors[j]) <= d1
            ):
                inside_zone = inside_zone.at[i].set(False)
                break

    # boundaries = miller_indices[inside_zone]
    planes = lattice_vectors[inside_zone]

    # Ax = b to Ax - b = 0 (this explains the minus)
    halfspaces = jnp.hstack(
        (
            planes,
            -0.5 * jnp.linalg.norm(planes, axis=-1).reshape(planes.shape[0], 1) ** 2,
        )
    )

    HalfSpaces = HalfspaceIntersection(halfspaces, np.zeros((dim,)))
    V = ConvexHull(HalfSpaces.intersections)

    return V.points


def automatic_broadcast(
    arr1: jax.Array, arr2: jax.Array
) -> tuple[jax.Array, jax.Array]:
    "Finds the shared shape and add dimensions to allow broadcasting."

    def match_last_shapes(arr: jax.Array, other_dim: int, other_axis: int):
        return jnp.expand_dims(
            arr, axis=tuple(i for i in range(1, other_dim - other_axis))
        )

    _arr1_shape = arr1.shape
    _arr2_shape = arr2.shape

    _dim1 = arr1.ndim
    _dim2 = arr2.ndim

    _lowest_dim = _dim1 if _dim1 <= _dim2 else _dim2

    if _arr1_shape[-_lowest_dim:] == _arr2_shape[-_lowest_dim:]:
        # If the arrays share the same last shapes, do nothing.
        new_arr1 = arr1
        new_arr2 = arr2
    else:
        _axis1 = []
        _axis2 = []

        for i, ss in enumerate(arr1.shape):
            for j, ts in enumerate(arr2.shape):
                if ss == ts:
                    _axis1.append(i)
                    _axis2.append(j)

        _nbdiff1 = _dim2 - len(_axis1)
        _nbdiff2 = _dim1 - len(_axis2)

        new_arr1 = arr1
        new_arr2 = arr2

        if _nbdiff1 > 0 and _nbdiff2 > 0:
            if _axis1[-1] < _axis2[-1]:
                new_arr2 = jnp.expand_dims(arr2, axis=_axis2[-1] + 1)
            else:
                new_arr1 = jnp.expand_dims(arr1, axis=_axis1[-1] + 1)
        elif _nbdiff1 <= 0:
            # If arr2 as not enough last shapes
            new_arr2 = match_last_shapes(arr2, _dim1, _axis1[-1])
        elif _nbdiff2 <= 0:
            # If arr1 as not enough last shapes
            new_arr1 = match_last_shapes(arr1, _dim2, _axis2[-1])

    return new_arr1, new_arr2


def homogeneous_multiplication(arr1: jax.Array, arr2: jax.Array):
    new_arr1, new_arr2 = automatic_broadcast(arr1, arr2)
    return new_arr1 * new_arr2


def generate_gaussian_on_sphere(
    nb_points: int,
    dim: int,
    radius: jax.Array = jnp.asarray(1.0),
    key=0,
):
    x = jrnd.normal(jrnd.PRNGKey(key), (nb_points, dim))
    z = jnp.linalg.norm(x, axis=1)
    z = z.reshape(-1, 1).repeat(x.shape[1], axis=1)

    return jnp.divide(x, z) * radius[..., jnp.newaxis]


def generate_uv_sphere(
    radius: float, inclination: jax.Array, azimuth: jax.Array
) -> jax.Array:
    """
    Get points on the surface of a sphere.

    Parameters:
        - radius (float): The radius of the sphere.
        - inclination (float): The angle between 0 and 180
        - azimuth (float): The angle between 0 and 360

    Returns:
        A NumPy array representing the coordinates of the point on the sphere.
    """
    # Convert angles to radians
    inclination_rad, azimuth_rad = jnp.meshgrid(
        jnp.deg2rad(inclination), jnp.deg2rad(azimuth)
    )
    # jnp.meshgrid(inclination, azimuth)

    # Calculate the Cartesian coordinates using the spherical coordinate system conversion formula
    x = radius * jnp.sin(inclination_rad) * jnp.cos(azimuth_rad)
    y = radius * jnp.sin(inclination_rad) * jnp.sin(azimuth_rad)
    z = radius * jnp.cos(inclination_rad)

    return jnp.asarray([x, y, z]).transpose(1, 2, 0)
