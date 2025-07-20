<?php
session_start();

// Database connection with PDO
$dsn = 'mysql:host=localhost;dbname=bank';
$db = new PDO($dsn, 'user', 'password', [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_EMULATE_PREPARES => false
]);

// Ensure user is authenticated
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);
$amount = filter_var($data['amount'], FILTER_VALIDATE_INT);
$target = filter_var($data['target_account'], FILTER_SANITIZE_STRING);

if ($amount === false || $amount <= 0 || empty($target)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid parameters']);
    exit;
}

// Parameterized query to update balance
$stmt = $db->prepare(
    'UPDATE accounts SET balance = balance + :amount WHERE user_id = :uid AND account_number = :acct'
);
$stmt->execute([
    ':amount' => $amount,
    ':uid' => $_SESSION['user_id'],
    ':acct' => $target
]);

echo json_encode(['status' => 'success']);
?>