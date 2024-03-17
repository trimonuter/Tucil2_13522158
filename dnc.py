from typing import List
import matplotlib.pyplot as plt
from termcolor import colored
from PIL import Image
from datetime import datetime
import time
import sys
import os

class Point():
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

class BezierCurve():
    def __init__(self, iterations: int) -> None:
        self.iterations: int = iterations
        self.iterationsList: List[List[Point]] = [[] for _ in range(iterations + 1)]
    
    def midpoint(self, A: Point, B: Point) -> Point:
        new_x: float = (A.x + B.x) / 2
        new_y: float = (A.y + B.y) / 2
        
        return Point(new_x, new_y)
    
    def reduce(self, arr: List[Point], left: List[Point], right: List[Point], iter: int) -> List[Point]:
        if iter == 0:
            self.iterationsList[iter] += left + right
        if self.iterations == 0:
            return []
        
        left_arr: List[Point] = [arr[0]]
        right_arr: List[Point] = [arr[len(arr) - 1]]
        
        while len(arr) > 1:
            new_arr: List[Point] = []
            for i in range(len(arr) - 1):
                new_arr.append(self.midpoint(arr[i], arr[i + 1]))
            
            left_arr += [new_arr[0]]
            right_arr = [new_arr[len(new_arr) - 1]] + right_arr
            arr = new_arr
            
        self.iterationsList[iter + 1] += left + arr + right
        if iter == self.iterations - 1:
            return arr
        else:
            iter += 1
            return self.reduce(left_arr + arr, left, arr, iter) + arr + self.reduce(arr + right_arr, [], right, iter)

def plot_graph(control: List[Point], curve: List[Point], iter: int):
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
    plt.title(f'Bezier Curve - Iteration {iter}')
    plt.legend()
    plt.grid(True)
    
def get_datetime():
    return str(datetime.now().time())[:8].replace(':', '_')

def create_gif(bez: BezierCurve, control: List[Point]):
    # Initialize variables
    datetime = get_datetime()
    filename = f'{datetime}'
    foldername = f'plot/{datetime}'
    os.makedirs(foldername)
    n = bez.iterations
    
    # Iterate through bezier curves and save iteration as image
    images: List[Image.Image] = []
    for i in range(n + 1):
        filename_i = f'{foldername}/{filename}_iter{i}'
        curve_i = bez.iterationsList[i]
        
        plot_graph(control, curve_i, i)
        
        plt.savefig(filename_i)
        images.append(Image.open(filename_i + '.png'))
        plt.close('all')
        
    # Compile all images as gif
    images[0].save(f'{foldername}/{filename}.gif', save_all=True, append_images=images[1:], loop=0, duration=1000)
    
    # Return filename
    return f'{foldername}/{filename}.gif'

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
        break
    
    # Check if input is two numbers
    if len(inp) != 2:
        slowprint(colored('Only input two numbers (x y)!', 'red'))
    else:
        try:
            # Create control point and put in control array
            point = Point(int(inp[0]), int(inp[1]))
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
    
    # Check if input is one numbers
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
        
# Get starting time
start = time.time()

# Initialize Bezier curve generation
bez = BezierCurve(iterations)
curve = [control[0]] + bez.reduce(control, [control[0]], [control[len(control) - 1]], 0) + [control[len(control) - 1]]

# Get calculation duration
duration = time.time() - start
slowprint('Duration: ' + colored(str(duration) + ' sec', 'yellow'))

# Create and open gif
gif = create_gif(bez, control)
open_gif = Image.open(gif)

open_gif.show()

# control = [
#     Point(5, 5), 
#     Point(6, 0), 
#     Point(16, 5), 
#     Point(12, 7),
#     Point(3, 11),
#     Point(-1, 13),
#     Point(9, 18),
#     Point(10, 13)
# ]
# control = [
#     Point(10, 5),
#     Point(15, 15),
#     Point(20, 0),
#     Point(25, 10)
# ]

# start = time.time()
# bez = BezierCurve(10)
# curve = [control[0]] + bez.reduce(control, [control[0]], [control[len(control) - 1]], 0) + [control[len(control) - 1]]

# x_control = [p.x for p in control]
# y_control = [p.y for p in control]

# x_curve = [p.x for p in curve]
# y_curve = [p.y for p in curve]

# duration = time.time() - start
# print(f'Duration: {duration} seconds')
# # Plot the points
# plt.plot(x_control, y_control, label='Control points')

# plt.plot(x_curve, y_curve, '-o', label='Bezier curve')

# # Add labels and title
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Curve Through Points')
# plt.legend()
# plt.grid(True)

# # Show the plot
# plt.show()