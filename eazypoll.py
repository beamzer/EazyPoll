import sqlite3
import smtplib
from email.mime.text import MIMEText
import uuid
from datetime import datetime

def read_email_list(filename):
    try:
        with open(filename, 'r') as file:
            # Read lines and remove whitespace, empty lines
            emails = [line.strip() for line in file if line.strip()]
        return emails
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        exit(1)

def create_database():
    conn = sqlite3.connect('poll_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS polls
                 (token TEXT PRIMARY KEY,
                  email TEXT,
                  vote TEXT,
                  voted_at DATETIME,
                  created_at DATETIME)''')
    conn.commit()
    conn.close()

def generate_and_send_emails(email_list, question):
    conn = sqlite3.connect('poll_database.db')
    c = conn.cursor()

    # Email settings
    smtp_server = "smtp.your_server.com"
    smtp_port = 587
    smtp_username = "your_email@domain.com"
    smtp_password = "your_password"

    try:
        # Connect to SMTP server
        print("Connecting to SMTP server...")
        ## server = smtplib.SMTP(smtp_server, smtp_port)
        ## server.starttls()
        ## server.login(smtp_username, smtp_password)

        base_url = "https://myserver/eazypoll/vote.php?token="

        total_emails = len(email_list)
        print(f"Sending emails to {total_emails} recipients...")

        for index, email in enumerate(email_list, 1):
            # Generate unique token
            token = str(uuid.uuid4())

            # Store in database
            c.execute("INSERT INTO polls (token, email, created_at) VALUES (?, ?, ?)",
                     (token, email, datetime.now()))

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
            msg['Subject'] = "Poll Question"
            msg['From'] = smtp_username
            msg['To'] = email

            # Send email
            ### server.send_message(msg)
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
    # File containing email addresses (one per line)
    email_file = "recipients.txt"

    # Read email addresses from file
    print(f"Reading email addresses from {email_file}...")
    email_list = read_email_list(email_file)

    # Your poll question
    question = "Do you approve this proposal?"

    # Create database if it doesn't exist
    create_database()

    # Generate and send emails
    generate_and_send_emails(email_list, question)

    print("Process completed!")

if __name__ == "__main__":
    main()
