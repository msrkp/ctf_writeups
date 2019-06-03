<?php
if ( isset($_GET["a"]) && isset($_GET["b"]) ){
	$a = $_GET["a"] ; 
	$b = $_GET["b"] ;
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "test";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	} 

	$sql = "INSERT INTO log_txt (a,b) VALUES ('$a', '$b');";
	$result = $conn->query($sql);
	$conn->close();
}
?>