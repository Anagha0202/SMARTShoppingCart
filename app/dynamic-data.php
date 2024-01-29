<?php
$servername = 'localhost';
$username = 'root';
$password = 'Anagha@02021998';
$dbname = 'shoppingcart';

$conn = new mysqli($servername,$username,$password, $dbname);
if($conn->connect_error){
    die("connection failed" . $conn->connect_error);
}

$sql = "SELECT * FROM ORDERITEMS";
$result = $conn->query($sql);

if($result->num_rows > 0) {
    while($row = $result->fetch_assoc()){
        echo "<div style='border:1'>";
        echo "UID : " . $row["UID"] . " & UPC : ". $row["UPC"]."<br>";
        echo "</div>";
    }
}
else{
    echo "cart empty";
}
?>
