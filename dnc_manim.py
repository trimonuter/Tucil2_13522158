from manim import *

class MyPoint():
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        
class PointAnimation(Scene):
    def __init__(self):
        self.dots: List[Dot] = []
        
    def construct(self):
        control = [
            MyPoint(100, 300),
            MyPoint(200, 50),
            MyPoint(300, 300),
            MyPoint(400, 50),
            MyPoint(500, 300),
        ]

        iterations = 1
        max_x, max_y = self.getMax(control)
        control = self.normalize(control, max_x, max_y)
        
        avg = self.getAverage(control)
        control = self.shift(control, avg)
        
        self.reduce(control, control[0], control[len(control) - 1], 0, iterations)
        
    def reduce(self, arr: List[MyPoint], left: List[MyPoint], right: List[MyPoint], iter: int, iterations: int) -> List[MyPoint]:
        left_arr: List[MyPoint] = [arr[0]]
        right_arr: List[MyPoint] = [arr[len(arr) - 1]]
        
        dots: List[Dot] = []
              
        while len(arr) > 1:
            for point in arr:
                dot = Dot(color=WHITE, radius=0.25).move_to([point.x, point.y, 0])
                dots.append(dot)
                self.play(Create(dot))
                
            new_arr: List[MyPoint] = []
            for i in range(len(arr) - 1):
                new_arr.append(self.midpoint(arr[i], arr[i + 1]))
                
                # Create line
                line = Line(dots[i].get_center(), dots[i + 1].get_center(), color=YELLOW, z_index=-999)
                
                self.play(Create(line))
                
                # Create midpoint
                mid_loc = self.midpoint(arr[i], arr[i + 1])
                midpoint = Dot(color=BLUE, radius=0.2).move_to([mid_loc.x, mid_loc.y, 0])
                
                self.play(Create(midpoint))
            
            left_arr += [new_arr[0]]
            right_arr = [new_arr[len(new_arr) - 1]] + right_arr
            arr = new_arr
            
        if iter == iterations - 1:
            return arr
        else:
            iter += 1
            return self.reduce(left_arr + arr, left, arr, iter, iterations) + arr + self.reduce(arr + right_arr, [], right, iter, iterations)
    
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
            point.x *= (10 / max_x)
            point.y *= (5 / max_y)
            
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