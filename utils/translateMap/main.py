import json

def is_bot(value):
	for i in range(len(bot)):
		if value == bot[i]:
			return True
	return False

def is_door(value):
	for i in range(len(door)):
		if value == door[i]:
			return True
	return False

def is_top(value):
	for i in range(len(top)):
		if value == top[i]:
			return True
	return False


map_src_file = open("map_out.json")
map_data = json.load(map_src_file)

dic_file = open("dict.json")
dic_data = json.load(dic_file)

bot_data = dic_data["bot"]
top_data = dic_data["top"]

bot = bot_data["ground"] + bot_data["water"] + bot_data["cutable_tree"] + bot_data["door"]
top = top_data["wall"] + top_data["houses"] + top_data["jumpable_wall"] + top_data["league_wall"] + top_data["mountain"] + top_data["panel"]
door = bot_data["door"]

bot_final = []
top_final = []

for row in map_data["map"]:
	tmp_row_bot = []
	tmp_row_top = []
	for sprite_idx in row:
		if is_bot(sprite_idx) or is_top(sprite_idx):
			if is_bot(sprite_idx):
				obj = ("ground", sprite_idx)
				tmp_row_bot.append(obj)
			else:
				obj = ("wall", sprite_idx)
				tmp_row_top.append(obj)
		else:
			obj = ()
			tmp_row_bot.append(obj)
			tmp_row_top.append(obj)
	bot_final.append(tmp_row_bot)
	top_final.append(tmp_row_top)
	

# Print in JSON - HARDCODE BECAUSE TIRED
print("{")
print("\t\"map\": {")
print("\t\t\"top\": ", top_final)
print("\t\t\"bottom\": ", bot_final)
print("\t}")
print("}")

