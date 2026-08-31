###TODO: Initialize this when actually posting website.

from django.core.management.base import BaseCommand
from django.utils import timezone
from game.models import Game
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes games that haven\'t been accessed in the last 7 days'

    def handle(self, *args, **kwargs):
        # Get the current time
        now = timezone.now()

        # Find all games where last_accessed is older than 7 days
        cutoff_time = now - timedelta(days=7)
        old_games = Game.objects.filter(last_accessed__lt=cutoff_time)

        # Delete the old games
        deleted_count, _ = old_games.delete()

        # Output how many games were deleted
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} old game(s) deleted.'))
