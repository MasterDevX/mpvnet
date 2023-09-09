let statusBar = document.getElementById("status-bar");
let btnVideoPlay = document.getElementById("video-play");
let btnAudioPlay = document.getElementById("audio-play");
let btnFitResoultion = document.getElementById("fit-resolution");
let btnVideoDownload = document.getElementById("video-download");
let btnAudioDownload = document.getElementById("audio-download");
let inputResolution = document.getElementById("input-resolution");

function updateStatus (status, color) {
    statusBar.innerText = status;
    statusBar.style.color = color;
}

function runLoader (cmdline) {
    updateStatus("Running command", "#3dc200")
    chrome.tabs.query({
        active: true,
        lastFocusedWindow: true
    }, function (tabs) {
        var url = tabs[0].url;
        var port = chrome.runtime.connectNative("com.mpvnet.loader");
        port.onMessage.addListener(function (msg) {
            if (msg.text == "return_normal") {
                updateStatus("Ready", "#3dc200")
            }
            if (msg.text == "return_error_invalid_url") {
                updateStatus("Invalid URL", "#ff455e");
            }
            port.disconnect();
            return;
        });
        port.onDisconnect.addListener(function() {
            updateStatus("Internal loader error", "#ff455e");
            return;
        });
        port.postMessage({ text: cmdline + url });
    });
}

function fitResolution () {
    if (inputResolution.value != "") {
        if (isNaN(inputResolution.value) || inputResolution.value < 1) {
            updateStatus("Invalid resolution limit", "#ff455e");
            return null;
        }
        return `[height<=${inputResolution.value}]`
    }
    return "";
}

btnFitResoultion.addEventListener("click", () => {
    var hReal = Math.round(window.devicePixelRatio * screen.height);
    inputResolution.value = hReal;
    updateStatus("Display resolution read", "#3dc200")
});

btnVideoPlay.addEventListener("click", () => {
    var hLimit = fitResolution();
    if (hLimit === null) return;
    var cmdline = `mpv video bv${hLimit}+ba/b${hLimit} `;
    runLoader(cmdline);
});

btnAudioPlay.addEventListener("click", () => {
    var cmdline = "mpv audio ba/b ";
    runLoader(cmdline);
});

btnVideoDownload.addEventListener("click", () => {
    var hLimit = fitResolution();
    if (hLimit === null) return;
    var cmdline = `ydl video bv${hLimit}+ba/b${hLimit} `;
    runLoader(cmdline);
});

btnAudioDownload.addEventListener("click", () => {
    var cmdline = "ydl audio ba/b ";
    runLoader(cmdline);
});

updateStatus("Ready", "#3dc200")