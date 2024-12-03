import sqlite3
import smtplib
from email.mime.text import MIMEText
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

def read_recipients(filename):
    try:
        with open(filename, 'r') as f:
            # Remove whitespace and empty lines
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f'Error reading recipients file: {str(e)}')
        exit(1)

def generate_and_send_emails(question, config, recipients):
    conn = sqlite3.connect('poll_database.db')
    c = conn.cursor()

    # Email settings from config
    smtp_server = config['email']['smtp_server']
    smtp_port = config['email']['smtp_port']
    smtp_username = config['email']['smtp_username']
    smtp_password = config['email']['smtp_password']
    smtp_from_email = config['email']['smtp_username']
    smtp_from_name = config['email']['smtp_from_name']
    formatted_from = f"{smtp_from_name} <{smtp_from_email}>"

    try:
        # Connect to SMTP server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        ## server.starttls()
        ## server.login(smtp_username, smtp_password)

        base_url = config['poll']['base_url']
        total_emails = len(recipients)
        print(f"Processing {total_emails} recipients...")

        for index, email in enumerate(recipients, 1):
            # Get token for this email
            c.execute("SELECT token FROM polls WHERE email = ?", (email,))
            result = c.fetchone()
            
            if not result:
                print(f"No token found for email: {email}")
                continue
                
            token = result[0]

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

            msg = MIMEText(html_content, 'html')
            msg['Subject'] = config['poll']['email_subject']
            msg['From'] = formatted_from
            msg['To'] = email

            # Send email
            server.send_message(msg)
            print(f"Sent email {index}/{total_emails} to {email} with token: {token}")
            time.sleep(0.100)

    except Exception as e:
        print(f"Error sending emails: {str(e)}")
    finally:
        #server.quit()
        conn.close()
        print("Done sending emails")

def main():
    # Read configuration
    config = read_config()

    # Read recipients
    recipients = read_recipients('recipients.txt')
    
    # Your poll question
    question = "Do you approve this proposal?"

    # Generate and send emails
    generate_and_send_emails(question, config, recipients)

    print("Process completed!")

if __name__ == "__main__":
    main()
