import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from premailer import transform
import os
import json

"""A class for preparing and composing an email from json"""
class EmailSender:
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    USERNAME = 'lukameteenk@gmail.com'
    PASSWORD = os.getenv('LUKAMETEENK_PYTHONSMTP_APP_PASSWORD')

    def __init__(self, spider, json_file):
        self.spider = spider
        self.json_file = json_file
        self.articles = []
        self.num_rows = 0
        self.inlined_html = ""

    def select_data(self):
        """Load data from a JSON file based on the spider."""
        try:
            with open(self.json_file) as data_file:
                self.articles = json.load(data_file)
                self.num_rows = len(self.articles)
        except FileNotFoundError:
            print(f"No data file found for spider: {self.spider}")
            self.articles = []
            self.num_rows = 0

    def generate_content(self):
        """Generate the email content based on the articles and templates."""

        with open('html/article_template.html', 'r') as file:
            article_template = file.read()

        articles_content = ""
        for article in self.articles:
            template = Template(article_template)
            articles_content += template.render(
                title=article['title'],
                url=article['url'],
                photo_url=article['photo_url'],
                description=article['description']
            )

        if self.spider == 'nospolitiekspider':
            topic = 'politiek'
            if self.num_rows == 1:
                header_text = f'Vandaag is er maar {self.num_rows} artikel. Veel plezier!'
            elif self.num_rows == 0:
                header_text = 'Vandaag zijn er geen artikelen.'
            else:
                header_text = f'Vandaag zijn er {self.num_rows} artikelen. Veel plezier!'
        if self.spider == 'nostechspider':
            topic = 'tech'
            if self.num_rows == 1:
                header_text = f'Deze week is er maar {self.num_rows} artikel. Veel plezier!'
            elif self.num_rows == 0:
                header_text = 'Deze week zijn er geen artikelen.'
            else:
                header_text = f'Deze week zijn er {self.num_rows} artikelen. Veel plezier!'

        with open('html/email.html', 'r') as file:
            email_template = file.read()

        with open('css/styles.css', 'r') as css_file:
            css_content = css_file.read()

        template = Template(email_template)
        html_content = template.render(articles_content=articles_content, header_text=header_text, topic=topic, inline_css=css_content)

        self.inlined_html = transform(html_content)

    def send_email(self, to_email):
        """Send the email using SMTP."""
        if not self.inlined_html:
            print("No content to send. Please generate the content first.")
            return

        msg = MIMEMultipart('alternative')
        msg['From'] = self.USERNAME
        msg['To'] = to_email
        if self.spider == 'nospolitiekspider':
            msg['Subject'] = 'Nieuwsbrief: Dagelijks Politiek Update'
        if self.spider == 'nostechspider':
            msg['Subject'] = 'Nieuwsbrief: Wekelijks Tech Update'

        msg.attach(MIMEText(self.inlined_html, 'html'))

        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.starttls()
            server.login(self.USERNAME, self.PASSWORD)
            try:
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                print('Email sent successfully!')
            except Exception as e:
                print(f"Failed to send email to {to_email}: {e}")

        
