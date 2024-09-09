import os
import subprocess
from emails.email_sender import EmailSender
from emails.templates import article_template, email_template

logging.basicConfig(filename='/home/luka/Projects/logs/scraper.log', level=logging.DEBUG)

SCRAPY_PROJECT_DIR = os.path.join(os.path.dirname(__file__), 'nieuwsscraper')
""" A runnable that executes main scripts that scrape data and send emails """
def run_spider(spider_name):
    os.chdir(SCRAPY_PROJECT_DIR)
    
    subprocess.run(['scrapy', 'crawl', spider_name, '-O', f'{spider_name}.json'], check=True)
    json_file = f'{spider_name}.json'

    return os.path.join(SCRAPY_PROJECT_DIR, json_file)

def send_email(spider_name):
    json_file = run_spider(spider_name)
    
    email_sender = EmailSender(spider_name, json_file)
    email_sender.select_data()  
    email_sender.generate_content(article_template, email_template)

    with open('recipients.txt', 'r') as recipients_file:
        for recipient_email in recipients_file:
            recipient_email = recipient_email.strip()
            if recipient_email:  
                email_sender.send_email(recipient_email)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Erros while usage: python scrape_and_send.py <spider_name>")
        sys.exit(1)

    spider_name = sys.argv[1]
    send_email(spider_name)
