<?php include 'header.php';?>
  <div id="subtitle_container">
    <h3>דיווחים</h3>
  </div>
  <main id="main_layout" class="unified_layout">

    <section class="options flex_me center_text">
      <div class="option_button">
        <a class="hide_link not_allowed" href=#><img src="http://u.cubeupload.com/Chibameta/ContactusIco.png"
            alt="לא פעיל בכוונה"><br>
          צור קשר
        </a>
      </div>
      <div class="option_button">
        <a class="hide_link" href=create_report.php><img src="http://u.cubeupload.com/Chibameta/CreateNewIco1.png"><br>
          צור דיווח
        </a>
      </div>
    </section>
    <section class="boxes_container flex_me">
      <section id="search" class="box">
        <h3 class=center_text> <u>חיפוש דיווחים:</u></h3>
        <form>
          <div class="form-row">
            <div class="col-md-8 mb-3">
              <label for="validationDefault01">עיר</label>
              <input type="text" class="form-control" id="validationDefault03">
            </div>
          </div>
          <div class="form-row">
            <div class="col-md-8 mb-3">
              <label for="validationDefault03">כתובת</label>
              <input type="text" class="form-control" id="validationDefault03">
            </div>
          </div>
          <div class="form-row">
            <div class="col-md-8 mb-3">
              <label for="validationDefault04">סוג הדיווח</label>
              <select class="custom-select" id="validationDefault04">
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
          </div>
          <div class="form-group">
            <div class="custom-control custom-radio custom-control-inline">
              <input type="radio" id="customRadioInline1" name="customRadioInline1" class="custom-control-input">
              <label class="custom-control-label" for="customRadioInline1">טופל</label>
            </div>
            <div class="custom-control custom-radio custom-control-inline">
              <input type="radio" id="customRadioInline2" name="customRadioInline1" class="custom-control-input">
              <label class="custom-control-label" for="customRadioInline2">לא טופל</label>
            </div>
          </div>
          <button class="btn btn-primary btn-lg" onclick=version_error() style="width: 66%;" type="submit">בצע חיפוש</button>
        </form>
      </section>
      <section id="report_list" class="box">
        <ul>
        <?php include 'show_reports.php';?>
        </ul>
      </section>
  </main>
  <?php include 'footer.php';?>

