from pyscipopt import Model, quicksum
from parser import parser, get_grid_dimensions

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

def get_number_of_cams_in_radius(x, y, cams, radius):
    n = 0
    disk = Disk(x, y, radius)
    for cam in cams:
        if disk.isInDisk(cam[0], cam[1]):
            n += 1
    return n

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

for artwork in artworks:
    CONS = get_number_of_cams_in_radius(artwork[0], artwork[1], cams, cams_caracs[0][0]) + get_number_of_cams_in_radius(artwork[0], artwork[1], cams, cams_caracs[1][0]) >= 1
    print(CONS)
    model.addCons(CONS)


cams1 = [cam for cam in cams if cam[2] == cams_caracs[0][0]]
cams2 = [cam for cam in cams if cam[2] == cams_caracs[1][0]]
costs_sum = len(cams1) * cams_caracs[0][1] + len(cams2) * cams_caracs[1][1]
model.setObjective(costs_sum, "minimize")
model.optimize()

if model.getStatus() != 'optimal':
    print('LP is not feasible')
else:
    print("Optimal value : ", model.getObjVal())
