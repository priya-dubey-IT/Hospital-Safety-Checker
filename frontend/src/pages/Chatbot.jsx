import React, { useState, useEffect, useRef } from 'react';
import { toast } from 'react-toastify';
import { sendChatMessage, getChatHistory } from '../services/api';
import { FaRobot, FaPaperPlane, FaUser } from 'react-icons/fa';
import './Chatbot.css';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [sessionId] = useState(`session_${Date.now()}`);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Add welcome message
        setMessages([
            {
                type: 'bot',
                text: "Hello! I'm your Hospital Safety Checker assistant. I can help you with patient information, doctor details, appointment status, and hospital workflow. How can I assist you today?",
                timestamp: new Date().toISOString()
            }
        ]);

        // Load chat history
        loadHistory();
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const loadHistory = async () => {
        try {
            const response = await getChatHistory(sessionId);
            if (response.success && response.history.length > 0) {
                const historyMessages = response.history.flatMap(item => [
                    {
                        type: 'user',
                        text: item.user_message,
                        timestamp: item.timestamp
                    },
                    {
                        type: 'bot',
                        text: item.bot_response,
                        timestamp: item.timestamp
                    }
                ]);
                setMessages(prev => [...prev, ...historyMessages]);
            }
        } catch (error) {
            // Ignore history loading errors
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();

        if (!inputMessage.trim()) {
            return;
        }

        const userMessage = {
            type: 'user',
            text: inputMessage,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setLoading(true);

        try {
            const response = await sendChatMessage(inputMessage, sessionId);

            if (response.success) {
                const botMessage = {
                    type: 'bot',
                    text: response.response,
                    timestamp: response.timestamp
                };
                setMessages(prev => [...prev, botMessage]);
            }
        } catch (error) {
            toast.error('Failed to send message');
            const errorMessage = {
                type: 'bot',
                text: "Sorry, I'm having trouble processing your request. Please try again.",
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const formatMessageText = (text) => {
        // Convert markdown-style formatting to HTML
        return text
            .split('\n')
            .map((line, index) => {
                // Bold text
                line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

                // Headers
                if (line.startsWith('**') && line.endsWith('**')) {
                    return `<div key=${index} class="message-header">${line.replace(/\*\*/g, '')}</div>`;
                }

                return `<div key=${index}>${line || '<br/>'}</div>`;
            })
            .join('');
    };

    const quickQuestions = [
        "How do I register?",
        "How many patients are there?",
        "What's the verification process?",
        "Tell me about the dashboard"
    ];

    const handleQuickQuestion = (question) => {
        setInputMessage(question);
    };

    return (
        <div className="chatbot-page">
            <div className="page-header">
                <h1>AI Chatbot Assistant</h1>
                <p>Ask me anything about the hospital system</p>
            </div>

            <div className="chatbot-container">
                <div className="messages-container">
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.type}`}>
                            <div className="message-icon">
                                {message.type === 'bot' ? <FaRobot /> : <FaUser />}
                            </div>
                            <div className="message-content">
                                <div
                                    className="message-text"
                                    dangerouslySetInnerHTML={{ __html: formatMessageText(message.text) }}
                                />
                                <div className="message-time">
                                    {new Date(message.timestamp).toLocaleTimeString()}
                                </div>
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="message bot">
                            <div className="message-icon">
                                <FaRobot />
                            </div>
                            <div className="message-content">
                                <div className="typing-indicator">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {messages.length <= 1 && (
                    <div className="quick-questions">
                        <p className="quick-questions-label">Quick questions:</p>
                        <div className="quick-questions-grid">
                            {quickQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    className="quick-question-btn"
                                    onClick={() => handleQuickQuestion(question)}
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                <form onSubmit={handleSendMessage} className="chat-input-form">
                    <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Type your message..."
                        className="chat-input"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading || !inputMessage.trim()}
                    >
                        <FaPaperPlane />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Chatbot;
