"""
CS121: Schelling Model of Housing Segregation

  Program for simulating a variant of Schelling's model of
  housing segregation.  This program takes six parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: a home at Location (k, l) is in
        the neighborhood of the home at Location (i,j) if 0 <= k < N,
        0 <= l < N, and 0 <= |i-k| + |j-l| <= R.

    similarity_satisfaction_range (lower bound and upper bound) -
         acceptable range for ratio of the number of
         homes of a similar color to the number
         of occupied homes in a neighborhood.

   patience - number of satisfactory homes that must be visited before choosing
              the last one visited.

   max_steps - the maximum number of passes to make over the city
               during a simulation.

  Sample: python3 schelling.py --grid_file=tests/a20-sample-writeup.txt --r=1
         --sim_lb=0.40 --sim_ub=0.7 --patience=3 --max_steps=1
  The sample command is shown on two lines, but should be entered on
  a single line in the linux command-line
"""

import click
import utility

def dist(location1, location2):
    '''
    Determine the distance of two locations from one another. 

    Inputs (tuples): 
        location1: first location 
        location2: second location
    Output: distance (int)
    '''

    d = abs(location1[0]-location2[0]) + abs(location1[1]-location2[1])

    return d

def similarity_score(grid, location, R):
    '''
    Calculates the similarity score for a neighborhood 

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
    Output: score (float)
    '''

    x,y = location
    S = 0
    H = 0

    for i in range(x-R, x+1+R):
        for j in range(y-R,y+1+R):
            if  i >= 0 and i < len(grid) and j >= 0 and j < len(grid):
                if dist((i, j), location) <= R:
                    if grid[i][j] == grid[x][y]:
                        S += 1
                        H += 1
                    elif grid[i][j] != "F":
                        H += 1
    
    score = S/H 

    return score

def is_satisfied(grid, R, location, sim_sat_range):
    '''
    Determine whether or not the homeowner at a specific location is
    satisfied using an R-neighborhood centered around the location.
    That is, is does their similarity score fall with the specified
    range (inclusive)

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
    Returns: bool
    '''
    
    x,y = location
    assert grid[x][y] != "F"
    lb,ub = sim_sat_range

    if lb <= similarity_score(grid, location, R) <= ub:
        return True
    else:
        return False



def find_new_home(grid, R, location, patience, sim_sat_range, homes_for_sale):
    '''
    Find and relocate homeowner to new home by placing the homeowner in a
    home for sale and checking if he is satisfied. When patience hits zero, 
    homeowner is relocated to a home where he is satisfied and city layout changes.

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        patience - number of satisfactory homes that must be visited 
        before choosing the last one visited
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score
        homes_for_sale: list of homes for sale
    Returns: updated grid, number of relocations
    '''

    x,y = location
    relocations = 0
    
    for home in homes_for_sale:
        a,b = home
        
        if patience > 1:
            grid[x][y], grid[a][b] = grid[a][b], grid[x][y] 

            if is_satisfied(grid, R, (a, b), sim_sat_range) == True:  
                patience -=1
                grid[x][y], grid[a][b] = grid[a][b], grid[x][y]     
                
            else:
                grid[x][y], grid[a][b] = grid[a][b], grid[x][y]     

        elif patience == 1:
            grid[x][y], grid[a][b] = grid[a][b], grid[x][y]

            if is_satisfied(grid, R, (a, b), sim_sat_range) == True:
                patience -=1
                homes_for_sale.insert(0,location)
                homes_for_sale.remove(home)
                relocations += 1
                break

            else:
                grid[x][y], grid[a][b] = grid[a][b], grid[x][y]
               

    return (grid, relocations)


def simulate_wave(grid, R, patience, sim_sat_range, homes_for_sale, color):
    '''
    Simulates one relocation wave for either maroon or blue homeowners

    Returns: updated grid
    '''

    counter = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == color:
                if is_satisfied(grid, R, (i,j), sim_sat_range) == False:
                    grid, relocations = find_new_home(grid, R, (i,j), patience, sim_sat_range, homes_for_sale)
                    counter += relocations

    return [grid, counter]


def simulate_step(grid, R, patience, sim_sat_range, homes_for_sale):
    '''
    Simulates one step of the simulation, where there's a maroon wave followed by a blue wave

    Returns: updated grid
    '''

    grid_after_m, maroon_relocations = simulate_wave(grid, R, patience, sim_sat_range, homes_for_sale, "M")
    
    updated_grid, blue_relocations = simulate_wave(grid_after_m, R, patience, sim_sat_range, homes_for_sale, "B")

    relocations = maroon_relocations + blue_relocations

    return (updated_grid, relocations)

def do_simulation(grid, R, sim_sat_range, patience, max_steps, homes_for_sale):
    '''

    Do a full simulation.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        max_steps (int): maximum number of steps to do
        for_sale (list of tuples): a list of locations with homes for sale

    Returns: (int) The number of relocations completed.
    '''
    steps = 0   
    total_relocations = 0

    while steps < max_steps:
        grid, relocations = simulate_step(grid, R, patience, sim_sat_range, homes_for_sale)
        if relocations == 0: 
            break 
        steps += 1
        total_relocations += relocations


    return total_relocations


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1,
              help="neighborhood radius")
@click.option('--sim_lb', type=float, default=0.40,
              help="Lower bound of similarity range")
@click.option('--sim_ub', type=float, default=0.70,
              help="Upper bound of similarity range")
@click.option('--patience', type=int, default=1, help="patience level")
@click.option('--max_steps', type=int, default=1)
def cmd(grid_file, r, sim_lb, sim_ub, patience, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)
    for_sale = utility.find_homes_for_sale(grid)
    sim_sat_range = (sim_lb, sim_ub)


    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    num_relocations = do_simulation(grid, r, sim_sat_range, patience,
                                    max_steps, for_sale)

    if len(grid) < 20:
        print("Final state of the city:")
        for row in grid:
            print(row)
        print()

    print("Total number of relocations done: " + str(num_relocations))

if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
