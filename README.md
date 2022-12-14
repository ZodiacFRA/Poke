## General

#### /utils/ressources:
- full map to be used by "image to map"
- tilesheet not used atm

#### /utils/image_to_sprite_map: done by seb to cut a mapimage, split it into sprites and deduplicate them
+ output a json with all the sprites indexes placed on the map

#### /utils/sprites
sprites created by image to map, but sorted by hand into categories to create the dict.json
which is later used by translateMap to convert sprites idxes into Entities

#### /utils/sprite_map_to_map
Convert the sprites indexes json into one usable by the map loader, where the entites types have been defined


## Server

#### TODOs:
- Handle entity movement with pathfinder when movement is not used and direction is changed instead
to prevent re running the algo

- Fix dijkstra problem, if player is stuck between 3 walls and pikachu, dijkstra won't be able to find a path from the player, as pikachu is colliding -> should be ok with the collision_treshold but does not work -> to be patched


#### Workarounds:
- Set a collision idx to specifiy if the pathfinder should ignore an entity or not
(collide with trees but not with players), needed for the "scan_zone" method to ignore
living entities. MAYBE entities should be separated from the map, however this would imply
to merge the living entities in the map before serializing it and would slow down the
(to be done) method of "find_specific_entity" needed by AIs to find an entity type
in their nearby area, as instead of searching near them we would need
to search the whole array of living entities and check the distance to their position each time

## Client
