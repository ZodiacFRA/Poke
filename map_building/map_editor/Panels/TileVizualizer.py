from .Panel import Panel


class TileVizualizer(Panel):
    def __init__(self, display, px_tile_size, sprites, context):
        super().__init__(display, px_tile_size, sprites, context)