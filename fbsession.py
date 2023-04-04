import re
import json
import random
from html import unescape
import requests
from useragent import UserAgent


class FBSession:

    def __init__(self):
        super().__init__()
        self.useragent = UserAgent("useragents\\useragents_win.txt")

    @staticmethod
    def set_proxy(session, login, password, ip, port):
        pstr = f"socks5://{login}:{password}@{ip}:{port}"
        # print(f"Using proxy: {pstr}")
        sproxy = {"https": pstr, "http": pstr}
        session.proxies = sproxy
        return

    @staticmethod
    def dump_cookies(sessioncookies):
        cookies = []
        for i in sessioncookies:
            cookies.append(
                {
                    "name": i.name,
                    "value": i.value,
                    "domain": i.domain,
                    "path": i.path,
                    "expires": i.expires,
                }
            )
        return cookies

    @staticmethod
    def get_redirect(text):
        match = re.search('window\.location\.replace\("([^"]+)', text)
        if match is None:
            return None
        redirect = match.group(1).replace("\\", "")
        return redirect

    def parse_token(self, text):
        match = re.search('EAAB[^"]+', text)
        return match.group(0) if match else None

    def get_token(self, session):
        session.headers.update({"User-Agent": "Mozilla5/0"})
        # session.cookies.pop("noscript", None)
        response = session.get(
            "https://www.facebook.com/ads/manager?locale=en_US",
            allow_redirects=True,
        )
        if "checkpoint" in response.url:
            print("Checkpoint!")
            return None
        if "login" in response.url:
            print("Account not logged in!")
            return None
        redirect = self.get_redirect(response.text)
        if redirect is not None:
            response = session.get(redirect, allow_redirects=True)
            return self.parse_token(response.text)
        return self.parse_token(response.text)

    @staticmethod
    def get_login_form_params(text):
        match = re.search('name="lsd"\s+value="([^"]+)"', text)
        lsd = match.group(1)
        match = re.search('name="jazoest"\s+value="([^"]+)"', text)
        jazoest = match.group(1)
        match = re.search('name="li"\s+value="([^"]+)"', text)
        li = match.group(1)
        match = re.search('name="m_ts"\s+value="([^"]+)"', text)
        mts = match.group(1)
        match = re.search('action="([^"]+)"', text)
        action = unescape(match.group(1))
        return lsd, jazoest, li, mts, action

    def set_useragent(self, session):
        # hardware_types = [HardwareType.COMPUTER.value]
        # user_agent_rotator = UserAgent(hardware_types=hardware_types)
        # user_agent = user_agent_rotator.get_random_user_agent()
        user_agent = random.choice(self.useragent)
        session.headers.update({"User-Agent": user_agent})
        return user_agent

    @staticmethod
    def set_headers(session):
        session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,"
                          "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
        )
        session.headers.update({"Accept-Encoding": "gzip"})
        session.headers.update({"Accept-Language": "ru,en-US;q=0.7,en;q=0.3"})
        session.headers.update({"Connection": "keep-alive"})
        session.headers.update({"Sec-Fetch-Dest": "document"})
        session.headers.update({"Sec-Fetch-Mode": "navigate"})
        session.headers.update({"Sec-Fetch-Site": "same-origin"})
        session.headers.update({"Sec-Fetch-User": "?1"})

    def login(self, session, email, password):
        response = session.get("https://m.facebook.com", timeout=30)
        lsd, jazoest, li, mts, action = self.get_login_form_params(response.text)

        email = email.strip()
        password = password.strip()

        response = session.post(
            f"https://m.facebook.com{action}",
            data={
                "lsd": lsd,
                "jazoest": jazoest,
                "m_ts": mts,
                "li": li,
                "try_number": 0,
                "unrecognized_tries": 0,
                "email": email,
                "pass": password,
                "login": "Log In",
                "had_cp_prefilled": False,
                "had_password_prefilled": False,
                "is_smart_lock": False,
                "bi_xrwh": 0
                # "_fb_noscript": True,
            },
            allow_redirects=False, timeout=30
        )
        if response.status_code == 302:
            if "c_user" in session.cookies:
                # print("Logged in!")
                return True

            location = response.headers["Location"]
            if "checkpoint" in location:
                print("Checkpoint!")
                return False
            if "recover" in location or "login" in location:
                print("Wrong login or password!")
                return False
        print(f"Your account may be disabled! Unknown response: {response.status_code} {response.url}")
        return False

    def get_data(self, acc_login, acc_password, pr_login, pr_password, pr_ip, pr_port):
        session = requests.session()
        self.set_headers(session)
        useragent = self.set_useragent(session)
        self.set_proxy(session, pr_login, pr_password, pr_ip, pr_port)
        loggedin = self.login(session, acc_login, acc_password)
        cookies = json.dumps(self.dump_cookies(session.cookies))
        try:
            token = self.get_token(session)
        except:
            token = " "
            pass
        # print(token)
        return useragent, cookies, token
