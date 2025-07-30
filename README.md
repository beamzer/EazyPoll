# EazyPoll

A simple, secure email-based polling system that allows you to conduct polls by sending personalized voting links to recipients.

## Overview

EazyPoll enables you to create polls where recipients vote by clicking links in emails. Each recipient receives a unique, secure token that prevents duplicate voting and ensures poll integrity.

## Features

- **Secure Voting**: Unique tokens prevent duplicate votes and maintain anonymity
- **Email Integration**: Automated email sending with customizable content
- **Web-based Results**: Real-time vote tracking and results display
- **Flexible Configuration**: Easy setup through configuration files
- **Database Management**: SQLite database for reliable data storage
- **Vote Verification**: Recipients can verify their vote was recorded correctly

## How It Works

1. **Setup**: Add recipient emails to a text file and configure your settings
2. **Database Creation**: Generate unique voting tokens for each recipient
3. **Email Distribution**: Send personalized voting emails with Yes/No links
4. **Vote Collection**: Recipients click their preferred option to cast votes
5. **Results Tracking**: View real-time results and vote status

## Quick Start

### 1. Configuration

Create or edit `config.ini`:

```ini
[email]
smtp_server = smtp.your_server.com
smtp_port = 587
smtp_username = your_email@domain.com
smtp_password = your_password
smtp_from_name = Poll Administrator

[poll]
base_url = https://myserver/eazypoll/vote.php?token=
email_subject = Poll Question
question = Do you approve this proposal?
body_text = <p>We are seeking your input on an important matter.</p>
    <p><strong>Please vote by clicking one of the options below:</strong></p>

[files]
recipients_file = recipients.txt
```

### 2. Add Recipients

Create `recipients.txt` with one email address per line:
```
alice@example.com
bob@example.com
charlie@example.com
```

### 3. Initialize Database

```bash
python create_poll_db.py
```

This creates `poll_database.db` with unique tokens for each recipient.

### 4. Send Poll Emails

```bash
python eazypoll.py
```

Recipients will receive emails with personalized voting links.

### 5. View Results

Transfer `poll_database.db` to your web server and access:
- `results.php` - Anonymous vote overview
- `results_email.php` - Vote overview with email addresses
- `myresults.php` - Individual vote confirmation page

## File Structure

### Python Scripts
- **`create_poll_db.py`** - Initializes database with recipient tokens
- **`eazypoll.py`** - Sends poll emails to all recipients  
- **`show_db.py`** - Displays current database contents

### Web Files (for server)
- **`vote.php`** - Processes incoming votes and redirects to myresults
- **`myresults.php`** - Shows individual vote confirmation and totals
- **`results.php`** - Shows anonymous voting results and statistics
- **`results_email.php`** - Shows voting results with email addresses

### Configuration Files
- **`config.ini`** - Main configuration (email, poll settings, file paths)
- **`recipients.txt`** - List of recipient email addresses
- **`poll_database.db`** - SQLite database (auto-generated)

## Security Features

- **One Vote Per Token**: Each recipient gets exactly one vote, this prevents re-using a token that is sniffed from the network. Also if the token is used before the intended recipient can use the token to vote, he of she will get an error and can inquire with the organizer what happened.
- **Token Expiration**: Tokens become invalid after voting
- **Secure Links**: Unique, non-guessable voting URLs
- **Anonymous Options**: Results can be displayed without email addresses
- **Vote Verification**: Recipients can confirm their vote was recorded

## Customization

### Email Content
Modify the `[poll]` section in `config.ini` to customize:
- Poll question and description
- Email subject line
- HTML formatting in body text

### Voting Options
The system defaults to Yes/No voting but can be easily modified in the PHP files to support multiple choice options.

### Results Display
Choose between anonymous results (`results.php`) or results with email addresses (`results_email.php`) based on your privacy requirements.

## Requirements

### Python Environment
- Python 3.x
- SQLite3 (included with Python)
- Email server access (SMTP)

### Web Server
- PHP-enabled web server
- SQLite support in PHP
- Write permissions for database file

## Database Schema

The `polls` table structure:
```sql
CREATE TABLE polls (
    token TEXT PRIMARY KEY,
    email TEXT,
    vote TEXT,
    voted_at DATETIME
);
```

## Troubleshooting

### Common Issues

**Database Already Exists**
- `create_poll_db.py` will prompt before overwriting existing databases
- Choose 'y' to recreate or 'n' to preserve existing data

**Email Sending Fails**  
- Verify SMTP settings in `config.ini`
- Check email server authentication requirements
- Ensure firewall allows SMTP connections

**Web Server Issues**
- Confirm PHP has SQLite support enabled
- Check file permissions on `poll_database.db`
- Verify web server can read/write database file

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
