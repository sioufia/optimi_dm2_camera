from pyscipopt import Model, quicksum
from parser import parser, get_grid_dimensions
from datetime import datetime

model = Model("Cameras")
# cams_caracs: ((a,b),(a',b')) a is the capacity radius and b the cost of the camera
# artworks: [(x1, y1), (x2, y2) ...]
cams_caracs, artworks = parser("input_9.txt")
width, height = get_grid_dimensions(artworks)

# variables = ()


class Disk(object):
    def __init__(self, center_x, center_y, radius):
        self.__x = center_x
        self.__y = center_y
        self.__radius = radius

    def isInDisk(self, x, y):
        return (x - self.__x) ** 2 + (y - self.__y) ** 2 <= self.__radius ** 2


def get_cams_in_radius(x, y, vars, cams, radius):
    cams_in_radius = []
    disk = Disk(x, y, radius)
    for index, cam in enumerate(cams):
        if disk.isInDisk(cam[0], cam[1]):
            cams_in_radius.append(vars[index])
    return cams_in_radius

# boolean variables corresponding to the cameras, corresponding to the pattern
# [(x, y, radius), ...]
cams = []
for j in range(height):
    for i in range(width):
        cams.append((i, j, cams_caracs[0][0]))
        cams.append((i, j, cams_caracs[1][0]))

vars = []
for var in cams:
    vars.append(model.addVar("cam", vtype="B"))

# need to filter the cams to ensure they are close from some artwork (maybe use isInDisk util ?)
# need to add constraints to ensure all artworks are covered

for index, artwork in enumerate(artworks):
    if index % 100 == 0:
        print(index)
    # a camera must be around in a dertermined radius
    t1 = datetime.now()
    cams_in_radius_1 = get_cams_in_radius(artwork[0], artwork[1], vars, cams, cams_caracs[0][0])
    t2 = datetime.now()
    cams_in_radius_2 = get_cams_in_radius(artwork[0], artwork[1], vars, cams, cams_caracs[1][0])
    t3 = datetime.now()
    model.addCons(quicksum(var for var in cams_in_radius_1) + quicksum(var for var in cams_in_radius_2) >= 1)
    t4 = datetime.now()
    print("D3:", t4 - t3, "D2:", t3 - t2, "D1:", t2 - t1,)
    # CONS = get_number_of_cams_in_radius(artwork[0], artwork[1], cams, cams_caracs[0][0]) + get_number_of_cams_in_radius(artwork[0], artwork[1], cams, cams_caracs[1][0]) >= 1
    # print(CONS)
    # model.addCons(CONS)


cams1 = [cam for cam in cams if cam[2] == cams_caracs[0][0]]
cams2 = [cam for cam in cams if cam[2] == cams_caracs[1][0]]
costs_sum = len(cams1) * cams_caracs[0][1] + len(cams2) * cams_caracs[1][1]
model.setObjective(costs_sum, "minimize")
model.optimize()

if model.getStatus() != 'optimal':
    print('LP is not feasible')
else:
    print("Optimal value : ", model.getObjVal())
