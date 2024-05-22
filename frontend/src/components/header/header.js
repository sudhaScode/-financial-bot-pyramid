import "./header.css";
import miniLogo from "../../images/Sentinel-Mini-Logo.png";
import userLogo from "../../images/user-circle.svg";
export function Header() {
  return (
    <div className="header">
      <img style={{ height: "35px" }} src={miniLogo} alt={"sentinal imgg"} />
      <img style={{ height: "35px" }} className="userLogo" src={userLogo} />
    </div>
  );
}
