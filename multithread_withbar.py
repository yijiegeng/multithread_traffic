import requests
import threading
import time
import queue
import urllib3
import logging
from alive_progress import alive_bar

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

t = time.strftime("%m_%d__%H_%M_%S", time.localtime())
logging.basicConfig(level=logging.INFO,
                    filename='log/%s.log' % t,
                    filemode='w',
                    format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')


class requestNode:
    def __init__(self, url='/', src_ip='', agent='', para='', method='GET'):
        self.url = url
        self.src_ip = src_ip
        self.agent = agent
        self.para = para
        self.method = method


def work(thread_name, prefix, q, initial_size):
    if thread_name == "Thread-0":
        with alive_bar(initial_size, manual=True) as bar:
            while True:
                curr_size = q.qsize()
                bar((initial_size - curr_size) / initial_size)
                if q.empty():
                    bar(1)
                    return
    else:
        while True:
            if q.empty():
                # print("Exiting ", thread_name)
                return
            else:
                crawler(thread_name, prefix, q)


def crawler(thread_name, prefix, q):
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
        # print(q.qsize(), thread_name, method, resp.status_code, url)
        logging.info("curr_qsize: %s, thread_name: %s, method: %s, code: %s, url: %s" %
                     (q.qsize(), thread_name, method, resp.status_code, url))
    except Exception as e:
        print("Error!!", thread_name, method, url, e)
        logging.error("curr_qsize: %s, thread_name: %s, method: %s, url: %s, msg: %s" %
                      q.qsize(), thread_name, method, url, e)


def threads_run(prefix, request_list=[], repeat_num=1, thread_num=10):
    start = time.time()
    print('domain:', prefix)
    logging.info(prefix)

    # create message queue
    work_queue = queue.Queue(1000)  # set queue size
    for _ in range(repeat_num):
        if len(request_list) == 0:
            work_queue.put(requestNode())  # default url = "/"
        for node in request_list:  # put the request_node to queue
            if isinstance(node, str): node = requestNode(url=node)  # in case node is a str (url)
            work_queue.put(node)
    initial_size = work_queue.qsize()

    # create threads list
    thread_list = []  # create thread_name
    for i in range(thread_num):
        thread_list.append('Thread-' + str(i))
    threads = []  # thread pool
    for tName in thread_list:  # create new thread
        thread = threading.Thread(target=work, args=(tName, prefix, work_queue, initial_size))
        threads.append(thread)

    for t in threads:  # waiting for all threads start
        t.start()
    for t in threads:  # waiting for all threads done
        t.join()

    # end = time.time()
    # print('Total time：', end - start)
    print('Exiting Main Thread')


# if __name__ == "__main__":
#     threads_run("https://52.78.82.9:8080", repeat_num=20, thread_num=5)
