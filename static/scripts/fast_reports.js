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
    const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=AIzaSyCeQSgOmTLHNxGk4Vg3JlTNCGD8BEO992Y&language=iw`;
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
        const recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "he-IL"; // spoken language: hebrew
        ChangeRecordIconToInProgress();
        recognition.start();

        // If voice recognition succeeded
        recognition.onresult = function (e) {
            const {transcript} = e.results[0][0];
            recognition.stop();
            ChangeRecordIconToStopped()
            submitQuickReport(transcript, address, csrfToken, createUrl);
        };

        // If voice recognition failed (for example: no voice at all)
        recognition.onerror = function (e) {
            recognition.stop();
            handleTextToSpeechError();
        }
        // If voice recognition is not available on the device
    } else {
        handleTextToSpeechError();
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
        handleTextToSpeechError();
    }
}

function handleTextToSpeechSuccess(responseJson) {
    const parent = document.getElementsByClassName('hidden')[0];
    const report_url = "/reports/view_report/-1".replace('-1', responseJson['id']);
    parent.innerHTML = '<div id="modal-content" style="text-align: center;direction: rtl;height:20%"><h3>הדיווח נשמר!</h3><div>הדיווח הקולי נשמר בהצלחה!</div><div><a href="' + report_url + '"><button class="btn btn-primary" style="margin: 2px;">צפייה בדיווח</button></a><a href="#close" rel="modal:close"><button class="btn btn-secondary">סגור</button></a>';
    $('#modal-content').modal({
        escapeClose: true,
        clickClose: true,
        showClose: false
    })

}

function handleTextToSpeechError() {
    ChangeRecordIconToStopped()
    const parent = document.getElementsByClassName('hidden')[0];
    parent.innerHTML = '<div id="modal-content" style="text-align: center;direction: rtl; height:20%"><h3>אופס...</h3><div>התרחשה שגיאה, אנא נסה/י שוב במועד מאוחר יותר</div><a href="#close" rel="modal:close"><button class="btn btn-secondary">סגור</button></a>';
    $('#modal-content').modal({
        escapeClose: true,
        clickClose: true,
        showClose: false
    })
}