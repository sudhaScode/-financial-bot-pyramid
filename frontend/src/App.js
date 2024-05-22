import "react-chatbot-kit/build/main.css";
import "./App.css";
import { ContextProvider } from "./store/Context";
import NavBar from "./components/nav/NavBar";
import LoginPage from "./components/login/LoginPage";
import { Route, Routes, useLocation } from "react-router-dom";
import ChatBot from "./Chatbot/maincomponent/ChatBot";
import UploadDocuments from "./components/uploaddocuments/UploadDocuments";
import { Header } from "./components/header/header";

function App() {
  const location = useLocation();
  return (
    <ContextProvider>
      <div className="main">
        <div className="navigation">
          {location.pathname !== "/" && <NavBar />}
        </div>
        <div className="pages" style={{ backgroundColor: "#2d1b33" }}>
          {location.pathname !== "/" && <Header />}
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/uploadDocument" element={<ChatBot />} />
            <Route
              path="/dashboard/uploaddocuments"
              element={<UploadDocuments />}
            />
          </Routes>
        </div>
      </div>
    </ContextProvider>
  );
}

export default App;
