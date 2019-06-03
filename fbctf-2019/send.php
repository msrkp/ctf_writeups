<?php
$time = $_GET['time'];
$flag = $_GET['flag'];

$file = fopen("brute.txt","a");

$data = $flag."-----".$time."\n";
fwrite($file,$data);
fclose($file);

?>