import imaplib
import email
import time
import re
from config import EMAIL_PASSWORD, EMAIL_ADDRESS
import datetime

IMAP_SERVER = "imap.gmail.com"
OTP_REGEX = r"\b(\d{6})\b"
email_password = EMAIL_PASSWORD
email_account=EMAIL_ADDRESS

def get_otp_from_email(timeout=150, poll_interval=5):
    from bs4 import BeautifulSoup
    
    search_start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
    
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(email_account, email_password)
    start_time = time.time()

    while time.time() - start_time < timeout:
        mail.select("INBOX")
        status, messages = mail.search(None, "UNSEEN")

        if status == "OK" and messages[0]:
            email_ids = messages[0].split()

            for email_id in reversed(email_ids[-3:]):
                status, msg_data = mail.fetch(email_id, "(RFC822)")

                for response_part in msg_data:
                    if not isinstance(response_part, tuple):
                        continue

                    msg = email.message_from_bytes(response_part[1])
                    date_str = msg.get("Date", "")

                    try:
                        from email.utils import parsedate_to_datetime
                        email_time = parsedate_to_datetime(date_str)
                        if email_time < search_start_time:
                            continue
                    except Exception:
                        pass

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                match = re.search(OTP_REGEX, body)
                                if match:
                                    mail.store(email_id, '+FLAGS', '\\Seen')
                                    mail.logout()
                                    return match.group(1)
                            
                            elif part.get_content_type() == "text/html":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                soup = BeautifulSoup(body, "html.parser")
                                text = soup.get_text()
                                match = re.search(OTP_REGEX, text)
                                if match:
                                    mail.store(email_id, '+FLAGS', '\\Seen')
                                    mail.logout()
                                    return match.group(1)
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                        match = re.search(OTP_REGEX, body)
                        if match:
                            mail.store(email_id, '+FLAGS', '\\Seen')
                            mail.logout()
                            return match.group(1)

        time.sleep(poll_interval)

    mail.logout()
    raise TimeoutError("OTP email not received within timeout")