import multithread

"""
<multithread.requestNode> parameter:
    url, src_ip='', agent='', para='', method='GET'

<multithread.threads_run> parameter:
    prefix, request_list, repeat_num=1, thread_num=10
"""


def generate_nodelist():
    urls = ["/US", "/CN", "/South-Africa", "/UK", "/Italy"]
    src_ips = ["100.43.0.0", "101.192.0.0", "102.66.0.0", "103.82.0.0", "104.91.0.0"]
    agent = "Cgichk"
    para = "?kw=1' order by 1#"
    nodelist = []

    # bot
    for i in range(len(urls)):
        node = multithread.requestNode(urls[i], src_ip=src_ips[i], agent=agent)
        nodelist.append(node)

    # sql
    for i in range(len(urls)):
        node = multithread.requestNode(urls[i], src_ip=src_ips[i], para=para)
        nodelist.append(node)
    return nodelist


if __name__ == "__main__":
    prefix = 'https://52.78.82.9:8080'
    request_list = generate_nodelist()
    multithread.threads_run(prefix, request_list, 1, 5)

