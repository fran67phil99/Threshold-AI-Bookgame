import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import { Bar } from 'react-chartjs-2';
import { Chart, BarElement, CategoryScale, LinearScale } from 'chart.js';
Chart.register(BarElement, CategoryScale, LinearScale);

function RelationshipChart({ data }) {
  const chartData = {
    labels: Object.keys(data.relationships),
    datasets: [
      {
        label: 'Relazione (-1 ostilità, 1 alleanza)',
        data: Object.values(data.relationships),
        backgroundColor: ['#00adb5', '#f8b400', '#ff2e63'],
      },
    ],
  };
  return <Bar data={chartData} options={{ scales: { y: { min: -1, max: 1 } } }} />;
}

function UserTensionChart({ data }) {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Tensione utente-agente (-1 ostilità, 1 alleanza)',
        data: Object.values(data),
        backgroundColor: ['#00adb5', '#f8b400', '#ff2e63'],
      },
    ],
  };
  return <Bar data={chartData} options={{ scales: { y: { min: -1, max: 1 } } }} />;
}

function App() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const [lore, setLore] = useState('');
  const chatEndRef = useRef(null);
  const [relData, setRelData] = useState({ relationships: {}, tension: 0 });
  const [userTension, setUserTension] = useState({ Gaia: 0, Prometheus: 0, Syra: 0 });

  // Carica la lore comune all'avvio e dopo ogni messaggio
  const fetchLore = async () => {
    const res = await fetch('http://localhost:5000/api/lore');
    const data = await res.json();
    setLore(data.lore);
  };

  const fetchRelationships = async () => {
    const res = await fetch('http://localhost:5000/api/relationships');
    const data = await res.json();
    setRelData(data);
  };

  const fetchUserTension = async () => {
    const res = await fetch('http://localhost:5000/api/user_tension');
    const data = await res.json();
    setUserTension(data);
  };

  useEffect(() => {
    fetchLore();
    fetchRelationships();
    fetchUserTension();
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) return;
    setChat(prev => [...prev, { sender: 'Tu', text: message }]);
    const res = await fetch('http://localhost:5000/api/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    const agentMessages = Object.entries(data).map(([agent, text]) => ({
      sender: agent,
      text,
    }));
    setChat(prev => [...prev, ...agentMessages]);
    setMessage('');
    fetchLore(); // aggiorna la lore dopo ogni messaggio
    fetchRelationships();
    fetchUserTension();
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  return (
    <div className="container">
      <h1>🤖 Threshold AI Bookgame</h1>
      <div className="lore-area">
        <h2>Lore comune</h2>
        <div className="lore-text">{lore}</div>
      </div>
      <div className="chat-area">
        {chat.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === 'Tu' ? 'user' : 'agent'} agent-${msg.sender.toLowerCase()}`}
          >
            <span className="chat-sender">{msg.sender}:</span>
            <span className="chat-text">{msg.text}</span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div className="input-area">
        <input
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Scrivi un messaggio agli agenti..."
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Invia</button>
      </div>
      <div className="chart-area">
        <h2>Relazioni tra agenti</h2>
        <RelationshipChart data={relData} />
        <div>Grado di tensione: <b>{relData.tension.toFixed(2)}</b></div>
        <h2>Tensione utente-agente</h2>
        <UserTensionChart data={userTension} />
      </div>
    </div>
  );
}

export default App;