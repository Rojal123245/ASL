function setupASLTool() {
    const imageUpload = document.getElementById('imageUpload');
      const videoUpload = document.getElementById('videoUpload');
      const previewSection = document.getElementById('previewSection');
      const cancelButtons = document.getElementById('cancelButtons');
      const webcamButton = document.getElementById('webcamButton');
      const captureButton = document.getElementById('captureButton');
      const webcamPreview = document.getElementById('webcamPreview');

      let mediaStream = null;
      let imageCapture = null;


    imageUpload.addEventListener('change', handleImageUpload);
      videoUpload.addEventListener('change', handleVideoUpload);
      webcamButton.addEventListener('click', enableWebcam);
      captureButton.addEventListener('click', captureImage);

      webcamButton.addEventListener('click', enableWebcam);



    function handleImageUpload(event) {
previewSection.innerHTML = ''; // Clear previous previews

for (let i = 0; i < event.target.files.length; i++) {
  const file = event.target.files[i];
  const imgContainer = document.createElement('div');
  imgContainer.classList.add('preview-image');
  const img = document.createElement('img');
  img.src = URL.createObjectURL(file);
  img.classList.add('uploaded-image');
  const cancelButton = document.createElement('button');
  cancelButton.classList.add('cancel-button');
  cancelButton.innerHTML = '✖';
  cancelButton.addEventListener('click', function() {
    imgContainer.remove();
  });
  imgContainer.appendChild(img);
  imgContainer.appendChild(cancelButton);
  previewSection.appendChild(imgContainer);
}

// Show cancel buttons
cancelButtons.style.display = 'block';
}

function handleVideoUpload(event) {
previewSection.innerHTML = ''; // Clear previous previews

for (let i = 0; i < event.target.files.length; i++) {
  const file = event.target.files[i];
  const videoContainer = document.createElement('div');
  videoContainer.classList.add('preview-video');
  const video = document.createElement('video');
  video.src = URL.createObjectURL(file);
  video.classList.add('uploaded-video');
  video.setAttribute('controls', true);
  const cancelButton = document.createElement('button');
  cancelButton.classList.add('cancel-button');
  cancelButton.innerHTML = '✖';
  cancelButton.addEventListener('click', function() {
    videoContainer.remove();
  });
  videoContainer.appendChild(video);
  videoContainer.appendChild(cancelButton);
  previewSection.appendChild(videoContainer);
}

// Show cancel buttons
cancelButtons.style.display = 'block';
}
function enableWebcam() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
          .then(function (stream) {
              mediaStream = stream;
              webcamPreview.srcObject = stream;
              const track = stream.getVideoTracks()[0];
              imageCapture = new ImageCapture(track);
          })
          .catch(function (error) {
              console.error('Error accessing webcam: ', error);
          });
  } else {
      console.error('Webcam access not supported');
  }
}
function captureImage() {
  if (mediaStream && imageCapture) {
      imageCapture.takePhoto()
          .then(function (blob) {
              const imageUrl = URL.createObjectURL(blob);
              const imageElement = document.createElement('img');
              imageElement.src = imageUrl;
              imageElement.classList.add('captured-image');
              const imagePreviews = document.getElementById('imagePreviews');
              imagePreviews.appendChild(imageElement);
          })
          .catch(function (error) {
              console.error('Error capturing image: ', error);
          });
  } else {
      console.error('Webcam not enabled');
  }
}
// Disable Button
const disableButton = document.getElementById('disableButton');
disableButton.addEventListener('click', disableASLTool);

function disableASLTool() {
  
  // Close the webcam and release media resources
  if (mediaStream) {
      mediaStream.getTracks().forEach(function (track) {
          track.stop();
      });
      mediaStream = null;
      imageCapture = null;
      webcamPreview.srcObject = null;
  }
}

// Predict Button
const predictButton = document.getElementById('predictButton');
predictButton.addEventListener('click', predictASL);

function predictASL() {
  // Get the uploaded images and videos
  const imageFiles = Array.from(document.getElementById('imageUpload').files);
  const videoFiles = Array.from(document.getElementById('videoUpload').files);

  // Perform prediction using the AI language model
  const predictionResult = performPrediction(imageFiles, videoFiles);

  // Display the result in the result section
  const resultSection = document.getElementById('resultSection');
  resultSection.innerHTML = `<h2>Result</h2><p>${predictionResult}</p>`;
}

function performPrediction(images, videos) {
  // Implement your logic to perform prediction using the uploaded images and videos
  // Here, you can interact with the AI language model to generate a prediction result
  // You can use the 'images' and 'videos' arrays to access the uploaded files

  // Example: Return a dummy prediction result
  return "This is the prediction result.";
}

      

      
      
  }

  // Call the setupASLTool function after the document is loaded
  document.addEventListener('DOMContentLoaded', setupASLTool);