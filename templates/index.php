<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Hakesh&Trom</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link href="..\static\pages_style.css" rel="stylesheet" type="text/css" />
  <link href="..\static\main_page.css" rel="stylesheet" type="text/css" />
</head>

<body class="flex_me center_text">
  <div class="push_notification">
    <a class="hide_link" href="report.php"><u><strong>דיווח חדש התקבל</strong></u><br>
      לחץ כאן בכדי לצפות בו</a>
  </div>
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
  <main id="main_layout" class="quick_trans">
    <section class="user_info">
      <div class="user">
        <img class="flex_me" src="http://u.cubeupload.com/Chibameta/TeamGif.gif" alt="Team photo">
      </div>
      <div class="usernames flex_me">
        <div>ישראל ישראלי</div>
        <div>יעקב יעקבי</div>
      </div>
    </section>
    <section class="buttons flex_me">
      <div class="icon">
        <a class="hide_link" href="first_steps.php"> <img src="http://u.cubeupload.com/Chibameta/FUNDIcoFix5.png"
            alt="תרומות"><br>
          תרומות</a>
      </div>
      <div class="icon">
        <a class="hide_link not_allowed" href="#"><img src="http://u.cubeupload.com/Chibameta/pplIcoFix.png"
            alt="לא פעיל בכוונה"><br>
          הצוות שלי</a>
      </div>
      <div class="icon">
        <a class="hide_link not_allowed" href="#"><img src="http://u.cubeupload.com/Chibameta/LBIcoFix.png"
            alt="לא פעיל בכוונה"><br>
          לוח הישגים</a>
      </div>
      <div class="icon">
        <a class="hide_link" href="report.php"><img src="http://u.cubeupload.com/Chibameta/RepIcoFix.png"
            alt="דיווחים"><br>
          דיווחים</a>
      </div>
    </section>
    <section class="progress">
      <span id="earned_money"></span>
      <div class="bar">
        <span id="prog_precen"></span>
      </div>
    </section>
  </main>
  <?php include 'footer.php';?>