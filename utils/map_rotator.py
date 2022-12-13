import numpy as np
import json

with open("./map_gen1.json", "r") as f:
    tmp = json.loads(f.read())
data = tmp["map"]
top = np.array(data["top"], dtype=object)
bottom = np.array(data["bot"], dtype=object)
print(top)
print(bottom)
top = np.rot90(top)
bottom = np.rot90(bottom)
tmp["map"]["top"] = top.tolist()
tmp["map"]["bot"] = bottom.tolist()
with open("./map_gen1_rot.json", "w") as f:
    f.write(json.dumps(tmp))
