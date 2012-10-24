#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from lizard_worker.worker.messaging_body import Body


class ConverterBody(Body):
    """
    Represens a body of amqp message.
    """

    FILE = "file"
    FORMAT_EXT = "format_ext"
    RESPONSE_QUEUE = "response_queue"

    def __init__(self):
        Body.__init__(self)
        self.body.update({
            ConverterBody.FILE: "",
            ConverterBody.FORMAT_EXT: "",
            ConverterBody.RESPONSE_QUEUE: ""})
