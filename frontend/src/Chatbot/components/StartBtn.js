import React, { useContext, useState } from "react";
import clearIcon from "../../images/Clear Chat.svg";
import { Context } from "../../store/Context";
import { createClientMessage, } from "react-chatbot-kit";
import Avatar from "./Avatar";


export default function StartBtn(props) {



  const CustomSummaryComponent = (ragsystem_summarize) => (
    <div>
      <h3>Summary</h3>
      <p >{ragsystem_summarize}
      </p>

      
    </div>

  );



  const handleOnGenerateAPISummary = async () => {

    const response = await fetch('http://127.0.0.1:8081/summarize');
    const data = await response.json(); 
    const ragsystem_summarize = data.ragsystem_summarize;
  
   

    //props.actions.createBotMessage(CustomSummaryComponent());
    console.log("ragsystem_summarize", ragsystem_summarize);
    createBotSummary(CustomSummaryComponent(ragsystem_summarize));
  
  };
  const CustomMessageComponent = () => (
    <div>
      <p>The document has been uploaded. How do you want to continue?</p>
      <div>
        <button
          style={{ width: "140px", height: "35px" }}
          className="file-container"
          onClick={ handleOnGenerateAPISummary}
        >
          Generate Summary
        </button>
        <button
          disabled={true}
          style={{
            width: "140px",
            height: "35px",
            marginLeft: "10px",
            opacity: "0.5",
          }}
          className="file-container"
        >
          Save to Repository
        </button>
      </div>
      <p style={{ marginTop: "10px" }}>
        Or type any query related to the uploaded document in the below chat
        box.
      </p>

    </div>
  );
  const { setFiles, files } = useContext(Context);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(false);

  const createClientMessage = (name) => {
    props.actions.createUserMessage(name);
  };
  const createBotMessage = (name) => {
    props.actions.createBotMessage(name);
  };

  const createBotSummary = (name) => {
    props.actions.createBotSummary(name);
  };

  const clearChat = () => {
    props.actions.clearChat();
  };
  const initialAction = () => {
    props.actions.initialAction();
  };
  const handleFileChange = (event) => {
    const selectedFiles = event.target.files;
    setFiles(Array.from(selectedFiles));
    createClientMessage(selectedFiles[0].name);
    setLoading(true);

    uploadHander(selectedFiles[0]);
    createBotMessage(CustomMessageComponent());
  };

const uploadHander= async (file)=>{
  const fileData = new FormData();
  fileData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8081/upload', {
        method: "POST",
        body: fileData,
      });

      if (response.status === 200) {
        setStatus(true);
        console.log('File uploaded successfully!');
      } else {
        console.error('Failed to upload file. Server response:', response.statusText);
        // Handle error, display a message, or log more details
      }
    } catch (error) {
      console.error('An error occurred:', error);
      // Handle error, display a message, or log more details
    } 
    finally {
      setLoading(false);
    }
  }

  const handleFileAPIUpload = async () => {

    document.getElementById("file-upload")?.click(); //handle file upload api

      
    };

  return (
    <div style={{ marginLeft: "45px" }}>
      <div className="file-container">
        <input id="file-upload" type="file" onChange={handleFileChange} />
        <button className="button-upload" onClick={handleFileAPIUpload}>
          Upload
        </button>
      </div>
      <button
        style={{
          position: "absolute",
          top: "-15px",
          right: "25px",
          width: "100px",
          height: "35px",
          background: "trasparent",
          border: "none",
          background: "transparent",
          display: "flex",
          alignItems: "center",
          color: "#EEE6FF",
          cursor: "pointer",
        }}
        className="button-clear"
        onClick={() => clearChat()}
      >
        <img style={{ marginRight: "5px" }} src={clearIcon} height={"20px"} />{" "}
        <span style={{ marginBottom: "3px" }}>Clear Chat</span>
      </button>

      {/* <button className="start-btn" onClick={() => initialAction()}>
        Upload
      </button> */}
    </div>
  );
}
