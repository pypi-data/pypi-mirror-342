from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import inspect
else:
    inspect, = jac_import('inspect', 'py')
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from typing import Optional, Type, Union
else:
    Optional, Type, Union = jac_import('typing', 'py', items={'Optional': None, 'Type': None, 'Union': None})
if typing.TYPE_CHECKING:
    from dataclasses import fields, MISSING
else:
    fields, MISSING = jac_import('dataclasses', 'py', items={'fields': None, 'MISSING': None})

class GraphNode(Node):
    id: str = field('')
    graph_children: bool = field(False)
    graph_self: bool = field(True)
    protected_attrs: list = field(gen=lambda: JacList(['id']))
    transient_attrs: list = field(gen=lambda: JacList(['__jac__', 'protected_attrs', 'transient_attrs', 'graph_children', 'graph_self', 'package_path']))
    _context: dict = field(gen=lambda: {})
    logger: static[Logger] = logging.getLogger(__name__)

    def __post_init__(self) -> None:
        if not self.id:
            self.id = jid(self)

    def get_type(self) -> str:
        return type(self).__name__

    def get_parent_type(self) -> str:
        return type(super()()).__name__

    def export(self, ignore_keys: list=JacList([]), modified_context: bool=False) -> dict:
        if modified_context:
            ignore_keys = ignore_keys + self.transient_attrs
            cls = type(self)
            default_values = {}
            for f in fields(self):
                if f.default is not MISSING:
                    default_values[f.name] = f.default
                elif f.default_factory is not MISSING:
                    default_values[f.name] = f.default_factory()
            node_export = Utils.export_to_dict(self, ignore_keys)
            return Utils.sanitize_dict_context(descriptor_data=node_export, action_data=default_values, keys_to_remove=ignore_keys)
        else:
            ignore_keys = ignore_keys + self.transient_attrs
            node_export = Utils.export_to_dict(self, ignore_keys)
            if isinstance(node_export['_context'], dict):
                node_export.update(node_export['_context'])
                del node_export['_context']
            return node_export

    def update(self, data: dict={}) -> GraphNode:
        if data:
            for attr in data.keys():
                if attr not in self.protected_attrs:
                    if hasattr(self, attr):
                        setattr(self, attr, data[attr])
                    else:
                        self._context[attr] = data[attr]
        self.postupdate()
        return self

    def postupdate(self) -> None:
        pass