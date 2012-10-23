import logging  # , threading, time, datetime, random, math
import cStringIO

from django.conf import settings
from lizard_html2document.converter_messaging_body import ConverterBody

log = logging.getLogger('flooding-lib.perform_task')


TASK_CONVERT_HTML2DOCUMENT = 200


def perform_task(body, tasktype_id, worker_nr, broker_logging_handler=None):
    """
    execute specific task
    scenario_id  = id of scenario
    tasktype_id  = id of tasktype (120,130,132)
    worker_nr = number of worker (1,2,3,4,5,6,7,8). Used for temp
    directory and sobek project.
    broker_logging_handler = sends loggings to broker
    """
    html = body['html']
    convert_to = body['convert_to']
    unique_code = body['curr_task_code']

    #logging handler
    # if broker_logging_handler is not None:
    #     log.addHandler(broker_logging_handler)
    # else:
    #     log.warning("Broker logging handler does not set.")

    #settings.py:
    # @TODO executable location hisssm_root = settings.HISSSM_ROOT
    # converter_program_root = settings.CONVERTER_PROGRAM_ROOT  # e: or c:
    print "execute document module"
    import subprocess
    success_code = True
    exefile = settings.PATH_CONVERTER_PROGRAMM
    tmp = settings.TMP
    command_line = [exefile, html, convert_to]
    log.debug('spawn the converter to subprocess')
    f_in = open(settings.TMP)
    file_handler = cStringIO.StringIO(f_in.read())
    body[ConverterBody.MESSAGE] = file_handler.getvalue()
    file_handler.close()
    f_in.close()
    #child = subprocess.Popen(command_line)
    #child.wait()

    return success_code
