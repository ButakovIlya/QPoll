import { useEffect, useState } from 'react';

const Timer = ({ initialTime, onTimeEnd }) => {
  const parseTime = (timeString) => {
    const [hours, minutes, seconds] = timeString.split(':').map(Number);
    return hours * 3600 + minutes * 60 + seconds;
  };

  const formatTime = (time = timeInSeconds) => {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = time % 60;
    return [hours, minutes, seconds].map((val) => val.toString().padStart(2, '0')).join(':');
  };

  const [timeInSeconds, setTimeInSeconds] = useState(() => parseTime(initialTime));

  useEffect(() => {
    if (timeInSeconds === 0) {
      localStorage.removeItem('remainingTime');
      onTimeEnd();
      return;
    }

    const countdown = setInterval(() => {
      setTimeInSeconds((prevTime) => {
        const nextTime = Math.max(prevTime - 1, 0);
        localStorage.setItem('remainingTime', JSON.stringify(formatTime(nextTime)));
        return nextTime;
      });
    }, 1000);

    return () => {
      clearInterval(countdown);
      if (timeInSeconds > 0) {
        localStorage.setItem('remainingTime', JSON.stringify(formatTime(timeInSeconds)));
      }
    };
  }, [timeInSeconds]);

  return (
    <div style={{ position: 'sticky', top: 0, zIndex: 999, background: 'white', padding: '10px' }}>
      {formatTime()}
    </div>
  );
};

export default Timer;
