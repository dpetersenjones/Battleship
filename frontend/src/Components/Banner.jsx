import React, { useEffect, useState } from "react";

export default function Banner({
  game_over = false,
  winner = null,
  playing = false,
  playerHit = false,
  playerSunk = false,
  playerShot = [],
  enemyHit = false,
  enemySunk = false,
  enemyShot = [],
}) {
  useEffect(() => {
    console.log(`game_over = ${game_over}`)
    console.log(`winner = ${winner}`)
    console.log(`playing = ${playing}`)
    console.log(`playerHit = ${playerHit}`)
    console.log(`playerSunk = ${playerSunk}`)
    console.log(`playerShot = ${playerShot}`)
    console.log(`enemyHit = ${enemyHit}`)
    console.log(`enemySunk = ${enemySunk}`)
    console.log(`enemyShot = ${enemyShot}`)
  }, [game_over, winner, playing, playerHit, playerSunk, playerShot, enemyHit, enemySunk, enemyShot])
  const [message, setMessage] = useState("Loading");
  const [playerMessage, setPlayerMessage] = useState("");
  const [enemyMessage, setEnemyMessage] = useState("");
  useEffect(() => {
    // console.log(`Game Over is ${game_over}`)
    if (!playing && playerShot.length === 0) {
      setMessage("Place your ship and press the submit button!");
    } else if (game_over) {
      setMessage(`Game over! Winner is ${winner}`);
    } else if (playing && playerShot.length === 0) {
      setMessage('Take your first shot.')
    } else {
      setMessage('')
    }
  }, [playing, game_over]);

  useEffect(() => {
    if (playerShot.length === 0) return; 
  
    if (playerSunk) {
      setPlayerMessage(`You shot at ${playerShot} and sunk the enemy's ${playerSunk}`);
    } else if (playerHit) {
      setPlayerMessage(`You shot at ${playerShot} and hit!`);
    } else {
      setPlayerMessage(`You shot at ${playerShot} and missed.`);
    }
  }, [playerSunk, playerHit, playerShot]);


  useEffect(() => {
    if (enemyShot.length === 0) return;
  
    if (enemySunk) {
      setEnemyMessage(`The enemy shot at ${enemyShot} and sunk one of your ships.`);
    } else if (enemyHit) {
      setEnemyMessage(`The enemy shot at ${enemyShot} and hit one of your ships.`);
    } else {
      setEnemyMessage(`The enemy shot at ${enemyShot} and missed.`);
    }
  }, [enemySunk, enemyHit, enemyShot]);

  return (
    <div className="banner">
      <h1>Battleship!</h1>
      {/* <h3>{(message && playing) || (playerMessage && " " && enemyMessage)}</h3> */}
      {(!playing || game_over) && message && <h3>{message}</h3>}
  {playing && !game_over && (
    <>
      {playerMessage && <h3>{playerMessage}</h3>}
      {enemyMessage && <h3>{enemyMessage}</h3>}
    </>
)}

    </div>
  );
}
