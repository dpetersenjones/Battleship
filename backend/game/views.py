import logging
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView #type: ignore
from rest_framework.permissions import AllowAny
from django.http import JsonResponse, HttpResponse
from .game import Game as GameClass
from django.views.decorators.csrf import csrf_exempt
from .models import Game as GameModel
import json

logger = logging.getLogger(__name__)

# Create your views here.
#TODO: Create Start Game View that takes the JSON of the starting position of the boats
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# @method_decorator(csrf_exempt, name='dispatch')
class StartGame(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        ###TODO: ADD GAME IS OVER RESPONSE
        game_id = request.session.get("game_id")
        if not game_id:
            return JsonResponse({"status": "no_game", "message": "No game found in session."}, status=202)
        
        try:
            game_model = GameModel.objects.get(id=game_id)
            curr_game = GameClass().deserialize(game_model)
            game_data = curr_game.serialize()
            # You decide what counts as "boats placed"
            boats_placed = any(cell != "" for row in game_data["player_board"] for cell in row)
            check = curr_game.game_over_check()
            to_send = {
                "game_over":check["game_over"],
                "winner":check["winner"],
                "player_data": {
                    "player_hits":curr_game.playerHits,
                    "player_misses":curr_game.playerMisses,
                    "player_ships":curr_game.player_board.boat_info["boats"],
                    "player_result":None
                    },
                "enemy_data": {
                    "enemy_hits":curr_game.enemyHits,
                    "enemy_misses":curr_game.enemyMisses,
                    "sunken_enemy_ships":[curr_game.enemy_board.boat_info["boats"][boattype] for boattype, ship in curr_game.enemy_board.boat_info["boats"].items() if ship["hits"] == ship["length"]],
                    "enemy_result":None
                    },
            }
            if boats_placed:
                return JsonResponse({
                    "success": True,
                    "status": "game_in_progress",
                    "message": "Game found and boats placed.",
                    "data": to_send,
                }, status=200)
            else:
                print("No data found")
                return JsonResponse({
                    "success":False,
                    "status": "awaiting_setup",
                    "message": "Game found but boats not placed.",
                    "data":None,
                }, status=200)
        except GameModel.DoesNotExist:
            return JsonResponse({
                "success":False,
                "status": "no_game", 
                "message": "No game found with stored ID.",
                "data":None,
                }, status=404)
    def post(self, request):
        try:
            pos = request.data['player_start']
            game = GameClass(pos["current"])
            game_data = game.serialize()
            game_model = GameModel.objects.create(
                player_board=game_data["player_board"],
                enemy_board=game_data["enemy_board"],
                ai_state=game_data["ai"],
                player_hits = game_data["playerHits"],
                player_misses = game_data["playerMisses"],
                enemy_hits = game_data["enemyHits"],
                enemy_misses = game_data["enemyMisses"]
            )
            request.session["game_id"] = game_model.id
            request.session.modified = True
            return JsonResponse({
                "success":True,
                "status": "success",
                "message": "Game started successfully.",
                "game_id": game_model.id,
                #TODO:Find if I need this game Data
                "data": game_data
            }, status=201)
        except KeyError as e:
            logger.error(f"In StartGame Post. Missing expected data: {str(e)}")
            return JsonResponse({
                "success":False,
                "status":"Error",
                "message": f"Missing data: {str(e)}",
                "data":None,
                }, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                "success":False,
                "status":"Error",
                "message": f"Something went wrong: {str(e)}",
                "data":None
                }, status=500)
            
#TODO: Player's shot, Create api where the player's shot is sent to the game object and then returns the enemy's attack, and if the game is over or not.
class PlayerMove(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        game_id = request.session.get("game_id")
        if not game_id:
            return JsonResponse({"detail":"Game not found"}, status=400)
        game_model = get_object_or_404(GameModel, id=game_id)
        player_shot = request.data.get("player_shot")
        curr_game = GameClass().deserialize(game_model)
        result = curr_game.processing_player_shoots(player_shot)
        enemy_shot = curr_game.enemy_shoots()
        #Check game over, serialize info and update in model, then return enemy_shot, if game is over.
        check = curr_game.game_over_check()
        game_info = curr_game.serialize()
        game_model.save_game(game_info["player_board"], game_info["enemy_board"], game_info["ai"])
        if check["game_over"]:
            return JsonResponse({
                                "success":True,
                                "status":"data submitted",
                                "message":"Shot logged",
                                "data": {
                                    "game_over":True, 
                                    "winner":check["winner"],
                                    "enemy_data": {
                                        "enemy_shot": enemy_shot["coor"],
                                        "enemy_result": enemy_shot["hit"],
                                        "enemy_ship":result["ship"] if result["sink"] else None,
                                        },
                                    "player_data":{
                                        "player_shot":player_shot,
                                        "player_result":result,
                                        },
                                    },
                                }, status=200)
        
        return JsonResponse({
                            "success":True,
                            "status":"data submitted",
                            "message":"Shot logged",
                            "data": {
                                "game_over":False, 
                                "winner":None,
                                "enemy_data": {
                                    "enemy_shot": enemy_shot["coor"],
                                    "enemy_result": enemy_shot["hit"],
                                    "enemy_ship":result["ship"] if result["sink"] else None,
                                    },
                                "player_data":{
                                    "player_shot":player_shot,
                                    "player_result":result,
                                    },
                                },
                            }, status=200)

class DeleteGame(APIView):
    permission_classes = [AllowAny]
    def delete(self, request):
        game_id = request.session.get("game_id")
        if not game_id:
            return JsonResponse({
                "success":False,
                "status":"Error",
                "message":"Game not found",
                "data":None,
                }, status=400)
        game_model = get_object_or_404(GameModel, id=game_id)
        game_model.delete()
        return JsonResponse({
            "success":True,
            "status":"game deleted",
            "message":"Game has been successfully deleted",
            "data":None,
            }, status=201)