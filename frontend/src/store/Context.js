import { useState } from "react";
import { createContext } from "react";

export const Context = createContext();

export const ContextProvider = function ContextProvider({ children }) {
  const [files, setFiles] = useState([]);
  const [isHRCheckin, setIsHRCheckin] = useState({});
  const [userUploadedImage, setUserUploadedImage] = useState("");

  return (
    <Context.Provider
      value={{
        userUploadedImage,
        setUserUploadedImage,
        isHRCheckin,
        setIsHRCheckin,
        files, setFiles
      }}
    >
      {children}
    </Context.Provider>
  );
};
