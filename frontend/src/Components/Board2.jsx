import React, { useEffect, useState } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import useTileSize from './useTileSize';
import GameBoard from './GameBoard';
import ShipDock from './ShipDock';
import EnemyBoard from './EnemyBoard';
import Banner from './Banner';

function Board2() {
  const [messageInfo, setMessageInfo] = useState({})
  const [playing, setPlaying] = useState(false)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [toSend, setToSend] = useState([])
  const [playerHits, setPlayerHits] = useState([])
  const [playerMisses, setPlayerMisses] = useState([])
  const [enemyHits, setEnemyHits] = useState([])
  const [enemyMisses, setEnemyMisses] = useState([])
  const [sunkenEnemies, setSunkenEnemies] = useState([])
  const [gameOver, setGameOver] = useState(false)
  const [winner, setWinner] = useState("")
  const [gameStart, setGameStart] = useState(false)
  const tileSize = useTileSize(10);

  const handleSubmit = async () => {
    if (gameOver || playing) {
      try {
        const response = await fetch("http://127.0.0.1:8000/delete/", {
          method: 'DELETE',
          credentials: 'include'
        })
        if (response.ok) {
          setPlaying(false);
          setData([]);
          setToSend([]);
          setPlayerHits([]);
          setPlayerMisses([]);
          setEnemyHits([]);
          setEnemyMisses([]);
          setSunkenEnemies([]);
          setGameOver(false);
          setMessageInfo({})
          setGameStart(false)
        }
      } catch (e) {
      setError(e)
      console.log(`Error is ${e}`)
      } finally {
        return
      }
    }
    if (toSend.current.length < 5) {
      alert("You need to place all the ships");
      return;
    };
    
    try {
      const response = await fetch("http://127.0.0.1:8000/start/", {
        method:"POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body:JSON.stringify({player_start:toSend}),
      })
      if (response.ok) {
        setData(toSend.current);
        setPlaying(true);
        setGameStart(true);
        setMessageInfo({})
      }
      setPlaying(true)
    } catch (e) {
      setError(e)
    } 
  }

  const handleClick = async (y, x) => {
    if (!playing || gameOver) {
      return
    }
    setPlaying(false)
    
    try {
      const response = await fetch("http://127.0.0.1:8000/move/", {
        method:"POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body:JSON.stringify({player_shot:[y, x]}),
      })
      const json = await response.json()
      const {enemy_data, player_data} = json["data"]
      const message = {}

      //Used for debugging
      console.log("In handleClick")
      console.log(enemy_data)
      console.log(player_data)

      message["player_shot"] = player_data["player_shot"]
      message["enemy_shot"] = enemy_data["enemy_shot"]

      if (player_data["player_result"]["hit"]) {
        // //Used for debugging
        // console.log("Hit");

        message["player_hit"] = true;
        message["player_position"] = player_data["player_shot"]
        setPlayerHits((prev) => [...prev, player_data["player_shot"]]);
        if (player_data["player_result"]["enemy_ship"]) {
          setSunkenEnemies((prev) => [...prev, player_data["player_result"]["enemy_ship"]])
          message["player_sunk"] = true;
        }
      } else {
        // //Used for debugging
        // console.log("Miss");

        message["player_hit"] = false;
        setPlayerMisses((prev) => [...prev, player_data["player_shot"]])
      }
      if (enemy_data["enemy_ship"]) {
        // //Used for debugging
        // console.log("In enemy_sink")

        message["enemy_sunk"] = true;
        setSunkenEnemies((prev) => [...prev, enemy_data["enemy_ship"]])
      }
      if (enemy_data["enemy_result"]) {
        // //Used for debugging
        // console.log("Enemy Hit")

        message["enemy_hit"] = true;
        message["enemy_position"]= enemy_data["enemy_shot"]
        setEnemyHits((prev) => [...prev, enemy_data["enemy_shot"]])
      } else {
        // //Used for debugging
        // console.log("Enemy Miss")

        message["enemy_hit"] = false;
        message["enemy_position"]= enemy_data["enemy_shot"]
        setEnemyMisses((prev) => [...prev, enemy_data["enemy_shot"]])
      }
      if (json["data"]["game_over"]) {
        // //Used for debugging
        // console.log(`Winner is ${json["data"]["winner"]}`)
        
        setWinner(json["data"]["winner"])
        setGameOver(true)
      } 
      setPlaying(true)
      setMessageInfo(message)
    } catch (e) {
      setError(e)
    } 
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/start/", {
          method:"GET",
          credentials: "include",
          headers: {
          "Content-Type": "application/json"
        },
        });        
        if (!response.ok) {
          throw new Error(`HTTP error status: ${response.status}`)
        }
        if (response.status === 202) {
          console.log("Found 202");
          return;
        }
        setGameStart(true)
        const json = await response.json();
        const {player_data, enemy_data} = json["data"]
        const all_ships = player_data["player_ships"]
        if (json["data"]) {
          if (json["data"]["game_over"]) {
            setGameOver(true)
            setWinner(json["data"]["winner"])
          }
          const container = []
          for (const key in all_ships) {
            container.push({
              ship: {
                direction: all_ships[key]["direction"],
                length: all_ships[key]["length"],
                type: all_ships[key]["type"]
              },
              x: all_ships[key]["start"][0],
              y: all_ships[key]["start"][1],
              direction: all_ships[key]["direction"],
              length: all_ships[key]["length"],
              type: all_ships[key]["type"]
            })}
          setPlaying(true);
          setData(container)
          //Set player hits and misses
          setPlayerHits(player_data["player_hits"])
          setPlayerMisses(player_data["player_misses"])
          setEnemyHits(enemy_data["enemy_hits"])
          setEnemyMisses(enemy_data["enemy_misses"])
          setSunkenEnemies(enemy_data["sunken_enemy_ships"])
        }
        // console.log(`In data: ${data}`)

      } catch (e) {
        setError(e)
      } finally {
        setLoading(false)
      }
    };
    fetchData();
    
  },[])

  // //Used for debugging
  // useEffect(() => {
  //   if (data) {
  //     console.log("Updated data:", data);
  //   }
  // }, [data]);

  // useEffect(() => {
  //   if (sunkenEnemies) {
  //     console.log("Updated sunkenEnemies:", sunkenEnemies);
  //   }
  // }, [sunkenEnemies]);

  // useEffect(() => {
  //   if (enemyHits) {
  //     console.log("Updated playerHist:", enemyHits);
  //   }
  // }, [enemyHits]);

  // useEffect(() => {
  //   if (enemyMisses) {
  //     console.log("Updated playerMisses:", enemyMisses);
  //   }
  // }, [enemyMisses]);

  if (loading) {
    return (
      <p>Loading...</p>
    )
  }

  // if (error) {
  //   return (
  //     <p>Error: {error.message}</p>
  //   )
  // }

  return (
    <DndProvider backend={HTML5Backend}>
      <Banner
        game_over={gameOver}
        winner = {winner}
        playing={playing}
        playerHit = {messageInfo["player_hit"]}
        playerSunk = {messageInfo["player_sunk"]}
        playerShot={messageInfo["player_shot"]}
        enemyHit={messageInfo["enemy_hit"]}
        enemySunk={messageInfo["enemy_sunk"]}
        enemyShot={messageInfo["enemy_shot"]}
        />
      <div className="board-container">
      <div className="left-panel" style={{ display: 'flex', gap: '20px' }}>
        
        <GameBoard 
          data={data} 
          playing={playing} 
          setToSend={setToSend} 
          enemyHits={enemyHits} 
          enemyMisses={enemyMisses} 
          gameOver={gameOver}
          tileSize={tileSize}
          />
        {/* <ShipDock /> */}
        <button onClick={handleSubmit}>{gameStart ? "Restart" : "Send Data"}</button>
        
      </div>
      <div className="right-panel" style={{ display: 'flex', gap: '20px' }}>
        {gameStart && <EnemyBoard handleClick = {handleClick} playerHits={playerHits} playerMisses={playerMisses} sunkenEnemies={sunkenEnemies} tileSize={tileSize}/>}
        {!gameStart && <ShipDock tileSize={tileSize}/>}
      </div>
      {/* <div style={{ display: 'flex', gap: '20px' }}>
        <ShipDock />
        <GameBoard />
      </div> */}
      </div>
    </DndProvider>
  );
}

export default Board2;