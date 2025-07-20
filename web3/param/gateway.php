<?php
session_start();

// Check if user is logged in (simple session auth example)
if (!isset($_SESSION['username'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

// Sample user accounts and roles
$user_accounts = [
    'alice' => ['role' => 'user'],
    'bob' => ['role' => 'user'],
    'admin' => ['role' => 'admin']
];

// Load account balances from JSON file
$balances_file = 'balances.json';
$balances = json_decode(file_get_contents($balances_file), true);

// Validate request method
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Only POST allowed']);
    exit;
}

// Get POST data and validate
$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['sender'], $input['recipient'], $input['amount'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

$sender = $input['sender'];
$recipient = $input['recipient'];
$amount = $input['amount'];

// Validate parameter types
if (!is_string($sender) || !is_string($recipient) || !is_numeric($amount) || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid parameter types or values']);
    exit;
}

// Authorization: only allow logged in user to transfer from their own account unless admin
$logged_in_user = $_SESSION['username'];
$user_role = isset($user_accounts[$logged_in_user]) ? $user_accounts[$logged_in_user]['role'] : 'user';

if ($logged_in_user !== $sender && $user_role !== 'admin') {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized to transfer from this account']);
    exit;
}

// Check sender balance
if (!isset($balances[$sender]) || $balances[$sender] < $amount) {
    http_response_code(400);
    echo json_encode(['error' => 'Insufficient balance']);
    exit;
}

// Check recipient exists
if (!isset($balances[$recipient])) {
    http_response_code(400);
    echo json_encode(['error' => 'Recipient does not exist']);
    exit;
}

// Perform transfer
$balances[$sender] -= $amount;
$balances[$recipient] += $amount;

// Save updated balances
file_put_contents($balances_file, json_encode($balances));

echo json_encode(['message' => 'Transfer completed', 'balances' => $balances]);
?>
