<?php
try {
    $db = new SQLite3('poll_database.db');

    // Retrieve token from URL
    $token = isset($_GET['token']) ? $_GET['token'] : null;

    if (!$token) {
        throw new Exception("Token parameter is required.");
    }

    // First check if the token exists
    $stmt = $db->prepare("SELECT COUNT(*) FROM polls WHERE token = :token");
    $stmt->bindValue(':token', $token, SQLITE3_TEXT);
    $token_exists = $stmt->execute()->fetchArray()[0];

    if (!$token_exists) {
        throw new Exception("Unknown token provided.");
    }

    // If we get here, the token exists, so proceed with the rest of the code
    $yes_votes = $db->querySingle("SELECT COUNT(*) FROM polls WHERE vote = 'yes'");
    $no_votes = $db->querySingle("SELECT COUNT(*) FROM polls WHERE vote = 'no'");
    $total_votes = $yes_votes + $no_votes;
    $pending_votes = $db->querySingle("SELECT COUNT(*) FROM polls WHERE vote IS NULL");

    // Calculate percentages
    $yes_percentage = $total_votes > 0 ? round(($yes_votes / $total_votes) * 100, 1) : 0;
    $no_percentage = $total_votes > 0 ? round(($no_votes / $total_votes) * 100, 1) : 0;

    // Get detailed results for the specific token
    $stmt = $db->prepare("SELECT token, vote, voted_at FROM polls WHERE token = :token ORDER BY voted_at DESC");
    $stmt->bindValue(':token', $token, SQLITE3_TEXT);
    $results = $stmt->execute();
    
    if (!$results) {
        throw new Exception("Failed to execute query: " . $db->lastErrorMsg());
    }

    // Display results
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Poll Results</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }
            .summary {
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .progress-bar {
                background-color: #e0e0e0;
                height: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .progress {
                background-color: #4CAF50;
                height: 100%;
                border-radius: 10px;
                text-align: right;
                padding-right: 5px;
                color: white;
                box-sizing: border-box;
            }
            .no-progress {
                background-color: #f44336;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f5f5f5;
            }
            .error {
                padding: 20px;
                background-color: #f2dede;
                border: 1px solid #ebccd1;
                border-radius: 4px;
                color: #a94442;
                max-width: 500px;
                margin: 20px auto;
                text-align: center;
            }
            .footer {
                margin-top: 40px;
                padding: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
            .footer a {
                color: #337ab7;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Poll Results for Token: <?php echo htmlspecialchars($token); ?></h1>

        <div class="summary">
            <h2>Summary</h2>
            <p>Total votes: <?php echo $total_votes; ?></p>
            <p>Pending votes: <?php echo $pending_votes; ?></p>

            <h3>Yes Votes: <?php echo $yes_votes; ?> (<?php echo $yes_percentage; ?>%)</h3>
            <div class="progress-bar">
                <div class="progress" style="width: <?php echo $yes_percentage; ?>%">
                    <?php echo $yes_percentage; ?>%
                </div>
            </div>

            <h3>No Votes: <?php echo $no_votes; ?> (<?php echo $no_percentage; ?>%)</h3>
            <div class="progress-bar">
                <div class="progress no-progress" style="width: <?php echo $no_percentage; ?>%">
                    <?php echo $no_percentage; ?>%
                </div>
            </div>
        </div>

        <h2>My Vote</h2>
        <table>
            <tr>
                <th>Token</th>
                <th>Vote</th>
                <th>Voted At</th>
            </tr>
            <?php while ($row = $results->fetchArray(SQLITE3_ASSOC)) { ?>
                <tr>
                    <td><?php echo htmlspecialchars($row['token']); ?></td>
                    <td><?php echo htmlspecialchars($row['vote']); ?></td>
                    <td><?php echo htmlspecialchars($row['voted_at']); ?></td>
                </tr>
            <?php } ?>
        </table>

        <div class="footer">
            <p>Powered by <strong>EazyPoll</strong> - Open source polling software</p>
            <p>Source code available at: <a href="https://github.com/beamzer/EazyPoll" target="_blank">https://github.com/beamzer/EazyPoll</a></p>
        </div>
    </body>
    </html>

    <?php
    // Close database connection
    $db->close();
    ?>

<?php
}
catch (Exception $e) {
    // Display only the error message in a styled div
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Error</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }
            .error {
                padding: 20px;
                background-color: #f2dede;
                border: 1px solid #ebccd1;
                border-radius: 4px;
                color: #a94442;
                max-width: 500px;
                margin: 20px auto;
                text-align: center;
            }
            .footer {
                margin-top: 40px;
                padding: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
            .footer a {
                color: #337ab7;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="error">
            <h2>Error</h2>
            <p><?php echo htmlspecialchars($e->getMessage()); ?></p>
        </div>

        <div class="footer">
            <p>Powered by <strong>EazyPoll</strong> - Open source polling software</p>
            <p>Source code available at: <a href="https://github.com/beamzer/EazyPoll" target="_blank">https://github.com/beamzer/EazyPoll</a></p>
        </div>
    </body>
    </html>
    <?php
}
?>
