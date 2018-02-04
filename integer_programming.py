from pyscipopt import Model, quicksum
from parser import main_parser

def main_int_prog():
    model = Model()

    cameras, artworks, l, c = main_parser("input_9.txt")


    #enabling cameras to have a decimal position. For example (1.4,4.9)
    possible_lines = [round(x * 0.1,1) for x in range(l*10 + 1)]
    possible_columns = [round(x * 0.1,1) for x in range(c*10 + 1)]

    #Variables are the position that can take the cameras of the 2 types. 
    print("Début Grid")
    grid = [(i,j) for i in possible_lines for j in possible_columns]
    print("Grid: OK")


    #Add the variables of the problem
    X = {}
    Y = {}
    D = {}
    print("Début AddVar")
    j = 0
    for artwork in artworks:
        print("artwork" + str(j))
        j+=1
        cameras1_art = getPositionAroundArtwork(artwork, cameras[0][0], grid)
        cameras2_art = getPositionAroundArtwork(artwork, cameras[1][0], grid)
        D[artwork] = (cameras1_art, cameras2_art)
        for elt in cameras2_art:
            if elt not in X:
                X[(elt[0], elt[1])] = model.addVar(name=str(elt), vtype='B')
                Y[(elt[0], elt[1])] = model.addVar(name=str(elt), vtype='B')

    print("Fin AddVar")

    #Add the constraint : each artwork should be convered by one camera at least
    i=0
    for artwork in artworks:
        print(i)
        cameras1_art = D[artwork][0]
        cameras2_art = D[artwork][0]
        model.addCons((quicksum(X[c1] for c1 in cameras1_art)+quicksum(Y[c2] for c2 in cameras2_art)) >= 1)
        i+=1
    
    print("Constraint: OK")
    
    #Add the constraint : the variables can have the values 0 or 1 (0 if there is not a camera, 1 if there is a camera)
    #for x in X:
    #    model.addCons(x <= 1)  
    #for y in Y:
    #    model.addCons(y <= 1)

    #Add the objective of the problem
    model.setObjective(quicksum(cameras[0][1]*X[elt] for elt in X) + quicksum(cameras[0][1]*Y[elt] for elt in Y),"minimize")
    print("Objective: OK")

    #Model
    model.optimize()
    print("Optimizer : OK")
    if model.getStatus() != 'optimal':
        print('Not feasible')
    else:
        for elt in X:
            print(model.getVal(X[elt]))
        for elt in Y:
            print(model.getVal(Y[elt]))

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

if  __name__=="__main__":
    a = main_int_prog()


