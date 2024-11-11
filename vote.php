<?php
try {
    // Connect to SQLite database
    $db = new SQLite3('poll_database.db');

    // Get parameters
    $token = $_GET['token'];
    $vote = $_GET['vote'];

    // Validate parameters
    if (empty($token) || !in_array($vote, ['yes', 'no'])) {
        throw new Exception('Invalid parameters');
    }

    // Check if token exists and hasn't been used
    $stmt = $db->prepare('SELECT * FROM polls WHERE token = :token AND vote IS NULL');
    $stmt->bindValue(':token', $token, SQLITE3_TEXT);
    $result = $stmt->execute()->fetchArray();

    if (!$result) {
        throw new Exception('Invalid or expired token');
    }

    // Record the vote
    $stmt = $db->prepare('UPDATE polls SET vote = :vote, voted_at = :voted_at WHERE token = :token');
    $stmt->bindValue(':vote', $vote, SQLITE3_TEXT);
    $stmt->bindValue(':voted_at', date('Y-m-d H:i:s'), SQLITE3_TEXT);
    $stmt->bindValue(':token', $token, SQLITE3_TEXT);
    $stmt->execute();

    // Close database connection
    $db->close();

    // Show success message
    echo "<!DOCTYPE html>
          <html>
          <head>
              <title>Vote Recorded</title>
              <meta http-equiv='refresh' content='2;url=myresults.php?token=" . urlencode($token) . "'>
              <style>
                  body {
                      font-family: Arial, sans-serif;
                      text-align: center;
                      margin-top: 50px;
                  }
                  .message {
                      padding: 20px;
                      background-color: #dff0d8;
                      border: 1px solid #d6e9c6;
                      border-radius: 4px;
                      color: #3c763d;
                      max-width: 500px;
                      margin: 0 auto;
                  }
              </style>
          </head>
          <body>
              <div class='message'>
                  <h2>Thank you for your vote!</h2>
		  <p>Your response has been recorded.</p>
                  <p>redirecting you to the results page....</p>
              </div>
          </body>
          </html>";

} catch (Exception $e) {
    // Handle errors
    http_response_code(400);
    echo "<!DOCTYPE html>
          <html>
          <head>
              <title>Error</title>
              <style>
                  body {
                      font-family: Arial, sans-serif;
                      text-align: center;
                      margin-top: 50px;
                  }
                  .error {
                      padding: 20px;
                      background-color: #f2dede;
                      border: 1px solid #ebccd1;
                      border-radius: 4px;
                      color: #a94442;
                      max-width: 500px;
                      margin: 0 auto;
                  }
              </style>
          </head>
          <body>
              <div class='error'>
                  <h2>Error</h2>
                  <p>" . htmlspecialchars($e->getMessage()) . "</p>
              </div>
          </body>
          </html>";
}
?>
