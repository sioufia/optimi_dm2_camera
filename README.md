Readme of the DM2 of optimisation project.

## Integer Programming method:

    Steps to run it:
        1/ Go to the folder optimi_dm2_camera via your terminal
        2/ Launch the integer_programming.py file with python: python integer_programming.py

    Explanations:
    The variables of the problem are X and Y.
    X is a list of coordinates of all the grid (800 x 800) --> It can takes the values:
        - 1 if there is a camera of type 1 in this position
        - 0 if not
    Y is the same but for the cameras of type 2

    The constraint is to have for each artwork a camera which covers it.

    The objective is to minimize the cost of the camera.

    Results: cost of 2680

## Local search:

    1. We take the same modelisation as we did with integer programming : X and Y set of variables for the two different types of cameras at each integer coordinate of the grid.
    2. We set each of those boolean variables to 1, ensuring we got a valid solution (the cameras are all covered by the artwork).
    4. We compute the total cost of this solution.
    5. We try to remove a random camera.
    6. We check that all the artwork is still covered by checking that each artwork item got a camera around (of type 1 or 2). If it's not the case, we put back the camera in the list and go back to step 5.
    7. We compute the cost of the new solution. If it's more expensive that the last cost, we put back the camera and go to step 5. If it's not, we just go to step 5 (our valid solution has now one camera less)
    8. We stop that loop when we reach a cost that is low enough (and that we've decided before). The lower this cost will be, the longer the solution might take to compute (it might even be impossible if it's lower than the optimal cost)

    We can also consider a cheaper solution by setting a list, for each artwork, of the cameras that covers it. Then when we remove a camera randomly, we just ensure that this list is not empty for all artwork items instead of looking for cameras for each artwork to ensure that our solution is still valid.
