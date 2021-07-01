<?php
require_once "pdo.php";

// Demand a GET parameter
if ( ! isset($_GET['who']) || strlen($_GET['who']) < 1  ) {
    die('Name parameter missing');
} else {
  $name = $_GET['who'];
}

// If the user requested logout go back to index.php
if ( isset($_POST['logout']) ) {
    header('Location: index.php');
    return;
}

if ( isset($_POST['addnew']) && isset($_POST['make']) && isset($_POST['year']) && isset($_POST['mileage'])) {
  $make = $_POST['make'];
  if (strlen($make) > 1) {
    if (is_numeric($_POST['year']) && is_numeric($_POST['mileage'])) {
      $sql = "INSERT INTO autos (make, year, mileage)
                VALUES (:make, :year, :mileage)";
      $stmt = $pdo->prepare($sql);
      $stmt->execute(array(
          ':make' => htmlentities($_POST['make']),
          ':year' => $_POST['year'],
          ':mileage' => $_POST['mileage']));
      } else {
        echo("Mileage and year must be numeric.");
      }
    } else {
      echo ("Make is required.");
    }
}


date_default_timezone_set('America/Chicago');
$lasthour = date('Y-m-d H:i', time() - 3600);

$stmt = $pdo->query("SELECT time, title from song where time > '{$lasthour}' order by time desc");
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<html>
<head>
<title>Muddys Song List</title>
</head><body>
  <?php echo("<h1>Music for $name</h1>\n");
  echo 'Last hour: '. $lasthour ."\n";
  ?>
<table border="1">
<?php
foreach ( $rows as $row ) {
    echo "<tr><td>";
    echo($row['time']);
    echo("</td><td>");
    echo($row['title']);
    echo("</td></tr>\n");
    #echo("</td><td>");
    # echo('<form method="post"><input type="hidden" ');
    # echo('name="auto_id" value="'.$row['auto_id'].'">'."\n");
    # echo('<input type="submit" value="Del" name="delete">');
    # echo("\n</form>\n");
    #echo("</td></tr>\n");
}
?>
</table>
<form method="post">
<input type="submit" name="logout" value="Logout">
</form>
</body>
