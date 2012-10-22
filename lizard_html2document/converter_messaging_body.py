#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from lizard_worker.worker.messaging_body import Body


class ConverterBody(Body):
    """
    Represens a body of amqp message.
    """

    HTML = "html"
    CONVERT_TO = "convert_to"
    RESPONSE_QUEUE = "response_queue"

    def __init__(self):
        Body.__init__(self)
        self.body.update({
            ConverterBody.HTML: "",
            ConverterBody.CONVERT_TO: "",
            ConverterBody.RESPONSE_QUEUE: ""})
