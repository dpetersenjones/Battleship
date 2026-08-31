import React, { useState, useEffect, useRef } from "react";
import Tile2 from "./Tile2";
import shipImage from "../Assets/battleship-1.png";
import waves from "../Assets/pattern_waves.png";
import { useDragLayer } from "react-dnd"; //New

export default function GameBoard({
  playing,
  data = [],
  setToSend,
  enemyHits,
  enemyMisses,
  gameOver,
  tileSize = 40,
}) {
  const width = 10;
  const height = 10;
  const [draggedShip, setDraggedShip] = useState(null); 
  const [hoveredTile, setHoveredTile] = useState(null); 

  const { item: draggingItem, isDragging } = useDragLayer((monitor) => ({
    item: monitor.getItem(),
    isDragging: monitor.isDragging(),
  })); 

  useEffect(() => {
    if (isDragging && draggingItem) {
      setDraggedShip(draggingItem);
    } else {
      setDraggedShip(null);
      setHoveredTile(null);
    }
  }, [isDragging, draggingItem]); 

  const handleHoverTile = (x, y, ship) => {
    setHoveredTile({ x, y, ship });
  };

  // //Used for debugging
  // useEffect(() => {
  //   if (data) {
  //     console.log("Updated data inside GameBoard:", data);
  //   }
  // }, [data]);

  const [placedShips, setPlacedShips] = useState([]);
  const placedShipsRef = useRef([]);

  useEffect(() => {
    if (!data || data.length == 0) {
      setPlacedShips([]);
      placedShipsRef.current = [];
      setToSend([]);
    }
  }, [playing, data]);

  useEffect(() => {
    if ((playing || gameOver) && data && data.length > 0) {
      const ships = data.map((element) => ({
        ship: {
          type: element["type"],
          direction: element["direction"],
          length: element["length"],
        },
        x: element["x"],
        y: element["y"],
        direction: element["direction"],
        length: element["length"],
        type: element["type"],
      }));
      setPlacedShips(ships);
      placedShipsRef.current = ships;
      setToSend(ships);
    }
  }, [playing, data, gameOver]);

  // Keep ref in sync with state
  useEffect(() => {
    if (playing) {
      return;
    }
    placedShipsRef.current = placedShips;
    setToSend(placedShipsRef);
  }, [placedShips]);

  const handleDropShip = (ship, x, y) => {
    const currentShips = placedShipsRef.current;
    const direction = ship.direction || "horizontal";
    if (
      (direction === "horizontal" && x + ship.length > width) ||
      (direction === "vertical" && y + ship.length > height)
    ) {
      console.warn("Ship does not fit on the board");
      return;
    }
    const filteredShips = currentShips.filter((s) => s.type !== ship.type);

    const newShipCoords = Array.from({ length: ship.length }).map((_, i) => ({
      x: direction === "horizontal" ? x + i : x,
      y: direction === "vertical" ? y + i : y,
    }));

    const isOverlap = filteredShips.some((placed) => {
      return Array.from({ length: placed.length }).some((_, i) => {
        const tileX =
          placed.direction === "horizontal" ? placed.x + i : placed.x;
        const tileY = placed.direction === "vertical" ? placed.y + i : placed.y;

        return newShipCoords.some(
          (coord) => coord.x === tileX && coord.y === tileY
        );
      });
    });

    if (isOverlap) {
      console.warn("Ship overlaps with another");
      return;
    }

    // Place ship
    setPlacedShips((prev) => [...filteredShips, { ...ship, x, y }]);
  };

  const renderShips = () => {
    // const tileSize = 30;

    return placedShips.map((ship, index) => {
      const isVertical = ship.direction === "vertical";

      const style = {
        position: "absolute",
        left: `${ship.x * tileSize + (isVertical ? tileSize : 0)}px`,
        top: `${ship.y * tileSize}px`,
        width: `${tileSize * ship.length}px`,
        height: `${tileSize * 1}px`,
        transform: isVertical ? "rotate(90deg)" : "none",
        transformOrigin: "top left",
        transitionDuration: "3000",
        backgroundImage: `url(${shipImage})`,
        backgroundSize: "100% 100%",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        pointerEvents: "none",
        zIndex: 0,
      };

      return <div key={index} style={style} />;
    });
  };

  const renderTiles = () => {
    const tiles = [];
    // //Just for debugging
    // console.log("In renderTiles");
    // console.log(placedShips);

    const highlightedCoords = new Set();

    if (hoveredTile && draggedShip) {
      const { x, y, ship } = hoveredTile;
      const direction = ship.direction;
      const length = ship.length;

      for (let i = 0; i < length; i++) {
        const tileX = direction === "horizontal" ? x + i : x;
        const tileY = direction === "vertical" ? y + i : y;

        if (tileX < width && tileY < height) {
          highlightedCoords.add(`${tileX}-${tileY}`);
        }
      }
    }

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const hit = enemyHits.some((coor) => coor[0] === y && coor[1] === x);
        const miss = enemyMisses.some((coor) => coor[0] === y && coor[1] === x);
        const isOccupied = placedShips.some((ship) => {
          if (ship.direction === "horizontal") {
            return Array.from({ length: ship.length }).some((_, i) => {
              return ship.x + i === x && ship.y === y;
            });
          } else {
            return Array.from({ length: ship.length }).some((_, i) => {
              return ship.x === x && ship.y + i === y;
            });
          }
        });

        tiles.push(
          <Tile2
            key={`${x}-${y}`}
            x={x}
            y={y}
            onDropShip={handleDropShip}
            isOccupied={isOccupied}
            isHit={hit}
            isMiss={miss}
            tileSize={tileSize}
            isHighlighted={highlightedCoords.has(`${x}-${y}`)}
            onHoverTile={handleHoverTile}
          />
        );
      }
    }

    return tiles;
  };

  return (
    <div
      className="board"
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${width}, ${tileSize}px)`,
        gridTemplateRows: `repeat(${height}, ${tileSize}px)`,
        position: "relative",
        width: width * tileSize + 2,
        height: height * tileSize + 2,
        backgroundImage: `url(${waves})`,
        backgroundSize: "250px 250px", // if you want each tile to have a wave
        backgroundRepeat: "repeat",
        backgroundPosition: "center",
      }}
    >
      <div className="board-overlay" />
      {renderTiles()}
      {renderShips()}
    </div>
  );
}
