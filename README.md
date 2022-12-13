## Org

#### image to map: done by seb to cut an image, split it into sprites and deduplicate them
+ output a json with all the sprites indexes

#### ressources:
full map to be used by "image to map"
tilesheet not used atm

#### sprites
sprites created by image to map, but sorted by hand into categories to be able to generate
the map json

#### translateMap
Convert the sprites indexes json into one usable by the map loader, where the entites types have been defined


## Server

#### TODOs:
- handle entity movement with pathfinder when movement is not used and direction is changed instead
to prevent re running the algo


#### Workarounds:
- Set a collision idx to specifiy if the pathfinder should ignore an entity or not
(collide with trees but not with players), needed for the "scan_zone" method to ignore
living entities. MAYBE entities should be separated from the map, however this would imply
to merge the living entities in the map before serializing it and would slow down the
(to be done) method of "find_specific_entity" needed by AIs to find an entity type
in their nearby area, as instead of searching near them we would need
to search the whole array of living entities and check the distance to their position each time

## Client
