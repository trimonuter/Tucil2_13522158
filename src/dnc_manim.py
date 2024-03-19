from manim import *

class MyPoint():
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

class PointAnimation(Scene):
    def construct(self):
        # Get control points and iterations from file
        with open('manim.txt', 'r') as file:
            # Number of iterations
            iterations = int(file.readline())
            
            # Control points
            control = []
            line = file.readline()
            while line != '':
                line = line.split(' ')
                control.append(MyPoint(float(line[0]), float(line[1])))
                
                line = file.readline()
        
        # Normalize coordinates to -1 <= x <= 1
        max_x, max_y = self.getMax(control)
        control = self.normalize(control, max_x, max_y)
        
        # Move points to the center of the screen
        avg = self.getAverage(control)
        control = self.shift(control, avg)
        
        # Set camera frame size
        self.set_frame_size(control)
        
        # Start recursive Bezier curve generation
        global iterationsList
        iterationsList = [[] for _ in range(iterations)]
        
        global rightmost
        rightmost = control[len(control) - 1]
        
        self.reduce(control, [control[0]], [control[len(control) - 1]], 0, iterations)
        
    def reduce(self, arr: List[MyPoint], left: List[MyPoint], right: List[MyPoint], iter: int, iterations: int) -> List[MyPoint]:
        left_arr: List[MyPoint] = [arr[0]]
        right_arr: List[MyPoint] = [arr[len(arr) - 1]]
              
        dots: List[Dot] = []
        while len(arr) > 1:
            # Fill dots array if empty
            if len(dots) == 0:
                for point in arr:
                    dot = Dot(color=WHITE, radius=0.25).move_to([point.x, point.y, 0])
                    dots.append(dot)
                    if point not in left + right or not iter:
                        self.play(Create(dot))
            
            # Iterate through arr to get midpoints
            new_arr: List[MyPoint] = []
            new_dots: List[Dot] = []
            lines: List[Line] = []
            for i in range(len(arr) - 1):
                # Append midpoint to new_arr
                new_arr.append(self.midpoint(arr[i], arr[i + 1]))
                
                # Create line
                line = Line(dots[i].get_center(), dots[i + 1].get_center(), color=YELLOW, z_index=-999)
                lines.append(line)
                
                self.play(Create(line))
                
                # Create midpoint
                mid_loc = self.midpoint(arr[i], arr[i + 1])
                midpoint = Dot(color=BLUE, radius=0.2).move_to([mid_loc.x, mid_loc.y, 0])
                new_dots.append(midpoint)
                
                self.play(Create(midpoint))
                
                # Delete current dot from screen
                if arr[i] != right[0]:
                    if not left or arr[i] != left[0]:
                        self.play(FadeOut(dots[i]))
            
            # Delete last dot
            last_point = arr[len(arr) - 1]
            if last_point != right[0]:
                self.play(FadeOut(dots[len(dots) - 1]))
                
            # Add to left_arr and right_arr
            left_arr += [new_arr[0]]
            right_arr = [new_arr[len(new_arr) - 1]] + right_arr
            arr = new_arr
            
            # Clear lines from screen
            for l in lines:
                self.play(FadeOut(l))
                
            # Make new_dots as dots
            for d in new_dots:
                d.set_color(WHITE)
            dots = new_dots
         
        # Draw current iteration of points
        global iterationsList
        iterationsList[iter] += left + arr + right
        
        global rightmost
        lines = []
        if right[0] == rightmost:
            for i in range(len(iterationsList[iter]) - 1):
                point_1: MyPoint = iterationsList[iter][i]
                point_2: MyPoint = iterationsList[iter][i + 1]
                
                coord_1: List[float] = [point_1.x, point_1.y, 0]
                coord_2: List[float] = [point_2.x, point_2.y, 0]
                
                line = Line(coord_1, coord_2, color=YELLOW, z_index=-999)
                lines.append(line)
                
                self.play(Create(line))
                
            self.wait(3)
            for l in lines:
                self.play(FadeOut(l))
                
        # Continue to next iteration   
        if iter == iterations - 1:
            return arr
        else:
            iter += 1
            return self.reduce(left_arr, left, arr, iter, iterations) + arr + self.reduce(right_arr, [], right, iter, iterations)
    
    def midpoint(self, A: MyPoint, B: MyPoint) -> MyPoint:
        new_x: float = (A.x + B.x) / 2
        new_y: float = (A.y + B.y) / 2
        
        return MyPoint(new_x, new_y)
    
    def getMax(self, arr: List[MyPoint]):
        max_x: float = 0
        max_y: float = 0
        
        for point in arr:
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y
        
        return (max_x, max_y)

    def normalize(self, arr: List[MyPoint], max_x: int, max_y: int):
        for point in arr:
            point.x *= (10 / max_x) if max_x else 1
            point.y *= (5 / max_y) if max_y else 1
            
        return arr
    
    def getAverage(self, arr: List[MyPoint]):
        sum_x = 0
        sum_y = 0
        
        for point in arr:
            sum_x += point.x
            sum_y += point.y
            
        ln = len(arr)
        return MyPoint(sum_x / ln, sum_y / ln)
    
    def shift(self, arr: List[MyPoint], avg):
        for point in arr:
            point.x -= avg.x
            point.y -= avg.y
            
        return arr
    
    def set_frame_size(self, arr: List[MyPoint]):
        for point in arr:
            width = self.camera.frame_width / 2
            height = self.camera.frame_height / 2
            
            if abs(point.x) > width:
                self.camera.frame_width = (abs(point.x) * 2) + 3
            if abs(point.y) > height:
                self.camera.frame_height = (abs(point.y) * 2) + 3