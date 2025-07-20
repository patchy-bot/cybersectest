<?php
session_start();

// CSRF token generation on login or form render
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

// Authentication check
if (empty($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error'=>'Unauthorized']);
    exit;
}

// Only accept JSON POST
$data = json_decode(file_get_contents('php://input'), true);
if (!isset($data['csrf_token']) || !hash_equals($_SESSION['csrf_token'], $data['csrf_token'])) {
    http_response_code(403);
    echo json_encode(['error'=>'Invalid CSRF token']);
    exit;
}

$action = $data['action'] ?? '';
$user_id = intval($data['user_id'] ?? 0);
$value = substr($data['value'] ?? '', 0, 100);

// Perform authorized account modification
// ... your logic here ...

echo json_encode(['status'=>'success']);
?>