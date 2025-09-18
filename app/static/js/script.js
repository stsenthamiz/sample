const uploadBtn = document.getElementById('uploadBtn');
const imageUpload = document.getElementById('imageUpload');
const cameraBtn = document.getElementById('cameraBtn');
const captureBtn = document.getElementById('captureBtn');
const video = document.getElementById('cameraStream');
const processedImage = document.getElementById('processedImage');
const originalImage = document.getElementById('originalImage');
const traitsDiv = document.getElementById('traits');
const languageSelect = document.getElementById('languageSelect');

// Language labels
const labels = {
    en: { title: "Cattle & Buffalo Trait Analyzer", traits: "Body Traits", upload: "Upload Image", camera: "Use Camera", capture: "Capture" },
    ta: { title: "மாடு மற்றும் பசு உடல் பண்புகள் பகுப்பாய்வு", traits: "உடல் பண்புகள்", upload: "படத்தை ஏற்றவும்", camera: "கேமரா பயன்படுத்தவும்", capture: "பிடி" },
    hi: { title: "गाय और भैंस शरीर विशेषता विश्लेषक", traits: "शारीरिक लक्षण", upload: "छवि अपलोड करें", camera: "कैमरा इस्तेमाल करें", capture: "कैप्चर" }
};

// Change language
languageSelect.addEventListener('change', () => {
    const lang = languageSelect.value;
    document.getElementById('title').innerText = labels[lang].title;
    uploadBtn.innerText = labels[lang].upload;
    cameraBtn.innerText = labels[lang].camera;
    captureBtn.innerText = labels[lang].capture;
});

// Upload image
uploadBtn.addEventListener('click', () => {
    if(imageUpload.files.length === 0) return alert("Select an image!");
    const file = imageUpload.files[0];
    sendImage(file);
});

// Camera button
cameraBtn.addEventListener('click', () => {
    video.style.display = 'block';
    captureBtn.style.display = 'block';
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream)
        .catch(err => console.error(err));
});

// Capture button
captureBtn.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    canvas.toBlob((blob) => {
        sendImage(blob);
    });
});

// Send image to backend
function sendImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/predict', { method: 'POST', body: formData })
    .then(response => response.json())
    .then(data => {
        originalImage.src = data.original_image.replace("\\", "/");
        processedImage.src = data.processed_image.replace("\\", "/");
        displayTraits(data.prediction, data.confidence, data.body_traits);
    })
    .catch(err => console.error(err));
}

// Display body traits
function displayTraits(prediction, confidence, body_traits) {
    traitsDiv.innerHTML = <h3>${labels[languageSelect.value].traits}</h3>;
    let html = <p>Prediction: ${prediction} (${confidence.toFixed(2)}%)</p>;
    for(let key in body_traits){
        html += <p>${key}: ${body_traits[key]}</p>;
    }
    traitsDiv.innerHTML += html;
}