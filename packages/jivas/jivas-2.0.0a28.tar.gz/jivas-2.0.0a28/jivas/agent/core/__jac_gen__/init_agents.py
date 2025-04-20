from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import yaml
else:
    yaml, = jac_import('yaml', 'py')
if typing.TYPE_CHECKING:
    import io
else:
    io, = jac_import('io', 'py')
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    import traceback
else:
    traceback, = jac_import('traceback', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from app import App
else:
    App, = jac_import('app', items={'App': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})
if typing.TYPE_CHECKING:
    from graph_walker import graph_walker
else:
    graph_walker, = jac_import('graph_walker', items={'graph_walker': None})
if typing.TYPE_CHECKING:
    from import_agent import import_agent
else:
    import_agent, = jac_import('import_agent', items={'import_agent': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import jvdata_file_interface
else:
    jvdata_file_interface, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'jvdata_file_interface': None})

class init_agents(graph_walker, Walker):
    reporting: bool = field(False)
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_app(self, here: App) -> None:
        if not self.visit(here.refs().filter(Agents, None)):
            self.logger.debug('agents node created')
            agents_node = here.connect(Agents())
            self.visit(agents_node)

    @with_entry
    def on_agents(self, here: Agents) -> None:
        if (agent_nodes := here.get_all()):
            for agent_node in agent_nodes:
                try:
                    self.logger.info(f'initializing agent {agent_node.name}')
                    file_bytes = jvdata_file_interface.get_file(agent_node.descriptor)
                    if not file_bytes:
                        self.logger.error(f'agent descriptor not found: {agent_node.descriptor}')
                        continue
                    descriptor = ''
                    file = io.BytesIO(file_bytes)
                    descriptor = yaml.safe_load(file)
                    if descriptor:
                        here.spawn(import_agent(descriptor=descriptor, reporting=self.reporting))
                except Exception as e:
                    self.logger.error(f'an exception occurred, {traceback.format_exc()}')