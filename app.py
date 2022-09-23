#!/usr/bin/python3


from mod_gv import *


# SYSTEM
import sys
import inspect
import threading
import datetime
from datetime import timedelta
import os
import shutil
import re
import time
import logging
from urllib.parse import urlparse
from pprint import pprint
import hashlib
import base64
import uuid
from subprocess import run, PIPE


# NETWORK
import asyncio
from tornado import gen
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.platform.asyncio import AnyThreadEventLoopPolicy



def chmod(filename):
	# log("%s (%s@%s) :: make [%s] executable..." % (inspect.stack()[0][3], inspect.currentframe().f_lineno, os.path.basename(__file__), GV.selfName))
	os.chmod(filename, 0o775)


def log(message, max_len = 0):
	try:
		ts = time.time()
		if (max_len > 0):
			message = message[:max_len]
		logging.warning(message)
	except Exception as e:
		logging.warning(e)


class TornadoRequestsHandler(tornado.web.RequestHandler):
	
	
	def parsePath(self, uri_path):
		res = {}
		path = uri_path.strip("/")
		path_ary = path.split("/")
		for k, v in zip(path_ary[::2], path_ary[1::2]):
			res[k] = v
		return res


	def GetHeader(self, name):
		try:
			return self.request.headers.get(name)
		except Exception as e:
			log("%s => %s (%s@%s) :: %s" % (self.__class__.__name__, inspect.stack()[0][3], inspect.currentframe().f_lineno, os.path.basename(__file__), e))
			return None
			
	@gen.coroutine
	def get(self, uri = None):
		_GET = { k: self.get_argument(k) for k in self.request.arguments }

		log("%s => %s (%s@%s) :: uri [ %s ], params [ %s ]" % (self.__class__.__name__, inspect.stack()[0][3], inspect.currentframe().f_lineno, os.path.basename(__file__), uri, _GET))
		headers = { k: self.request.headers.get(k) for k in self.request.headers }
		# pprint(headers)
		

		if uri == 'status':
			self.write('+OK')
			
			
		elif uri == 'exec':
			
			auth_token = self.GetHeader('Auth-Token')
			cmd = self.get_argument('cmd', None)
			
			if auth_token and auth_token in GV.auth_tokens:
				if cmd and cmd in GV.apps:
					
					commands = dict()
					app = '%s/%s' % (GV.apps_path, cmd)
					commands[app] = app
					
					for k, v in _GET.copy().items():
						if k != 'cmd':
							k = '-%s' % k
							commands[k] = k
							commands[v] = v


					p = run(list(dict.fromkeys(commands)), stdout=PIPE, stderr=PIPE)

					
					self.set_status(200+p.returncode)
					self.write(p.stdout.decode())
					
					
				else:
					## Forbidden -> app is not allowed
					self.set_status(403)
					self.write('Err: app [ %s ] is not allowed' % cmd)
			else:
				## Not auth -> bad token
				self.set_status(401)
				self.write('Err: bad auth')
		else:
			## Not found -> bad url
			self.set_status(404)
			self.write('Err: not found')


	@gen.coroutine
	def post(self, uri = None):
		_POST = { k: self.get_argument(k) for k in self.request.arguments }



# Main program logic follows:
if __name__ == '__main__':
	
	############################################################################################################
	#
	# CRITICAL
	# ERROR
	# WARNING
	# INFO
	# DEBUG
	# NOTSET
	#

	logFile = GV.selfName.split('.')[0] + '.log'

	# Save last log file
	# try:
		# logFileBak = GV.selfName.split('.')[0] + str(datetime.datetime.today().strftime('-%Y%m%d-%H%M%S')) + '.log'
		# logFileBak = logFile + '.bak'
		# os.rename(logFile, logFileBak)
		# shutil.move(logFileBak, './logs/')
	# except:
		# pass



	logFormatter = logging.Formatter(GV.appName + " %(asctime)s: (%(threadName)s) %(message)s")
	rootLogger = logging.getLogger()
	rootLogger.setLevel(logging.WARNING)
	# rootLogger.setLevel(logging.DEBUG)

	# fileHandler = logging.FileHandler(logFile, mode = "w")
	# fileHandler.setFormatter(logFormatter)
	# rootLogger.addHandler(fileHandler)

	consoleHandler = logging.StreamHandler(sys.stdout)
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)
	
	
	chmod(GV.selfName)
	

	try:

		# log("%s (%s@%s)" % (inspect.stack()[0][3], inspect.currentframe().f_lineno, os.path.basename(__file__)))
		#log("%s => %s (%s@%s)" % (self.__class__.__name__, inspect.stack()[0][3], inspect.currentframe().f_lineno, os.path.basename(__file__)))
		asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
		asyncio.set_event_loop(asyncio.new_event_loop())

		tornadoApp = tornado.web.Application( [ (r"/(.*)", TornadoRequestsHandler) ], cookie_secret=GV.secret_key, debug=True )


		if GV.use_ssl:
			tornadoApp.listen(GV.http_port, GV.http_host, ssl_options={"certfile": GV.certfile, "keyfile": GV.keyfile})
		else:
			tornadoApp.listen(GV.http_port, GV.http_host)
			
			
			
		tornado.ioloop.IOLoop.current().start()

	except Exception as e:
		log("%s (%s@%s) :: %s" % (inspect.stack()[0][3], inspect.currentframe().f_lineno, os.path.basename(__file__), e))





















