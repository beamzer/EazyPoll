# EazyPoll
simple poll website, sending out polls via emails and voting by clicking links

Very simply poll software
eazypoll.py reads the file recipients.txt and creates a unique token for them and stores this in a newly created sqlite database (poll_databasedb), next it sends each recipient an e-mail with two (or more) url's. There is one URL for yes, and one for NO, but you can easily modify this if needed.
If the user clicks one of the urls, it will record the vote and the time of the vote for that specific user/token. Once the vote is recorded, that token can't be used again for voting, so only the first vote counts. After the vote is recorded via vote.php, the user will be redirected to myresults.php where the total of all YES/NO votes is shown and how my votes are still pending. Also his/here vote is shown through the used token, the vote (YES or NO) and the time that the vote was done. This servers as a way to check that the right vote information was recorded.
