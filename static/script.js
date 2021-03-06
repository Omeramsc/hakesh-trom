// about_org's slide show:
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

function onLoad() {
    let slideIndex = showSlides(0);

    setInterval(() => {
        slideIndex = showSlides(slideIndex)
    }, 5000); // 5 seconds
}

// Donation's donation box&buttons:
function donation() {
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
}

function ShowPayPalSuccessMessage() {
    const parent = document.getElementsByClassName('hidden')[0];
    parent.innerHTML = '<div id="modal-content" class="report_modal" style="text-align: center;direction: rtl;"><h3>PayPal</h3><div>תשלום ה-PayPal התקבל בהצלחה!</div><a href="#close" rel="modal:close"><button class="btn btn-secondary">סגור</button></a></div>';
    $('#modal-content').modal({
        escapeClose: true,
        clickClose: true,
        showClose: false
    })
}

function ShowWelcomeMessage(team_url, team_id) {
    const parent = document.getElementsByClassName('hidden')[0];
    parent.innerHTML = '<div id="modal-content" class="report_modal" style="text-align: center;direction: rtl;"><h3>ברוכים הבאים צוות ' + team_id + '</h3><div>אנו מזמינים אתכם לעדכן את פרטי הצוות ולבחור לעצמכם כינוי!</div><a href="' + team_url + '"><button class="btn btn-primary" style="margin: 2px;">לעמוד הצוות</button></a><a href="#close" rel="modal:close"><button class="btn btn-secondary">סגור</button></a></div>';
    $('#modal-content').modal({
        escapeClose: true,
        clickClose: true,
        showClose: false
    })
}
