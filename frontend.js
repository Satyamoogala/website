// Frontend (JavaScript)
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Request access to the webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    video.play();
  })
  .catch(error => {
    console.error('Error accessing webcam:', error);
  });

// Send the video feed to the backend for analysis
setInterval(() => {
  ctx.drawImage(video)})