# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# -*- coding: utf-8 -*-

from __future__ import annotations

import brainunit as u
import jax
import numbers
from typing import Callable

from brainstate import environ, init, surrogate
from brainstate._state import HiddenState, ParamState
from brainstate.nn._exp_euler import exp_euler_step
from brainstate.nn._module import Module
from brainstate.typing import Size, ArrayLike
from ._dynamics_neuron import Neuron

__all__ = [
    'LeakyRateReadout',
    'LeakySpikeReadout',
]


class LeakyRateReadout(Module):
    """
    Leaky dynamics for the read-out module used in the Real-Time Recurrent Learning.
    """
    __module__ = 'brainstate.nn'

    def __init__(
        self,
        in_size: Size,
        out_size: Size,
        tau: ArrayLike = 5. * u.ms,
        w_init: Callable = init.KaimingNormal(),
        name: str = None,
    ):
        super().__init__(name=name)

        # parameters
        self.in_size = (in_size,) if isinstance(in_size, numbers.Integral) else tuple(in_size)
        self.out_size = (out_size,) if isinstance(out_size, numbers.Integral) else tuple(out_size)
        self.tau = init.param(tau, self.in_size)
        self.decay = u.math.exp(-environ.get_dt() / self.tau)

        # weights
        self.weight = ParamState(init.param(w_init, (self.in_size[0], self.out_size[0])))

    def init_state(self, batch_size=None, **kwargs):
        self.r = HiddenState(init.param(init.Constant(0.), self.out_size, batch_size))

    def reset_state(self, batch_size=None, **kwargs):
        self.r.value = init.param(init.Constant(0.), self.out_size, batch_size)

    def update(self, x):
        self.r.value = self.decay * self.r.value + x @ self.weight.value
        return self.r.value


class LeakySpikeReadout(Neuron):
    """
    Integrate-and-fire neuron model with leaky dynamics.
    """

    __module__ = 'brainstate.nn'

    def __init__(
        self,
        in_size: Size,
        tau: ArrayLike = 5. * u.ms,
        V_th: ArrayLike = 1. * u.mV,
        w_init: Callable = init.KaimingNormal(unit=u.mV),
        V_initializer: ArrayLike = init.ZeroInit(unit=u.mV),
        spk_fun: Callable = surrogate.ReluGrad(),
        spk_reset: str = 'soft',
        name: str = None,
    ):
        super().__init__(in_size, name=name, spk_fun=spk_fun, spk_reset=spk_reset)

        # parameters
        self.tau = init.param(tau, (self.varshape,))
        self.V_th = init.param(V_th, (self.varshape,))
        self.V_initializer = V_initializer

        # weights
        self.weight = ParamState(init.param(w_init, (self.in_size[-1], self.out_size[-1])))

    def init_state(self, batch_size, **kwargs):
        self.V = HiddenState(init.param(self.V_initializer, self.varshape, batch_size))

    def reset_state(self, batch_size, **kwargs):
        self.V.value = init.param(self.V_initializer, self.varshape, batch_size)

    @property
    def spike(self):
        return self.get_spike(self.V.value)

    def get_spike(self, V):
        v_scaled = (V - self.V_th) / self.V_th
        return self.spk_fun(v_scaled)

    def update(self, spk):
        # reset
        last_V = self.V.value
        last_spike = self.get_spike(last_V)
        V_th = self.V_th if self.spk_reset == 'soft' else jax.lax.stop_gradient(last_V)
        V = last_V - V_th * last_spike
        # membrane potential
        x = spk @ self.weight.value
        dv = lambda v: (-v + self.sum_current_inputs(x, v)) / self.tau
        V = exp_euler_step(dv, V)
        self.V.value = self.sum_delta_inputs(V)
        return self.get_spike(V)
