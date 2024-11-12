<?php
// Basic authentication (you should implement proper authentication)
$username = "santa";
$password = "secret";

if (!isset($_SERVER['PHP_AUTH_USER']) ||
    !isset($_SERVER['PHP_AUTH_PW']) ||
    $_SERVER['PHP_AUTH_USER'] != $username ||
    $_SERVER['PHP_AUTH_PW'] != $password) {
    header('WWW-Authenticate: Basic realm="Poll Results"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Authentication required';
    exit;
}

try {
    $db = new SQLite3('poll_database.db');

    // Get vote counts
    $yes_votes = $db->querySingle("SELECT COUNT(*) FROM polls WHERE vote = 'yes'");
    $no_votes = $db->querySingle("SELECT COUNT(*) FROM polls WHERE vote = 'no'");
    $total_votes = $yes_votes + $no_votes;
    $pending_votes = $db->querySingle("SELECT COUNT(*) FROM polls WHERE vote IS NULL");

    // Calculate percentages
    $yes_percentage = $total_votes > 0 ? round(($yes_votes / $total_votes) * 100, 1) : 0;
    $no_percentage = $total_votes > 0 ? round(($no_votes / $total_votes) * 100, 1) : 0;

    // Get detailed results - only for registered votes
    $results = $db->query("SELECT token, vote, voted_at FROM polls WHERE vote IS NOT NULL ORDER BY voted_at DESC");
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
        </style>
    </head>
    <body>
        <h1>Poll Results</h1>

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

        <h2>Detailed Results (<?php echo $total_votes; ?> registered votes)</h2>
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
    </body>
    </html>

    <?php
    // Close database connection
    $db->close();
    ?>

<?php
}
catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}
?>
