from typing import List
import matplotlib.pyplot as plt
from termcolor import colored
from PIL import Image
from datetime import datetime
from numpy import linspace
from math import comb
import time
import sys
import os
import shutil
import subprocess

# Point
class Point():
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

# Bezier Curve
class BezierCurve():
    def __init__(self, iterations: int) -> None:
        # Number of iterations for the Bezier curve
        self.iterations: int = iterations
        
        # Stores previous iterations of the Bezier curve
        self.iterationsList: List[List[Point]] = [[] for _ in range(iterations + 1)]
    
    # Gets the midpoint of two points
    def midpoint(self, A: Point, B: Point) -> Point:
        new_x: float = (A.x + B.x) / 2
        new_y: float = (A.y + B.y) / 2
        
        return Point(new_x, new_y)
    
    # Calculates the points of the Bezier curve using a decrease and conquer algorithm
    def reduce(self, arr: List[Point], left: List[Point], right: List[Point], iter: int) -> List[Point]:
        # If at 0th iteration -> append leftmost and rightmost point 
        if iter == 0:
            self.iterationsList[iter] += left + right
        
        # If number of iterations = 0 -> return leftmost and rightmost as control points
        if self.iterations == 0:
            return []
        
        # Initialize left array and right array for recursion
        left_arr: List[Point] = [arr[0]]
        right_arr: List[Point] = [arr[len(arr) - 1]]
        
        # Reduce the number of points from N -> (N - 1) -> ... -> 1
        while len(arr) > 1:
            # Initialize new array of midpoints
            new_arr: List[Point] = []
            
            # Append midpoints to new_arrs
            for i in range(len(arr) - 1):
                new_arr.append(self.midpoint(arr[i], arr[i + 1]))
            
            # Add leftmost and rightmost to left_arr and right_arr
            left_arr += [new_arr[0]]
            right_arr = [new_arr[len(new_arr) - 1]] + right_arr
            arr = new_arr
        
        # Add points to iterationsList
        self.iterationsList[iter + 1] += left + arr + right
        
        # If current iteration is enough, finish recursion. 
        if iter == self.iterations - 1:
            return arr
        else: # Else, call reduce method to left side and right side
            iter += 1
            return self.reduce(left_arr + arr, left, arr, iter) + arr + self.reduce(arr + right_arr, [], right, iter)
        
    # Calculates the points of the Bezier curve using a bruteforce algorithm
    def bruteforce(self, control: List[Point]):
        # Get results for all iterations from 0 to N
        for iter in range(self.iterations + 1):
            n = len(control) - 1            # Number of control points
            point_count = (2**iter) + 1     # Number of curve points
            
            t_values = list(linspace(0, 1, num=point_count))    # Number of t values
            
            # For all t values, calculate midpoint using the explicit Bezier curve formula
            for t in t_values:
                x = 0
                y = 0
                
                for i in range(n + 1):
                    point_i_x = control[i].x
                    point_i_y = control[i].y
                    
                    x += (comb(n, i) * ((1 - t)**(n - i)) * (t**i) * point_i_x)
                    y += (comb(n, i) * ((1 - t)**(n - i)) * (t**i) * point_i_y)
                    
                new_point = Point(x, y)
                self.iterationsList[iter] += [new_point]

def plot_graph(control: List[Point], curve: List[Point], iter: int, bruteforce=False):
    # Get x and y values for control points
    x_control = [p.x for p in control]
    y_control = [p.y for p in control]
    
    # Get x and y values for curve
    x_curve = [p.x for p in curve]
    y_curve = [p.y for p in curve]
    
    # Plot graph
    plt.plot(x_control, y_control, label='Control points')
    plt.plot(x_curve, y_curve, '-o', label='Bezier curve')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Bezier Curve - Iteration {iter}' if not bruteforce else f'Bezier Curve with Bruteforce - Iteration {iter}')
    plt.legend()
    plt.grid(True)
    
def get_datetime():
    return str(datetime.now().time())[:8].replace(':', '_')

def create_gif(bez: BezierCurve, control: List[Point], bruteforce=False, file=None):
    # Initialize variables
    datetime = get_datetime()
    filename = f'{datetime}' if not file else file
    foldername = f'plot/{filename}' if not bruteforce else f'plot_bruteforce/{filename}'
    os.makedirs(foldername)
    n = bez.iterations
    
    # Iterate through bezier curves and save iteration as image
    images: List[Image.Image] = []
    for i in range(n + 1):
        filename_i = f'{foldername}/{filename}_iter{i}'
        curve_i = bez.iterationsList[i]
        
        plot_graph(control, curve_i, i, bruteforce)
        
        plt.savefig(filename_i)
        images.append(Image.open(filename_i + '.png'))
        plt.close('all')
        
    # Compile all images as gif
    images[0].save(f'{foldername}/{filename}.gif', save_all=True, append_images=images[1:], loop=0, duration=1000)
    
    # Return foldername
    return (f'{foldername}', f'{filename}')

def write_to_file(control: List[Point], iterations: int):
    with open('manim.txt', 'w') as file:
        # Write iterations
        file.write(str(iterations) + '\n')
        
        # Write control points
        for i in range(len(control)):
            x = control[i].x
            y = control[i].y
            
            file.write(f'{x} {y}\n')

def render_manim(filename: str):
    # Render Manim animation
    cmd = f'manim -ql dnc_manim.py PointAnimation -o {filename}.mp4'
    subprocess.run(cmd, shell=True)

def slowprint(string: str, sleep: float = 0.03, endl=True):
    for c in string:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(sleep)
    time.sleep(0.5)
    if endl:
        print()

# Start interface
slowprint('Welcome to ' + colored('Bezier Simulator!', 'yellow'))

# Input parameters
print()
slowprint(colored('Please input the following parameters: ', 'blue'))
print()

# Input control points
slowprint(colored('Control Points', 'yellow') + ' (Input empty line to finish): ')
slowprint(colored('Format:', 'blue') + ' x y')
print()

control = []
while True:
    # Get user input
    i = len(control) + 1
    slowprint(colored(f'Point {i}: ', 'green'), endl=False)
    inp = input().split(' ')
    
    # Break loop if user input is empty
    if inp == ['']:
        if len(control) < 3:
            slowprint(colored('Please input at least 3 points!', 'red'))
            continue
        else:
            break
    
    # Check if input is two numbers
    if len(inp) != 2:
        slowprint(colored('Only input two numbers (x y)!', 'red'))
    else:
        try:
            # Create control point and put in control array
            point = Point(float(inp[0]), float(inp[1]))
            control.append(point)
        except:
            slowprint(colored('Invalid point input!', 'red'))

# Input iteration number      
iterations = 0
while True:
    # Print prompt
    print()
    slowprint(colored('Iterations: ', 'yellow'), endl=False)

    # Get user input
    inp = input().split(' ')
    
    # Check if input is one number
    if len(inp) > 1:
        slowprint(colored('Only input one number!', 'red'))
        continue
    try:
        # Check if input is negative
        if int(inp[0]) < 0:
            slowprint(colored('Only input positive values!', 'red'))
            continue
        
        # Set number of iterations
        iterations = int(inp[0])
        break
    except:
        slowprint(colored('Invalid input!', 'red'))
print()    
  
# Get starting time
start = time.time()

# Initialize Bezier curve generation
bez = BezierCurve(iterations)
curve = [control[0]] + bez.reduce(control, [control[0]], [control[len(control) - 1]], 0) + [control[len(control) - 1]]

# Get calculation duration
duration = time.time() - start
slowprint('Time taken: ' + colored(str(duration) + ' sec', 'yellow'))

# Create gif
gif = create_gif(bez, control)

# Print output
slowprint(colored('Bezier curve successfully generated at ', 'blue') + colored(gif[0], 'green'))
print()

# Write coordinates to folder
write_to_file(control, iterations)
shutil.copy('manim.txt', gif[0] + '/coordinates.txt')

# Create bruteforce curve
bez_bruteforce = BezierCurve(iterations)

start_bruteforce = time.time()
bez_bruteforce.bruteforce(control)
duration_bruteforce = time.time() - start_bruteforce
slowprint('Time taken for bruteforce method: ' + colored(str(duration_bruteforce) + ' sec', 'yellow'))

gif_bruteforce = create_gif(bez_bruteforce, control, bruteforce=True, file=gif[1])
slowprint(colored('Bezier curve (bruteforce) successfully generated at ', 'blue') + colored(gif_bruteforce[0], 'green'))

# Create Manim animation
time.sleep(0.2)
print()
slowprint(colored('Do you want to render your Bezier curve as a Manim animation?', 'blue'))
slowprint(colored('(Note: Rendering an animation will take significantly longer to finish.) [Y/y to proceed]: '), endl=False)

choice = input()
iterations = 0
print()
if choice != 'Y' and choice != 'y':
    slowprint('Program finished successfully.')
else:
    slowprint('The process of rendering the animation will take time.')
    slowprint(colored('It is highly recommended that the Bezier curve is 4 iterations or less.', 'yellow'))
    slowprint(colored('You should not animate more than 5 iterations unless you are ready to wait for the rendering process.', 'yellow'))
    
    print()
    slowprint('You can reduce the amount of iterations you want to animate with the prompt below.')
    print()
    
    while True:
        slowprint(colored('Insert the amount of iterations you want to animate: ', 'yellow'), endl=False)
        inp = input().split(' ') 
        
        # Check if input is one number
        if len(inp) != 1:
            slowprint(colored('Input only a single number!', 'red'))
        else:
            try:
                iterations = int(inp[0])
                write_to_file(control, iterations)
                render_manim(gif[1])
                break
            except:
                slowprint(colored('Invalid point input!', 'red'))