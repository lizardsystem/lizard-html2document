#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

#from lizard_worker.models import Workflow
#from lizard_worker.models import WorkflowTask
#from lizard_worker.models import WorkflowTemplate
#from lizard_worker.models import WorkflowTemplateTask
from lizard_worker.worker.action import Action
from lizard_html2document.converter_messaging_body import ConverterBody

from pika import BasicProperties

import time
import logging


class ActionConverterPublisher(Action):
    """
    Publish a message to convert html.
    """
    def __init__(self, connection, queue_code="210", html="",
                 response_queue="999", convert_to="doc"):
        self.connection = connection
        self.log = logging.getLogger(__name__)
        self.channel = self.connection.channel()
        self.queue_code = queue_code
        self.response_queue = response_queue
        self.convert_to = convert_to
        self.html = html

    def perform(self):
        """
        Creates message body as instruction
        Sends message the broker
        """
        self.set_message_properties()
        self.set_message_body()
        try:
            self.send_trigger_message(
                self.body,
                "HEARBEAT emitted to queue {}".format(self.queue_code),
                self.queue_code)
            return True
        except:
            return False

    def set_message_body(self):
        """
        Creates a body of a message.
        """
        instruction = {self.queue_code: self.queue_code,
                       self.response_queue: self.queue_code}
        tmp_failures = {self.queue_code: 0}
        failures = {self.queue_code: 0}
        self.body = ConverterBody().body
        self.body[ConverterBody.TIME] = time.time()
        self.body[ConverterBody.HTML] = self.html
        self.body[ConverterBody.CONVERT_TO] = self.convert_to
        self.body[ConverterBody.RESPONSE_QUEUE] = self.response_queue
        self.body[ConverterBody.INSTRUCTION] = instruction
        self.body[ConverterBody.CURR_TASK_CODE] = self.queue_code
        self.body[ConverterBody.MAX_FAILURES_TMP] = tmp_failures
        self.body[ConverterBody.MAX_FAILURES] = failures

    def set_message_properties(self, priority=0, message_id=0):
        self.properties = BasicProperties(
            content_type="application/json",
            delivery_mode=2,
            priority=priority)

    def callback(self, ch, method, properties, body):
        pass
