import time
from imap_tools import MailBox


class EmailReader:

    def __init__(self, server, email, password):
        super().__init__()
        self.mailbox = MailBox(server).login(str(email), str(password))

    def get_facebook_code(self, delay):
        for _ in range(delay):
            messages = self.mailbox.fetch()
            for msg in messages:
                if msg.from_ == "registration@facebookmail.com":
                    code = msg.subject[:5]
                    self.mailbox.delete(msg.uid)     # удаляем письмо с кодом
                    return code
            time.sleep(1)
        print("Code did not come")
        return False
