import "./Nav.css";
import "../../App.css";
import "react-chatbot-kit/build/main.css";
import { Link, useLocation } from "react-router-dom";
import React, { useContext, useState } from "react";
import { Context } from "../../store/Context";
import { MdArrowForwardIos } from "react-icons/md";
function NavBar() {
  const { isHRCheckin, setIsHRCheckin } = useContext(Context);
  const { isOpen, setIsOpen } = useState(true);
  const location = useLocation();

  const handleLogOut = () => {
    setIsHRCheckin(false);
  };

  return (
    <>
      <div className={isOpen ? "sidebar open" : "sidebar"}>
        <ul style={{marginTop:"40%"}}>
          <li
            className={`${
              location.pathname === "/uploadDocument" ? "active" : ""
            }`}
          >
            <Link className="link" to="/uploadDocument">
              Upload a document <MdArrowForwardIos />
            </Link>
          </li>
          <li
            className={`${
              location.pathname === "/fileExplorer" ? "active" : ""
            }`}
          >
            <Link to="/fileExplorer" className="link">
              File Explorer <MdArrowForwardIos />
            </Link>
          </li>

          <li
            className={`${location.pathname === "/auditSmart" ? "active" : ""}`}
          >
            <Link to="/auditSmart" className="link">
              Audit Smart <MdArrowForwardIos />
            </Link>
          </li>
        </ul>
      </div>
    </>
  );
}

export default NavBar;
