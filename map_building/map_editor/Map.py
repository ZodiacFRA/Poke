import map_utils


class Map(object):
    def __init__(self, map_json_path, backdrop, crop):
        """TODO: Create a map the size of the biggest between the backdrop and the json map"""
        self.backdrop = backdrop
        self.map, self.t_size = map_utils.load_map_from_json(map_json_path, crop=crop)

    def get(self, layer, t_pos):
        return self.map[layer][t_pos.y][t_pos.x]

    def set(self, layer, t_pos, entity_data):
        self.map[layer][t_pos.y][t_pos.x] = entity_data
        # print(f"Setting {entity_data} at {t_pos} on {layer}")

    def is_valid_t_pos(self, t_pos):
        if (
            t_pos.x < 0
            or t_pos.y < 0
            or t_pos.x >= self.t_size.x
            or t_pos.y >= self.t_size.y
        ):
            return False
        else:
            return True
