"""The layout is based on the default tile size (px_tile_size)
All distances / positions prefixed with t_ are in tiles unit
All distances / positions prefixed with px_ are in pixels"""
from Vector2 import Vector2

px_tile_size = 32

t_map_editor_panel_size = Vector2(32, 32)
t_tile_vizualizer_size = Vector2(8, 11)
t_sprite_selection_panel_size = Vector2(
    t_tile_vizualizer_size.x, t_map_editor_panel_size.y - t_tile_vizualizer_size.y - 1
)

# The layout defines the window size
t_window_size = Vector2(
    t_map_editor_panel_size.x + 1 + t_tile_vizualizer_size.x,
    t_map_editor_panel_size.y,
)
