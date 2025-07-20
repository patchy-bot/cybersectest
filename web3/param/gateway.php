<?php
session_start();
header('Content-Type: application/json');

// Authentication check
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

// Parse and validate JSON input
$input = json_decode(file_get_contents('php://input'), true);
$from_account = filter_var($input['from_account'] ?? '', FILTER_SANITIZE_STRING);
$to_account   = filter_var($input['to_account']   ?? '', FILTER_SANITIZE_STRING);
$amount       = filter_var($input['amount']       ?? 0,    FILTER_VALIDATE_FLOAT);

if (!$from_account || !$to_account || $amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit;
}

// Authorization: ensure the user owns the from_account
if ($_SESSION['user_id'] !== $from_account) {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

try {
    $pdo = new PDO(
        'mysql:host=localhost;dbname=finance;charset=utf8mb4',
        'db_user',
        'db_pass',
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
    // Use prepared statements for updates
    $stmt1 = $pdo->prepare(
        'UPDATE accounts SET balance = balance - :amount WHERE account_id = :from'
    );
    $stmt1->execute([':amount' => $amount, ':from' => $from_account]);

    $stmt2 = $pdo->prepare(
        'UPDATE accounts SET balance = balance + :amount WHERE account_id = :to'
    );
    $stmt2->execute([':amount' => $amount, ':to' => $to_account]);

    echo json_encode(['status' => 'success']);
} catch (PDOException $e) {
    http_response_code(500);
    // Log $e->getMessage() internally, but do not expose to client
    echo json_encode(['error' => 'Server error']);
}
?>