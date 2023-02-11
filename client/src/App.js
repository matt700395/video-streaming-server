import React from "react"
import './App.css';
import LiveStream from './LiveStream';

function App() {
  return (
    <div className="App">
      <LiveStream streamUrl="rtmp://localhost:1935/live/abc123"/>
    </div>
  );
}

export default App;
