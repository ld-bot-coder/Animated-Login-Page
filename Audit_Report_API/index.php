<?php
// Allow CORS requests from any origin
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json');  // Set header to JSON

// Handle preflight (OPTIONS) requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    // Return only the headers and not the content on OPTIONS requests
    exit(0);
}

// Connect to the database (Replace with your database details)
$servername = "localhost";
$username = "ultiplie_cipla_top_Pulmonologyst";
$password = "9+CZ=pm{d)Ox";
$database = "ultiplie_cipla_top_Pulmonologysts";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    echo json_encode(array("status" => "error", "message" => "Connection failed: " . $conn->connect_error));
    exit();
}

// Collect form data from POST request
$data = json_decode(file_get_contents('php://input'), true);

if (!$data) {
    echo json_encode(array("status" => "error", "message" => "No data received"));
    exit();
}

// Extract data
$name = $data['name'] ?? '';
$pincode = $data['pincode'] ?? '';
$phone = $data['phone'] ?? '';
$speciality = $data['speciality'] ?? '';
$area = $data['area'] ?? '';
$city = $data['city'] ?? '';
$state = $data['state'] ?? '';
$gmb_link = $data['gmb_link'] ?? '';

// Set gmb_status based on whether gmb_link is provided
$gmb_status = !empty($gmb_link) ? 'Yes' : 'No';

// Set default values for status, created_date, and modified_date
$status = 0;  // Default to inactive
$created_date = date('Y-m-d H:i:s');
$modified_date = $created_date;

// Prepare SQL query using prepared statements
$stmt = $conn->prepare("INSERT INTO whatsapp_dr_details (name, pincode, phone, speciality, area, city, state, gmb_status, gmb_link, modified_date, created_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
$stmt->bind_param("ssssssssssss", $name, $pincode, $phone, $speciality, $area, $city, $state, $gmb_status, $gmb_link, $modified_date, $created_date, $status);

if ($stmt->execute()) {
    echo json_encode(array("status" => "success", "message" => "New record created successfully"));
} else {
    echo json_encode(array("status" => "error", "message" => "Error: " . $stmt->error));
}

$stmt->close();
$conn->close();
?>
