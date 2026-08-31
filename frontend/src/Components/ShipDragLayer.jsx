// ShipDragLayer.jsx
import React from 'react';
import { useDragLayer } from 'react-dnd';
import battleShip from "../Assets/battleship-1.png";

const layerStyles = {
  position: 'fixed',
  pointerEvents: 'none',
  zIndex: 100,
  left: 0,
  top: 0,
};

// Use mouse position (clientOffset) directly
function getItemStyles(clientOffset, direction, tileSize) {
  if (!clientOffset) return { display: 'none' };

  let { x, y } = clientOffset;

  if (direction === "horizontal") {
    x = x - tileSize/2;
    y = y - tileSize/2;
  } else {
    x = x + tileSize/2;
    y = y - tileSize/2;
  }

  return {
    transform: `translate(${x}px, ${y}px)`,
  };
}

export default function ShipDragLayer({ tileSize, direction }) {
  const {
    item,
    isDragging,
    clientOffset,
  } = useDragLayer((monitor) => ({
    item: monitor.getItem(),
    isDragging: monitor.isDragging(),
    clientOffset: monitor.getClientOffset(), // current mouse position
  }));

  if (!isDragging || !item) return null;

  const size = tileSize;
  const isVertical = item.direction === "vertical";

  return (
    <div style={layerStyles}>
      <div style={getItemStyles(clientOffset, direction, tileSize)}>
        <div
          style={{
            width: size * item.length,
            height: size,
            backgroundImage: `url(${battleShip})`,
            backgroundSize: '100% 100%',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center',
            transform: isVertical ? 'rotate(90deg)' : 'none',
            transformOrigin: 'top left',
          }}
        />
      </div>
    </div>
  );
}
