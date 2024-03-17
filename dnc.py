from typing import List
import matplotlib.pyplot as plt
import time

class Point():
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

class BezierCurve():
    def __init__(self, nodes: int, iterations: int) -> None:
        self.nodes: int = nodes
        self.iterations: int = iterations
        self.iterationsList: List[List[Point]] = [[] for _ in range(iterations)]
    
    def midpoint(self, A: Point, B: Point) -> Point:
        new_x: float = (A.x + B.x) / 2
        new_y: float = (A.y + B.y) / 2
        
        return Point(new_x, new_y)
    
    def reduce(self, arr: List[Point], left: List[Point], right: List[Point], iter: int) -> List[Point]:
        left_arr: List[Point] = [arr[0]]
        right_arr: List[Point] = [arr[len(arr) - 1]]
        
        while len(arr) > 1:
            new_arr: List[Point] = []
            for i in range(len(arr) - 1):
                new_arr.append(self.midpoint(arr[i], arr[i + 1]))
            
            left_arr += [new_arr[0]]
            right_arr = [new_arr[len(new_arr) - 1]] + right_arr
            arr = new_arr
            
        self.iterationsList[iter] += left + arr + right
        if iter == self.iterations - 1:
            return arr
        else:
            iter += 1
            return self.reduce(left_arr + arr, left, arr, iter) + arr + self.reduce(arr + right_arr, [], right, iter)
        
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

control = [
    Point(100, 300),
    Point(200, 50),
    Point(300, 300),
    Point(400, 50),
    Point(500, 300),
]

start = time.time()
bez = BezierCurve(5, 2)
curve = [control[0]] + bez.reduce(control, [control[0]], [control[len(control) - 1]], 0) + [control[len(control) - 1]]
curve_1 = bez.iterationsList[0]

x_control = [p.x for p in control]
y_control = [p.y for p in control]

x_curve = [p.x for p in curve]
y_curve = [p.y for p in curve]

x_curve1 = [p.x for p in curve_1]
y_curve1 = [p.y for p in curve_1]

duration = time.time() - start
print(f'Duration: {duration} seconds')
# Plot the points
plt.plot(x_control, y_control, label='Control points')

plt.plot(x_curve, y_curve, '-o', label='Bezier curve')

plt.plot(x_curve1, y_curve1, linestyle='--', color='gray', label='Previous Curve')

# Add labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Curve Through Points')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()