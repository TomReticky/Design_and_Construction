from itertools import product
# Quantity, Length, Width, Thickness, cost, weight [milimeters, grams]
sheet_x = [3, 1500, 148.4, 0.8, 500, 483]
sheet_y = [4, 1500, 40, 0.8, 300, 128]
stringer = [8, 1500, 20, 1.5, 150, 237]

# Quantity, cost, weight [milimeters, grams]
bolt_nut = [60, 50, 2.33]

sigma_ult = 220 # [Mpa]
sigma_y = 150 # [Mpa]
E = 69700 # [Mpa]
rho = 2680 # [kg/m^3]
beams = [] #flanges, stringer up, stringerdown
flanges = []
stringers = []
reinforcestringers = 2

# for extra_flange in range(0, 2):
#     for extra_stringer in range(2, 8 , 2):
#         if extra_flange == 1:
#             for flange_position in range(0, 1):
#                 beams.append([extra_flange, extra_stringer, flange_position])
#         else:
#             beams.append([extra_flange, extra_stringer, None])

for flangenum in range(1,3):
    flangeup = flangenum
    if flangenum == 2:
        flangedown = 1
        flanges.append((flangeup,flangedown))
    else:
        for i in range(1,3):
            flangedown = i
            flanges.append(((flangeup,flangedown)))

for stringernum in range(1,4):
    for n in range(1,4):
        stringerup = n
        if stringernum == 3:
            stringerdown = 1
            stringers.append((stringerup, stringerdown, stringernum))
        else:
            for i in range(1,4):
                stringerdown = i
                stringers.append(((stringerup,stringerdown, stringernum)))



print(flanges)

data = stringers

groups = {}
for c1, c2, obj in data:
    groups.setdefault(obj, []).append((c1, c2, obj))

# 2) Sort objectnumbers to keep order
objs = sorted(groups.keys())

# 3) Build only those combinations where sum(config1+config2) ≤ 8
valid_combinations = [
    list(choice)
    for choice in product(*(groups[obj] for obj in objs))
    if sum(c1 + c2 for c1, c2, _ in choice) <= 8
]

print(f"Found {len(valid_combinations)} valid combinations.\n")
# Example:
for combo in valid_combinations[:21]:
    print(combo)
