<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $file = fopen("mail.txt", "a");
    fwrite($file, $email . "\n");
    fclose($file);
}
?>
