#！ /user/bin.python
# -*- coding:UTF-8 -*-
import os
from bs4 import BeautifulSoup
import requests

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Referer": "http://www.4399dmw.com/"
}
# 通过代理访问
proxies = {"HTTP": "http://101.34.214.152"}

def pachong(page):
    #网址
    url = "http://www.4399dmw.com/search/dh-1-0-0-0-0-{}-0/".format(page)
    #发送网页请求，用resp返回
    resp = requests.get(url=url, headers=headers,proxies=proxies)
    #返回的内容用utf-8解码，解码后内容为源代码
    html_doc = resp.content.decode("utf-8")
    #用BS去处理源代码
    soup = BeautifulSoup(html_doc, 'lxml')
    # number =len(soup.find_all('a',class_='u-card'))
    #把所有class值为lst的div标签取出来，并且找到所有class值为u-card的a标签
    list = soup.find('div', class_='lst').find_all('a', class_='u-card')
    #用for循环找出图片对应的名字
    pic_urls = []
    for item in list:
        # 取出名字
        mingzi = item.find('p', class_='u-tt').get_text()
        # 取出地址
        urla = item.find('img').get('data-src')
        #print(mingzi + "-------" + 'http:' + urla)
        pic_urls.append(urla)
    for tar,url in enumerate(pic_urls):
        # 因为url的格式是“//xxx.com/xxxx.img”，前面少了协议，所以要加上
        urln = "http:"+url
        save_img(urln,tar)
    # 创建保存路径
def mk_dir(path):
    # os.path.exists(name)判断是否存在路径
    # os.path.join(path, name)连接目录与文件名
    isExist = os.path.exists(os.path.join('E:\pachong', path))
    if not isExist:
        print("mkdir" + path)
        # 在E:\pachong中创建文件夹
        os.mkdir(os.path.join('E:\pachong', path))
        # 将路径转移到新建文件夹中，这样保存的图片就在这里
        os.chdir(os.path.join('E:\pachong', path))
        return True
    else:
        print(path + " already exists")
        os.chdir(os.path.join('E:\pachong', path))
        return False
def save_img(img_src,img_tar):
    try:
        #发送网页请求，得到都是图片的url地址
        img = requests.get(img_src,headers=headers,proxies=proxies)
        #给图片命名
        img_name = "picture_{}.jpg".format(img_tar+1)
        #用追加的方式将图片以二进制写入
        with open(img_name,'ab') as f:
            f.write(img.content)
            print(img_name)
    except Exception as e:
        print(e)

def main():
    #从第一页开始，爬取1到5页
    for i in range(1,6):
        path="第"+str(i)+"页"
        try:
            mk_dir(path)
            pachong(i)
        except Exception as e:
            print(e)
        print("第"+str(i)+"页保存完毕")
    pass

if __name__ == '__main__':
    main()
