<?php
// Simple token-based authentication
$valid_tokens = array('secrettoken123');

$headers = apache_request_headers();
if (!isset($headers['Authorization']) || !in_array($headers['Authorization'], $valid_tokens)) {
    http_response_code(401);
    echo json_encode(array('error' => 'Unauthorized'));
    exit;
}

// Read raw POST data
$input = json_decode(file_get_contents('php://input'), true);

// Validate input
if (!isset($input['amount']) || !isset($input['recipient'])) {
    http_response_code(400);
    echo json_encode(array('error' => 'Invalid input'));
    exit;
}

$amount = $input['amount'];
$recipient = $input['recipient'];

// Basic validation
if (!is_numeric($amount) || $amount <= 0) {
    http_response_code(400);
    echo json_encode(array('error' => 'Invalid amount'));
    exit;
}

if (!is_string($recipient) || strlen($recipient) == 0) {
    http_response_code(400);
    echo json_encode(array('error' => 'Invalid recipient'));
    exit;
}

// Load existing data
$file = 'data.json';
$data = array();
if (file_exists($file)) {
    $json = file_get_contents($file);
    $data = json_decode($json, true);
    if (!is_array($data)) {
        $data = array();
    }
}

// Append new entry
$data[] = array('amount' => $amount, 'recipient' => $recipient, 'timestamp' => time());

// Save back to file
file_put_contents($file, json_encode($data));

http_response_code(200);
echo json_encode(array('status' => 'Success'));
?>
