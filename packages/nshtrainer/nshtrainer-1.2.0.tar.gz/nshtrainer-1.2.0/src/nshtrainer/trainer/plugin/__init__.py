from __future__ import annotations

from typing import Annotated

from typing_extensions import TypeAliasType

from . import environment as environment
from . import io as io
from . import layer_sync as layer_sync
from . import precision as precision
from .base import Plugin as Plugin
from .base import PluginConfigBase as PluginConfigBase
from .base import plugin_registry as plugin_registry

PluginConfig = TypeAliasType(
    "PluginConfig",
    Annotated[PluginConfigBase, plugin_registry.DynamicResolution()],
)
