import sqlite3
import smtplib
from email.mime.text import MIMEText
import uuid
from datetime import datetime
import configparser

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
    formatted_from = f"{smtp_from_name} <{smtp_from_email}>"

    try:
        # Connect to SMTP server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        ## server.starttls()
        ## server.login(smtp_username, smtp_password)

        base_url = config['poll']['base_url']

        # Get all emails from database that don't have a token yet
        c.execute("SELECT email FROM polls WHERE token IS NULL")
        emails = c.fetchall()
        
        total_emails = len(emails)
        print(f"Sending emails to {total_emails} recipients...")

        for index, (email,) in enumerate(emails, 1):
            # Generate unique token
            token = str(uuid.uuid4())

            # Update database with token
            c.execute("UPDATE polls SET token = ? WHERE email = ? AND token IS NULL",
                     (token, email))

            # Create email message
            html_content = f"""
            <html>
            <body>
            <h2>{question}</h2>
            <p>Please click one of the following options to vote:</p>
            <p><a href="{base_url}{token}&vote=yes">Yes</a></p>
            <p><a href="{base_url}{token}&vote=no">No</a></p>
            </body>
            </html>
            """

            print(f"Yes URL = {base_url}{token}&vote=yes")
            print(f"No URL = {base_url}{token}&vote=no")
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = config['poll']['email_subject']
            msg['From'] = formatted_from
            msg['To'] = email

            # Send email
            server.send_message(msg)
            print(f"Sent email {index}/{total_emails} to {email} with token: {token}\n")

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
