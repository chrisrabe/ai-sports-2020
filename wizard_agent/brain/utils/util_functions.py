from . import constants

ACTIONS = constants.ACTIONS


def manhattan_distance(start, end):
    """
    returns the manhattan distance between two tiles, calculated as:
    |x1 - x2| + |y1 - y2|
    """
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return distance


def get_surrounding_tiles(location, game_state):
    """Given a tile location as an (x,y) tuple, this function will return the surrounding tiles up, down, left and to
    the right as a list (i.e. [(x1,y1), (x2,y2),...]) as long as they do not cross the edge of the map """
    x = location[0]
    y = location[1]

    # find all the surrounding tiles relative to us
    # location[0] = col index; location[1] = row index
    tile_up = (x, y - 1)
    tile_down = (x, y + 1)
    tile_left = (x - 1, y)
    tile_right = (x + 1, y)

    # combine these int a list
    all_surrounding_tiles = [tile_up, tile_down, tile_right, tile_left]

    # get ones that are within bounds
    valid_surrounding_tiles = []

    for tile in all_surrounding_tiles:
        if game_state.is_in_bounds(tile):
            valid_surrounding_tiles.append(tile)

    return valid_surrounding_tiles


def get_empty_tiles(tiles, game_state):
    """
    Given a list of tiles, return ones that are actually empty
    """
    empty_tiles = []

    for tile in tiles:
        if not game_state.is_occupied(tile):
            empty_tiles.append(tile)

    return empty_tiles


def get_safest_tile(location, tiles, bombs):
    """
    Given a list of tiles and bombs, find the tile that's safest to move to
    """

    bomb_distance = 10
    closest_bomb = bombs[0]

    for bomb in bombs:
        new_bomb_distance = manhattan_distance(bomb, location)
        if new_bomb_distance < bomb_distance:
            bomb_distance = new_bomb_distance
            closest_bomb = bomb

    safe_dict = {}
    for tile in tiles:
        distance = manhattan_distance(closest_bomb, tile)
        safe_dict[tile] = distance

    # return the tile with the furthest distance from any bomb
    safest_tile = max(safe_dict, key=safe_dict.get)

    return safest_tile


def move_to_tile(location, tile):
    """
    Determines the action based on the tile. The other tile must be adjacent to the location tile
    """
    diff = tuple(x - y for x, y in zip(location, tile))

    if diff == (0, 1):
        return ACTIONS["down"]
    elif diff == (1, 0):
        return ACTIONS["left"]
    elif diff == (0, -1):
        return ACTIONS["up"]
    elif diff == (-1, 0):
        return ACTIONS["right"]
    else:
        return ACTIONS["none"]
