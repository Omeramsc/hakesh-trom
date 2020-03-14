<?php
        include 'database_connect.php';
        $sql="SELECT creation_time, type, city, address, answered FROM report";
        $result=$conn->query($sql);
        if($result->num_rows>0){
            while($row=$result->fetch_assoc()){
            if($row["answered"]){
                $path="../static/report_answered.png";
            }
            else{
                $path="../static/report_unanswered.png";
            }
            echo "<li><img src=".$path."><a id='report_summary' 
                class='hide_link not_allowed' href=#>".$row["creation_time"]."<br><strong>"
                .$row["type"]."</strong><br>".$row["city"].", ".$row["address"]."</a></li>";
            }
        }
?>