import { ItemTypes } from "../Constants/ItemTypes"
import { useDrag } from "react-dnd"

const shipTypes = {
    destroyer: { length: 2 },
    submarine: { length: 3 },
    // add more types
  };

function Ship() {
    const [{isDragging}, drag] = useDrag(() => ({
        type: ItemTypes.SHIP,
        collect: monitor => ({
            isDragging: monitor.isDragging(),
        })
    }))
    return <span ref={drag}>🚢</span>
}

export default Ship