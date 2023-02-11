import Video from 'react-native-video';

const Videos = () => {
    return (
        <Video  
            source={{ url: 'http://localhost:5000'}}                  // the video file
            paused={false}                  // make it start    
        />
    )
}