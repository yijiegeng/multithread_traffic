import requests
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def visit(prefix, url, para, src_ip, agent, method):
	headers = {'User-Agent':agent, 'X-Forwarded-For':src_ip}
	resp = 'invalid method!'
	if method == 'GET':
		resp = requests.get(prefix + url + para, headers = headers, verify=False, timeout=10)
	elif method == 'POST':
		resp = requests.post(prefix + url + para, headers = headers, verify=False, timeout=10)
	elif method == 'PUT':
		resp = requests.put(prefix + url + para, headers = headers, verify=False, timeout=10)
	elif method == 'DELETE':
		resp = requests.delete(prefix + url + para, headers = headers, verify=False, timeout=10)
	elif method == 'PATCH':
		resp = requests.patch(prefix + url + para, headers = headers, verify=False, timeout=10)

	print("msg: {resp}, url: <{url}>, agent: <{agent}>".format(resp=resp, url=url, agent=agent))


prefix = 'https://52.78.82.9:8080'
methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
codes = ['600', '601', '602', '603', '604', '605']
urls = ["/US", "/CN", "/SA", "/UK", "/It"]
src_ips = ["100.43.0.0", "101.192.0.0", "102.66.0.0", "103.82.0.0", "104.91.0.0"]
agents = ['us-agent', 'cn-agent', 'sa-agent', 'uk-agent', 'it-agent']

count = 0
for k in range(1):
	print ('hostname: ' + prefix)
	for method in methods:
		print(">>>>>>>>>> " + method + " >>>>>>>>>>")
		for code in codes:
			para = '?code=' + code
			print("==========================")
			for i in range(5):
				url = '/traffic' + urls[i]
				visit(prefix, url, para, src_ips[i], agents[i], method)
				count += 1
	print("-------------------------count " + str(k))

print("Finished. total: " + str(count))