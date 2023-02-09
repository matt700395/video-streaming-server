import './App.css';
import HLSVideoPlayer from './HLSVideoPlayer';

function App() {
  return (
    <div className="App">
      <HLSVideoPlayer streamUrl="http://localhost:8000/live/abc123.m3u8"/>
    </div>
  );
}

export default App;
