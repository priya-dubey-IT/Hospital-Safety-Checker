import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { FaCamera, FaRedo, FaUpload } from 'react-icons/fa';
import './WebcamCapture.css';

const WebcamCapture = ({ onCapture, label = "Capture Photo" }) => {
    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);
    const [isCameraOn, setIsCameraOn] = useState(false);
    const fileInputRef = useRef(null);

    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user"
    };

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc);
        setIsCameraOn(false); // Turn off camera after capture
        if (onCapture) {
            onCapture(imageSrc);
        }
    }, [webcamRef, onCapture]);

    const retake = () => {
        setImgSrc(null);
        // Do not automatically turn on camera, let user choose again
        if (onCapture) {
            onCapture(null);
        }
    };

    const toggleCamera = () => {
        setIsCameraOn(!isCameraOn);
        if (isCameraOn) {
            setImgSrc(null);
            if (onCapture) {
                onCapture(null);
            }
        }
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result;
                setImgSrc(base64String);
                setIsCameraOn(false); // Ensure camera is off
                if (onCapture) {
                    onCapture(base64String);
                }
            };
            reader.readAsDataURL(file);
        }
    };

    const triggerFileUpload = () => {
        fileInputRef.current.click();
    };

    return (
        <div className="webcam-container">
            <label className="form-label">{label}</label>

            {!isCameraOn && !imgSrc && (
                <div className="capture-options">
                    <button
                        type="button"
                        className="btn btn-secondary w-full mb-2"
                        onClick={toggleCamera}
                    >
                        <FaCamera /> Turn On Camera
                    </button>

                    <div className="separator text-center my-2">OR</div>

                    <button
                        type="button"
                        className="btn btn-outline-primary w-full"
                        onClick={triggerFileUpload}
                    >
                        <FaUpload /> Upload Image
                    </button>
                    <input
                        type="file"
                        accept="image/*"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        style={{ display: 'none' }}
                    />
                </div>
            )}

            {isCameraOn && !imgSrc && (
                <div className="webcam-wrapper">
                    <Webcam
                        audio={false}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        videoConstraints={videoConstraints}
                        className="webcam-video"
                    />
                    <div className="webcam-controls">
                        <button
                            type="button"
                            className="btn btn-primary"
                            onClick={capture}
                        >
                            <FaCamera /> Capture
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={toggleCamera}
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}

            {imgSrc && (
                <div className="webcam-preview">
                    <img src={imgSrc} alt="Captured" className="captured-image" />
                    <button
                        type="button"
                        className="btn btn-secondary mt-2"
                        onClick={retake}
                    >
                        <FaRedo /> Retake / Upload New
                    </button>
                </div>
            )}
        </div>
    );
};

export default WebcamCapture;
