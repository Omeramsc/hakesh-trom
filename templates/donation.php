<?php include 'header.php';?>
  <div id="subtitle_container">
    <h3>תרומה</h3>
  </div>
  <main id="main_layout" class="unified_layout">
    <button class="guide_btn" id="btnShow"><i class="fa fa-question-circle-o"></i></button>
    <div id="guide_box">
      <p>
        <p>
          <strong>שלב 1: הזנת סכום התרומה</strong><br>
          באפשרותך להזין את סכום התרומה המבוקש באמצעות לחיצה על כפתור ה"+" וה"-", או לחלופין על-ידי הקשה על חלונית הסכום
          והקשת המספר
        </p>
        <p>
          <strong>שלב 2: בחירת אמצעי התשלום</strong><br>
          ניתן לבחור את אמצעי התשלום המבוקר באמצעות לחיצה על העיגול הנמצא מתחת לאמצעי התשלום.<br>
          שימו לב: בגרסא זו של המערכת, מזומן הינו אמצעי התשלום היחיד שפעיל
        </p>
        <p>
          <strong>שלב 3: שליחת חשבונית</strong><br>
          יש להקיש על חלונית האימייל ולהזין את כתובת האימייל של המתרים, כך שהקבלה תשלח מיידית לכתובת זו
        </p>
        <p>
          <strong>שלב 4: השלמת התהליך</strong><br>
          בכדי לאשר סופית את מתן התרומה, יש ללחוץ על כפתור "סיים"
        </p>
        <strong>ניתן לקבל סיוע או הדרכה נוספת דרך כפתור "צור קשר" בעמוד הדיווחים</strong>
      </p>
    </div>
    <form style="all:unset" onsubmit="return donationValidation()" action="index.php">
      <section class='ctrl flex_me center_text'>
        <div class=' ctrl__button--increment'>+</div>
        <div class='ctrl__counter'>
          <input class='ctrl__counter-input center_text' id="donation" name="donation" maxlength='7' type='text' value='0'>
          <div class='ctrl__counter-num'>0</div>
        </div>
        <div class=' ctrl__button--decrement'>&ndash;</div>
      </section>
      <section class="payment_choice flex_me center_text">
        <div class="payment_option">
          <img class="not_allowed" src="http://u.cubeupload.com/Chibameta/payplIcoFix.png" alt="לא פעיל בכוונה"><br>
          <input type="radio" name="payment" value="paypal"> PayPal
        </div>
        <div class="payment_option">
          <img class="not_allowed" src="http://u.cubeupload.com/Chibameta/CreditCardFix.png" alt="לא פעיל בכוונה"><br>
          <input type="radio" name="payment" value="credit"> אשראי
        </div>
        <div class="payment_option">
          <img src="http://u.cubeupload.com/Chibameta/mnymzumniIcoFix.png" alt="תשלום במזומן"> <br>
          <input type="radio" name="payment" value="cash"> מזומן
        </div>
        <div class="payment_option">
          <img class="not_allowed" src="http://u.cubeupload.com/Chibameta/BITicoFIx.png" alt="לא פעיל בכוונה"><br>
          <input type="radio" name="payment" value="bit"> bit
        </div>
      </section>
      <section id="mail" class="center_text">
        *כתובת מייל למשלוח קבלה:<br>
        <input type="email" name="email" id="emailInput"><br>
      </section>
      <a class="finish_btn flex_me" href="#">
        <button type=submit class="btn btn-primary btn-lg" type="button">סיים</button> </a>
    </form>
  </main>
  <script>
    donation();
    activate_box();
  </script>
<?php include 'footer.php';?>