lizard-html2document
==========================================

Provides client-server tier application to convert .htm to .doc, .docx, .rtf


Initial setup
=================
1	Buildout
-----------------

1.1 	Add the app to the project's setup.py and settings.py
1.2 	Set next setting to your project:

	.....

	TASK_CODE = "210"

	BROKER_SETTINGS = {
		"BROKER_HOST": "xxxxxxx",
		"BROKER_PORT": xxxx,
		"BROKER_USER": "xxxx",
		"BROKER_PASSWORD": "xxxx",
		"BROKER_VHOST": "xxxx"}

	QUEUES = {
    		TASK_CODE: {
        		"exchange": "router",
        		"binding_key": TASK_CODE},
    		"logging": {
        		"exchange": "router",
        		"binding_key": "logging"},
    		"failed": {
        		"exchange": "router",
        		"binding_key": "failed"}
		}

	PERFORM_TASK_MODULE = "lizard_html2document.perform_task"
	PERFORM_TASK_FUNCTION = "perform_task"
	.....

1.3 	Run bin/buildout


2. Client
-----------------------------

2.1	Usage
	............................................
	from lizard_html2document.converter_publisher import ConverterRpcClient

	def convert_html2document(html_string, convert_to):
    		"""
    		Run rpcclient to send a html and receive a document.

		Arguments:
		convert_to - string (options: doc, docx, rtf)
		"""
    		task_code = settings.TASK_CODE
    		converter = ConverterRpcClient()
    		document = converter.call(html_string, convert_to, task_code)
    		return document
	.............................................

3. Server for Windows(worker)
-----------------------------

3.1	Checkout Converter (not public, check requirements to use the converter in README)

	- git clone https://github.com/nens/HTML2DocumentConverter [target]
	- mkdir bin
	- copy HTML2DocumentConverter/bin/Debug/HTML2DocumentConverter.exe bin
	- mkdir temp
	- mkdir temp/[worker_nr]

3.2	Checkout the project
	
	- git clone [this repo url] [targer dir]
	- git checkout [tag version]
	
3.3	Setup
	- cd [target dir]
	- python bootstrap.py
	- bin/buildout
	
3.4	Conguration

	- create bin directory
	- add to localsetting.py next setting:
	
	PATH_CONVERTER_PROGRAM = "c:\\HTML2Document\\bin\\HTML2DocumentConverter.exe"
	WORK_DIR = "c:\\HTML2Document\\temp"

	BROKER_SETTINGS = {
		"BROKER_HOST": "xxxxxxx",
		"BROKER_PORT": xxxx,
		"BROKER_USER": "xxxx",
		"BROKER_PASSWORD": "xxxx",
		"BROKER_VHOST": "xxxx"}

3.5 	Configuration RabbitMQ

	- configure RabbitMQ conform 'RabbitMQ setting' part in setting.py
	
3.6	Start worker

	bin/django lw_task_worker --task_code 210 --worker_nr 1 --log_level INFO

3.7	Security

	To avoid security issue on getting the images from a secured site:
	- open IE
	- add the url to trusted sites
	- login to the site
	- let IE remember the login
