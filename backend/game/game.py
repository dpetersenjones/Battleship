from .enemy_ai import EnemyAI
from .enemy_board import EnemyBoard
from .player_board import PlayerBoard
import json

#JSON file saying Start Game to start the Object

class Game():
    """
    This is the game class. It contains the PlayerBoard, the EnemyBoard, and enemy AI.
    """
    def __init__(self, boats:list[dict] = None):
        """
        To initialize, the positions must be entered for the player board

        Args:
            pos (list[dict]): The position for each boat, should be structure dictionary[boat], which in turn will be a dictionary having the following area: size, starting position, orientation.
        """
        self.ai = EnemyAI()
        self.enemy_board = EnemyBoard()
        self.player_board = PlayerBoard(boats) if boats else None
        self.playerHits = []
        self.playerMisses = []
        self.enemyHits = []
        self.enemyMisses = []
        # self.player_board.print_board()
        
    #TODO:Add game over check
    def game_over_check(self):
        if self.player_board and self.player_board.game_over_check():
            return {"game_over": True, "winner": "enemy"}
        elif self.enemy_board and self.enemy_board.check_game_over():
            return {"game_over": True, "winner": "player"}
        else:
            return {"game_over": False, "winner":False}

    def player_position_and_shots():
        pass

    def processing_player_shoots(self, coor) -> dict:
        """
        This marks the result of the player's shot
        """
        resulting_hit = self.enemy_board.take_hit(coor) #Returns a dictionary, saying if 'boat_hit' or if 'boat_sunk'
        if resulting_hit["hit"]:
            self.playerHits.append(coor)
        else:
            self.playerMisses.append(coor)
        return resulting_hit
    
    def enemy_shoots(self):
        if self.ai.next_hit:
            enemy_shot = self.ai.next_hit        
        else:
            enemy_shot = self.ai.shoot()
        player_result = self.player_board.take_hit(enemy_shot)
        self.ai.response(pos=enemy_shot, hit=player_result["hit"], boat=player_result["sink"])
        hit = False
        if enemy_shot in self.player_board.boat_info["all_boats_coor"]:
            hit = True
            self.enemyHits.append(enemy_shot)
        else:
            self.enemyMisses.append(enemy_shot)
        return {"coor": enemy_shot, "hit": hit}
    
    def logging_enemy_shot_result(self, result):
        ###TODO: This doesn't make sense. It needs to be fixed.
        """
        This logs the result of what the enemy shot at.
        """
        self.enemy_board(result["pos"], result["hit"], result["boat"])
        
        
    def serialize(self):
        return ({
            "ai": self.ai.serialize(),
            "enemy_board": self.enemy_board.serialize(),
            "player_board": self.player_board.serialize() if self.player_board else None,
            "playerHits": self.playerHits,
            "playerMisses": self.playerMisses,
            "enemyHits": self.enemyHits,
            "enemyMisses": self.enemyMisses,
        })

    @classmethod
    def deserialize(cls, info):
        try:
            ai_info = json.loads(info.ai_state)
            enemy_info = json.loads(info.enemy_board)
            player_info = json.loads(info.player_board)
            new_game = cls()
            new_game.ai = EnemyAI.deserialize(ai_info)
            new_game.enemy_board = EnemyBoard.deserialize(enemy_info)
            new_game.player_board = PlayerBoard.deserialize(player_info) if info.player_board else None
            new_game.playerHits = info.player_hits
            new_game.playerMisses = info.player_misses
            new_game.enemyHits = info.enemy_hits
            new_game.enemyMisses = info.enemy_misses
            return new_game
        except KeyError as e:
            raise ValueError(f"Missing required data for deserialization: {e}")