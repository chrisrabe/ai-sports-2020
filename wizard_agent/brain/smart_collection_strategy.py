from typing import List
import operator
from . import strategy
from .utils import util_functions as utils, constants

'''
Strategy: 

Retreive location of ammo and treasure blocks, 
find the tile with highest score, and get 
corresponding ideal path.

'''


class SmartCollectionStrategy(strategy.Strategy):
    def __init__(self):
    	self.ammo_state = {}
    	self.prev_bombs = []

        self.game_state = None
        self.player_state = None

        # value between 0-1, closer to 1 means it's more likely to go to tile
        self.ammo_priority = 0.5
        self.treasure_priority = 1
        self.reachable_priority = 1
        self.urgent_priority = 1

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        
        location = player_state.location
        ammo_blocks = game_state.ammo
        treasure_blocks = game_state.treasure
        bombs = game_state.bombs

        exploded_bombs = self.get_exploded_bombs(bombs)
        self.prev_bombs = bombs

        empty_near_ammo = self.get_empty_near_blocks(ammo_blocks)
        empty_near_treasure = self.get_empty_near_blocks(treasure_blocks)
        all_empty = empty_near_ammo + empty_near_treasure
 

        # retrieve the best tile
        ideal_tile = self.get_ideal_tile(all_empty, empty_near_ammo, empty_near_treasure, location)

        # navigate to ideal tile
        if ideal_tile is not None:
            path = utils.get_shortest_path(location, ideal_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            return action_seq

        return [constants.ACTIONS["none"]]
    
    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state

        location = player_state.location
        ammo = player_state.ammo
        ammo_blocks = game_state.ammo
        treasure_blocks = game_state.treasure
        empty_near_ammo = self.get_empty_near_blocks(ammo_blocks)
        empty_near_treasure = self.get_empty_near_blocks(treasure_blocks)
        all_empty = empty_near_ammo + empty_near_treasure
        reachable_tiles = utils.get_reachable_tiles(location, all_empty, game_state)
        return ammo > 0 and reachable_tiles


    def get_ideal_tile(self, all_empty, empty_near_ammo, empty_near_treasure, location):
        opponent_list = self.game_state.opponents(self.player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        tile_map = self.get_tile_map(all_empty, empty_near_ammo, empty_near_treasure, location)
        p_tile_map = dict(sorted(tile_map.items(), key=operator.itemgetter(1), reverse=True))
        possible_tiles = list(p_tile_map.keys())
        ideal_tile = None
        while len(possible_tiles) > 0:
            tile = possible_tiles.pop(0)
            if not utils.is_opponent_closer(location, opponent, tile):
                ideal_tile = tile
                break
        return ideal_tile

    def get_tile_map(self, all_empty, empty_near_ammo, empty_near_treasure, location):
        tile_map = {}
        for tile in all_empty:
            score = self.get_score(tile, empty_near_ammo, empty_near_treasure, location)
            if tile in tile_map:
                tile_map[tile] += score
            else:
                tile_map[tile] = score
        return tile_map

    def get_score(self, tile, empty_near_ammo, empty_near_treasure, location):
        path = utils.get_shortest_path(location, tile, self.game_state)
        score = 0

        # ensure that tile is reachable by putting reward / punishment
        if path is not None:
            score += self.reachable_priority
        else:
            score -= self.reachable_priority

        if tile in empty_near_ammo:
            score += self.ammo_priority
        if tile in empty_near_treasure:
            score += self.treasure_priority

        return score

    def get_empty_near_blocks(self, blocks):
        empty_near_blocks = []
        for tile in blocks:
            empty_surround = utils.get_surrounding_empty_tiles(tile, self.game_state)
            empty_near_blocks = empty_near_blocks + empty_surround
        return empty_near_blocks
