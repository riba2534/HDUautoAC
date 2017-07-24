import requests
from bs4 import BeautifulSoup
import os
import bs4
import  time

CookieID = ''  # 存储全局cookie
start_id=1109
end_id=4110



def search(id):  # 传入的id是题号，寻找是否可以搜到代码,搜到返回一个列表，里面是地址
    url = 'http://www.acmsearch.com/article?ArticleListSearch[Foj]=hdoj&ArticleListSearch[Fproblem_id]=' + str(
        id) + '&ArticleListSearch[Fproblem_name]=&ArticleListSearch[Farticle_name]=&ArticleListSearch[Fsource]=accepted&ArticleListSearch[Fread_num]=&ArticleListSearch[Fstar_avg]='
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    html = r.text  # 存储这个页面的html代码
    soup = BeautifulSoup(html, 'html.parser')
    try:
        tbody = soup.find('tbody')  # tbody中包含信息
        tr = tbody.find_all('tr')  # tr里面包含编号
        list = []
        for name in tr:
            if (str(name['data-key']).isdigit() == True):
                list.append(str(name['data-key']))  # 当返回的是数字的时候添加在列表里
        return list  # 返回一个列表
    except:
        list = []
        return list  # 如果有异常出现，会返回一个空列表


def get_url(id):  # 用来构造题解的代码，返回一个构造好的地址
    list = search(id)
    if (len(list) == 0):
        return 'error'
    else:
        str = 'http://www.acmsearch.com/article/show/' + list[0]
        return str


def get_code(id):  # 用来获得对应题目的代码
    url = get_url(id)
    if (url == 'error'):
        return 'error'
    else:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        html = r.text  # 存储这个页面的html代码
        soup = BeautifulSoup(html, 'html.parser')
        try:
            list = soup.find('textarea')
            code = list.get_text()
            return code
        except:
            return 'error'

def submit(id):
    url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
    code = get_code(id)
    if (code == 'error'):
        print('代码获取错误')
        return 'error'
    data = {
        'check': '0',
        'problemid': str(id),
        'language': '2',
        'usercode': str(code)
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=' + CookieID,
        'Host': 'acm.hdu.edu.cn',
        'Origin': 'http://acm.hdu.edu.cn',
        'Referer': 'http://acm.hdu.edu.cn/submit.php?pid=' + str(id),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115       Safari/537.36'
    }
    r2 = s.post(url, data=data, headers=headers)
    if (r2.text.find('Realtime Status') != -1):
        print('已经成功提交题号为'+str(id)+'的题目')
        return 'ok'


def start(st,ed):
    id=0
    try:
        for id in range(st, ed):
            f=open('log.txt','a',encoding='utf-8')
            if (submit(id) == 'ok'):
                f.write('已经成功提交' + str(id) + '\n')
                f.close()
            else:
                f.write('警告！警告！' + str(id) + '提交失败\n')
                f.close()
                continue
            time.sleep(10)
    except:
        f.write('在执行'+str(id)+'时出错\n')
        f.close()
        exit()
    f.close()

# def test():
#     url='http://acm.hdu.edu.cn/status.php?user=riba2535'

if __name__ == '__main__':
    #登录
    post_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'  # 登录的post提交地址
    data = {
        'username': '你的账号',
        'userpass': '你的密码',
        'login': 'Sign In'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'http://acm.hdu.edu.cn/'
    }
    try:
        global s
        s = requests.Session()  # 用来维持cookie
        r = s.post(post_url, data=data, headers=headers)
        html = r.text
        if (html.find('No such user or wrong password.') != -1):
            print('用户名或密码错误')
        else:
            print('登陆成功')
            CookieID = r.cookies['PHPSESSID']
    except:
        print('运行出错了')
        exit()
    #开始提交
    start(start_id,end_id)


