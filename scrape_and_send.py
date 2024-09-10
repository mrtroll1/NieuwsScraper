import os
import subprocess
from emails.email_sender import EmailSender
from emails.templates import article_template, email_template
import sys
import time
from datetime import datetime, timedelta

LOCKFILE = '/tmp/my_script.lock'
LAST_EMAIL_FILE = '/tmp/last_email_sent.txt'  

def is_running():
    """Check if the lock file exists and the script is running."""
    return os.path.exists(LOCKFILE)

def create_lock():
    """Create the lock file to indicate the script is running."""
    with open(LOCKFILE, 'w') as f:
        f.write(str(os.getpid()))  

def remove_lock():
    """Remove the lock file after the script finishes."""
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

def was_email_sent_last_hour():
    """Check if an email was already sent in the last hour."""
    if os.path.exists(LAST_EMAIL_FILE):
        with open(LAST_EMAIL_FILE, 'r') as f:
            last_sent_timestamp = f.read().strip()
            try:
                last_sent_time = datetime.strptime(last_sent_timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return False  

            one_hour_ago = datetime.now() - timedelta(hours=1)
            if last_sent_time > one_hour_ago:
                print("Email was sent in the last hour. Exiting.")
                return True
    return False

def update_last_email_sent_timestamp():
    """Update the file to store the current timestamp after sending the email."""
    with open(LAST_EMAIL_FILE, 'w') as f:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(current_time)

try:
    if is_running():
        print("Script is already running. Exiting.")
        sys.exit(1)

    create_lock()

    if was_email_sent_last_hour():
        sys.exit(0)  

    print("Running the script...")

    SCRAPY_PROJECT_DIR = os.path.join(os.path.dirname(__file__), 'nieuwsscraper')

    """ A runnable that executes main scripts that scrape data and send emails """
    def run_spider(spider_name):
        os.chdir(SCRAPY_PROJECT_DIR)
        
        try:
            subprocess.run(['scrapy', 'crawl', spider_name, '-O', f'{spider_name}.json'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run spider {spider_name}: {e}")
            sys.exit(1)  
        
        json_file = f'{spider_name}.json'
        return os.path.join(SCRAPY_PROJECT_DIR, json_file)

    def send_email(spider_name):
        json_file = run_spider(spider_name)

        email_sender = EmailSender(spider_name, json_file)
        email_sender.select_data()  
        email_sender.generate_content(article_template, email_template)

        with open('/home/luka/Projects/NieuwsScraper/recipients.txt', 'r') as recipients_file:
            for recipient_email in recipients_file:
                recipient_email = recipient_email.strip()
                if recipient_email:  
                    email_sender.send_email(recipient_email)

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Error while usage: python scrape_and_send.py <spider_name>")
            sys.exit(1)

        spider_name = sys.argv[1]
        send_email(spider_name)

        update_last_email_sent_timestamp()

        print("Script finished successfully.")

finally:
    remove_lock()
