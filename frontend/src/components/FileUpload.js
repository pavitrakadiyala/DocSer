import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./FileUpload.css"; 

const FileUpload = () => {
    const [files, setFiles] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");  // State to handle errors
    const [uploading, setUploading] = useState(false);  // State to track upload status
    const navigate = useNavigate();

    const handleFileChange = (event) => {
        setFiles(event.target.files);
        setErrorMessage("");  // Update error messages when new files are selected
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (files.length === 0) {
            setErrorMessage("Please select at least one file to upload.");
            return;  // Error if empty input
        }

        setUploading(true);  // Uploading
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append("files", files[i]);
        }

        try {
            const response = await fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                alert("Files uploaded successfully!");
                setUploading(false);  // Stop the uploading status
                navigate("/query");
            } else {
                alert("Error uploading files.");
                setUploading(false);  // Stop the uploading status
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Error uploading files.");
            setUploading(false);  // Stop the uploading status
        }
    };

    return (
        <div className="container">
            <div className="file-upload-container">
                <h1>Document Semantic Search</h1>
                <p>Upload PDF or TXT files to perform semantic searches on the content.</p>
                <form onSubmit={handleSubmit} className="upload-form">
                    <div className="upload-section">
                        <label htmlFor="fileInput" className="file-label">Choose your files (PDF/TXT):</label>
                        <input
                            id="fileInput"
                            type="file"
                            onChange={handleFileChange}
                            accept="application/pdf,text/plain"
                            multiple
                            className="file-input"
                        />
                    </div>
                    {errorMessage && <p className="error-message">{errorMessage}</p>}  
                    {uploading && <p className="uploading-message">Uploading files, please wait...</p>}  
                    <button type="submit" className="upload-button" disabled={uploading}>Upload</button> 
                </form>
            </div>
        </div>
    );
};

export default FileUpload;
