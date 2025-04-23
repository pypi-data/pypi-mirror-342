import asyncio
import logging

from datetime import datetime
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dbus2mqtt import AppContext
from dbus2mqtt.config import FlowConfig, FlowTriggerConfig
from dbus2mqtt.event_broker import FlowTriggerMessage
from dbus2mqtt.flow import FlowAction, FlowExecutionContext
from dbus2mqtt.flow.actions.context_set import ContextSetAction
from dbus2mqtt.flow.actions.mqtt_publish import MqttPublishAction

logger = logging.getLogger(__name__)

class FlowScheduler:

    def __init__(self, app_context: AppContext):
        self.config = app_context.config
        self.event_broker = app_context.event_broker
        self.scheduler = AsyncIOScheduler()

    async def _schedule_flow_strigger(self, flow, trigger_config: FlowTriggerConfig):
        trigger = FlowTriggerMessage(flow, trigger_config, datetime.now())
        await self.event_broker.flow_trigger_queue.async_q.put(trigger)

    async def scheduler_task(self):

        self.scheduler.start()

        # configure global flow trigger
        self.start_flow_set(self.config.flows)

        while True:
            await asyncio.sleep(1000)

    def start_flow_set(self, flows: list[FlowConfig]):
        for flow in flows:
            for trigger in flow.triggers:
                if trigger.type == "schedule":
                    existing_job = self.scheduler.get_job(trigger.id)
                    if existing_job:
                        logger.debug(f"Skipping creation, flow scheduler already exists, id={trigger.id}")
                    if not existing_job and trigger.type == "schedule":
                        logger.info(f"Starting scheduler[{trigger.id}] for flow {flow.id}")
                        if trigger.interval:
                            # Each schedule gets its own job
                            self.scheduler.add_job(
                                self._schedule_flow_strigger,
                                "interval",
                                id=trigger.id,
                                max_instances=1,
                                misfire_grace_time=5,
                                coalesce=True,
                                args=[flow, trigger],
                                **trigger.interval
                            )
                        elif trigger.cron:
                            # Each schedule gets its own job
                            self.scheduler.add_job(
                                self._schedule_flow_strigger,
                                "cron",
                                id=trigger.id,
                                max_instances=1,
                                misfire_grace_time=5,
                                coalesce=True,
                                args=[flow, trigger],
                                **trigger.cron
                            )

    def stop_flow_set(self, flows):
        for flow in flows:
            for trigger in flow.triggers:
                if trigger.type == "schedule":
                    logger.info(f"Stopping scheduler[{trigger.id}] for flow {flow.id}")
                    self.scheduler.remove_job(trigger.id)

class FlowActionContext:

    def __init__(self, app_context: AppContext, flow_config: FlowConfig, global_flows_context: dict[str, Any], flow_context: dict[str, Any]):
        self.app_context = app_context
        self.global_flows_context = global_flows_context
        self.flow_context = flow_context
        self.flow_config = flow_config

        self.flow_actions = self._setup_flow_actions()

    def _setup_flow_actions(self) -> list[FlowAction]:

        res = []
        for action_config in self.flow_config.actions:
            action = None
            if action_config.type == "context_set":
                action = ContextSetAction(action_config, self.app_context)
            if action_config.type == "mqtt_publish":
                action = MqttPublishAction(action_config, self.app_context)
            if action:
                res.append(action)

        return res

    async def execute_actions(self, trigger_context: dict[str, Any] | None):

        # per flow execution context
        context = FlowExecutionContext(
            self.flow_config.name,
            global_flows_context=self.global_flows_context,
            flow_context=self.flow_context)

        if trigger_context:
            context.context.update(trigger_context)

        for action in self.flow_actions:
            await action.execute(context)

class FlowProcessor:

    def __init__(self, app_context: AppContext):
        self.app_context = app_context
        self.event_broker = app_context.event_broker

        self._global_context: dict[str, Any] = {}

        self._flows: dict[str, FlowActionContext] = {}

        # register global flows
        self.register_flows(app_context.config.flows)

        # register dbus subscription flows
        for subscription in app_context.config.dbus.subscriptions:
            flow_context = {
                "subscription_bus_name": subscription.bus_name,
                "subscription_path": subscription.path,
                "subscription_interfaces": [i.interface for i in subscription.interfaces],
            }
            self.register_flows(subscription.flows, flow_context)

    def register_flows(self, flows: list[FlowConfig], flow_context: dict[str, Any] = {}):
        """Register flows with the flow processor."""

        for flow_config in flows:
            flow_action_context = FlowActionContext(
                self.app_context,
                flow_config,
                self._global_context,
                flow_context
            )
            self._flows[flow_config.id] = flow_action_context

    async def flow_processor_task(self):
        """Continuously processes messages from the async queue."""

        # logger.info(f"flow_processor_task: configuring flows={[f.name for f in self.app_context.config.flows]}")

        while True:
            flow_trigger_message = await self.event_broker.flow_trigger_queue.async_q.get()  # Wait for a message
            try:
                await self._process_flow_trigger(flow_trigger_message)

            except Exception as e:
                logger.warning(f"flow_processor_task: Exception {e}", exc_info=True)
            finally:
                self.event_broker.flow_trigger_queue.async_q.task_done()

    async def _process_flow_trigger(self, flow_trigger_message: FlowTriggerMessage):
        log_message = f"on_trigger: {flow_trigger_message.flow_trigger_config.type}, time={flow_trigger_message.timestamp.isoformat()}"
        if flow_trigger_message.flow_trigger_config.type != "schedule":
            logger.info(log_message)
        else:
            logger.debug(log_message)

        flow_id = flow_trigger_message.flow_config.id
        # flow_name = flow_trigger_message.flow_config.name

        flow = self._flows[flow_id]
        await flow.execute_actions(trigger_context=flow_trigger_message.context)

# # Create a flow from the YAML configuration
# for flow_config in config['flows']:
#     flow_name = flow_config['name']
#     triggers = flow_config.get('triggers', [])
#     actions = flow_config.get('actions', [])

#     with Flow(flow_name) as flow:
#         data = "sensor_data"
#         for action in actions:
#             if action['type'] == 'python_script':
#                 process_data(data)
#             elif action['type'] == 'mqtt_publish':
#                 mqtt_publish(action['topic'], action['message_template'], data)

#         # Add scheduling trigger if defined
#         for trigger in triggers:
#             if trigger['type'] == 'schedule' and 'cron' in trigger:
#                 flow.schedule = CronSchedule(cron=trigger['cron'])
