import json
import numpy as np

with open("./map_gen1.json", "r") as f:
    tmp = json.loads(f.read())
data = tmp["map"]
top = np.rot90(np.array(data["top"], dtype=object))
bottom = np.rot90(np.array(data["bot"], dtype=object))
tmp["map"]["top"] = top.tolist()
tmp["map"]["bot"] = bottom.tolist()
with open("./map_gen1_rot.json", "w") as f:
    f.write(json.dumps(tmp))
