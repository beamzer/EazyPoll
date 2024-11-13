# EazyPoll

## Simple poll website, sending out polls via email. Recipients can vote by clicking the link with the desired answer

EazyPoll is a very simple poll software. ```eazypoll.py``` reads the file ```recipients.txt``` and creates a unique token for each recipient, storing this in a newly created SQLite database (```poll_database.db```). It then sends each recipient an email with two (or more) URLs - one for "Yes" and one for "No" (this can be easily modified if needed).

If the user clicks one of the URLs, it will record the vote and the time of the vote for that specific user/token. Once the vote is recorded, that token cannot be used again for voting, so only the first vote counts. After the vote is recorded via ```vote.php```, the user will be redirected to ```myresults.php``` where the total of all "Yes" and "No" votes is shown, as well as how many votes are still pending. The user's own vote (Yes or No) and the time it was cast are also displayed, serving as a way to check that the right vote information was recorded.
- To use, copy all files to the webserver in a directory eazypoll (or modify to your needs)
- Fill ```recipients.txt``` with the e-mail addresses of the people that are going to vote, one per line
- Change ```config.ini``` so the URL that is being send out is correct
- Change ```config.ini``` so that the mailserver info is correct for your environment to send out e-mail
- Default the mail functionality is commented out, so you can do a dry run first
- Change passwords on ```results.php``` and ```results_email.php``` so that you are the only one with access
- Change ```_htaccess``` to ```.htaccess``` and make sure your webserver interprets this file correctly, so try to open recipients.txt through your webbrowser and verify that access is denied. With security settings, always test, never assumen!
- Make sure mod_rewrite is active in Apache. We use mod_rewrite to prevent Microsoft ATP SafeLinks from voting for us
- Make sure the webserver can write poll_database.db to record the votes
- Do a dry run, copy one of the generated URLs into the address bar of your browser and see if the vote gets cast
- Do a whet run, remove ```poll_database.db``` and fill ```recipients.txt``` with one or two email adresses that you have access to. Remove the comments in ```eazypoll.py``` so that it will send out mails when run, modify the e-mail text in the cody to your liking and run the code
- If it's really important that things go well, or when using a large list of recipients, I would recommend to do the step above again with some friends and/or collegues
- Prepare for the real run, remove ```poll_database.db```, fill ```recipients.txt```  with the real recipients and sit back and relax

The screenshot below shows what the user sees after the voting url:
<img width="977" alt="screenshot" src="https://github.com/user-attachments/assets/066849ab-3df5-4b7e-ab07-5a8ab8988aff">
