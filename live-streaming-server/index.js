const express = require('express');
const SimpleWebRTC = require('simplewebrtc');
const cv = require('opencv4nodejs');
const ffmpeg = require('fluent-ffmpeg');

const app = express();
app.use(express.static(__dirname + '/public'));

const webcamPort = 0;
const cap = new cv.VideoCapture(webcamPort);

ffmpeg()
  .input(cap)
  .inputFormat('rawvideo')
  .outputFormat('vp9')
  .videoCodec('vp9')
  .audioCodec('opus')
  .outputOptions([
    '-deadline realtime',
    '-error-resilient 1'
  ])
  .output(function(stdout, stderr) {
    const webrtc = new SimpleWebRTC({
      localStream: stdout,
      remoteVideosEl: 'remote-videos',
      autoRequestMedia: false
    });

    webrtc.startLocalVideo();
    webrtc.connect('your-room-name');
  });

app.listen(3000, function () {
  console.log('WebRTC app listening on port 3000!');
});
