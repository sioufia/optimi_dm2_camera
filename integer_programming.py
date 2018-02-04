from pyscipopt import Model, quicksum
from parser import main_parser

def main():
    model = Model()

    cameras, artworks, l, c = main_parser("input_9.txt")


    #enabling cameras to have a decimal position. For example (1.4,4.9)
    possible_lines = [round(x * 0.1,1) for x in range(l)]
    possible_columns = [round(x * 0.1,1) for x in range(c)]

    #Variables are the position that can take the cameras of the 2 types. 
    grid = {(i,j):{0,1} for i in possible_lines for j in possible_columns}
    cameras1 = {(i,j):{0,1} for i in possible_lines for j in possible_columns}
    cameras2 = {(i,j):{0,1} for i in possible_lines for j in possible_columns}

    #Add the variables of the problem
    for position in cameras1:
        model.addVar("C1" + position)
    for position in cameras2:
        model.addVar("C2" + position)

    #Add the constraint of the problem
    for artwork in artworks:
        cameras1_art = getPositionAroundArtwork(artwork, cameras[0][0], grid)
        cameras2_art = getPositionAroundArtwork(artwork, cameras[1][0], grid)
        model.addCons(quicksum(cameras1[c1] for c1 in cameras1_art)+quicksum(cameras2[c2] for c2 in cameras2_art) >= 1)

    #Add the objective of the problem
    model.setObjective(quicksum(cameras[0][1]*cameras1[elt] for elt in cameras1) + quicksum(cameras[0][1]*cameras2[elt] for elt in cameras2),"minimize")

    #Model
    model.data = cameras1, cameras2
    return model

def getPositionAroundArtwork(pos_art, r_camera, grid):
    """Function that gives the positions (x,y) around an artwork depending of the coverage
    of a camera. 
    The coordonates of the results can have one decimal"""
    #First filter
    grid_lines = (pos_art[0] - r_camera, pos_art[0] + r_camera)
    grid_column = (pos_art[1] - r_camera, pos_art[1] + r_camera)
    grid_around_art = [i for i in grid if i[0] <= grid_lines[1] and i[0] >= grid_lines[0] and i[1] <= grid_column[1] and i[1] >= grid_column[0] ]

    #Second filter more precise executed on the result of the first filter
    grid_around_art2 = [ pos for pos in grid_around_art if (pos[0] - pos_art[0])**2 + (pos[1] - pos_art[1])**2 <= r_camera**2 ]
    return grid_around_art2
