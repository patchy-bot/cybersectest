<?php
// web3/param/gateway.php
// Simple API gateway with authentication and sanitization
header('Content-Type: application/json');

// Basic API key check
$headers = getallheaders();
if (empty($headers['X-API-KEY']) || $headers['X-API-KEY'] !== getenv('API_KEY')) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

$from = filter_var($input['from'], FILTER_SANITIZE_STRING);
$to = filter_var($input['to'], FILTER_SANITIZE_STRING);
$amount = filter_var($input['amount'], FILTER_VALIDATE_FLOAT);
if ($amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

// Load and update ledger
$path = __DIR__ . '/data.json';
$data = json_decode(file_get_contents($path), true);
if (!isset($data[$from]) || $data[$from] < $amount) {
    http_response_code(400);
    echo json_encode(['error' => 'Insufficient funds']);
    exit;
}

$data[$from] -= $amount;
$data[$to] = ($data[$to] ?? 0) + $amount;
file_put_contents($path, json_encode($data, JSON_PRETTY_PRINT));

echo json_encode(['success' => true, 'balances' => [$from => $data[$from], $to => $data[$to]]]);
