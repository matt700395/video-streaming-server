import React, { useState, useEffect } from 'react';
import Hls from 'hls.js';

function HLSVideoPlayer({ streamUrl }) {
  const [videoRef, setVideoRef] = useState(null);

  useEffect(() => {
    if (Hls.isSupported() && videoRef) {
      const hls = new Hls();
      hls.loadSource(streamUrl);
      hls.attachMedia(videoRef);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        videoRef.play();
      });
    }
  }, [streamUrl, videoRef]);

  return (
    <video
      ref={(video) => setVideoRef(video)}
      controls
      autoPlay
    />
  );
}

export default HLSVideoPlayer;
