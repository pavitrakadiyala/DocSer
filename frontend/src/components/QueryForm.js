import React, { useState } from "react";
import "./QueryForm.css";

const QueryForm = () => {
    const [query, setQuery] = useState("");
    const [answer, setAnswer] = useState("");
    const [documents, setDocuments] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch("http://localhost:5000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query }),
            });

            if (response.ok) {
                const data = await response.json();
                setAnswer(data.answer);
                setDocuments(data.documents);
            } else {
                setAnswer("Error fetching answer.");
                setDocuments([]);
            }
        } catch (error) {
            console.error("Error:", error);
            setAnswer("Error fetching answer.");
            setDocuments([]);
        }
    };

    return (
        <div className="container">
            <div className="query-form-container">
                <h2>Query Documents</h2>
                <form onSubmit={handleSubmit} className="query-form">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Ask a question"
                        className="query-input"
                    />
                    <button type="submit" className="submit-button">Submit</button>
                </form>

                <h3>Answer:</h3>
                <p className="answer-text">{answer}</p>

                <div className="document-cards">
                    {documents.map((doc, index) => (
                        <div key={index} className="document-card">
                            <h4>Document {index + 1}</h4>
                            <p><strong>Source:</strong> {doc.metadata.source}</p>
                            <p><strong>Page Number:</strong> {doc.metadata.page_number}</p>
                            <p><strong>Preview:</strong> {doc.content}...</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default QueryForm;
