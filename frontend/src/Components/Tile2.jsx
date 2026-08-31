import React, { useEffect } from "react";
import { useDrop } from "react-dnd";
import RedXSvg from "./RedXSvg"; //ignore
import Circle from "./Circle";
// import shipSegmentImg from '../Assets/battleship-1.png'; // adjust as needed

export default function Tile2({
  x,
  y,
  onDropShip,
  isOccupied,
  isHit,
  isMiss,
  isHighlighted,
  onHoverTile,
  tileSize = 40,
}) {
  const [{ isOver, canDrop }, dropRef] = useDrop(() => (
    
    {
    accept: "SHIP",
    hover: (item, monitor) => {
      if (monitor.isOver({ shallow: true })) {
        onHoverTile && onHoverTile(x, y, item);
      }
    },
    drop: (item) => {
      onDropShip(item, x, y);
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
    
  }));

  
  

  const backgroundColor = isOccupied
    ? "transparent"
    : isHighlighted
    ? "lightgreen"
    : isOver
    ? canDrop
      ? "lightgreen"
      : "lightcoral"
    : "transparent";

  return (
    <div
      ref={dropRef}
      style={{
        width: tileSize,
        height: tileSize,
        backgroundColor,
        border: "1px solid black",
        position: "relative",
      }}
      className="tile"
    >
      {/* {isOccupied && (
        <div
          style={{
            width: '100%',
            height: '100%',
            backgroundImage: `url(${shipSegmentImg})`,
            backgroundSize: '100% 100%',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center',
          }}
        />
      )} */}
      {isHit && <RedXSvg />}
      {isMiss && <Circle />}
    </div>
  );
}
