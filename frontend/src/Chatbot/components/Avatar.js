import React from "react";
import sentinelIcon from "../../images/Sentinel Round mini.svg";
export default function Avatar() {
  return (
    <div style={{display:"flex"}}>
      <img className="BOT" src={sentinelIcon} alt="BOT" />
      <p style={{fontWeight:"600", color:"#CCBEEA", marginLeft:"12px"}}>Sentinel</p>
    </div>
  );
}
