<?php
session_start();
// Simple authentication check
type_check();

function type_check() {
    if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
        http_response_code(403);
        exit('Unauthorized');
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    // Validate expected fields
    if (!isset($input['user']) || !is_string($input['user'])) {
        http_response_code(400);
        exit('Invalid user');
    }
    if (!isset($input['balance']) || !is_int($input['balance'])) {
        http_response_code(400);
        exit('Invalid balance');
    }
    $dataFile = 'data.json';
    $data = json_decode(file_get_contents($dataFile), true);
    $user = htmlspecialchars($input['user'], ENT_QUOTES, 'UTF-8');
    $data[$user] = $input['balance'];
    file_put_contents($dataFile, json_encode($data, JSON_PRETTY_PRINT));
    echo json_encode(['status'=>'ok']);
} else {
    http_response_code(405);
    echo 'Method Not Allowed';
}
?>