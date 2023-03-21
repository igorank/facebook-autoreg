import requests


class IPChanger:

    @staticmethod
    def change_ip(url, get_ip=False, username=None, password=None, host=None, port=None):
        if len(url) != 0:
            try:
                print('Changing the IP address.', end=' ')
                requests.get(url, timeout=12)
                if get_ip:
                    ip = IPChanger.get_ip(username, password, host, port)
                    print(f"Done ({str(ip)}).\n")
                else:
                    print("Done.\n")
            except:
                print("Failed.\n")
        else:
            print("IP address has not been changed")
            return

    @staticmethod
    def get_ip(username, password, host, port):
        ip = requests.get('https://api.ipify.org', proxies=dict(
            http='socks5://' + str(username) + ':' + str(password) + '@' + str(host) + ':' + str(port),
            https='socks5://' + str(username) + ':' + str(password) + '@' + str(host) + ':' + str(port))).text
        return ip
