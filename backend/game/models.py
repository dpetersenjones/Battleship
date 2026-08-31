from django.db import models
from django.utils import timezone

class Game(models.Model):
    """
    Stores the full game state in the database.
    """
    player_board = models.JSONField()
    enemy_board = models.JSONField()
    ai_state = models.JSONField()
    
    # New fields to track shots
    player_hits = models.JSONField(default=list)
    player_misses = models.JSONField(default=list)
    enemy_hits = models.JSONField(default=list)
    enemy_misses = models.JSONField(default=list)

    game_over = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(default=timezone.now)

    def save_game(self, player_board, enemy_board, ai_state,
                  player_hits=None, player_misses=None,
                  enemy_hits=None, enemy_misses=None):
        """
        Save the game state and update the last accessed timestamp.
        """
        self.player_board = player_board
        self.enemy_board = enemy_board
        self.ai_state = ai_state

        if player_hits is not None:
            self.player_hits = player_hits
        if player_misses is not None:
            self.player_misses = player_misses
        if enemy_hits is not None:
            self.enemy_hits = enemy_hits
        if enemy_misses is not None:
            self.enemy_misses = enemy_misses

        self.last_accessed = timezone.now()
        self.save()

    def load_game(self):
        """
        Load the saved game state.
        """
        return {
            "player_board": self.player_board,
            "enemy_board": self.enemy_board,
            "ai_state": self.ai_state,
            "player_hits": self.player_hits,
            "player_misses": self.player_misses,
            "enemy_hits": self.enemy_hits,
            "enemy_misses": self.enemy_misses
        }
