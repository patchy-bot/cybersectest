<?php
// Allowed keys and their expected types
$allowed_keys = [
    'name'  => 'string',
    'age'   => 'int',
    'email' => 'string'
];

$key = $_POST['key'] ?? '';
$value = $_POST['value'] ?? '';

if (!array_key_exists($key, $allowed_keys)) {
    http_response_code(400);
    echo 'Invalid key provided.';
    exit;
}

// Read existing data
$json = file_get_contents('data.json');
$data = json_decode($json, true);
if (!is_array($data)) {
    http_response_code(500);
    echo 'Data store corrupted.';
    exit;
}

// Validate and sanitize value based on expected type
switch ($allowed_keys[$key]) {
    case 'int':
        if (!ctype_digit($value)) {
            http_response_code(400);
            echo 'Value must be an integer.';
            exit;
        }
        $value = (int)$value;
        break;
    case 'string':
        $value = trim($value);
        $value = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
        break;
}

// Update and save
$data[$key] = $value;
file_put_contents('data.json', json_encode($data, JSON_PRETTY_PRINT));

echo 'Update successful.';
?>