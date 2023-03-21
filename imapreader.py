import time
from imap_tools import MailBox


class EmailReader:

    def __init__(self, server, email, password):
        super().__init__()
        self.mb = MailBox(server).login(str(email), str(password))

    def get_facebook_code(self, delay):
        it = 0
        while it <= delay:
            messages = self.mb.fetch()
            for msg in messages:
                if msg.from_ == "registration@facebookmail.com":
                    code = msg.subject[:5]
                    self.mb.delete(msg.uid)     # удаляем письмо с кодом
                    return code
                    #print(msg.subject)
            time.sleep(1)
            it += 1
        print("Code did not come")
        return False

    def get_cloudflare_code(self, delay):
        it = 0
        while it <= delay:
            messages = self.mb.fetch()
            for msg in messages:
                if msg.from_ == "noreply@notify.cloudflare.com":
                    text = str(msg.text)
                    index = text.find("https://")
                    start = text[index:]
                    link = start.partition('\n')[0]
                    if link[-1].isspace():
                        return link[:len(link) - 1]
                    return link
            time.sleep(1)
            it += 1
        return False

    def get_netlify_ver_link(self, delay):
        it = 0
        while it <= delay:
            messages = self.mb.fetch()
            for msg in messages:
                if msg.from_ == "team@netlify.com":
                    text = str(msg.html)
                    index = text.find("https://app.netlify.com/signup?redirect=https://app.netlify.com/#verify_token=")
                    start = text[index:]
                    # link = start.partition('"')[0]

                    index2 = text.find("https://app.netlify.com/#verify_token=")    #TEST
                    start2 = text[index2:]
                    link = start2.partition('"')[0]

                    return link
            time.sleep(1)
            it += 1
        return False
