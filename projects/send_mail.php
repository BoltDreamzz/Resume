<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $to = "your@email.com"; // Replace with your actual email address
    $subject = $_POST["subject"];
    $message = $_POST["message"];
    $headers = "From: " . $_POST["email"];

    // Create a mailto link
    $mailtoLink = "mailto:$to?subject=" . urlencode($subject) . "&body=" . urlencode($message . "\n\nFrom: " . $headers);

    // Redirect to the mailto link
    header("Location: $mailtoLink");
    exit();
}
?>
