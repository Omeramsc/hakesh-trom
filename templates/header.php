<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Hakesh&Trom</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous" />
    <link href="http://www.cssscript.com/wp-includes/css/sticky.css" rel="stylesheet" type="text/css">
    <link href="http://ajax.aspnetcdn.com/ajax/jquery.ui/1.8.9/themes/blitzer/jquery-ui.css" rel="stylesheet"
        type="text/css" />
    <link href="..\static\pages_style.css" rel="stylesheet" type="text/css" />
    <link href="..\static\main_page.css" rel="stylesheet" type="text/css" />
</head>

<body class="flex_me" onload="onLoad()">
    <header class="flex_me">
        <img class="user_type" src="http://u.cubeupload.com/Chibameta/TEAM8.png">
        <a href="index.php" class="logo"><img src="http://u.cubeupload.com/Chibameta/HEADERLOGOCENTERPNGF.png"
            alt="חזור לעמוד הראשי"></a>
        <button class="nav_btn" onclick="toggleSideNav()"><i class="fa fa-bars"></i></button>
    </header>
    <aside>
        <nav id="hamburger" class="quick_trans hide_link">
            <button class="nav_btn" onclick="toggleSideNav()"><i class="fa fa-times"></i></button>
            <img id="nav_logo" src="http://u.cubeupload.com/Chibameta/HEADERLOGOCENTERPNGF.png"
                style="width:190px; height: 50px; margin:6px auto;">
            <hr>
            <a href="first_steps.php">תרומות<img src="http://u.cubeupload.com/Chibameta/FUNDIcoFix5.png" alt="תרומות"></a>
            <a href="report.php">דיווחים<img src="http://u.cubeupload.com/Chibameta/RepIcoFix.png" alt="דיווחים"></a>
            <a class="not_allowed" href="#">הצוות שלי<img src="http://u.cubeupload.com/Chibameta/pplIcoFix.png"
                alt="לא פעיל בכוונה"></a>
            <a class="not_allowed" href="#">לוח הישגים<img src="http://u.cubeupload.com/Chibameta/LBIcoFix.png"
                alt="לא פעיל בכוונה"></a>
            <a class="not_allowed" href="#">התראות<img src="http://u.cubeupload.com/Chibameta/BellIcofix.png"
                alt="לא פעיל בכוונה"></a>
            <hr>
            <a class="not_allowed" href="#">החלף שפה<img src="http://u.cubeupload.com/Chibameta/LangIcoFix.png"
                alt="לא פעיל בכוונה"></a>
            <a class="not_allowed" href="#">נגישות<img src="http://u.cubeupload.com/Chibameta/DisIcoFix.png"
                alt="לא פעיל בכוונה"></a>
            <a class="not_allowed" href="#">התנתקות<img src="http://u.cubeupload.com/Chibameta/DDISicofix.png"
                alt="לא פעיל בכוונה"></a>
        </nav>
    </aside>