<?php
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "test";

	$conn = new mysqli($servername, $username, $password, $dbname);

	$sql = "SELECT a,b FROM log_txt ORDER BY id DESC LIMIT 1;";
	$result = $conn->query($sql);
	$conn->close();

	while($row = $result->fetch_assoc()) {
        echo $row["a"]." ~^~ ".$row["b"];
    }
?>