import Tile from "./Tile"
import RenderTiles from "./RenderTiles";
import { useDrop } from "react-dnd"

function Board(props) {
    const position = []
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 10; j++) {
            position.push([i, j]);
        }
    }

    return (
        <div className="board">
            {position.map((item, index) => {
               return <RenderTiles pos = {item} key = {index} setBoat = {props.setBoat[0]} boatPos = {props.boatPos} test = {props.test}/>
            })}
        </div>
    )
    
}

export default Board