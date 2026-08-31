import Ship from "./Ship"

function Tile(props) {
        
    function handleClick(e) {
        props.test(props.pos)
        props.setBoat(props.pos)
    }
    
    // place = isBoat ? <Ship /> : null;

    return (
        <div className="tile" onClick={handleClick}>{props.pos}{props.children}</div>
    )
}

export default Tile