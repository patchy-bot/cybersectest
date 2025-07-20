<?php
header('Content-Type: application/json');

// Simple auth check (e.g., session or token)
session_start();
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (json_last_error() !== JSON_ERROR_NONE) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

// Validate allowed keys and types
$allowed_keys = ['amount', 'recipient_id'];
foreach ($allowed_keys as $key) {
    if (!isset($input[$key])) {
        http_response_code(400);
        echo json_encode(['error' => "Missing $key"]);
        exit;
    }
}
$amount = filter_var($input['amount'], FILTER_VALIDATE_INT);
$recipient = filter_var($input['recipient_id'], FILTER_VALIDATE_INT);
if ($amount === false || $amount <= 0 || $recipient === false) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid parameters']);
    exit;
}

// Use prepared statements to update
$db = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass', [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$stmt = $db->prepare('UPDATE accounts SET balance = balance - :amt WHERE user_id = :uid');
$stmt->execute([':amt'=>$amount,':uid'=>$_SESSION['user_id']]);

$stmt2 = $db->prepare('UPDATE accounts SET balance = balance + :amt WHERE user_id = :rec');
$stmt2->execute([':amt'=>$amount,':rec'=>$recipient]);

echo json_encode(['status'=>'success']);