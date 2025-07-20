<?php
session_start();
// Ensure user is authenticated
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error'=>'Unauthorized']);
    exit;
}
// Read JSON
$accounts = json_decode(file_get_contents('accounts.json'), true);

// Validate and sanitize POST params
if (!isset($_POST['from'], $_POST['to'], $_POST['amount'])) {
    http_response_code(400);
    echo json_encode(['error'=>'Missing parameters']);
    exit;
}
$from = intval($_POST['from']);
$to = intval($_POST['to']);
$amount = floatval($_POST['amount']);

// Business logic checks
if ($amount <= 0) {
    http_response_code(400);
    echo json_encode(['error'=>'Amount must be positive']);
    exit;
}
if (!isset($accounts[$from]) || !isset($accounts[$to])) {
    http_response_code(404);
    echo json_encode(['error'=>'Account not found']);
    exit;
}

// Perform transfer atomically
if ($accounts[$from]['balance'] < $amount) {
    http_response_code(400);
    echo json_encode(['error'=>'Insufficient funds']);
    exit;
}
$accounts[$from]['balance'] -= $amount;
$accounts[$to]['balance'] += $amount;

// Persist
file_put_contents('accounts.json', json_encode($accounts, JSON_PRETTY_PRINT));

echo json_encode(['status'=>'success']);
?>