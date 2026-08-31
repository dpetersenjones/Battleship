import React, { useState, useEffect } from "react";
import Ship2 from "./Ship2";
import ShipDragLayer from "./ShipDragLayer";

export default function ShipDock({ tileSize }) {
  const [orientation, setOrientation] = useState("horizontal");
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkWidth = () => setIsMobile(window.innerWidth <= 600);
    checkWidth(); // initial check
    window.addEventListener("resize", checkWidth);
    return () => window.removeEventListener("resize", checkWidth);
  }, []);

  const handleClick = () => {
    setOrientation((prev) =>
      prev === "horizontal" ? "vertical" : "horizontal"
    );
  };

  const dockStyle = {
    // display: 'flex',
    // flexDirection: orientation === "vertical" ? "row" : "column",
    height: `${tileSize * 6} px`,
    // flexDirection: "row",
    // gap: '10px', // optional: spacing between ships
    // alignItems: 'center',
    // marginBottom: '10px',
    // margin: '10px',
    // padding: '50px 10px'
  };

  return (
    <div className="dock-container">
      <h3>Ship Dock {orientation}</h3>
      <div
        className="ship-dock"
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: isMobile && orientation === "horizontal" ? 'flex-start' : 'center',
          alignItems: "center",
          gap: isMobile && orientation === "horizontal" ? '4px' : '10px',
          height: `${tileSize * 7}px`,
          padding: "15px",
          transition: "all 0.3s ease",
          flexWrap: orientation === "horizontal" ? 'wrap' : "nowrap",

        }}
      >
        <Ship2
          type="destroyer"
          length={2}
          direction={orientation}
          size={tileSize}
        />
        <Ship2
          type="submarine"
          length={3}
          direction={orientation}
          size={tileSize}
        />
        <Ship2
          type="cruiser"
          length={3}
          direction={orientation}
          size={tileSize}
        />
        <Ship2
          type="battleship"
          length={4}
          direction={orientation}
          size={tileSize}
        />
        <Ship2
          type="carrier"
          length={5}
          direction={orientation}
          size={tileSize}
        />
        <ShipDragLayer tileSize = {tileSize} direction = {orientation} />
      </div>
      <button onClick={handleClick}>Change Orientation</button>
    </div>
  );
}
