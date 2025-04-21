from __future__ import annotations

import signal
from typing import Literal

from typing_extensions import TypeAliasType, override

from .base import PluginConfigBase, plugin_registry


@plugin_registry.register
class KubeflowEnvironmentPlugin(PluginConfigBase):
    """Environment for distributed training using the PyTorchJob operator from Kubeflow.

    This environment, unlike others, does not get auto-detected and needs to be passed
    to the Fabric/Trainer constructor manually.
    """

    name: Literal["kubeflow_environment"] = "kubeflow_environment"

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.kubeflow import KubeflowEnvironment

        return KubeflowEnvironment()


@plugin_registry.register
class LightningEnvironmentPlugin(PluginConfigBase):
    """The default environment used by Lightning for a single node or free cluster (not managed).

    There are two modes the Lightning environment can operate with:
    1. User launches main process by `python train.py ...` with no additional environment variables.
       Lightning will spawn new worker processes for distributed training in the current node.
    2. User launches all processes manually or with utilities like `torch.distributed.launch`.
       The appropriate environment variables need to be set, and at minimum `LOCAL_RANK`.
    """

    name: Literal["lightning_environment"] = "lightning_environment"

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.lightning import LightningEnvironment

        return LightningEnvironment()


@plugin_registry.register
class LSFEnvironmentPlugin(PluginConfigBase):
    """An environment for running on clusters managed by the LSF resource manager.

    It is expected that any execution using this ClusterEnvironment was executed
    using the Job Step Manager i.e. `jsrun`.
    """

    name: Literal["lsf_environment"] = "lsf_environment"

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.lsf import LSFEnvironment

        return LSFEnvironment()


@plugin_registry.register
class MPIEnvironmentPlugin(PluginConfigBase):
    """An environment for running on clusters with processes created through MPI.

    Requires the installation of the `mpi4py` package.
    """

    name: Literal["mpi_environment"] = "mpi_environment"

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.mpi import MPIEnvironment

        return MPIEnvironment()


SignalAlias = TypeAliasType(
    "SignalAlias",
    Literal[
        "SIGABRT",
        "SIGFPE",
        "SIGILL",
        "SIGINT",
        "SIGSEGV",
        "SIGTERM",
        "SIGBREAK",
        "CTRL_C_EVENT",
        "CTRL_BREAK_EVENT",
        "SIGALRM",
        "SIGBUS",
        "SIGCHLD",
        "SIGCONT",
        "SIGHUP",
        "SIGIO",
        "SIGIOT",
        "SIGKILL",
        "SIGPIPE",
        "SIGPROF",
        "SIGQUIT",
        "SIGSTOP",
        "SIGSYS",
        "SIGTRAP",
        "SIGTSTP",
        "SIGTTIN",
        "SIGTTOU",
        "SIGURG",
        "SIGUSR1",
        "SIGUSR2",
        "SIGVTALRM",
        "SIGWINCH",
        "SIGXCPU",
        "SIGXFSZ",
        "SIGEMT",
        "SIGINFO",
        "SIGCLD",
        "SIGPOLL",
        "SIGPWR",
        "SIGRTMAX",
        "SIGRTMIN",
        "SIGSTKFLT",
    ],
)


@plugin_registry.register
class SLURMEnvironmentPlugin(PluginConfigBase):
    """An environment for running on clusters managed by the SLURM resource manager."""

    name: Literal["slurm_environment"] = "slurm_environment"

    auto_requeue: bool = True
    """Whether automatic job resubmission is enabled or not."""

    requeue_signal: SignalAlias | None = None
    """The signal that SLURM will send to indicate that the job should be requeued."""

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.slurm import SLURMEnvironment

        requeue_signal = None
        if self.requeue_signal is not None:
            try:
                requeue_signal = signal.Signals[self.requeue_signal]
            except KeyError:
                raise ValueError(
                    f"Invalid signal name: {self.requeue_signal}. "
                    "Please provide a valid signal name from the signal module."
                )

        return SLURMEnvironment(
            auto_requeue=self.auto_requeue,
            requeue_signal=requeue_signal,
        )


@plugin_registry.register
class TorchElasticEnvironmentPlugin(PluginConfigBase):
    """Environment for fault-tolerant and elastic training with torchelastic."""

    name: Literal["torchelastic_environment"] = "torchelastic_environment"

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.torchelastic import (
            TorchElasticEnvironment,
        )

        return TorchElasticEnvironment()


@plugin_registry.register
class XLAEnvironmentPlugin(PluginConfigBase):
    """Cluster environment for training on a TPU Pod with the PyTorch/XLA library."""

    name: Literal["xla_environment"] = "xla_environment"

    @override
    def create_plugin(self, trainer_config):
        from lightning.fabric.plugins.environments.xla import XLAEnvironment

        return XLAEnvironment()
