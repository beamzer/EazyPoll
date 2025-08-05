import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import configparser
import time
import argparse
import sys
import os

POLL_DB_FILE = 'poll_database.db'

def read_config():
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please ensure config.ini exists in the current directory.")
        exit(1)
    
    try:
        config.read(config_file)
    except Exception as e:
        print(f"Error reading configuration file '{config_file}': {str(e)}")
        exit(1)
    
    # Validate required sections and variables
    required_sections = ['email', 'poll']
    required_vars = {
        'email': ['smtp_server', 'smtp_port', 'smtp_username', 'smtp_password', 'smtp_from_name', 'smtp_replyto'],
        'poll': ['question', 'body_text', 'email_subject', 'base_url']
    }
    
    for section in required_sections:
        if section not in config:
            print(f"Error: Missing required section '[{section}]' in {config_file}")
            exit(1)
            
        for var in required_vars[section]:
            if var not in config[section]:
                print(f"Error: Missing required variable '{var}' in section '[{section}]' of {config_file}")
                exit(1)
    
    return config

def get_recipients(send_to_all=False):
    """Get recipients based on whether to send to all or only non-voters"""
    conn = sqlite3.connect(POLL_DB_FILE)
    c = conn.cursor()
    
    if send_to_all:
        # Send to all recipients
        c.execute("SELECT email, token FROM polls")
        print("Sending to ALL recipients...")
    else:
        # Send only to those who haven't voted yet (vote is NULL)
        c.execute("SELECT email, token FROM polls WHERE vote IS NULL")
        print("Sending reminders to recipients who haven't voted yet...")
    
    records = c.fetchall()
    conn.close()
    
    return records

def generate_and_send_emails(config, send_to_all=False, is_reminder=False):
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
    
    # Use reminder text if available and this is a reminder
    if is_reminder and not send_to_all:
        reminder_body = config.get('poll', 'reminder_body_text', fallback=None)
        if reminder_body:
            body_text = reminder_body
            print("Using reminder body text from config...")

    try:
        # Connect to SMTP server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        base_url = config['poll']['base_url']

        # Get recipients based on parameters
        records = get_recipients(send_to_all)
        
        if not records:
            if send_to_all:
                print("No recipients found in database!")
            else:
                print("Great! All recipients have already voted. No reminders needed.")
            return
        
        total_emails = len(records)
        email_type = "emails" if send_to_all else "reminder emails"
        print(f"Sending {email_type} to {total_emails} recipients...")

        for index, (email, token) in enumerate(records, 1):
            # Create email message
            subject_prefix = "REMINDER: " if (is_reminder and not send_to_all) else ""
            
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

            msg = MIMEText(html_content, 'html')
            msg['Subject'] = subject_prefix + config['poll']['email_subject']
            msg['From'] = formatted_from
            msg['To'] = email
            msg['Reply-To'] = smtp_replyto

            # Send email
            server.send_message(msg)
            action = "email" if send_to_all else "reminder"
            print(f"Sent {action} {index}/{total_emails} to {email} with token: {token}")
            time.sleep(0.100)

    except Exception as e:
        print(f"Error sending emails: {str(e)}")
    finally:
        try:
            server.quit()
        except:
            pass
        print("Email sending completed.")

def show_voting_status():
    """Show current voting statistics"""
    conn = sqlite3.connect(POLL_DB_FILE)
    c = conn.cursor()
    
    try:
        # Get total count
        c.execute("SELECT COUNT(*) FROM polls")
        total = c.fetchone()[0]
        
        # Get voted count
        c.execute("SELECT COUNT(*) FROM polls WHERE vote IS NOT NULL")
        voted = c.fetchone()[0]
        
        # Get not voted count
        not_voted = total - voted
        
        # Get vote breakdown
        c.execute("SELECT vote, COUNT(*) FROM polls WHERE vote IS NOT NULL GROUP BY vote")
        vote_breakdown = c.fetchall()
        
        print("\n=== CURRENT VOTING STATUS ===")
        print(f"Total recipients: {total}")
        print(f"Voted: {voted}")
        print(f"Not voted yet: {not_voted}")
        
        if vote_breakdown:
            print("\nVote breakdown:")
            for vote_type, count in vote_breakdown:
                print(f"  {vote_type}: {count}")
        
        print("=" * 30 + "\n")
        
    except Exception as e:
        print(f"Error getting voting status: {str(e)}")
    finally:
        conn.close()

def main():
    # Check if config.ini exists first
    config_file = 'config.ini'
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please ensure config.ini exists in the current directory.")
        exit(1)
    
    # Check if poll database exists
    if not os.path.exists(POLL_DB_FILE):
        print(f"Error: Poll database file '{POLL_DB_FILE}' not found.")
        print("Please run create_poll_db.py to create the database first.")
        exit(1)
    
    parser = argparse.ArgumentParser(
        description='Send poll emails or reminders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python eazypoll.py                    # Show voting status and exit
  python eazypoll.py --reminder        # Send reminders to non-voters only
  python eazypoll.py --all             # Send to all recipients
        """
    )
    
    parser.add_argument(
        '--all', 
        action='store_true',
        help='Send poll emails to all recipients'
    )
    
    parser.add_argument(
        '--reminder',
        action='store_true',
        help='Send reminder emails to non-voters only'
    )
    
    args = parser.parse_args()
    
    # Read configuration (already validated config.ini exists)
    config = read_config()
    
    # Always show status first
    show_voting_status()
    
    # Default behavior: show status and exit
    if not args.all and not args.reminder:
        print("Use --reminder to send reminders to non-voters or --all to send to all recipients.")
        sys.exit(0)
    
    # Determine what type of sending this is
    if args.all:
        print("Mode: Sending to ALL recipients")
        is_reminder = False
        send_to_all = True
    elif args.reminder:
        print("Mode: Sending REMINDERS to non-voters only")
        is_reminder = True
        send_to_all = False
    
    # Confirm before sending
    try:
        response = input("Do you want to proceed with sending emails? (y/N): ").strip()
        if response.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    
    # Generate and send emails
    generate_and_send_emails(config, send_to_all=send_to_all, is_reminder=is_reminder)
    
    print("Process completed!")
    
    # Show final status
    show_voting_status()

if __name__ == "__main__":
    main()
