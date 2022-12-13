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