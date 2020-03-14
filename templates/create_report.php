<?php include 'header.php';?>
  <div id="subtitle_container">
    <h3>יצירת דיווח</h3>
  </div>
  <main id="main_layout" class="unified_layout">
    <form class="report_form" method="GET" action="post_report.php">
      <div class="form-group">
        <label for="inputAddress">*עיר:</label>
        <input type="text" class="form-control" id="inputAddress" placeholder="הכנס עיר" name="city" maxlength="25"
          required>
      </div>
      <div class="form-group">
        <label for="inputAddress">*כתובת:</label>
        <input type="text" class="form-control" id="inputAddress" placeholder="הכנס כתובת" name="address" maxlength="50"
          required>
      </div>
      <div class="form-group">
        <label for="inputAddress">*סוג הדיווח:</label>
        <select class="custom-select custom-select" name="type" required>
          <option selected disabled value="ללא סוג">בחר סוג...</option>
          <option value="מפגע">מפגע</option>
          <option value="רחוב חסום">רחוב חסום</option>
          <option value="כלב משוחרר">כלב משוחרר</option>
          <option value="תאונה">תאונה</option>
          <option value="הצפה">הצפה</option>
          <option value="בניין נעול">בניין נעול</option>
          <option value="אחר">אחר</option>
        </select>
      </div>
      <div class="form-group">
        <label for="exampleFormControlTextarea1">*תיאור:</label>
        <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder="תאר את המפגע"
          maxlength="300" name="description" required></textarea>
      </div>
      <div class="control_buttons">
        <button type="submit" class="btn btn-primary btn-lg btn-block">שלח</button>
        <a href="report.php"><button type="button" class="btn btn-secondary btn-lg btn-block">בטל</button></a>
      </div>
    </form>
  </main>
  <?php include 'footer.php';?>
