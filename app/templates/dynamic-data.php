<?php
$servername = 'localhost';
$username = 'root';
$password = 'Anagha@02021998';
$dbname = 'shoppingcart';

$conn = new mysqli($servername,$username,$password, $dbname);
if($conn->connect_error){
echo "<div style='border:1'>";
        echo $servername;
        echo "</div>";
    die("connection failed" . $conn->connect_error);

}else{
echo "<div style='border:1'>";
        echo $dbname;
        echo "</div>";
}
?>
