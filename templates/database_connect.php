<?php
    $servername="localhost";  
        $username="rotemla";
        $password="tL?R1casWa";
        $dbname="rotemla_hakesh&trom";
        $conn = new mysqli($servername, $username, $password, $dbname);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        if (!$conn->set_charset("utf8")) {
            printf("Error loading character set utf8: %s\n", $conn->error);
            exit();
        }
?>