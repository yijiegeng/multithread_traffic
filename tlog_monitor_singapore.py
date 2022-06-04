import multithread
import time

"""
<multithread.requestNode> parameter:
    url, src_ip='', agent='', para='', method='GET'

<multithread.threads_run> parameter:
    prefix, request_list, repeat_num=1, thread_num=10
"""


def generate_nodelist():
    urls = ["/US", "/Korea", "/Singapore", "/Canada", "/Tokyo", "/Hongkong"]
    codes = ['600', '601', '602', '603', '604', '605']
    agents = ['agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'agent6']
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
    nodelist = []

    url = '/traffic' + urls[2] # Singapore
    for k in range(6):
        for i in range(k, 6):
            para = "?code=" + codes[i]
            node = multithread.requestNode(url, agent=agents[i], para=para, method=methods[i])
            nodelist.append(node)
    return nodelist


if __name__ == "__main__":
    prefix = 'https://52.78.82.9:8080'
    request_list = generate_nodelist()
    
    start = time.time()
    for i in range(9999):
        multithread.threads_run(prefix, request_list, 1, 5) # repeat_time, thread_number
        time_interval = time.time() - start
        print ('< time spend:', round(time_interval/60), 'mins,', round(time_interval%60, 2), 'seconds >')
        if time_interval >= 3000:
            print ('>>>>>>>>>> Finish 1 hour >>>>>>>>>>')
            break
        print ('>>>>>>>>>> finish {i}, sleep 15 seconds... >>>>>>>>>>'.format(i=i))
        time.sleep(15)