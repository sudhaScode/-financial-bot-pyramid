import React, { useContext, useEffect } from "react";
import { Context } from "../../store/Context";
import { createClientMessage } from "react-chatbot-kit";
import config from "./config";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const { files } = useContext(Context);
  
  const createUserMessage = (name) => {
    const message = createClientMessage(name);
    updateState(message, "age");
  };

  const createBotMessage = (name) => {
    const message = createChatBotMessage(name);
    updateState(message, "age");
  };

  const createBotSummary = (response) => {
    const message = createChatBotMessage(response);
    updateState(message, 'age');
  };


  const clearChat = () => {
    setState((state) => ({
      ...state,
      messages: config.initialMessages,
    }));
  };
  // Your other action functions here...

  const initialAction = () => {
    const message = createChatBotMessage("Just type in your name to begin.");
    //updateState(message, "age");
  };

  const afterNameMessage = () => {
    const message = createChatBotMessage(
      "Let me know your age so I can suggest the best ride for you."
    );
    //updateState(message, "preference");
  };

  const afterAgeMessage = () => {
    const message = createChatBotMessage(
      "do you lean towards a fast and thrilling ride or prefer a more relaxed and comfortable one?",
      {
        widget: "startSlow",
      }
    );
    //updateState(message);
  };

  const finalResult = (name, age, preference, vehicle) => {
    const message = createChatBotMessage(
      `Got it, ${name}! Based on your age ${age} and preference for a ${preference} ride, I recommend the '${vehicle}.' Enjoy the thrill!`,
      {
        widget: "finalImage",
      }
    );
    //updateState(message);
  };

  const updateState = (message, checker) => {
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, message],
      checker,
    }));
  };

  const sendMessageToAPI = async (message) => {
    //message += " if it is greeting greet the user"
    //console.log(message)
    try {
      const response = await fetch("http://127.0.0.1:8081/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      });

      if (response.ok) {
        const result = await response.json();
        // Call the appropriate actions based on the API response
        console.log(result);
        return result.ragsystem_response;
      } else {
        console.error("Failed to fetch data from the server");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    if (files.length > 0) {
      createChatBotMessage(files[0].name);
    }
  }, [files]);

  const handleAPIResponse = async (response) => {
    try {
      const result = await sendMessageToAPI(response);
      console.log(result);

      const message = createChatBotMessage(result);
      updateState(message);
    } catch (error) {
      console.error("Error handling API response:", error);
    }
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            initialAction,
            afterNameMessage,
            afterAgeMessage,
            finalResult,
            handleAPIResponse,
            createUserMessage,
            createBotMessage,
            createBotSummary,
            clearChat,
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;
