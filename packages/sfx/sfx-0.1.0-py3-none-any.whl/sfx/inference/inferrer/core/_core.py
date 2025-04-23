# type: ignore
__all__ = [
    "Ansatz",
    "BasisCriterions",
    "Coefficients",
    "Inferrer",
    "InferrerNL",
    "Projections",
    "InferenceOptions",
    "MultiModelSelection",
]

from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Dict, Optional

import jax
import jax.numpy as jnp
from jax import lax
from jax.tree_util import Partial

from sfx.basis.basis import Basis
from sfx.basis.parameters import ParameterGroup
from sfx.core.sfx_object import SFXCallable, SFXIterable, SFXObject, SFXGroup
from sfx.helpers.format import make_func_differentiable
from sfx.inference.data import Data, DataGroup
from sfx.inference.projector import OrthonormalizationMatrix, Projector


@dataclass(kw_only=True, repr=False)
class InferenceOptions(SFXObject):
    """Base class for inference options."""

    __slots__ = ["__dict__"]

    def __init__(self, **kwargs):
        _default_kwargs = {"use_svd": False, "use_bridge": 0}

        self.__dict__.update(_default_kwargs | kwargs)


class Coefficients(SFXIterable):
    """Base class for coefficients."""

    __slots__ = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Projections(SFXIterable):
    """Base class for projections."""

    __slots__ = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class MultiModelSelection(SFXCallable):
    """Base class for OptimizationResult."""

    __slots__ = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class BasisCriterions(SFXGroup):
    """Base class for Basis criterions."""

    __slots__ = []

    def __init__(self, grp, gid=["NLLH", "BIC", "GBIC", "GBICp", "AIC", "GAIC"]):
        if len(grp) - len(gid) == 3:
            gid += ["EBIC", "GIC", "HGBICp"]

        elif len(grp) - len(gid) == 4:
            gid += ["EBIC", "GIC", "HGBICp", "AICC"]
        super().__init__(gid=gid, grp=grp)


class Inferrer(SFXCallable):
    """Base class for inferrer."""

    __slots__ = [
        "projector",
        "coefficients",
        "orthonormalization_matrix",
    ]

    _coefficient_type = Coefficients

    def __init__(
        self,
        projector: Projector,
        coefficients: Optional[DataGroup] = None,
        orthonormalization_matrix: Optional[DataGroup] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.projector = projector
        self.coefficients = coefficients
        self.orthonormalization_matrix = orthonormalization_matrix

    def __call__(
        self,
        data: Data,
        parameters: ParameterGroup,
        options: InferenceOptions = InferenceOptions(),
    ) -> None:
        super().__call__()

        _cls = type(self)

        (
            projections,
            orthonormalization_matrix,
            estimated_covariance,
            nbpoints,
        ) = self.projector.trajectory_integral.sum(
            self._project_on_basis,
            data,
            parameters=parameters,
            options=options,
        )

        self.projections = self.convert_projections(projections)
        _orthonormalization_matrix_type = OrthonormalizationMatrix(
            interactions=self.projector.basis.function.functions
        )

        self.orthonormalization_matrix = orthonormalization_matrix.map(
            lambda matrix: _orthonormalization_matrix_type.regroup(matrix),
        )
        self.estimated_covariance = estimated_covariance
        self.nbpoints = nbpoints
        return

    @abstractmethod
    def _project_on_basis(
        self,
        data: Data,
        parameters: ParameterGroup,
        options: InferenceOptions,
    ):
        raise NotImplementedError("Abstract method.")

    def convert_coefficients(self, coefficients):
        _cls = type(self)

        return _cls.convert_to_coefficient_type(
            jax.tree_util.tree_map(
                # Third group by interaction type
                lambda coeff: [
                    self.projector.basis.function.functions.regroup(c) for c in coeff
                ],
                # Second group basis criterions
                jax.tree_util.tree_map(
                    lambda coefficient: [BasisCriterions(c) for c in coefficient],
                    # First convert to DataGroup
                    self.projector.trajectory_integral.group.regroup(coefficients),
                ),
            )
        )

    def convert_hessian(self, hessian):
        _orthonormalization_matrix_type = OrthonormalizationMatrix(
            interactions=self.projector.basis.function.functions
        )

        return jax.tree_util.tree_map(
            # Third group by interaction type
            lambda hess: [_orthonormalization_matrix_type.regroup(h) for h in hess],
            # Second group basis criterions
            jax.tree_util.tree_map(
                lambda hess: [BasisCriterions(h) for h in hess],
                # First convert to DataGroup
                self.projector.trajectory_integral.group.regroup(hessian),
            ),
        )

    def convert_projections(self, projections):
        _cls = type(self)

        return _cls.convert_to_projection_type(
            jax.tree_util.tree_map(
                lambda proj: [
                    self.projector.basis.function.functions.regroup(p) for p in proj
                ],
                projections,
            )
        )

    def convert_criterions(self, criterions):
        return jax.tree_util.tree_map(
            lambda criterion: [BasisCriterions(c) for c in criterion],
            # Convert to DataGroup first
            self.projector.trajectory_integral.group.regroup(criterions),
        )

    def convert_orthonormalization_matrix(self, orthonormalization_matrix):
        _orthonormalization_matrix_type = OrthonormalizationMatrix(
            interactions=self.projector.basis.function.functions
        )

        return jax.tree_util.tree_map(
            lambda matrix: [
                _orthonormalization_matrix_type.regroup(mat) for mat in matrix
            ],
            orthonormalization_matrix,
        )

    @classmethod
    def convert_to_coefficient_type(cls, coefficient):
        """Generic method to convert to the coefficient type defined as a class attribute."""
        return cls._coefficient_type(coefficient)

    @classmethod
    def convert_to_projection_type(cls, projection):
        """Generic method to convert to the coefficient type defined as a class attribute."""
        return cls._projection_type(projection)


class InferrerNL(SFXCallable):
    __slots__ = [
        "projector",
        "average_inverse_diffusion",
        "optimization_result",
        "parameters",
        "errors",
    ]

    def __init__(
        self,
        projector: Projector,
        average_inverse_diffusion,
        optimization_result=None,
        parameters=None,
        errors=None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.projector = projector
        self.average_inverse_diffusion = average_inverse_diffusion
        self.optimization_result = optimization_result
        self.parameters = parameters
        self.errors = errors

    def __call__(self, data: Data, parameters: ParameterGroup):
        diff_func, diff_args, recombine = make_func_differentiable(
            self.cost_function, parameters, data
        )

        self.optimization_result = self._minimize(diff_func, data, diff_args)

        self.parameters = self.projector.trajectory_integral.map(
            lambda opt_res: recombine(opt_res.x),
            self.optimization_result,
        )

        self.errors = self.projector.trajectory_integral.map(
            lambda opt_res: recombine(2 * jnp.sqrt(jnp.diag(opt_res.hess_inv))),
            self.optimization_result,
        )

    @abstractmethod
    def _minimize(self, cost_function: Callable, data: Data, parameters: jax.Array):
        return None

    @abstractmethod
    def cost_function(self):
        pass


class Ansatz(SFXCallable):
    """Base class for ansatz."""

    __slots__ = ["basis", "combine_modifier"]

    def __init__(
        self,
        basis: Basis,
        combine_modifier: Callable | None = None,
        # coefficients: Coefficients,
        # parameters: ParameterGroup,
        *args,
        **kwargs,
    ) -> None:
        """
        :param modifier: modifies the output of the function.
        """
        super().__init__(*args, **kwargs)
        self.basis = basis

        if combine_modifier is None:

            @Partial
            def default_combine_modifier(coefficients, basis_values):
                # if type(coefficients) is type(basis_values):
                output = [
                    jnp.einsum(
                        "a,a...->...",
                        coeff.array,
                        bv.array,
                        precision=lax.Precision.HIGHEST,
                    )
                    for coeff, bv in zip(coefficients.grp, basis_values.grp)
                ]
                # [
                #    jnp.einsum(
                #        "a->",
                #        # "a,a...->...",
                #        coeff.grp,
                #        # bv.grp,
                #        precision=lax.Precision.HIGHEST,
                #    )
                #    for coeff, bv in zip(coefficients.grp, basis_values.grp)
                # ]

                # else:
                #     output = [
                #         [
                #             [
                #                 jnp.einsum(
                #                     "a,a...->...",
                #                     cc[i].grp,
                #                     bv.grp,
                #                     precision=lax.Precision.HIGHEST,
                #                 )
                #                 for i, bv in enumerate(basis_values.grp)
                #             ]
                #             for cc in c.grp
                #         ]
                #         for c in coefficients.grp
                #     ]
                return output

            self.combine_modifier = default_combine_modifier
        else:
            self.combine_modifier = combine_modifier

    def __call__(
        self, data: Data, parameters: ParameterGroup, coefficients: Coefficients
    ):
        super().__call__()

        # if len(data) > 1:
        #     groups = self.__scan_local__(data, parameters, coefficients)
        #     output = coefficients.regroup(groups)
        # else:
        output = coefficients.regroup(
            self.__call_local__(data, parameters, coefficients)
        )
        return output

    @partial(jax.jit, static_argnums=(0,))
    def __call_local__(
        self, data: Data, parameters: ParameterGroup, coefficients: Coefficients
    ):
        """Creates an ansatz by combining the coefficients with the interactions."""
        return self.combine_modifier(coefficients, self.basis(data, parameters))

    # @partial(jax.jit, static_argnums=(0,))
    # def __scan_local__(
    #     self, data: Data, parameters: ParameterGroup, coefficients: Coefficients
    # ) -> Any:
    #     @ProgressBarScan(len(data), message="Computing ansatz")
    #     def scan_compute_data(carry, data):
    #         parameters, coefficients = carry
    #         return (carry, self.__call_local__(data, parameters, coefficients))
    #
    #     return jax.lax.scan(
    #         scan_compute_data,
    #         (parameters, coefficients),
    #         (jnp.arange(len(data)), data),
    #     )[-1]
