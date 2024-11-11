# EazyPoll

## Simple poll website, sending out polls via emails and recording votes cast by clicking links

EazyPoll is a very simple poll software. ```eazypoll.py``` reads the file ```recipients.txt``` and creates a unique token for each recipient, storing this in a newly created SQLite database (```poll_database.db```). It then sends each recipient an email with two (or more) URLs - one for "Yes" and one for "No" (this can be easily modified if needed).

If the user clicks one of the URLs, it will record the vote and the time of the vote for that specific user/token. Once the vote is recorded, that token cannot be used again for voting, so only the first vote counts. After the vote is recorded via ```vote.php```, the user will be redirected to ```myresults.php``` where the total of all "Yes" and "No" votes is shown, as well as how many votes are still pending. The user's own vote (Yes or No) and the time it was cast are also displayed, serving as a way to check that the right vote information was recorded.
The screenshot below shows what the user sees after voting:
<img width="977" alt="screenshot" src="https://github.com/user-attachments/assets/066849ab-3df5-4b7e-ab07-5a8ab8988aff">
