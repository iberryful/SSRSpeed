#coding:utf-8

import requests
import os
import sys
import logging
import time

logger = logging.getLogger("Sub")

from config import config

config = config["exportResult"]

def pushToServer(filename):
	result = {
		"status":-1,
		"code":-1
	}
	try:
		logger.info("Pushing %s to server." % filename)
		files = {
			"file":open(filename,"rb")
		}
		param = {
			"token":config["apiToken"],
			"remark":config["remark"]
		}
		rep = requests.post(config["server"],files=files,data=param,timeout=10)
		result["status"] = rep.status_code
		if (rep.status_code == 200):
			if (rep.text == "ok"):
				result["code"] = 0
		return result
	except requests.exceptions.Timeout:
		logger.error("Connect to server timeout.")
		return result
	except:
		logger.exception("Pushing result to server error.")
		return result

def uploadToTransfer(filename):
	url = config.get('transferUrl', None) or "https://transfer.sh/"
	files = {'file': open(filename, 'rb')}
	try:
		r = requests.post(url, files=files)
	except:
		logger.exception("Uploading to transfer error.")
		return None
	return r.text

def sendToServerChan(head, body):
	url = config.get('serverChanUrl', None)
	if not url:
		return
	payload = {
		"text": head,
		"desp": body
	}
	try:
		r = requests.get(url, params=payload)
	except:
		logger.exception("Sending to serverchan error")


if (__name__ == "__main__"):
	print(pushToServer("test.png"))


