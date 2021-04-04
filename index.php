 <!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="styles.css">
<script src="javascript.js"></script> 
<title>Sisäilma-asema</title>
</head>
<body>
<div class="bgimg">
<h1>
<a href="index.php">Sisäilma-asema</a>
</h1>
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
    <th id="values"><a id="av" href="24h.php">24.5</a></th>
</tr>
</table>
<table id="fronttable">
    <tr>
        <th id="tableheader">Humidity</th>
    </tr>
    <tr>
    <th id="values"><a id="av" href="24h.php">45 %</a></th>
    </tr>
    </table>
</div>
</body>
</html> 