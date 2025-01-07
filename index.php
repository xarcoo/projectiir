<?php
echo "PROJECT IIR <br>";
echo "KEPO.COM";
echo '<form action="result.php" method="POST">';
echo '<b>Keyword :</b> <input type="text" name="keyword"><br><br>';
echo '<b>Source :</b> ';
echo '<input type="radio" name="method" value="X" checked/>X ';
echo '<input type="radio" name="method" value="Instagram"/>Instagram';
echo '<input type="radio" name="method" value="Youtube"/>Youtube<br>';
echo '<b>Similarity Method :</b> ';
echo '<input type="radio" name="method" value="Asymetric" checked/>Asymetric ';
echo '<input type="radio" name="method" value="Overlap"/>Overlap<br><br>';
echo '<input type="submit" name="crawl" value="Search"> ';
echo '</form>';
?>