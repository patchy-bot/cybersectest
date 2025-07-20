<?php
session_start();
header('Content-Type: application/json');
// Ensure session cookie settings are secure in php.ini:
// session.cookie_secure = 1
// session.cookie_httponly = 1

if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$raw = file_get_contents('php://input');
$input = json_decode($raw, true);
$from_user = $_SESSION['user_id'];
$to_account = isset($input['to_account']) ? filter_var($input['to_account'], FILTER_SANITIZE_STRING) : '';
$amount = isset($input['amount']) ? filter_var($input['amount'], FILTER_VALIDATE_FLOAT) : false;

if (!$to_account || $amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid parameters']);
    exit;
}

$file = __DIR__ . '/data/accounts.json';
$fp = fopen($file, 'c+');
if (!$fp) {
    http_response_code(500);
    echo json_encode(['error' => 'Storage error']);
    exit;
}

if (flock($fp, LOCK_EX)) {
    $json = stream_get_contents($fp);
    $data = json_decode($json, true) ?: [];
    if (!isset($data[$from_user]) || $data[$from_user] < $amount) {
        flock($fp, LOCK_UN);
        fclose($fp);
        http_response_code(400);
        echo json_encode(['error' => 'Insufficient funds']);
        exit;
    }
    $data[$from_user] -= $amount;
    if (!isset($data[$to_account])) {
        $data[$to_account] = 0;
    }
    $data[$to_account] += $amount;

    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data, JSON_PRETTY_PRINT));
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);

    echo json_encode(['status' => 'success']);
} else {
    fclose($fp);
    http_response_code(500);
    echo json_encode(['error' => 'Could not lock storage']);
}
?>