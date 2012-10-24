import logging  # , threading, time, datetime, random, math
import binascii
import os
import subprocess

from django.conf import settings

log = logging.getLogger('worker.perform_task')


def prepaire_workdir(work_dir, worker_nr, html_file, converted_file):
    """
    Create worker dir, remove file.
    """
    if not os.path.isdir(work_dir):
        os.makedirs(work_dir)

    if os.path.exists(html_file):
        os.remove(html_file)

    if os.path.exists(converted_file):
        os.remove(converted_file)


def save_htmlfile(html_filepath, context):
    """
    Save passed context as html file
    """
    html_file = open(html_filepath, "w")
    html_file.write(context)
    html_file.close()


def set_body(body, converted_file):
    """
    Set file to the messaging body
    """
    f_in = open(converted_file, "rb")
    body['file'] = binascii.hexlify(f_in.read())
    f_in.close()


def encode_context(context):
    try:
        encoded_context = context.encode("UTF-8")  # Unicode
    except UnicodeEncodeError:
        encoded_context = context.encode("ISO-8859-1")  # Latin
    return encoded_context


def perform_task(body, tasktype_id, worker_nr, broker_logging_handler=None):
    """
    Use this function on worker callback.
    Converte html string to doc, docx, rtf file
    using external program.
    Set the converted file as binary string into messaging body.
    """
    log.debug("Retrieve data from messaging body.")
    context = encode_context(body['file'])
    format_ext = body['format_ext']
    unique_code = body['response_queue']
    success_code = True
    worker_nr = str(worker_nr)

    log.debug("Prepare work dir.")
    exefile = settings.PATH_CONVERTER_PROGRAM
    log.debug("Set work dir.")
    work_dir = os.path.join(settings.WORK_DIR, worker_nr)
    log.debug("set html filepath")
    html_filepath = os.path.join(
        work_dir, "{0}.{1}".format(unique_code, "htm"))
    log.debug("set filepath for converted doc.")
    converted_filepath = os.path.join(
        work_dir, "{0}.{1}".format(unique_code, format_ext))
    log.debug("check work dir.")
    prepaire_workdir(work_dir, worker_nr, html_filepath, converted_filepath)
    log.debug("set context : {}".format(context))
    save_htmlfile(html_filepath, context)
    log.debug("Convert file.")
    command_line = [exefile, work_dir, unique_code, format_ext]
    subprocess.Popen(command_line).wait()
    log.debug("Set converted file to messaging body.")
    set_body(body, converted_filepath)
    prepaire_workdir(work_dir, worker_nr, html_filepath, converted_filepath)

    return success_code
