<?php
session_start();

// Reject if not authenticated
if (!isset($_SESSION['username'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$from   = $input['from_account'] ?? '';
$to     = $input['to_account']   ?? '';
$amount = $input['amount']       ?? '';

// Validate ownership: only allow sender to modify their own balance
if ($from !== $_SESSION['account']) {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized account']);
    exit;
}

// Input validations
if (!is_string($to) || trim($to) === '' || !preg_match('/^[A-Za-z0-9_]+$/', $to)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid recipient']);
    exit;
}
if (!is_numeric($amount) || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

// Load balances
$balancesFile = __DIR__ . '/balances.json';
$balances = json_decode(file_get_contents($balancesFile), true);

// Check sufficient funds
if (!isset($balances[$from]) || $balances[$from] < $amount) {
    http_response_code(400);
    echo json_encode(['error' => 'Insufficient balance']);
    exit;
}

// Perform transfer
$balances[$from] -= $amount;
if (!isset($balances[$to])) {
    $balances[$to] = 0;
}
$balances[$to] += $amount;

// Persist
file_put_contents($balancesFile, json_encode($balances, JSON_PRETTY_PRINT));

echo json_encode(['status' => 'ok', 'from_balance' => $balances[$from]]);
?>