 <!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="styles.css">
<script src="javascript.js"></script> 
<title>Sisäilma-asema</title>
</head>
<body>
<div class="bgimg">
<h1>Sisäilma-asema</h1>
<a href="24h.php">
    <img class="imglink" src="Images/24h.png" width="80" height="80">
</a>
<table id="txtbox">
    <tr>
        <th>
            <?php
            $myfile = fopen("perfect.txt", "r") or die("Unable to open file!");
            echo fread($myfile,filesize("perfect.txt"));
            fclose($myfile);
            ?>
        </th>
    </tr>
</table>
<table id="fronttable">
<tr>
    <th id="tableheader">Temperature</th>
</tr>
<tr>
    <th id="values">24.5</th>
</tr>
</table>
<br>
<table id="fronttable">
    <tr>
        <th id="tableheader">Humidity</th>
    </tr>
    <tr>
        <th id="values">45 %</th>
    </tr>
    </table>
</div>
</body>
</html> 