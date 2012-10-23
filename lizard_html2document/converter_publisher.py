#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from lizard_html2document.action_converter_workflow import (
    ActionConverterPublisher,)
from lizard_worker.worker.broker_connection import BrokerConnection
from lizard_worker.worker.message_logging_handler import AMQPMessageHandler
#from lizard_worker.models import WorkflowTask
from django.conf import settings
import logging
log = logging.getLogger("converter.start_rpc_client")


class ConverterRpcClient(object):
    """
    Publish a message to execute the converter.
    """
    def __init__(self, log_level='INFO'):
        self.numeric_level = getattr(logging, log_level.upper(), None)
        self.connection = BrokerConnection().connect_to_broker()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.response_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.response_queue)

    def on_response(self, ch, method, props, body):
        self.response = body
        print "On_response"
        # f = open("/tmp/test10.docx", "w")
        # f.write(body.get("MESSAGE"))
        # f.close()
        if self.connection.is_open:
            self.connection.close()
        #if connection is None:
        #    log.error("Could not connect to broker.")
        #return

    def call(self, html, convert_to, queue_code):
        html = "<html><body>Test</body></html>"
        keys = settings.QUEUES.keys()
        self.response = None
        action = ActionConverterPublisher(
            self.connection, queue_code, html, self.response_queue, convert_to)

        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_handler = logging.handlers.AMQPMessageHandler(
            action, self.numeric_level)

        action.set_broker_logging_handler(broker_handler)
        success = action.perform()

        while self.response is None:
            self.connection.process_data_events()
        return success
