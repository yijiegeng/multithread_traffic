import requests
import threading
import time
import queue
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class requestNode:
    def __init__(self, url, src_ip='', agent='', para='', method='GET'):
        self.url = url
        self.src_ip = src_ip
        self.agent = agent
        self.para = para
        self.method = method


def work(thread_name, q, prefix):
    while True:
        if q.empty():
            print("Exiting ", thread_name)
            return
        else:
            crawler(thread_name, q, prefix)


def crawler(thread_name, q, prefix):
    request = q.get()
    url = request.url
    src_ip = request.src_ip
    agent = request.agent
    para = request.para
    method = request.method

    headers = {}
    # special case
    if url == "/bot":
        headers['User-Agent'] = 'Cgichk'
    elif url == "/rootkit.php":
        headers['X_File'] = 'data.txt'

    if src_ip != '':
        headers['X-Forwarded-For'] = src_ip
    if agent != '':
        headers['User-Agent'] = agent

    try:
        if method == 'GET':
            resp = requests.get(prefix + url + para, headers=headers, verify=False, timeout=20)
        elif method == 'POST':
            resp = requests.post(prefix + url + para, headers=headers, verify=False, timeout=20)
        elif method == 'PUT':
            resp = requests.put(prefix + url + para, headers=headers, verify=False, timeout=20)
        elif method == 'DELETE':
            resp = requests.delete(prefix + url + para, headers=headers, verify=False, timeout=20)
        elif method == 'PATCH':
            resp = requests.patch(prefix + url + para, headers=headers, verify=False, timeout=20)
        elif method == 'OPTIONS':
            resp = requests.options(prefix + url + para, headers=headers, verify=False, timeout=20)
        else:
            raise Exception("Invalid method!", method)
        # 打印：队列长度，线程名，响应吗，正在访问的url
        print(q.qsize(), thread_name, method, resp.status_code, url, para)
    except Exception as e:
        print(q.qsize(), thread_name, "Error: ", method, url, para, e)


def threads_run(prefix, request_list, repeat_num=1, thread_num=10):
    start = time.time()
    print('domain:', prefix)

    # create message queue
    work_queue = queue.Queue(1000)  # set queue size
    for _ in range(repeat_num):
        for node in request_list:  # put the request_node to queue
            if isinstance(node, str): node = requestNode(node)  # in case node is a str
            work_queue.put(node)

    # create threads list
    thread_list = []  # create thread_name
    for i in range(thread_num):
        thread_list.append('Thread-' + str(i))
    threads = []  # thread pool
    for tName in thread_list:  # create new thread
        thread = threading.Thread(target=work, args=(tName, work_queue, prefix))
        threads.append(thread)

    for t in threads:  # waiting for all threads start
        t.start()
    for t in threads:  # waiting for all threads done
        t.join()

    end = time.time()
    print('Total time：', end - start)
    print('Exiting Main Thread')

# if __name__ == "__main__":
#     prefix = 'https://ygeng-prod-data2.fortiweb-cloud-test.com'
#
#
#     threads_run(prefix, [], 50, 20)

