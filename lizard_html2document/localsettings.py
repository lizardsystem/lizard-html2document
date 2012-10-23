PATH_CONVERTER_PROGRAMM = "..\worker_batches\converter.exe"
#TMP = "C:\temp"
#TMP = "/home/alexandr/Downloads/test_html10.docx"

BROKER_SETTINGS = {
    "BROKER_HOST": "localhost",
    "BROKER_PORT": 5672,
    "BROKER_USER": "flooding",
    "BROKER_PASSWORD": "frmq60A",
    "BROKER_VHOST": "flooding-test",
    "HEARTBEAT": False
}

PERFORM_TASK_MODULE = "lizard_html2document.perform_task"
PERFORM_TASK_FUNCTION = "perform_task"

#queue's setting for flooding-worke
QUEUES = {
    "210": {
        "exchange": "router",
        "binding_key": "210"},
    "logging": {
        "exchange": "router",
        "binding_key": "logging"},
    "failed": {
        "exchange": "router",
        "binding_key": "failed"}
}

HEARTBEAT_QUEUES = ["210"]
