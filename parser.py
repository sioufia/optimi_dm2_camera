def parser(filename):
    """Function that parses the entry doc into 2 variables:
       - cameras is under the format : ((a,b),(a',b')) a is the capacity radius and b the cost of the camera
       - artworks is the list of the coordinates of the artworks
       """
    with open(filename, 'r') as f:
        lines = f.readlines()
        line1 = (lines[0].replace("\n", "")).split(",")
        line2 = (lines[1].replace("\n", "")).split(",")
        cameras = ((int(line1[0]),int(line2[0])), (int(line1[1]),int(line2[1])))
        artworks = []
        for line in lines[2:]:
            line = (line.replace("\n", "")).split(",")
            artworks.append((int(line[0]), int(line[1])))
        
        return cameras, artworks