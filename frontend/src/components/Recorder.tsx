import { useState, useRef } from 'react';

const Recorder = () => {
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
    }
  };

  const handleStopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  return (
    <div>
      <h2>🎙️ Recorder</h2>
      {recording ? (
        <button onClick={handleStopRecording}>⏹️ Stop Recording</button>
      ) : (
        <button onClick={handleStartRecording}>⏺️ Start Recording</button>
      )}

      {audioUrl && (
        <div style={{ marginTop: '1rem' }}>
          <h3>🎧 Recorded Audio</h3>
          <audio src={audioUrl} controls />
        </div>
      )}
    </div>
  );
};

export default Recorder;
