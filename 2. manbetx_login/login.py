import random
import requests
from PIL import Image
import io
import ddddocr
import execjs

ocr = ddddocr.DdddOcr()
session = requests.session()


def get_fkey(username):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://cn.fawmx.com/home/register",
    }
    url = "https://cn.fawmx.com/ee/loginverification"
    data = {
        "eeblackbox": '',
        "info": username,
        "p": "",
        "fkey": "0"
    }
    response = session.post(url, headers=headers, data=data)

    print(response.text)
    return response.json()


def login(username, fkey, captcha, password):
    pwd = execjs.compile(open('./enpwd.js').read()).call('enpwd', password)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Referer": "https://cn.fawmx.com/home/register",
    }
    url = "https://cn.fawmx.com/kz/member/loginAdvance"
    params = {
        "r": random.random()
    }
    data = {
        "loginpwd": pwd,
        "loginame": username,
        "verifycode": captcha,
        "fkey": fkey,
        "captchaMethod": "0",
        "captchaToken": "",
        "loginMethod": "0"
    }
    response = session.post(url, headers=headers, params=params, data=data)
    print(f'{response.status_code} : {response.text}')
    # print(response)


def home():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    url = "https://cn.fawmx.com/home/register"
    response = session.get(url, headers=headers)
    # print(response.text)
    print(session.cookies.get_dict())


def get_JSESSIONID():
    headers = {
        "Referer": "https://cn.fawmx.com/home/register",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    url = "https://cn.fawmx.com/service/verifycode"
    response = session.get(url, headers=headers)

    # print(response.text)
    # print(response.cookies.get_dict())
    print(session.cookies.get_dict())


def get_captcha_image():
    headers = {
        "Referer": "https://cn.fawmx.com/home/register",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    url = "https://cn.fawmx.com/service/verifycode"
    params = {
        "x": "0.8942202666043904"
    }
    response = session.get(url, headers=headers, params=params)

    # print(response.text)
    print(session.cookies.get_dict())
    # with open('./debug.png', 'wb') as f:
    #     f.write(response.content)
    im = Image.open(io.BytesIO(response.content))
    # im.show()
    with open('./debug.png', 'wb') as f:
        f.write(response.content)
    return response.content


def extract_captcha(byte):
    return ocr.classification(byte)


def main():
    username = '12345678901'
    pwd = '1'
    home()
    get_JSESSIONID()
    fkey = get_fkey(username)
    img = get_captcha_image()
    captcha = extract_captcha(img)
    login(username, fkey, captcha, pwd)


if __name__ == '__main__':
    main()
