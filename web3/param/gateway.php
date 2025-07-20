<?php
session_start();
// Basic auth check
if (!isset($_SESSION['user']) || $_SESSION['role'] !== 'admin') {
    http_response_code(403);
    echo json_encode(['error' => 'Forbidden']);
    exit;
}

$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!isset($data['account']) || !preg_match('/^[a-zA-Z0-9_]{3,30}$/', $data['account'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid account name']);
    exit;
}
// Load and decode
$accounts = json_decode(file_get_contents('accounts.json'), true);
// Update only allowed fields
$account = $data['account'];
$accounts[$account]['status'] = $data['status'] ?? $accounts[$account]['status'];

target = fopen('accounts.json', 'w');
fwrite($target, json_encode($accounts, JSON_PRETTY_PRINT));
fclose($target);

echo json_encode(['success' => true]);
?>