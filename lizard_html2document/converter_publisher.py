#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import logging
import binascii
import base64

from django.utils import simplejson

from lizard_html2document.action_converter_workflow import (
    ActionConverterPublisher,)
from lizard_worker.worker.broker_connection import BrokerConnection
from lizard_worker.worker.message_logging_handler import AMQPMessageHandler

log = logging.getLogger("converter.start_rpc_client")


class ConverterRpcClient(object):
    """
    Publish a message to execute the converter.
    """
    def __init__(self, log_level='INFO'):
        self.numeric_level = getattr(logging, log_level.upper(), None)
        self.document = None
        self.connection = BrokerConnection().connect_to_broker()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.response_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.response_queue)

    def on_response(self, ch, method, props, body):
        self.response = body
        self.body = simplejson.loads(body)
        #self.document = binascii.unhexlify(self.body["file"])
        self.document = base64.b64encode(self.body["file"])
        if self.connection.is_open:
            self.connection.close()

    def call(self, html, format_ext, queue_code):
        self.response = None
        action = ActionConverterPublisher(
            self.connection, queue_code, html, self.response_queue, format_ext)

        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_handler = logging.handlers.AMQPMessageHandler(
            action, self.numeric_level)

        action.set_broker_logging_handler(broker_handler)
        success = action.perform()

        while self.response is None:
            self.connection.process_data_events()
        return self.document
