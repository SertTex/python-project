import random
import re
import requests
from bs4 import BeautifulSoup
import lxml
import json

page = 0
number = 0
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
#设置代理ip：
#proxies的格式是一个字典：{‘http’: ‘http://42.84.226.65:8888‘}
ip_list = ['http://118.187.58.34','http://111.155.116.249','http://60.177.225.218','http://223.241.118.9','http://60.177.228.250']
#ip = random.choice(ip_list)
while True:
    page+=1
    ip = random.choice(ip_list)
    proxie = {'http': str(ip)}
    listurl = 'https://list.jd.com/list.html?cat=737,794,798&page='+str(page)
    req = requests.get(listurl,headers = header,proxies = proxie).text#connect 到主页
    soup = BeautifulSoup(req,'lxml').find_all('a')#创建soup对象
    link = re.findall(r'//item.jd.com/\d*.html',str(soup))#匹配地址
    for href in set(link):
        number+=4
        #return href
        html = requests.get('https:'+str(href),headers= header,proxies = proxie).text#connect商品地址
        global pid
        pid = re.findall(r'\d*',href)[14]#get到商品id
        p_json = requests.get('https://p.3.cn/prices/mgets?skuIds='+str(pid),headers = header,proxies = proxie).json()
        #prize = json.loads(str(p_json))['p']
        # 将 JSON 对象转换为 Python 字典
        global prize
        prize = (p_json[0]['p'])#得到商品价格
        shop_soup = BeautifulSoup(html,"lxml").find_all('div',class_="name")
        global shop
        try:
            shop = re.findall(">(.*?)</a>",str(shop_soup))[0]

        except:
            continue#得到商店名
        name_soup = BeautifulSoup(html,'lxml').find_all('img',id="spec-img")
        global name
        for name in name_soup:
            print('正在爬取第%d个数据'%number)
            name = name.get('alt')#得到商品名
            #print(name)
            #print(pid)
        if number>100001:
            break
        result = [{"id": pid},{'name':name},{"seller":shop},{"prize":prize}]
        with open("data.txt","a") as fp:
            fp.write(str(result)+'\n')
            fp.close()
        print(result)
