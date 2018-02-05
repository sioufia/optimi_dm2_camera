from pyscipopt import Model, quicksum
from parser import main_parser

def main_int_prog(input_filename, results_filename):
    model = Model()

    cameras, artworks, l, c = main_parser(input_filename)

    #Init the grid
    print("Début Grid")
    grid = [(i,j) for i in range(l+1) for j in range(c+1)]
    print("Grid: OK")


    #Add the variables of the problem.
    #X corresponds to the position of the type 1 camera (Y for type 2 camera).
    #Possible values are 1 if there is a camera at the (i,j) position, and 0 if not.
    X = {}
    Y = {}
    print("Beginning AddVar")
    for elt in grid:
        X[(elt[0], elt[1])] = model.addVar(name=str(elt), vtype='B')
        Y[(elt[0], elt[1])] = model.addVar(name=str(elt), vtype='B')
    print("End AddVar")

    #Add the constraint : each artwork should be convered by one camera at least
    for artwork in artworks:
        cameras1_art = getPositionAroundArtwork(artwork, cameras[0][0])
        cameras2_art = getPositionAroundArtwork(artwork, cameras[1][0])
        model.addCons((quicksum(X[c1] for c1 in cameras1_art)+quicksum(Y[c2] for c2 in cameras2_art)) >= 1)
    print("Constraint: OK")

    #Add the objective of the problem: 
    model.setObjective(quicksum(X[elt] for elt in X)*cameras[0][1] + quicksum(Y[elt] for elt in Y)*cameras[1][1],"minimize")
    print("Objective: OK")

    #Model
    model.optimize()
    print("Optimizer : OK")

    if model.getStatus() != 'optimal':
        print('Not feasible')
    else:
        with open(results_filename,"a") as f:
            for elt in X:
                if model.getVal(X[elt]) == 1:
                    f.write("1,"+str(elt[0])+","+str(elt[1])+"\n")      
            for elt in Y:
                if model.getVal(Y[elt]) == 1:
                    f.write("2,"+str(elt[0])+","+str(elt[1])+"\n")
        f.close()
        print("Results append to the file: OK")


def getPositionAroundArtwork(pos_art, r_camera):
    """Function that gives the positions (x,y) around an artwork depending of the coverage
    of a camera."""
    #First filter (a square around the artwork)
    grid_around_art = []
    for i in range(pos_art[0]-r_camera, pos_art[0]+r_camera+1):
        for j in range(pos_art[1]-r_camera,pos_art[1]+r_camera+1):
            if i >= 0 and j >= 0 and j<=800 and i<=800:
                grid_around_art.append((i,j))

    #Second filter more precise executed on the result of the first filter
    grid_around_art2 = [ pos for pos in grid_around_art if (pos[0] - pos_art[0])**2 + (pos[1] - pos_art[1])**2 <= r_camera**2 ]
    return grid_around_art2

if  __name__=="__main__":
    input_filename = input("Path of the input file: ")
    results_filename = input("Path of the result file: ")
    main_int_prog(input_filename, results_filename)


