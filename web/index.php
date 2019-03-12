<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<?php
	$APP_NAME='Pobshare';
	$TITLE_PAGE='Pobshare! Share large files and folders within your network.';
	$LOGO='imgs/pobshare-green.png';
?>
<head>
	<title><?php echo $TITLE_PAGE?></title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta charset="utf-8">
    	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<script src="js/jquery.min.js"></script>
	<link rel="stylesheet" href="css/bootstrap.min.css">
	<link rel="stylesheet" href="css/local.css">
	<link rel="shortcut icon" type="image/png" href="imgs/favicon.png"/>
	<script src="js/bootstrap.bundle.min.js"></script>
</head>

<body>


<nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top ">
  <a class="navbar-brand" href="index.php"><img src="<?php echo $LOGO?>" width="30" height="30" class="d-inline-block align-top" alt="" style="margin-right: 5px"><?php echo $APP_NAME ?></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div class="navbar-nav">
      <a class="nav-item nav-link" href="index.php?page=screenshots">Screenshots</a>
      <a class="nav-item nav-link" href="index.php?page=downloads">Downloads</a>
      <a class="nav-item nav-link" href="index.php?page=license">License</a>
      <a class="nav-item nav-link" href="index.php?page=authors">Authors</a>
      <a class="nav-item nav-link" href="index.php?page=documentation">Documentation</a>
      <a class="nav-item nav-link" href="https://github.com/pobfdm/pobshare/issues">Report a problem</a>
    </div>
  </div>
</nav>

<?php
	switch ($_GET['page']) {
    case "home":
       include('pages/home.php');
        break;
    case "screenshots":
        include('pages/screenshots.php');
        break;
    case "license":
        include('pages/license.php');
        break;    
    case "downloads":
        include('pages/downloads.php');
        break;
     case "documentation":
        include('pages/documentation.php');
        break;
     case "authors":
        include('pages/authors.php');
        break;       
    default:
        include('pages/home.php');
}

?>

</body>
</html>
