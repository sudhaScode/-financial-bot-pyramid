import React from "react";
export default function ClearChat(props) {
  console.log("Clear props", props);
  const clearChat = () => {
    props.actions.clearChat();
  };
  return (
    <button className="button-upload" onClick={() => clearChat()}>
      Clear
    </button>
  );
}
