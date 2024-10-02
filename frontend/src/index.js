// import reportWebVitals from './reportWebVitals';
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);  // Create root for rendering the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
// reportWebVitals();