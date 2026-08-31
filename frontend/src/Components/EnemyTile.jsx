import React from 'react';
import { useDrop } from 'react-dnd';

export default function EnemyTile({ x, y }) {

  return (
    <div
      style={{
        width: 30,
        height: 30,
        backgroundColor,
        border: '1px solid black',
      }}
      className='tile'
    >
    </div>
  );
}