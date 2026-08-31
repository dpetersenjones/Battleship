import Tile from "./Tile";
import Ship from "./Ship";
import { useDrop } from "react-dnd"
import { ItemTypes } from "../Constants/ItemTypes";


//Turn into componant again. See if that works.
function RenderTiles(props) {
    const [boatX, boatY] = props.boatPos;
    const isBoat = boatX === props.pos[0] && boatY === props.pos[1]    
    const place = isBoat ? <Ship /> : null
    const [{ isOver, canDrop }, drop] = useDrop(() => ({
        accept: ItemTypes.SHIP,
        drop: () => {
            console.log(props.pos)
            props.setBoat(props.pos)},
        collect: (monitor) => ({
            isOver: monitor.isOver(),
            canDrop: monitor.canDrop()
        })
    }), [props.pos])

    return <Tile ref={drop} test = {props.test} pos = {props.pos} setBoat = {props.setBoat}>{place}</Tile>
}

export default RenderTiles