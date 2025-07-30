import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import configparser
import time

def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        return config
    except Exception as e:
        print(f'Error reading configuration: {str(e)}')
        exit(1)

def generate_and_send_emails(question, config):
    conn = sqlite3.connect('poll_database.db')
    c = conn.cursor()

    # Email settings from config
    smtp_server = config['email']['smtp_server']
    smtp_port = config['email']['smtp_port']
    smtp_username = config['email']['smtp_username']
    smtp_password = config['email']['smtp_password']
    smtp_from_email = config['email']['smtp_username']  # Use authenticated email as sender
    smtp_from_name = config['email']['smtp_from_name']
    smtp_replyto = config['email']['smtp_replyto']
    formatted_from = f"{smtp_from_name} <{smtp_from_email}>"

    # Read question and body text from config
    question = config['poll']['question']
    body_text = config['poll']['body_text']

    try:
        # Connect to SMTP server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        ## server.starttls()
        ## server.login(smtp_username, smtp_password)

        base_url = config['poll']['base_url']

        # Get all emails and tokens from database
        c.execute("SELECT email, token FROM polls")
        records = c.fetchall()
        
        total_emails = len(records)
        print(f"Sending emails to {total_emails} recipients...")

        for index, (email, token) in enumerate(records, 1):

            # Create email message
            html_content = f"""
<html>
<body>
<h2>{question}</h2>
<p>{body_text}</p>
<p><a href="{base_url}{token}&vote=yes">Yes</a></p>
<p><a href="{base_url}{token}&vote=no">No</a></p>
</body>
</html>
            """

            # print(f"Yes URL = {base_url}{token}&vote=yes")
            # print(f"No URL = {base_url}{token}&vote=no")
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = config['poll']['email_subject']
            msg['From'] = formatted_from
            msg['To'] = email
            msg['Reply-To'] = smtp_replyto

            # Send email
            server.send_message(msg)
            print(f"Sent email {index}/{total_emails} to {email} with token: {token}")
            time.sleep(0.100)

            # Commit after each successful send
            conn.commit()

    except Exception as e:
        print(f"Error sending emails: {str(e)}")
        conn.rollback()
    finally:
        #server.quit()
        #conn.close()
        print(f"")

def main():
    # Read configuration
    config = read_config()

    # Your poll question
    question = "Do you approve this proposal?"

    # Generate and send emails
    generate_and_send_emails(question, config)

    print("Process completed!")

if __name__ == "__main__":
    main()
