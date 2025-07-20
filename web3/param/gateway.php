<?php
session_start();
header('Content-Type: application/json');

// Simple authentication check
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit();
}

// Read accounts.json under lock
$filename = 'accounts.json';
$fp = fopen($filename, 'c+');
if (flock($fp, LOCK_EX)) {
    $data = stream_get_contents($fp);
    $accounts = json_decode($data, true);
    if (!$accounts) { $accounts = []; }
    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'GET') {
        // Return the calling user's account only
        $user_id = $_SESSION['user_id'];
        $balance = $accounts[$user_id] ?? 0;
        echo json_encode(['user' => $user_id, 'balance' => $balance]);
    } elseif ($method === 'POST') {
        $input = json_decode(file_get_contents('php://input'), true);
        $amount = floatval($input['amount'] ?? 0);
        $user_id = $_SESSION['user_id'];
        if ($amount <= 0) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid amount']);
        } else {
            $accounts[$user_id] = ($accounts[$user_id] ?? 0) + $amount;
            ftruncate($fp, 0);
            rewind($fp);
            fwrite($fp, json_encode($accounts, JSON_PRETTY_PRINT));
            echo json_encode(['status' => 'ok', 'new_balance' => $accounts[$user_id]]);
        }
    } else {
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
    }
    fflush($fp);
    flock($fp, LOCK_UN);
}
fclose($fp);
?>