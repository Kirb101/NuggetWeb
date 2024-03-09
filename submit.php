<?php
if (isset($_GET["email"])) {
    $email = $_GET["email"];
    file_put_contents("mail.txt", $email . PHP_EOL, FILE_APPEND | LOCK_EX);
    echo "Email added successfully!";
} else {
    echo "No email provided!";
}
?>
