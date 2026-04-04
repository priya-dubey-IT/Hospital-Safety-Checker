import React, { useState, useEffect } from 'react';

const LiveTimer = ({ startTime }) => {
    const [duration, setDuration] = useState('00:00:00');

    useEffect(() => {
        const calculateDuration = () => {
            if (!startTime) return;

            // Ensure startTime is treated as UTC if it doesn't have timezone info
            // But since we updated backend to add 'Z', new Date(startTime) should work correctly
            const start = new Date(startTime).getTime();
            const now = new Date().getTime();

            // Difference in milliseconds
            let diff = now - start;

            // If negative (clock skew), show 0
            if (diff < 0) diff = 0;

            const seconds = Math.floor((diff / 1000) % 60);
            const minutes = Math.floor((diff / (1000 * 60)) % 60);
            const hours = Math.floor((diff / (1000 * 60 * 60)));

            const paddedHours = hours.toString().padStart(2, '0');
            const paddedMinutes = minutes.toString().padStart(2, '0');
            const paddedSeconds = seconds.toString().padStart(2, '0');

            setDuration(`${paddedHours}:${paddedMinutes}:${paddedSeconds}`);
        };

        // Update immediately
        calculateDuration();

        // Update every second
        const interval = setInterval(calculateDuration, 1000);

        return () => clearInterval(interval);
    }, [startTime]);

    return (
        <span className="live-timer" style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>
            Waiting: {duration}
        </span>
    );
};

export default LiveTimer;
