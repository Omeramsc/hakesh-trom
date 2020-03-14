    function totalProgressImitation() {
        // This JS is meant to imitate a real-time senario, instead of using hard-coded numbers
        var earnedMoneyImitation = Math.floor(Math.random() * 1000) + 1;
        var progressImitation = Math.ceil(earnedMoneyImitation / 10);
        document.getElementById("earned_money").innerHTML = '₪' + 'סכום שנאסף: ' + earnedMoneyImitation;
        document.getElementById("prog_precen").style.width = progressImitation + '%';
        document.getElementById("prog_precen").innerHTML = progressImitation + '%';

        if (progressImitation > 80) {
            document.getElementById("prog_precen").style.backgroundColor = '#35d10d';
            if (progressImitation == 100) {
                window.onload = () => alert("הגעתם ליעד, כל הכבוד!");
            }
        }
    }

    function toggleSideNav() {
        var x = document.getElementById("hamburger");
        var fadedElements;
        var fadedElement1 = document.getElementById("main_layout");
        var fadedElement2 = document.getElementById("unified_footer");
        var fadedElement3 = document.getElementById("subtitle_container");
        if (getComputedStyle(x).width <= "1px") {
            x.style.width = "260px";
            fadedElement1.style.opacity = "0.2";
            fadedElement2.style.opacity = "0.2";
            fadedElement3.style.opacity = "0.2";
        } else {
            x.style.width = "0px";
            fadedElement1.style.opacity = "1";
            fadedElement2.style.opacity = "1";
            fadedElement3.style.opacity = "1";
        }
    }

    function sucessful_report() {
        alert("הדיווח התקבל בהצלחה! אנא המתן למענה מהאחראי");
        window.location.href = "report.php";
    }

    function version_error() {
        alert("פונקציה זו לא פעילה בגרסא הייעודית לקורס זה.");
    }

    function showSlides(currentSlideIndex) {
        let slideIndex = currentSlideIndex;
        const slides = document.getElementsByClassName("slide-container");

        for (const slide of slides) {
            slide.style.display = "none";
        }

        slideIndex++;

        if (slideIndex > slides.length) {
            slideIndex = 1;
        }

        slides[slideIndex - 1].style.display = "block";

        return slideIndex;
    }

    function donationValidation() {
        var payment = document.getElementsByName('payment');
        var x = parseInt(document.getElementById('donation').value, 10);
        var email = document.getElementById('emailInput').value;
        var isValid = true;
        var error_content = 'לא ניתן להשלים את התרומה:\n';
		
		
		if(email.trim().length === 0) {
			error_content += "* אנא הזן כתובת מייל תקינה.\n";
            isValid = false;
		}
        if (x == 0) {
            error_content += "* אנא הקש סכום הגבוה מאפס.\n";
            isValid = false;
        }
        if (!(payment[2].checked)) {
            error_content += "* בגרסא זו ניתן לשלם במזומן בלבד, אנא בחר באפשרות זו.\n";
            isValid = false;
        }
        if (isValid) {
            alert(' התקבלה תרומה על סך ' + x + ' ש"ח ' + '\n המשיכו כך!');
            // window.open('mailto:' + email); OPTIONAL if we want to send the email ourselvs
        } else {
            alert(error_content);
        }
		
		return isValid;
    }

    $(function activate_box() {
        $("#guide_box").dialog({
            modal: true,
            autoOpen: false,
            title: "<div style='padding: 0px 100px;'>אופן ביצוע התרומה<div>",
            width: 400,
            height: 500,
        });
        $("#btnShow").click(function () {
            $('#guide_box').dialog('open');
        });
    });

    (function donation() {
        'use strict';

        function ctrls() {
            var _this = this;

            this.counter = 0;
            this.els = {
                decrement: document.querySelector('.ctrl__button--decrement'),
                counter: {
                    container: document.querySelector('.ctrl__counter'),
                    num: document.querySelector('.ctrl__counter-num'),
                    input: document.querySelector('.ctrl__counter-input')
                },
                increment: document.querySelector('.ctrl__button--increment')
            };

            this.decrement = function () {
                var counter = _this.getCounter();
                var nextCounter = (_this.counter > 0) ? --counter : counter;
                _this.setCounter(nextCounter);
            };

            this.increment = function () {
                var counter = _this.getCounter();
                var nextCounter = (counter < 9999999999) ? ++counter : counter;
                _this.setCounter(nextCounter);
            };

            this.getCounter = function () {
                return _this.counter;
            };

            this.setCounter = function (nextCounter) {
                _this.counter = nextCounter;
            };

            this.debounce = function (callback) {
                setTimeout(callback, 100);
            };

            this.render = function (hideClassName, visibleClassName) {
                _this.els.counter.num.classList.add(hideClassName);

                setTimeout(function () {
                    _this.els.counter.num.innerText = _this.getCounter();
                    _this.els.counter.input.value = _this.getCounter();
                    _this.els.counter.num.classList.add(visibleClassName);
                }, 100);

                setTimeout(function () {
                    _this.els.counter.num.classList.remove(hideClassName);
                    _this.els.counter.num.classList.remove(visibleClassName);
                }, 200);
            };

            this.ready = function () {
                _this.els.decrement.addEventListener('click', function () {
                    _this.debounce(function () {
                        _this.decrement();
                        _this.render('is-decrement-hide', 'is-decrement-visible');
                    });
                });

                _this.els.increment.addEventListener('click', function () {
                    _this.debounce(function () {
                        _this.increment();
                        _this.render('is-increment-hide', 'is-increment-visible');
                    });
                });

                _this.els.counter.input.addEventListener('input', function (e) {
                    var parseValue = parseInt(e.target.value);
                    if (!isNaN(parseValue) && parseValue >= 0) {
                        _this.setCounter(parseValue);
                        _this.render();
                    }
                });

                _this.els.counter.input.addEventListener('focus', function (e) {
                    _this.els.counter.container.classList.add('is-input');
                });

                _this.els.counter.input.addEventListener('blur', function (e) {
                    _this.els.counter.container.classList.remove('is-input');
                    _this.render();
                });
            };
        };

        // init
        var controls = new ctrls();
        document.addEventListener('DOMContentLoaded', controls.ready);
    })();

    function onLoad() {
        let slideIndex = showSlides(0);

        setInterval(() => {
            slideIndex = showSlides(slideIndex)
        }, 5000); // 5 seconds
    }