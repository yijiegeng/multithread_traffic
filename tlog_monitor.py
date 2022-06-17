import sys
from optparse import OptionParser
import multithread
import time
import socket

"""
<multithread.requestNode> parameter:
    url, src_ip='', agent='', para='', method='GET'

<multithread.threads_run> parameter:
    prefix, request_list, repeat_num=1, thread_num=10
"""


def domain_standardize(s):  # add 'https://'
    s = s.strip()
    if not (s.startswith('http://') or s.startswith('https://')):
        s = 'https://' + s
    if s.endswith('/'):
        s = s[:-1]
    return s


def main():
    usage = "usage: %prog [options] arg (refer %prog --help)"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--domain", action="store", dest="domain",
                      help="Domain name (required!)")
    (options, args) = parser.parse_args()
    if options.domain is None:
        parser.error("Domain is required!")
    return domain_standardize(options.domain)


def generate_nodelist():
    hostname = socket.gethostname()
    print(hostname)
    ip = socket.gethostbyname(hostname)
    print(ip)

    urls = ["/US", "/Korea", "/Singapore", "/Canada", "/Tokyo", "/Hongkong"]
    codes = ['600', '601', '602', '603', '604', '605']
    agents = ['agent0', 'agent1', 'agent2', 'agent3', 'agent4', 'agent5']
    methods = ['OPTIONS', 'PATCH', 'DELETE', 'PUT', 'POST', 'GET']
    nodelist = []

    url = '/traffic'
    sleep = 100
    if ip == '127.0.1.1':
        url += urls[0]  # US
        sleep = 5
    elif ip == '172.31.19.118':
        url += urls[1]  # Korea
        sleep = 10
    elif ip == '172.31.3.108':
        url += urls[2]  # Singapore
        sleep = 20
    elif ip == '172.31.0.207':
        url += urls[3]  # Canada
        sleep = 30
    elif ip == '172.31.10.50':
        url += urls[4]  # Tokyo
        sleep = 40
    elif ip == '172.31.7.91':
        url += urls[5]  # Hongkong
        sleep = 50

    for k in range(6):
        for i in range(k, 6):
            para = "?code=" + codes[i]
            node = multithread.requestNode(url, agent=agents[i], para=para, method=methods[i])
            nodelist.append(node)
    return nodelist, sleep


if __name__ == "__main__":
    prefix = main()
    s = input((">>>>>>>> %s >>>>>>>>" % prefix) + "\n[y/n] (press any key for yes):")
    if s == "n":
        print("Modify and run again.")
        sys.exit(0)
    request_list, sleep = generate_nodelist()

    start = time.time()
    for i in range(9999):
        multithread.threads_run(prefix, request_list, 1, 5)  # repeat_time, thread_number
        time_interval = time.time() - start
        print('< time spend:', round(time_interval / 60), 'mins,', round(time_interval % 60), 'seconds >')
        if time_interval >= 3000:
            print('>>>>>>>>>> Finish 1 hour >>>>>>>>>>')
            break
        print('>>>>>>>>>> finish %s, sleep %s seconds... >>>>>>>>>>' % (i, sleep))
        time.sleep(sleep)
