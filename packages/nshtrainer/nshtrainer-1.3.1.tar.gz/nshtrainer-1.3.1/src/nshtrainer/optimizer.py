from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Annotated, Any, Literal, Tuple, Union

import nshconfig as C
import torch.nn as nn
from torch import Tensor
from torch.optim import Optimizer
from typing_extensions import TypeAliasType, final, override


class OptimizerConfigBase(C.Config, ABC):
    @abstractmethod
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ) -> Optimizer: ...


optimizer_registry = C.Registry(OptimizerConfigBase, discriminator="name")


@final
@optimizer_registry.register
class AdamWConfig(OptimizerConfigBase):
    name: Literal["adamw"] = "adamw"

    lr: float
    """Learning rate for the optimizer."""

    weight_decay: float = 1.0e-2
    """Weight decay (L2 penalty) for the optimizer."""

    betas: tuple[float, float] = (0.9, 0.999)
    """
    Betas for the optimizer:
    (beta1, beta2) are the coefficients used for computing running averages of
    gradient and its square.
    """

    eps: float = 1e-8
    """Term added to the denominator to improve numerical stability."""

    amsgrad: bool = False
    """Whether to use the AMSGrad variant of this algorithm."""

    maximize: bool = False
    """Maximize the objective with respect to the params, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import AdamW

        return AdamW(
            parameters,
            lr=self.lr,
            weight_decay=self.weight_decay,
            betas=self.betas,
            eps=self.eps,
            amsgrad=self.amsgrad,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
        )


@final
@optimizer_registry.register
class AdafactorConfig(OptimizerConfigBase):
    name: Literal["adafactor"] = "adafactor"
    lr: float
    """Learning rate for the optimizer. If None, uses relative step size."""

    eps1: float | None = None
    """Term added to the denominator to improve numerical stability (default: None)."""

    eps2: float = 1e-3
    """Term added to the denominator to improve numerical stability (default: 1e-3)."""

    beta2_decay: float = -0.8
    """Coefficient used for computing running averages of square gradient (default: -0.8)."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) (default: 0.0)."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import Adafactor

        return Adafactor(
            parameters,
            lr=self.lr,
            eps=(self.eps1, self.eps2),
            beta2_decay=self.beta2_decay,
            weight_decay=self.weight_decay,
            maximize=self.maximize,
        )


@final
@optimizer_registry.register
class AdadeltaConfig(OptimizerConfigBase):
    name: Literal["adadelta"] = "adadelta"

    lr: float
    """Learning rate for the optimizer."""

    rho: float = 0.9
    """Coefficient used for computing a running average of squared gradients."""

    eps: float = 1e-6
    """Term added to the denominator to improve numerical stability."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import Adadelta

        return Adadelta(
            parameters,
            lr=self.lr,
            rho=self.rho,
            eps=self.eps,
            weight_decay=self.weight_decay,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
        )


@final
@optimizer_registry.register
class AdagradConfig(OptimizerConfigBase):
    name: Literal["adagrad"] = "adagrad"

    lr: float
    """Learning rate for the optimizer."""

    lr_decay: float = 0.0
    """Learning rate decay."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    initial_accumulator_value: float = 0.0
    """Initial value for the accumulator."""

    eps: float = 1e-10
    """Term added to the denominator to improve numerical stability."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    fused: bool | None = None
    """Whether the fused implementation is used."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import Adagrad

        return Adagrad(
            parameters,
            lr=self.lr,
            lr_decay=self.lr_decay,
            weight_decay=self.weight_decay,
            initial_accumulator_value=self.initial_accumulator_value,
            eps=self.eps,
            maximize=self.maximize,
            foreach=self.foreach,
            differentiable=self.differentiable,
            fused=self.fused,
        )


@final
@optimizer_registry.register
class AdamConfig(OptimizerConfigBase):
    name: Literal["adam"] = "adam"

    lr: float
    """Learning rate for the optimizer."""

    betas: tuple[float, float] = (0.9, 0.999)
    """Coefficients used for computing running averages of gradient and its square."""

    eps: float = 1e-8
    """Term added to the denominator to improve numerical stability."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    amsgrad: bool = False
    """Whether to use the AMSGrad variant of this algorithm."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    fused: bool | None = None
    """Whether the fused implementation is used."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import Adam

        return Adam(
            parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            amsgrad=self.amsgrad,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
            fused=self.fused,
        )


@final
@optimizer_registry.register
class AdamaxConfig(OptimizerConfigBase):
    name: Literal["adamax"] = "adamax"

    lr: float
    """Learning rate for the optimizer."""

    betas: tuple[float, float] = (0.9, 0.999)
    """Coefficients used for computing running averages of gradient and its square."""

    eps: float = 1e-8
    """Term added to the denominator to improve numerical stability."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import Adamax

        return Adamax(
            parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
        )


@final
@optimizer_registry.register
class ASGDConfig(OptimizerConfigBase):
    name: Literal["asgd"] = "asgd"

    lr: float
    """Learning rate for the optimizer."""

    lambd: float = 1e-4
    """Decay term."""

    alpha: float = 0.75
    """Power for eta update."""

    t0: float = 1e6
    """Point at which to start averaging."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import ASGD

        return ASGD(
            parameters,
            lr=self.lr,
            lambd=self.lambd,
            alpha=self.alpha,
            t0=self.t0,
            weight_decay=self.weight_decay,
            maximize=self.maximize,
        )


@final
@optimizer_registry.register
class NAdamConfig(OptimizerConfigBase):
    name: Literal["nadam"] = "nadam"

    lr: float
    """Learning rate for the optimizer."""

    betas: tuple[float, float] = (0.9, 0.999)
    """Coefficients used for computing running averages of gradient and its square."""

    eps: float = 1e-8
    """Term added to the denominator to improve numerical stability."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    momentum_decay: float = 4e-3
    """Momentum decay."""

    decoupled_weight_decay: bool = False
    """Whether to use decoupled weight decay."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import NAdam

        return NAdam(
            parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            momentum_decay=self.momentum_decay,
            decoupled_weight_decay=self.decoupled_weight_decay,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
        )


@final
@optimizer_registry.register
class RAdamConfig(OptimizerConfigBase):
    name: Literal["radam"] = "radam"

    lr: float
    """Learning rate for the optimizer."""

    betas: tuple[float, float] = (0.9, 0.999)
    """Coefficients used for computing running averages of gradient and its square."""

    eps: float = 1e-8
    """Term added to the denominator to improve numerical stability."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    decoupled_weight_decay: bool = False
    """Whether to use decoupled weight decay."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import RAdam

        return RAdam(
            parameters,
            lr=self.lr,
            betas=self.betas,
            eps=self.eps,
            weight_decay=self.weight_decay,
            decoupled_weight_decay=self.decoupled_weight_decay,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
        )


@final
@optimizer_registry.register
class RMSpropConfig(OptimizerConfigBase):
    name: Literal["rmsprop"] = "rmsprop"

    lr: float
    """Learning rate for the optimizer."""

    alpha: float = 0.99
    """Smoothing constant."""

    eps: float = 1e-8
    """Term added to the denominator to improve numerical stability."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    momentum: float = 0.0
    """Momentum factor."""

    centered: bool = False
    """If True, compute the centered RMSProp, the gradient is normalized by an estimation of its variance."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    capturable: bool = False
    """Whether this instance is safe to capture in a CUDA graph."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import RMSprop

        return RMSprop(
            parameters,
            lr=self.lr,
            alpha=self.alpha,
            eps=self.eps,
            weight_decay=self.weight_decay,
            momentum=self.momentum,
            centered=self.centered,
            maximize=self.maximize,
            foreach=self.foreach,
            capturable=self.capturable,
            differentiable=self.differentiable,
        )


@final
@optimizer_registry.register
class RpropConfig(OptimizerConfigBase):
    name: Literal["rprop"] = "rprop"

    lr: float
    """Learning rate for the optimizer."""

    etas: tuple[float, float] = (0.5, 1.2)
    """Pair of (etaminus, etaplus), multiplicative increase and decrease factors."""

    step_sizes: tuple[float, float] = (1e-6, 50.0)
    """Pair of minimal and maximal allowed step sizes."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import Rprop

        return Rprop(
            parameters,
            lr=self.lr,
            etas=self.etas,
            step_sizes=self.step_sizes,
            maximize=self.maximize,
        )


@final
@optimizer_registry.register
class SGDConfig(OptimizerConfigBase):
    name: Literal["sgd"] = "sgd"

    lr: float
    """Learning rate for the optimizer."""

    momentum: float = 0.0
    """Momentum factor."""

    dampening: float = 0.0
    """Dampening for momentum."""

    weight_decay: float = 0.0
    """Weight decay (L2 penalty) for the optimizer."""

    nesterov: bool = False
    """Enables Nesterov momentum."""

    maximize: bool = False
    """Maximize the params based on the objective, instead of minimizing."""

    foreach: bool | None = None
    """Whether foreach implementation of optimizer is used."""

    differentiable: bool = False
    """Whether autograd should occur through the optimizer step in training."""

    fused: bool | None = None
    """Whether the fused implementation is used."""

    @override
    def create_optimizer(
        self,
        parameters: Iterable[nn.Parameter] | Iterable[dict[str, Any]],
    ):
        from torch.optim import SGD

        return SGD(
            parameters,
            lr=self.lr,
            momentum=self.momentum,
            dampening=self.dampening,
            weight_decay=self.weight_decay,
            nesterov=self.nesterov,
            maximize=self.maximize,
            foreach=self.foreach,
            differentiable=self.differentiable,
            fused=self.fused,
        )


OptimizerConfig = TypeAliasType(
    "OptimizerConfig",
    Annotated[OptimizerConfigBase, optimizer_registry.DynamicResolution()],
)
