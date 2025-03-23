import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(new Audio());

  const trackList = [
    {
      name: "it kills me",
      artist: "dxmentia",
      src: "/audio/it kills me.mp3",
      image: "/images/it kills me.jpeg",
    },
    {
      name: "LIMBO",
      artist: "keshi",
      src: "/audio/LIMBO.mp3",
      image: "/images/limbo.jpeg",
    },
    {
      name: "Soft Spot",
      artist: "keshi",
      src: "/audio/Soft Spot.mp3",
      image: "/images/soft spot.jpeg",
    },
  ];

  // Load & Play track when currentTrackIndex changes
  useEffect(() => {
    audioRef.current.src = trackList[currentTrackIndex].src;
    audioRef.current.load();

    audioRef.current.onloadedmetadata = () => {
      setDuration(audioRef.current.duration);
    };

    if (isPlaying) {
      audioRef.current.play();
    }

    // Update current time as the song plays
    audioRef.current.ontimeupdate = () => {
      setCurrentTime(audioRef.current.currentTime);
    };
  }, [currentTrackIndex]);

  // Play or pause track
  const playPauseTrack = () => {
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  // Next track
  const nextTrack = () => {
    setCurrentTrackIndex((prevIndex) =>
      prevIndex + 1 < trackList.length ? prevIndex + 1 : 0
    );
  };

  // Previous track
  const prevTrack = () => {
    setCurrentTrackIndex((prevIndex) =>
      prevIndex - 1 >= 0 ? prevIndex - 1 : trackList.length - 1
    );
  };

  // Seek to a new position when slider is moved
  const seekTo = (e) => {
    const newTime = e.target.value;
    audioRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  // Format time (mm:ss)
  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

  return (
    <>
      <h1>Music Player</h1>
      <div className="player">
        <div className="now-playing">Playing: {trackList[currentTrackIndex].name}</div>
        
        {/* Album Cover */}
        <div className="album-cover">
          <img src={trackList[currentTrackIndex].image} alt="Album Cover" />
        </div>

        <div className="details">
          <div className="track-name">{trackList[currentTrackIndex].name}</div>
          <div className="track-artist">{trackList[currentTrackIndex].artist}</div>
        </div>


        <div className="buttons">
          <div className="prev-track" onClick={prevTrack}>
            <i className="fa fa-step-backward fa-2x"></i>
          </div>
          <div className="playpause-track" onClick={playPauseTrack}>
            <i className={`fa ${isPlaying ? "fa-pause-circle" : "fa-play-circle"} fa-5x`}></i>
          </div>
          <div className="next-track" onClick={nextTrack}>
            <i className="fa fa-step-forward fa-2x"></i>
          </div>
        </div>

        {/* Progress Slider */}
        <div className="slider_container">
          <span className="current-time">{formatTime(currentTime)}</span>
          <input
            type="range"
            min="0"
            max={duration}
            value={currentTime}
            className="seek_slider"
            onChange={seekTo}
          />
          <span className="total-duration">{formatTime(duration)}</span>
        </div>

        {/* Volume Slider */}
        <div className="slider_container">
          <i className="fa fa-volume-down"></i>
          <input
            type="range"
            min="0"
            max="100"
            defaultValue="99"
            className="volume_slider"
            onChange={(e) => (audioRef.current.volume = e.target.value / 100)}
          />
          <i className="fa fa-volume-up"></i>
        </div>
      </div>
    </>
  );
}

export default App;
