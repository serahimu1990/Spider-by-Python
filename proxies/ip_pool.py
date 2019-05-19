import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3729.157 Safari/537.36'}
IP =[]

def handle_request(url):
        response =requests.get(url,headers=headers)
        return response

def test_request(proxies):
    url_test = 'https://www.baidu.com/'
    response=requests.get(url=url_test, proxies=proxies, headers=headers, timeout=2)
    return response

# def ip_save(ip):


def parse_response(response):
        tree = etree.HTML(response.text)
        trs = tree.xpath("//tr[@class='odd']")
        for tr in trs:
            ip1 = tr.xpath(".//td/text()")[0]
            port = tr.xpath(".//td/text()")[1]
            ip=ip1+':'+port
            proxies ={'http':'http://'+ip,'https':'https://'+ip}
            try:
                r=test_request(proxies)
                if r.status_code ==200:
                    IP.append(ip)
            except:
                print('Timeout')

def main():
    start_page =int(input("start page: "))
    end_page = int(input("end page: "))
    for i in range(start_page,end_page+1):
        url ='https://www.xicidaili.com/nn/'+str(i)
        response=handle_request(url)
        parse_response(response)
    with open('proxy.csv', 'a', encoding='utf8') as fp:
        for i in range(len(IP)):
            fp.write(IP[i] + '\n')


if __name__=='__main__':
    main()

