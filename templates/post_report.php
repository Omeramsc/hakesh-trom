<?php
    include 'database_connect.php';
    if ($_GET){ 
        $city=$_GET['city'];
        $address=$_GET['address'];
        $type=$_GET['type'];
        $description=$_GET['description'];
        $sql="INSERT into report(city, address, type, description) values ('".$city."','".$address."','".$type."','".$description."')";
        if(!$conn->query($sql)){
            echo "Couldn't create a new report:\n".$conn->error;
            exit();
        }
    }
    $conn->close();
    header("location: ".'report.php');
?>