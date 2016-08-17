#!  /Users/edelsonc/anaconda/bin/python
"""Bit Map Drawer for ppm style files"""
from math import sqrt
from sys import argv



def grid_draw(d1, d2, r, g, b):
    """Creates and empty grid for Netpbm image formating

    Arguments
    --------
    d1, d2 -- height and width of grid
    """
    grid = []
    for i in range(d2):
        row = []
        for j in range(d1):
            row.append([r, g, b])
        grid.append(row)

    return grid


def write_ppm(grid, file, grid_dim):
    """Writes a grid with points to the image file in .ppm formate

    Arguments
    --------
    grid -- grid with rgb values
    file -- write to file
    """
    image_file = open(file, 'w')
    image_file.write("P3\n%r %r\n255\n" % (grid_dim[0], grid_dim[1]))

    for row in grid:
        for column in row:
            image_file.write("%r %r %r " % (column[0], column[1], column[2]))
        image_file.write("\n")


def draw_point(r, g, b, m, n, grid):
    """Draws a point on the ppm grid

    Arguments
    ---------
    r, g, b -- RGB values for the point
    m, n -- row, column
    grid -- ppm grid being edited
    """
    grid[m][n][0], grid[m][n][1], grid[m][n][2] = r, g, b

    return grid


def draw_rectangle(r, g, b, m, n, height, width, grid):
    """Draws a rectangle on the ppm grid

    Arguments
    ---------
    r,g,b -- RGB values
    m, n -- start point
    height, width -- rectangle hight and width
    grid -- ppm grid to be edited
    """
    rect = grid_draw(width, height, r, g, b)
    for i in range(height):
        for j in range(width):
            grid[m+i][n+j] = rect[i][j]
    return grid


def draw_line(r, g, b, y1, x1, y2, x2, grid):
    """Draws a line on the ppm grid

    Arguments
    --------
    r, g, b -- RGB values for line
    m1, n1 -- start point of line
    m2, n2 -- end point of line
    grid -- ppm grid
    """
    dx = x2 - x1
    dy = y2 - y1
    x = [x for x in range(x1, x2+1)]

    for x_i in x:
        y_i = y1 + dy*(x_i - x1) / (dx + 10**-15)
        grid[round(y_i)][x_i] = [r, g, b]

    return grid


def draw_circle(r, g, b, y, x, radius, grid):
    """Draws a circle on the ppm grid

    Arguments
    ---------
    r, g, b -- RGB values
    y, x, radius -- center of the circle with radius radius
    grid -- ppm grid
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):

            distance = sqrt((i-y)**2 + (j-x)**2)

            if distance <= radius:
                grid[i][j] = [r, g, b]

            else:
                pass

    return grid


def main():

    try:
        file = argv[1]
    except IndexError:
        raise ValueError("No write to file argument specified")
    
    # retrieve the input dimensions from user
    print("Welcome to the bitmap drawer!")
    print("What size image are you making (in pixels)?") 
    grid_dim = [ 
        int(x) for x in input("Width(w) Height(h)-> " ).strip().split(" ")
        ]


    # create starting blank grid
    print("Creating your grid...")
    grid = grid_draw(grid_dim[0], grid_dim[1], 0, 0, 0)
    print("...done!")
    print("When you're done, just hit enter. For help, type \"help\"")

    # while loop for user drawing input
    line = input("\t-> ")
    while line != "":
        if "point" in line:
            draw = line.strip().split(" ")
            grid = draw_point(int(draw[1]), int(draw[2]), int(draw[3]),
                int(draw[4]), int(draw[5]), grid)

        elif "rect" in line:
            draw = line.strip().split(" ")
            grid = draw_rectangle(int(draw[1]), int(draw[2]), int(draw[3]),
                int(draw[4]), int(draw[5]), int(draw[6]), int(draw[7]), grid)

        elif "line" in line:
            draw = line.strip().split(" ")
            grid = draw_line(int(draw[1]), int(draw[2]), int(draw[3]),
                int(draw[4]), int(draw[5]), int(draw[6]), int(draw[7]), grid)

        elif "circle" in line:
            draw = line.strip().split(" ")
            grid = draw_circle(int(draw[1]), int(draw[2]), int(draw[3]),
                int(draw[4]), int(draw[5]), int(draw[6]), grid)
        
        elif line == "help":
            print("Here are the options:")
            print("\tpoint r g b h-pixel w-pixel")
            print("\trect r g b h-pixel w-pixel hight width")
            print("\tline r g b h-start w-start h-end w-end")
            print("\tcircle r g b h-center w-center radius\n")

        else:
            print("NOT A VALID INPUT")

        line = input("\t-> ")

    write_ppm(grid, file, grid_dim)

if __name__ == "__main__":
    main()