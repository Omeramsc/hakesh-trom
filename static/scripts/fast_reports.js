async function createFastReport(csrfToken, createUrl) {
    const address = await getCurrentAddress();
    recordAndPostQuickReport(address, csrfToken, createUrl);
}

function getCurrentAddress() {
    return new Promise(function (resolve) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => handleCurrentPosition(position, resolve), () => resolve('שירותי המיקום לא פעילים'));
        } else {
            resolve('שירותי המיקום לא פעילים');
        }
    })
}

async function handleCurrentPosition(position, resolve) {
    const {latitude, longitude} = position.coords;
    const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=AIzaSyB8k9cPqYxYcm-6RjRlB0BJnCsPaFDQAAY&language=iw`;
    try {
        const response = await fetch(url, {method: 'GET'});

        if (response.ok) {
            const responseJson = await response.json();
            const address = responseJson.results[0].formatted_address.split(",")[0].trim();
            resolve(address);
        }
        resolve('לא ניתן לאתר מיקום');
    } catch (e) {
        resolve('לא ניתן לאתר מיקום');
    }
}

function ChangeRecordIconToStopped() {
    const icons = document.getElementsByClassName('reco_icon');
    for (var i = 0; i < icons.length; i++) {
        icons[i].src = "/static/fast_report.png";
    }
}

function ChangeRecordIconToInProgress() {
    const icons = document.getElementsByClassName('reco_icon');
    for (var i = 0; i < icons.length; i++) {
        icons[i].src = "/static/fast_report_recording.png";
    }
}

function recordAndPostQuickReport(address, csrfToken, createUrl) {
    if (window.hasOwnProperty('webkitSpeechRecognition')) { // WHEN I DIDN'T USE WEBKIT IT RETURNED FALSE!
        const recognition = window.currentRecognition || new webkitSpeechRecognition();

        if (window.isUserRecording) {
            // The user is already recording, aborting the recording
            recognition.abort();
            ChangeRecordIconToStopped();
            window.isUserRecording = false;
            return;
        }

        window.currentRecognition = recognition;

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "he-IL"; // spoken language: hebrew
        ChangeRecordIconToInProgress();
        window.isUserRecording = true;
        recognition.start();

        // If voice recognition succeeded
        recognition.onresult = function (e) {
            window.isUserRecording = false;
            const {transcript} = e.results[0][0];
            recognition.stop();
            ChangeRecordIconToStopped()
            showLoading(transcript);
            submitQuickReport(transcript, address, csrfToken, createUrl);
        };

        // If voice recognition failed (for example: no voice at all)
        recognition.onerror = function (e) {
            window.isUserRecording = false;
            if (e.error === "aborted") {
                // Not a problem at all!
                return;
            }

            recognition.stop();
            handleTextToSpeechError();
        }
        // If voice recognition is not available on the device
    } else {
        handleTextToSpeechError("שירותי ההקלטה אינם מאושרים או קיימים במכשיר זה, או שהינך משתמש בדפדפן שאינו נתמך.");
    }
}

async function submitQuickReport(transcript, address, csrfToken, createUrl) {
    const response = await fetch(createUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({transcript, address})
    });
    if (response.ok) {
        const responseJson = await response.json();
        handleTextToSpeechSuccess(responseJson);
    } else {
        //error in SENDING the report
        handleTextToSpeechError("התרחשה שגיאה במהלך שליחת הדיווח. אנא נסה/י שוב במועד מאוחר יותר");
    }
}

function handleTextToSpeechSuccess(responseJson) {
    const parent = document.getElementsByClassName('hidden')[0];
    const report_url = "/reports/view_report/-1".replace('-1', responseJson['id']);
    parent.innerHTML = '<div id="modal-content" class="report_modal" style="text-align: center;direction: rtl;"><h3>הדיווח נשמר!</h3><div>הדיווח הקולי נשמר בהצלחה!</div><div><a href="' + report_url + '"><button class="btn btn-primary" style="margin: 2px;">צפייה בדיווח</button></a><a href="#close" rel="modal:close"><button class="btn btn-secondary">סגור</button></a></div>';
    $('#modal-content').modal({
        escapeClose: true,
        clickClose: true,
        showClose: false
    })
}

function handleTextToSpeechError(errorInfo = "התרחשה שגיאה, אנא נסה/י שוב במועד מאוחר יותר") {
    ChangeRecordIconToStopped()
    const parent = document.getElementsByClassName('hidden')[0];
    parent.innerHTML = '<div id="modal-content" class="report_modal" style="text-align: center;direction: rtl;"><h3>אופס...</h3><div>' + errorInfo + '</div><a href="#close" rel="modal:close"><button class="btn btn-secondary">סגור</button></a></div>';
    $('#modal-content').modal({
        escapeClose: true,
        clickClose: true,
        showClose: false
    })
}

function showLoading(transcript) {
    const parent = document.getElementsByClassName('hidden')[0];
    parent.innerHTML = `<div id="modal-content" class="report_modal" style="text-align: center;direction: rtl;"><h3>שולח דיווח</h3>שולח את הדיווח הבא: <br/><p>${transcript}</p></div>`;
    $('#modal-content').modal({
        escapeClose: false,
        clickClose: false,
        showClose: false
    })
}