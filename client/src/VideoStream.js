import React, { useState } from 'react';

const VideoStream = () => {
  const [videoSrc, setVideoSrc] = useState('http://localhost:5000');

  return (
    <div>
      <iframe width="1280" height="720" src={videoSrc} />
    </div>
  );
};

export default VideoStream;
