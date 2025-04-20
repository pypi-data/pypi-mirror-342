from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
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
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core import graph_node, purge
else:
    graph_node, purge = jac_import('jivas.agent.core', items={'graph_node': None, 'purge': None})
if typing.TYPE_CHECKING:
    from graph_node import GraphNode
else:
    GraphNode, = jac_import('graph_node', items={'GraphNode': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.action import Action
else:
    Action, = jac_import('jivas.agent.action.action', items={'Action': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.interact_action import InteractAction
else:
    InteractAction, = jac_import('jivas.agent.action.interact_action', items={'InteractAction': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory import Memory
else:
    Memory, = jac_import('jivas.agent.memory.memory', items={'Memory': None})

class Agent(GraphNode, Node):
    logger: static[Logger] = logging.getLogger(__name__)
    published: bool = field(True)
    name: str = field('')
    description: str = field('')
    descriptor: str = field('')
    jpr_api_key: str = field('')
    agent_logging: bool = field(True)
    message_limit: int = field(1024)
    flood_block_time: int = field(300)
    window_time: int = field(20)
    flood_threshold: int = field(4)
    frame_size: int = field(10)
    tts_action: str = field('ElevenlabsTTSAction')
    stt_action: str = field('DeepgramSTTAction')
    vector_store_action: str = field('TypesenseVectorStoreAction')
    healthcheck_status: int = field(501)
    meta: dict = field(gen=lambda: {})

    def __post_init__(self) -> None:
        super().__post_init__()
        self.protected_attrs += JacList(['id', 'actions', 'descriptor', 'healthcheck_status', 'meta'])

    def get_memory(self) -> None:
        memory_node = Utils.node_obj(self.refs().filter(Memory, None))
        if not memory_node:
            self.connect((memory_node := Memory()))
            self.logger.debug('memory node created')
        return memory_node

    def get_actions(self) -> None:
        actions_node = Utils.node_obj(self.refs().filter(Actions, None))
        if not actions_node:
            self.connect((actions_node := Actions()))
            self.logger.debug('actions node created')
        return actions_node

    def get_tts_action(self) -> None:
        if (tts_action_node := self.get_actions().get(action_label=self.tts_action)):
            if tts_action_node.enabled:
                return tts_action_node
        return None

    def get_stt_action(self) -> None:
        if (stt_action_node := self.get_actions().get(action_label=self.stt_action)):
            if stt_action_node.enabled:
                return stt_action_node
        return None

    def get_vector_store_action(self) -> None:
        if (vector_store_action_node := self.get_actions().get(action_label=self.vector_store_action)):
            if vector_store_action_node.enabled:
                return vector_store_action_node
        return None

    def update(self, data: dict={}, with_actions: bool=False) -> Agent:
        agent_node = super().update(data=data)
        if with_actions and len(data.get('actions', JacList([]))) > 0:
            self.get_actions().install_actions(self.id, data['actions'], self.jpr_api_key)
        healthcheck_report = self.get_healthcheck_report()
        if healthcheck_report['status'] == 200:
            self.logger.info(healthcheck_report['message'])
        else:
            for label, detail in healthcheck_report['trace'].items():
                if detail.get('status') == False:
                    self.logger.error(f"[{label}] {detail.get('message')}")
                elif detail.get('status') == True and detail.get('severity') == 'warning':
                    self.logger.warning(f"[{label}] {detail.get('message')}")
        return agent_node

    def is_logging(self) -> None:
        return self.agent_logging

    def set_logging(self, agent_logging: bool) -> None:
        self.agent_logging = agent_logging

    def export_descriptor(self, file_path: str='', modified_context: bool=False) -> dict:
        try:
            self.logger.debug(f'exporting agent: {self.name}')
            agent_data = self.export(JacList([]), modified_context)
            agent_actions = JacList([])
            agent_actions = self.spawn(_export_actions(modified_context=modified_context)).action_nodes
            agent_data = {**agent_data, **{'actions': agent_actions}}
            if file_path:
                Utils.dump_yaml_file(file_path=file_path, data=agent_data)
            else:
                Utils.dump_yaml_file(file_path=self.descriptor, data=agent_data)
            return agent_data
        except Exception as e:
            self.logger.error(f'an exception occurred, {traceback.format_exc()}')
        return {}

    def healthcheck(self) -> Union[bool, dict]:
        trace = {}
        if not self.published:
            trace['published'] = {'status': False, 'message': 'Agent must be published to interact with it.', 'severity': 'error'}
        if len(self.jpr_api_key.strip()) == 0:
            trace['jpr_api_key'] = {'status': True, 'message': 'JPR API key not set. Your agent will not be able to access private JIVAS package repo items.', 'severity': 'warning'}
        if isinstance(self.name, str) and len(self.name.strip()) == 0:
            trace['name'] = {'status': False, 'message': 'Agent name must be a non-empty string with no leading or trailing spaces.', 'severity': 'error'}
        if isinstance(self.description, str) and len(self.description.strip()) == 0:
            trace['description'] = {'status': False, 'message': 'Agent description must be a non-empty string with no leading or trailing spaces.', 'severity': 'error'}
        if len(self.descriptor.strip()) == 0:
            trace['descriptor'] = {'status': False, 'message': 'Agent descriptor path not set.', 'severity': 'error'}
        if not isinstance(self.message_limit, int) or self.message_limit <= 0:
            trace['message_limit'] = {'status': False, 'message': 'Message limit must be a positive integer.', 'severity': 'error'}
        if not isinstance(self.flood_block_time, int) or self.flood_block_time <= 0:
            trace['flood_block_time'] = {'status': False, 'message': 'Flood block time must be a positive integer representing seconds.', 'severity': 'error'}
        if not isinstance(self.window_time, int) or self.window_time <= 0:
            trace['window_time'] = {'status': False, 'message': 'Window time must be a positive integer representing seconds.', 'severity': 'error'}
        if not isinstance(self.flood_threshold, int) or self.flood_threshold <= 0:
            trace['flood_threshold'] = {'status': False, 'message': 'Flood threshold must be a positive integer.', 'severity': 'error'}
        if not isinstance(self.frame_size, int) or self.frame_size <= -1:
            trace['frame_size'] = {'status': False, 'message': 'Frame size must be 0 or a positive integer.', 'severity': 'error'}
        return trace

    def get_healthcheck_report(self) -> dict:
        result = {'status': 501, 'message': 'Agent healthcheck was unable to execute.', 'trace': {}}
        error_warning_trace = {}
        trace = self.healthcheck()
        trace.update(self.spawn(_healthcheck_actions()).trace)
        for key, value in trace.items():
            if isinstance(value, dict):
                if value.get('status') == False:
                    result['status'] = 503
                    error_warning_trace[key] = {'status': False, 'message': value.get('message', f'Agent healthcheck failed on {key}. Inspect configuration and try again.'), 'severity': value.get('severity')}
                elif value.get('status') == True and value.get('severity') == 'warning':
                    error_warning_trace[key] = {'status': True, 'message': value.get('message', f'Agent healthcheck warning on {key}.'), 'severity': value.get('severity')}
            elif value == False:
                result['status'] = 503
                error_warning_trace[key] = {'status': False, 'message': f'Agent healthcheck failed on {key}. Inspect configuration and try again.', 'severity': 'error'}
        if result['status'] == 501:
            result['status'] = 200
            result['message'] = 'Agent healthcheck passed.'
            result['trace'] = error_warning_trace
        elif result['status'] == 503:
            result['message'] = 'Agent healthcheck failed.'
            result['trace'] = error_warning_trace
        self.healthcheck_status = result['status']
        return result

class _healthcheck_actions(Walker):
    trace: dict = field(gen=lambda: {})

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Actions, None))

    @with_entry
    def on_actions(self, here: Actions) -> None:
        self.visit(here.refs().filter(Action, None).filter(None, lambda item: item.enabled == True))

    @with_entry
    def on_action(self, here: Action) -> None:
        self.trace[here.label] = here.healthcheck()

class _export_actions(Walker):
    transient_export_attrs: list = field(gen=lambda: JacList(['_package']))
    action_nodes: list = field(gen=lambda: JacList([]))
    node_index: dict = field(gen=lambda: {})
    modified_context: bool = field(False)

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Actions, None))

    @with_entry
    def on_actions(self, here: Actions) -> None:
        self.visit(here.refs().filter(Action, None))

    @with_entry
    def on_action(self, here: Action) -> None:
        if here.label != 'ExitInteractAction':
            children = JacList([])
            if isinstance(here, InteractAction):
                child_nodes = here.get_children()
                for child in child_nodes:
                    children.append(child.id)
            self.node_index.update({here.id: {'action': here._package['name'], 'context': here.export(self.transient_export_attrs, self.modified_context), 'children': children}})
            self.ignore(here)
        self.visit(here.refs().filter(Action, None))

    @with_exit
    def on_exit(self, here) -> None:
        if self.node_index:
            node_keys = list(self.node_index.keys())
            node_keys.reverse()
            for key in node_keys:
                resolved_nodes = JacList([])
                for child_id in self.node_index[key]['children']:
                    resolved_nodes.append(self.node_index[child_id])
                    self.node_index.pop(child_id)
                if resolved_nodes:
                    self.node_index[key]['children'] = resolved_nodes
                else:
                    self.node_index[key].pop('children')
            self.action_nodes = list(self.node_index.values())