import { useState } from "react"
import Board from "./Board"
import Ship from "./Ship"
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

function BoardHolder(props) {
    
    const [boat2, setBoat2 ] =useState([0, 0])
    const [boat3, setBoat3 ] =useState()
    const [boat4, setBoat4 ] =useState()
    const [boat5, setBoat5 ] =useState()

    function send_players_shot(pos) {
        // add api to send player's shot
        console.log(pos)
    }
    
    function send_players_pos(boat2, boat3, boat4, boat5) {
        //add api to send player's boat coor
    }
    
    return (
        <div>
        <DndProvider backend={HTML5Backend}>
            <div className="board-container">
                {/* player's board */}
                <Board setBoat={[setBoat2, setBoat3, setBoat4, setBoat5]} test = {send_players_shot} boatPos = {boat2} player = {true}/>
                {/* enemy's board */}
                {/* <Board send={send_players_shot} boatPos = {null}/> */}
            </div>
            <div className="button-container">
                <Ship />
            </div>
            </DndProvider>
        </div>
    )
}

export default BoardHolder