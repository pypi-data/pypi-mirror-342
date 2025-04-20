"""Main package for Django Components."""

# Public API
# NOTE: Middleware is exposed via django_components.middleware
# NOTE: Some of the documentation is generated based on these exports
# isort: off
from django_components.app_settings import ContextBehavior, ComponentsSettings
from django_components.attributes import format_attributes, merge_attributes
from django_components.autodiscovery import autodiscover, import_libraries
from django_components.util.command import (
    CommandArg,
    CommandArgGroup,
    CommandHandler,
    CommandLiteralAction,
    CommandParserInput,
    CommandSubcommand,
    ComponentCommand,
)
from django_components.component import (
    Component,
    ComponentInput,
    ComponentVars,
    all_components,
    get_component_by_class_id,
)
from django_components.component_media import ComponentMediaInput, ComponentMediaInputPath
from django_components.component_registry import (
    AlreadyRegistered,
    ComponentRegistry,
    NotRegistered,
    RegistrySettings,
    register,
    registry,
    all_registries,
)
from django_components.components import DynamicComponent
from django_components.dependencies import render_dependencies
from django_components.extension import (
    ComponentExtension,
    OnComponentRegisteredContext,
    OnComponentUnregisteredContext,
    OnRegistryCreatedContext,
    OnRegistryDeletedContext,
    OnComponentClassCreatedContext,
    OnComponentClassDeletedContext,
    OnComponentInputContext,
    OnComponentDataContext,
)
from django_components.extensions.cache import ComponentCache
from django_components.extensions.defaults import ComponentDefaults, Default
from django_components.extensions.view import ComponentView
from django_components.extensions.url import ComponentUrl, get_component_url
from django_components.library import TagProtectedError
from django_components.node import BaseNode, template_tag
from django_components.slots import SlotContent, Slot, SlotFunc, SlotRef, SlotResult
from django_components.tag_formatter import (
    ComponentFormatter,
    ShorthandComponentFormatter,
    TagFormatterABC,
    TagResult,
    component_formatter,
    component_shorthand_formatter,
)
from django_components.template import cached_template
import django_components.types as types
from django_components.util.loader import ComponentFileEntry, get_component_dirs, get_component_files
from django_components.util.routing import URLRoute, URLRouteHandler
from django_components.util.types import EmptyTuple, EmptyDict

# isort: on


__all__ = [
    "all_components",
    "all_registries",
    "AlreadyRegistered",
    "autodiscover",
    "BaseNode",
    "cached_template",
    "CommandArg",
    "CommandArgGroup",
    "CommandHandler",
    "CommandLiteralAction",
    "CommandParserInput",
    "CommandSubcommand",
    "Component",
    "ComponentCache",
    "ComponentCommand",
    "ComponentDefaults",
    "ComponentExtension",
    "ComponentFileEntry",
    "ComponentFormatter",
    "ComponentInput",
    "ComponentMediaInput",
    "ComponentMediaInputPath",
    "ComponentRegistry",
    "ComponentVars",
    "ComponentView",
    "ComponentUrl",
    "ComponentsSettings",
    "component_formatter",
    "component_shorthand_formatter",
    "ContextBehavior",
    "Default",
    "DynamicComponent",
    "EmptyTuple",
    "EmptyDict",
    "format_attributes",
    "get_component_by_class_id",
    "get_component_dirs",
    "get_component_files",
    "get_component_url",
    "import_libraries",
    "merge_attributes",
    "NotRegistered",
    "OnComponentClassCreatedContext",
    "OnComponentClassDeletedContext",
    "OnComponentDataContext",
    "OnComponentInputContext",
    "OnComponentRegisteredContext",
    "OnComponentUnregisteredContext",
    "OnRegistryCreatedContext",
    "OnRegistryDeletedContext",
    "register",
    "registry",
    "RegistrySettings",
    "render_dependencies",
    "ShorthandComponentFormatter",
    "SlotContent",
    "Slot",
    "SlotFunc",
    "SlotRef",
    "SlotResult",
    "TagFormatterABC",
    "TagProtectedError",
    "TagResult",
    "template_tag",
    "types",
    "URLRoute",
    "URLRouteHandler",
]
