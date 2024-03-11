import argparse
import poplib
import re
import time
from email.parser import Parser

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChromeDriver:
    def __init__(self):
        self.driver = None
        self.options = ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--no-sandbox")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])

    def get_chrome_driver(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(30)
        return self.driver


class EmailReceiver:
    def __init__(self, pop_server, pop_port, pop_email_address, pop_email_password):
        self.pop_server = pop_server
        self.pop_port = pop_port
        self.email_address = pop_email_address
        self.password = pop_email_password

    def get_one_time_code(self):
        server = poplib.POP3_SSL(self.pop_server, self.pop_port)
        server.set_debuglevel(1)

        server.user(self.email_address)
        server.pass_(self.password)

        email_num, total_size = server.stat()
        resp, lines, octets = server.retr(email_num)
        server.quit()

        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        body = None
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = part.get("Content-Disposition")

                if content_type == "text/plain" and content_disposition is None:
                    body = part.get_payload(decode=True).decode()

        match = re.search(r"ワンタイムパスワード:\s*(\d+)", body)
        if match:
            otp = match.group(1)
            return otp


def save_cookies(cookies):
    env_file_path = '.env'
    with open(env_file_path, 'w') as file:
        for cookie in cookies:
            file.write(f'{cookie["name"]}={cookie["value"]}\n')


def Run(driver, email_receiver, jrecin_address, jrecin_password):
    wait = WebDriverWait(driver, 30)

    driver.get("https://jrecin.jst.go.jp/seek/Login")

    email_input = wait.until(EC.element_to_be_clickable((By.ID, "address")))
    email_input.clear()
    email_input.send_keys(jrecin_address)
    print("input jrecin address")

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(jrecin_password)
    print("input jrecin password")

    login_button = driver.find_element(By.ID, "login-btn")
    login_button.click()
    print("try login")

    driver.get("https://jrecin.jst.go.jp/seek/Hunter/Factor/Otp/Mail/Init")

    otp_input = wait.until(EC.element_to_be_clickable((By.ID, "onetimePass")))
    otp_input.clear()

    time.sleep(5)
    otp_input.send_keys(email_receiver.get_one_time_code())
    print("get one time login code")

    otp_auth_button = driver.find_element(By.ID, "otpMailAuthBtn")
    otp_auth_button.click()

    driver.get("https://jrecin.jst.go.jp/seek/Hunter/Mypage")
    print("login")

    save_cookies(driver.get_cookies())
    print("get jrecin cookies")

    driver.quit()


def get_args():
    parser = argparse.ArgumentParser(description='get-jrecin-cookies v0.0.1')
    parser.add_argument('--pop_server', type=str, default='outlook.office365.com',
                        help='Specify the address of the pop server you are using.')
    parser.add_argument('--pop_port', type=int, default=995,
                        help='Specify the port of the pop service you are using.')
    parser.add_argument('--pop_email_address', type=str, default=None,
                        help='Specify the e-mail address you are using '
                             'to log in to the pop service.')
    parser.add_argument('--pop_email_password', type=str, default=None,
                        help='Specify the login password for the pop service you are using.')
    parser.add_argument('--jrecin_address', type=str, default=None,
                        help='Specify the login username for the jrecin service you are using.')
    parser.add_argument('--jrecin_password', type=str, default=None,
                        help='Specify the login password for the jrecin service you are using.')
    return parser.parse_args()


if __name__ == "__main__":
    chromeDriver = ChromeDriver()
    args = get_args()
    emailReceiver = EmailReceiver(args.pop_server, args.pop_port, args.pop_email_address, args.pop_email_password)
    Run(chromeDriver.get_chrome_driver(), emailReceiver, args.jrecin_address, args.jrecin_password)
