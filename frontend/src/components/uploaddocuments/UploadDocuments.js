import { useState } from "react";
import "./UploadDocuments.css";

function UploadDocuments() {
  const [files, setFiles] = useState([]);

  const handleFileChange = (event) => {
    const selectedFiles = event.target.files;
    setFiles(Array.from(selectedFiles));
  };

  const handleSubmitClick = () => {
    // call the api to take the files
    console.log("Submitted");
  };

  return (
    <div
      style={{
        height: "90vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div className="file-container">
        <input
          id="file-upload"
          type="file"
          multiple
          onChange={handleFileChange}
        />
        <button
          className="button-upload"
          onClick={() => document.getElementById("file-upload")?.click()}
        >
          Upload Documents
        </button>
      </div>
      <div className="submit-button-container">
        <button
          style={{ opacity: `${files.length <= 0 ? "0.5" : "1"}` }}
          disabled={files.length > 0 ? false : true}
          className="submit-button"
          onClick={handleSubmitClick}
        >
          Submit
        </button>
      </div>
      {files.length > 0 && (
        <div className="file-list">
          <h2>Selected files:</h2>
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default UploadDocuments;
