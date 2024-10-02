// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import FileUpload from "./components/FileUpload";
import QueryForm from "./components/QueryForm";
import "./App.css";

const App = () => {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<FileUpload />} />
                    <Route path="/query" element={<QueryForm />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
