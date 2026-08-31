// Ship2.jsx
import React, { useEffect } from 'react';
import { useDrag } from 'react-dnd';
import { getEmptyImage } from 'react-dnd-html5-backend';
import battleShip from "../Assets/battleship-1.png";

export default function Ship2({ type, length, direction, size }) {
  const [{ isDragging }, dragRef, dragPreview] = useDrag(() => ({
    type: 'SHIP',
    item: { type, length, direction },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }), [type, length, direction]);

  useEffect(() => {
    dragPreview(getEmptyImage(), { captureDraggingState: true });
  }, [dragPreview]);


  return (
    <div
      ref={dragRef}
      style={{
        opacity: isDragging ? 0.5 : 1,
        width: size * length,
        height: size,
        transform: direction === "vertical" ? 'rotate(90deg)' : 'none',
        backgroundImage: `url(${battleShip})`,
        backgroundSize: '100% 100%',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
        cursor: 'grab',
      }}
    />
  );
}
