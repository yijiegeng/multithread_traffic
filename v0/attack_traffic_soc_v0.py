import requests
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def visit(prefix, url, src_ip, agent):
    headers = {'User-Agent':agent, 'X-Forwarded-For':src_ip}
    resp = requests.get(prefix + url, headers = headers, verify=False, timeout=10)
    print("msg: {resp}, url: <{url}>, agent: <{agent}>".format(resp=resp, url=url, agent=agent))


def onetime(prefix, suffix, bot_flag=False):
    print("@visit: {prefix}".format(prefix=prefix))
    agent = "Cgichk" if bot_flag else "test"
    para = "" if bot_flag else "?kw=1' order by 1#"

    urls = ["/US", "/CN", "/South-Africa", "/UK", "/Italy"]
    urls = [item + "_" + str(suffix) + para for item in urls]
    src_ip = ["100.43.0.0", "101.192.0.0", "102.66.0.0", "103.82.0.0", "104.91.0.0"]

    threads = []
    for i in range(0, len(src_ip)):
        thread = threading.Thread(target = visit(prefix, urls[i], src_ip[i], agent))
        threads.append(thread)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Threads finish!")

## test for tenant "mr.yijiegeng@gmail.com"
# prefix1 = 'https://ygeng-dev-c8.fortiweb-cloud-test.com'
# onetime(prefix1, "c8", True)
# prefix2 = 'https://ygeng-dev-soc.fortiweb-cloud-test.com'
# onetime(prefix2, "soc")

## test for tenant "ygeng.fortinet@gmail.com"
# prefix3 = 'https://ygeng-dev-soc2.fortiweb-cloud-test.com'
# onetime(prefix3, "0331bot", True)
# prefix4 = 'https://ygeng-dev-soc2.fortiweb-cloud-test.com'
# onetime(prefix4, "0331SQL")

## test for MSSP
# prefix5 = 'https://ygeng-dev-socmssp.fortiweb-cloud-test.com'
# onetime(prefix5, "socmssp", True)
# prefix6 = 'https://ygeng-dev-socmssp2.fortiweb-cloud-test.com'
# onetime(prefix6, "socmssp2")

# test for AWS
# prefix10 = 'https://ygeng-dev-soc3.fortiweb-cloud-test.com'
# onetime(prefix10, "aws1-0420BOT", True)
# prefix11 = 'https://ygeng-dev-soc3.fortiweb-cloud-test.com'
# onetime(prefix11, "aws1-0420SQL")
# prefix12 = 'https://ygeng-dev-soc4.fortiweb-cloud-test.com'
# onetime(prefix12, "aws2-0401BOT", True)
# prefix13 = 'https://ygeng-dev-soc4.fortiweb-cloud-test.com'
# onetime(prefix13, "aws2-0401SQL")


# test for QA
# prefix80 = 'https://ygeng-qa-soc.fortiweb-cloud-test.com'
# onetime(prefix80, "aws-0419BOT", True)
# prefix81 = 'https://ygeng-qa-soc.fortiweb-cloud-test.com'
# onetime(prefix81, "aws-0419SQL")


# test for PROD
# prefix90 = 'https://ygeng-prod-data.fortiweb-cloud-test.com'
# onetime(prefix90, "aws-0405BOT", True)
# prefix91 = 'https://ygeng-prod-data.fortiweb-cloud-test.com'
# onetime(prefix91, "aws-0405SQL")
# prefix92 = 'https://ygeng-prod-data2.fortiweb-cloud-test.com'
# onetime(prefix92, "awsold-0405BOT", True)
# prefix93 = 'https://ygeng-prod-data2.fortiweb-cloud-test.com'
# onetime(prefix93, "awsold-0405SQL")


