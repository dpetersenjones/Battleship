import { useState, useEffect } from 'react';

export default function useTileSize(boardWidth = 40) {
  const [tileSize, setTileSize] = useState(40);

  useEffect(() => {
    const updateSize = () => {
      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;
      const maxBoardPixels = Math.min(screenWidth * 0.8, screenHeight * 0.5);
      const newTileSize = Math.floor(maxBoardPixels / boardWidth);
      setTileSize(Math.min(newTileSize, 100)); // cap at 50px
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, [boardWidth]);

  return tileSize;
}
