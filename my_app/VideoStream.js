import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';

const VideoStream = () => {
  const [videoSrc, setVideoSrc] = useState('http://localhost:5000/video_feed');

  return (
    <WebView
      source={{html: `<div>
                        <iframe width="1280" height="720" src=${videoSrc} />
                      </div>`}}
    />
  );
};

export default VideoStream;
