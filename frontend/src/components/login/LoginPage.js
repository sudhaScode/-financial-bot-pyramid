import { useContext, useState } from "react";
import "./Login.css";
import "react-chatbot-kit/build/main.css";
import "../../App.css";
import { useNavigate } from "react-router-dom";
import { Context } from "../../store/Context";
import largeLogo from "../../images/Sentinel-Large-Logo.png";
function LoginPage() {
  const { setIsHRCheckin } = useContext(Context);
  const userName = "sentinel@gmail.com";
  const password = "sentinel";
  const [loginForm, setLoginForm] = useState({
    userName: "sentinel@gmail.com",
    password: "sentinel",
    checkbox: false,
  });
  const [error, setError] = useState(false);

  const navigation = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === "checkbox" ? checked : value;
    setLoginForm((prevState) => ({
      ...prevState,
      [name]: newValue,
    }));
    setError(false);
  };

  const handleLogin = (e) => {
    e.preventDefault();
    if (loginForm.userName === userName && loginForm.password === password) {
      setError(false);
      setIsHRCheckin(loginForm.checkbox);
      navigation("/uploadDocument");
    } else {
      setError(true);
    }
  };
  return (
    <>
      <div className="main-container">
        <form className="form-container" onSubmit={handleLogin}>
          <img style={{ height: "35%" }} src={largeLogo} alt={"sentinal img"} />
          <div className="input-container">
            <input
              type="text"
              name="userName"
              required
              value={loginForm.userName}
              onChange={handleChange}
              placeholder="Enter Email ID"
              autoComplete="username"
              className={`input-box ${error && "error-container"}`}
            />
          </div>
          <div className="input-container">
            <input
              placeholder="Enter password"
              type="password"
              name="password"
              required
              value={loginForm.password}
              onChange={handleChange}
              autoComplete="current-password"
              className={`input-box ${error && "error-container"}`}
            />
          </div>
          <div className="button-container">
            <input className="button" type="submit" value="Log In" />
          </div>
        </form>

        {error && (
          <p style={{ color: "red", marginTop: "10px" }}>Invalid credentials</p>
        )}
      </div>
    </>
  );
}

export default LoginPage;
