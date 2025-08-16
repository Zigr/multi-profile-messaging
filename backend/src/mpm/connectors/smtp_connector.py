import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional


class SMTPConnector:
    def __init__(
        self,
        host: str,
        user: Optional[str] = None,
        port: int = 587,
        password: Optional[str] = None,
        use_ssl: bool = True,
        use_mailcatcher: bool = False,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_ssl = use_ssl
        self.use_mailcatcher = use_mailcatcher

    def send_email(self, to_address: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = self.user or "no-reply@example.com"
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.set_content(body)

        # MailCatcher: plaintext SMTP, no auth
        if self.use_mailcatcher:
            server = smtplib.SMTP(self.host, self.port)
            server.send_message(msg)
            server.quit()
            return

        # Real SMTP over SSL/TLS
        if self.use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
                if self.user and self.password:
                    server.login(self.user, self.password)
                server.send_message(msg)
        else:
            raise ValueError("user login and password are required")

