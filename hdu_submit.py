import sys
import requests
import time
from bs4 import BeautifulSoup


class HDUSubmit(object):

    log_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
    status_url = 'http://acm.hdu.edu.cn/status.php?'
    language_map = {
        "Java": 5,
        "Cpp": 0
    }

    def __init__(self, user_id, password):

        self.id = user_id
        self.password = password
        self.session = requests.session()
        self.session.headers.update({
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        })
        self.cookie_jar = requests.cookies.RequestsCookieJar()

    def login(self):
        params = {
            "username": self.id,
            "userpass": self.password,
            "login": "Sign In"
        }
        r = self.session.request('POST', self.log_url,
                                 data=params, cookies=self.cookie_jar)
        print('log status_code:', r.status_code)
        return r

    def submit(self, pid, code, language='Cpp'):
        params = {
            'check': 0,
            'problemid': pid,
            'language': self.language_map[language],
            'usercode': code
        }
        r = self.session.request(
            'POST', self.submit_url, data=params, cookies=self.cookie_jar)
        print("submit status_code", r.status_code)

        if r.status_code == 200:
            print('submit success')
            time.sleep(10)

            # 处理状态查询

            return self.status(pid)

        else:
            print('submit failed')
        return r

    def status(self, pid):
        params = {
            'pid': pid,
            'user': self.id
        }
        r = self.session.get(self.status_url, params=params)
        soup = BeautifulSoup(r.text, 'lxml')
        trs = soup.find('div', {'id': 'fixed_table'})('tr')
        model = [td.string for td in trs[0]('td')]
        data = [td.string for td in trs[1]('td')]
        pat = ['{:^%d}' % (max(len(model[i]), len(data[i])))
               for i in range(len(data))]
        for i in range(len(model)):
            print(pat[i].format(model[i]), end=' ')
        print()
        for i in range(len(data)):
            print(pat[i].format(data[i]), end=' ')
        return r


def read_code(filename):
    code = None

    with open(filename) as f:
        code = f.read()
    return code


def main(lan='Cpp', argv=None):

    if argv is None:
        try:
            argv = sys.argv[1:]
        except:
            print("请输入id和密码:")
            argv = []
            argv.append(input("id:"))
            argv.append(input("password:"))
            argv.append(input("代码文件名:"))
            argv.append(input("题号:"))
    code = read_code(argv[2])
    hdu = HDUSubmit(argv[0], argv[1])
    hdu.login()
    hdu.submit(argv[3], code, lan)


if __name__ == '__main__':
    main()
