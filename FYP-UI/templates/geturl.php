<?php
	header("Access-Control-Allow-Origin: http://localhost:5000");
	$url = $_GET['url'];
	echo "'<script>console.log("wassup")</script>'";
	if(!($data = file_get_contents($url))) 
		return false;
	if(preg_match("#<title>(.+)<\/title>#iU", $data, $t))  
		return trim($t[1]);
	else
		return false;
?>