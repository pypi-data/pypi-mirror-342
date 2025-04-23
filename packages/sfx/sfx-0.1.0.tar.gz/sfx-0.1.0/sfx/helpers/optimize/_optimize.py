"""Helpers to batch process an operation."""

__all__ = [
    "tcg_solve_states",
    "tcg_solve",
    "trust_tcg_solve",
    "TrustRegionResults",
    "TrustTCGOptions",
    "TCGOptions",
]

from collections import namedtuple
from dataclasses import dataclass
from functools import partial

import jax
import jax.numpy as jnp
from jax import lax

from sfx.core.sfx_object import SFXIterable, SFXObject

_vdot = partial(jnp.vdot, precision=lax.Precision.HIGHEST)


@dataclass(kw_only=True, repr=False)
class TCGOptions(SFXObject):
    """Base class for truncated gradient options."""

    __slots__ = ["__dict__"]

    def __init__(self, **kwargs):
        _default_kwargs = {
            "maxiter": None,
            "precond": None,
            "theta": 0.5,
            "fgr": 0.1,
        }

        self.__dict__.update(_default_kwargs | kwargs)


@dataclass(kw_only=True, repr=False)
class TrustTCGOptions(SFXObject):
    """Base class for trust-region with truncated gradient options."""

    __slots__ = ["__dict__"]

    def __init__(self, **kwargs):
        _default_kwargs = {
            "maxiter": None,
            "radius": 1.0,
            "min_ratio": 0.01,
            "max_ratio": 0.9,
            "min_scale": 0.25,
            "max_scale": 2.5,
            "eps_radius": jnp.finfo(0.0).eps,
            "eps_gradient": jnp.sqrt(jnp.finfo(0.0).eps),
            "tcg_options": TCGOptions(),
        }

        self.__dict__.update(_default_kwargs | kwargs)


class TrustRegionResults(SFXIterable):
    """Base class for trust-region method results."""

    __slots__ = [
        "x",
        "f",
        "g",
        "H",
        "radius",
        "ratio",
        "k",
    ]

    def __init__(self, x, f, g, H, radius, ratio, k):
        """Initialize the results."""
        self.x = x
        self.f = f
        self.g = g
        self.H = H
        self.radius = radius
        self.ratio = ratio
        self.k = k


def trust_tcg_solve(fun, x0, args=(), *, options=TrustTCGOptions()):
    dim = x0.shape[0]

    if options.maxiter is None:
        maxiter = 10 * dim
    else:
        maxiter = options.maxiter

    def model(x):
        fk = fun(x, *args)
        gk = jax.grad(fun)(x, *args)
        Hk = jax.hessian(fun)(x, *args)
        return fk, gk, Hk

    def radius_update(rho_new, sk_norm, radius, g, s, f, m_new, f_new):
        def _cond0():
            gdots = _vdot(g, s)

            gamma_bad = jnp.divide(
                (1 - options.max_ratio) * _vdot(g, s),
                (1 - options.max_ratio)
                * (f + gdots + options.max_ratio * m_new - f_new),
            )
            _a = options.min_scale * sk_norm
            _b = jnp.where(0.0625 >= gamma_bad, 0.625, gamma_bad) * radius
            return jnp.where(_a < _b, _a, _b)

        def _cond1():
            return options.min_scale * sk_norm

        def _cond2():
            return radius

        def _cond3():
            _a = options.max_scale * sk_norm
            _b = radius
            return jnp.where(_a >= _b, _a, _b)

        return jax.lax.switch(
            0 * (rho_new < 0.0)
            + 1 * ((rho_new > 0.0) & (rho_new < options.min_ratio))
            + 2 * ((rho_new >= options.min_ratio) & (rho_new < options.max_ratio))
            + 3 * (rho_new >= options.max_ratio),
            [_cond0, _cond1, _cond2, _cond3],
        )

    def cond_fun(value):
        x, _, g, H, radius, _, _, k = value
        # Could be replaced by an approximation of the inverse Hessian
        invH = jnp.linalg.inv(H[k])
        x_norm = jnp.linalg.norm(x[k])
        return (
            (radius[k] > options.eps_radius * x_norm)
            & (g[k].T @ invH @ g[k] > options.eps_gradient)
            & (k < maxiter)
        )

    def body_fun(value):
        x, f, g, H, radius, ratio, it, k = value

        xk = x[k]
        fk = f[k]
        gk = g[k]
        Hk = H[k]
        rk = radius[k]

        # Step 2. Acceptance of the trial point
        sk = tcg_solve(Hk, gk, rk, options=options.tcg_options)

        # Step 3. Acceptance of the trial point
        x_trial = xk + sk
        f_new = fun(x_trial, *args)
        # f_new, g_new, H_new = model(x_trial)

        # mk = fk + gk.T @ xk + 0.5 * xk.T @ Hk @ xk
        # m_new = f_new + g_new.T @ x_trial + 0.5 * x_trial.T @ H_new @ x_trial
        nominator = fk - f_new
        denominator = -gk.T @ sk - 0.5 * sk.T @ Hk @ sk

        rho_new = jnp.divide(nominator, denominator)

        x_new, f_new, g_new, H_new = jax.lax.cond(
            rho_new >= options.min_ratio,
            lambda: (xk + sk, *model(xk + sk)),
            lambda: (xk, fk, gk, Hk),
        )

        # Step 4. Trust-regio radius update
        sk_norm = jnp.linalg.norm(sk)
        radius_new = radius_update(
            rho_new,
            sk_norm,
            rk,
            gk,
            sk,
            fk,
            fk - denominator,
            f_new,
        )

        k_new = k + 1

        return (
            x.at[k_new].set(x_new),
            f.at[k_new].set(f_new),
            g.at[k_new].set(g_new),
            H.at[k_new].set(H_new),
            radius.at[k_new].set(radius_new),
            ratio.at[k_new].set(rho_new),
            it.at[k_new].set(k_new),
            k_new,
        )

    _length = maxiter + 1

    _x = jnp.full((_length, dim), jnp.nan).at[0].set(x0)

    f0, g0, H0 = model(x0)
    _f = jnp.full((_length,), jnp.nan).at[0].set(f0)
    _g = jnp.full((_length, dim), jnp.nan).at[0].set(g0)
    _H = jnp.full((_length, dim, dim), jnp.nan).at[0].set(H0)

    _radius = jnp.full((_length,), jnp.nan).at[0].set(options.radius)
    _ratio = jnp.full((_length), jnp.nan)
    _iter = jnp.zeros(_length, dtype=jnp.int_)

    initial_value = (_x, _f, _g, _H, _radius, _ratio, _iter, 0)

    return TrustRegionResults(*lax.while_loop(cond_fun, body_fun, initial_value)[:-1])


def tcg_solve(
    H, g, radius, options=TCGOptions()
):  # M=None, theta=0.5, kfgr=0.1, maxiter=None):
    """Algorithm 7.5.1 from https://doi.org/10.1137/1.9780898719857"""
    dim = g.shape[0]

    if options.precond is None:
        M = jnp.eye(dim)
    else:
        M = options.precond

    if options.maxiter is None:
        maxiter = 10 * dim
    else:
        maxiter = options.maxiter

    theta = options.theta
    kfgr = options.fgr

    invM = jnp.linalg.inv(M)
    normg0 = jnp.linalg.norm(g)
    kfgrg0 = normg0**theta
    tolerance = normg0 * (kfgr * (kfgr <= kfgrg0) + kfgrg0 * (kfgrg0 < kfgr))

    def Mdot(a, b):
        return a.T @ M @ b

    def Mnorm(x):
        return jnp.sqrt(Mdot(x, x))

    def cond_fun(value):
        _, g, _, _, k, stop = value
        return (jnp.linalg.norm(g) >= tolerance) & (k < maxiter) & jnp.logical_not(stop)

    def true_fun(s, g, v, p, k, _):
        Mnormp2 = Mdot(p, p)

        sigma = jnp.divide(
            -Mdot(s, p)
            + jnp.sqrt(Mdot(s, p) ** 2 + Mnormp2 * (radius**2 - Mdot(s, s))),
            Mnormp2,
        )

        return (s + sigma * p, g, v, p, k, True)

    def false_fun(s, g, v, p, k, alpha):
        s_new = s + alpha * p
        g_new = g + alpha * H @ p
        v_new = invM @ g_new
        beta = jnp.divide(_vdot(g_new, v_new), _vdot(g, v))
        p_new = -v_new + beta * p
        return (s_new, g_new, v_new, p_new, k + 1, False)

    def body_fun(value):
        s, g, v, p, k, _ = value
        kappa = p @ H @ p
        alpha = g @ v / kappa

        return jax.lax.cond(
            (kappa <= 0.0) | (Mnorm(s + alpha * p) >= radius),
            true_fun,
            false_fun,
            s,
            g,
            v,
            p,
            k,
            alpha,
        )

    s0 = jnp.zeros_like(g)
    g0 = g
    v0 = invM @ g0
    p0 = -v0
    initial_value = (s0, g, v0, p0, 0, False)

    s_final, *_ = lax.while_loop(cond_fun, body_fun, initial_value)

    return s_final


_tcg_states = namedtuple("tcg_states", "s g v p k stop")


def tcg_solve_states(H, g, radius, M=None, theta=0.5, kfgr=0.1, maxiter=None):
    """Algorithm 7.5.1 from https://doi.org/10.1137/1.9780898719857"""
    dim = g.shape[0]
    if M is None:
        M = jnp.eye(dim)

    if maxiter is None:
        maxiter = 10 * dim

    invM = jnp.linalg.inv(M)
    normg0 = jnp.linalg.norm(g)
    kfgrg0 = normg0**theta
    tolerance = normg0 * (kfgr * (kfgr <= kfgrg0) + kfgrg0 * (kfgrg0 < kfgr))

    def Mdot(a, b):
        return a.T @ M @ b

    def Mnorm(x):
        return jnp.sqrt(Mdot(x, x))

    def cond_fun(value):
        _, g, _, _, _, stop, i = value
        return (
            (jnp.linalg.norm(g[i]) >= tolerance)
            & (i < maxiter)
            & jnp.logical_not(stop[i])
        )

    def true_fun(s, g, v, p, k, _):
        Mnormp2 = Mdot(p, p)

        sigma = jnp.divide(
            -Mdot(s, p)
            + jnp.sqrt(Mdot(s, p) ** 2 + Mnormp2 * (radius**2 - Mdot(s, s))),
            Mnormp2,
        )

        return (s + sigma * p, g, v, p, k + 1, True)

    def false_fun(s, g, v, p, k, alpha):
        s_new = s + alpha * p
        g_new = g + alpha * H @ p
        v_new = invM @ g_new
        beta = jnp.divide(_vdot(g_new, v_new), _vdot(g, v))
        p_new = -v_new + beta * p
        return (s_new, g_new, v_new, p_new, k + 1, False)

    def body_fun(value):
        s, g, v, p, k, stop, i = value
        kappa = p[i] @ H @ p[i]
        alpha = g[i] @ v[i] / kappa

        s_new, g_new, v_new, p_new, i_new, stop_new = jax.lax.cond(
            (kappa <= 0.0) | (Mnorm(s[i] + alpha * p[i]) >= radius),
            true_fun,
            false_fun,
            s[i],
            g[i],
            v[i],
            p[i],
            i,
            alpha,
        )

        return (
            s.at[i_new].set(s_new),
            g.at[i_new].set(g_new),
            v.at[i_new].set(v_new),
            p.at[i_new].set(p_new),
            k.at[i_new].set(i_new),
            stop.at[i_new].set(stop_new),
            i_new,
        )

    _length = maxiter + 1
    _s = jnp.full((_length, dim), jnp.nan).at[0].set(jnp.zeros_like(g))
    _g = jnp.full((_length, dim), jnp.nan).at[0].set(g)
    _v = jnp.full((_length, dim), jnp.nan).at[0].set(invM @ _g[0])
    _p = jnp.full((_length, dim), jnp.nan).at[0].set(-_v[0])
    _k = jnp.zeros(_length, dtype=jnp.int_)
    _stop = jnp.zeros((_length), dtype=jnp.bool_)
    initial_value = (_s, _g, _v, _p, _k, _stop, 0)

    return _tcg_states(*lax.while_loop(cond_fun, body_fun, initial_value)[:-1])
