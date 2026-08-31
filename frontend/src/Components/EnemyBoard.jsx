import React, { useEffect, useState } from "react"
import Tile2 from "./Tile2"
import shipImage from '../Assets/battleship-1.png'; 
import waves from '../Assets/pattern_waves.png'

export default function EnemyBoard({handleClick, playerHits = [], playerMisses = [], sunkenEnemies = [], tileSize= 40}) {
    const height = 10;
    const width = 10;

    const [clicked, setClicked] = useState([])

    // //Used for debugging
    // useEffect(() => {
    //     console.log(playerHits);
    //     console.log(playerMisses);
    //     console.log(`Enemy Sunken Ships: ${sunkenEnemies}`)
    // }, [playerHits, playerMisses, sunkenEnemies])

    const renderShips = () => {
          
            return sunkenEnemies.map((ship, index) => {
              const isVertical = ship.direction === 'vertical';
          
              const style = {
                position: 'absolute',
                left: `${(ship.start[1] * tileSize) + (isVertical ? tileSize : 0)}px`,
                top: `${ship.start[0] * tileSize}px`,
                width: `${tileSize * (ship.length)}px`,
                height: `${tileSize * (1)}px`,
                transform: isVertical ? "rotate(90deg)" : "none",
                transformOrigin: "top left",
                transitionDuration: "3000",
                backgroundImage: `url(${shipImage})`,
                backgroundSize: '100% 100%',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center',
                pointerEvents: 'none',
                zIndex:0,
              };
          
              return <div key={index} style={style} />;
            });
          };

    const renderTile = () => {
        const tiles = []
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const isHit = playerHits.some(
                    (coor) => coor[0] === y && coor[1] === x
                    )
                const isMiss = playerMisses.some(
                    (coor) => coor[0] === y && coor[1] === x
                )
                tiles.push(
                    <div onClick={()=>{!isHit && !isMiss && handleClick(y, x)}}>
                        <Tile2
                            key={`${x}-${y}`}
                            x = {x}
                            y = {y}
                            onDropShip={()=>{}}
                            isOccupied={false}
                            isHit = {isHit}
                            isMiss = {isMiss}
                            tileSize={tileSize}
                        />
                    </div>
                )
            }
        }
        return tiles
    }
    return (
        <div className="board"
        style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${width}, ${tileSize}px)`,
            gridTemplateRows: `repeat(${height}, ${tileSize}px)`,
            position: 'relative',
            width: width * tileSize,
            height: height * tileSize,
            backgroundImage: `url(${waves})`,
            backgroundSize: '250px 250px', // if you want each tile to have a wave
            backgroundRepeat: 'repeat',
            backgroundPosition: 'center',
          }}
        >
            {renderTile()}
            {renderShips()}
        </div>
    
    )
}