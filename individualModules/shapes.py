import math
class Point:
    definition: str = "Abstract unit that represents a location in space"
    def __init__(self, given_x: float = 0, given_y: float = 0):
        self.x: float = given_x
        self.y: float = given_y
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    def reset(self):
        self.x = 0
        self.y = 0
    def compute_distance(self, point) -> float:
        return ((self.x - point.x)**2 + (self.y - point.y)**2 )**0.5
    def compare(self, point): #Is the same point?
        return self.x == point.x and self.y == point.y
   
    def make_vector(self, point, direction=0):
        if direction == 0: #Self to point
            return (point.x - self.x, point.y - self.y)
        return (self.x - point.x, self.y - point.y)
   
    def __str__(self) -> str:
       return f"({self.x}, {self.y})"
   

class Line():
    def __init__(self, start: Point , end: Point) -> None:
        self.start = start
        self.end = end
        self.lenght = self.__compute_lenght()
        self.slope = self.__compute_slope()

        self.left = min(self.start.x, self.end.x)
        self.right = max(self.start.x, self.end.x)
        self.top = max(self.start.y, self.end.y)
        self.bottom = min(self.start.y, self.end.y)
        self._cutY = self.__calculate_cutY()

        self.vector = self.start.make_vector(self.end, 0)
    
    def get_length(self):
        return self.length

    def set_length(self, new_length):
        self.length = new_length

    def get_slope(self):
        return self.slope

    def set_slope(self, new_slope):
        self.slope = new_slope

    def __compute_lenght(self):
        return self.start.compute_distance(self.end)
    
    def __compute_slope(self):
        if self.start.x - self.end.x == 0:
            return None
        return (self.start.y - self.end.y)/ (self.start.x - self.end.x)

    def compute_horizontal_cross(self):
        return (self.left <= 0 and self.right >= 0)
    
    def compute_vertical_cross(self):
        return (self.bottom <= 0 and self.top >= 0)
    
    def __calculate_cutY(self):
        if self.slope == None:
            return None
        return self.start.y - self.slope * self.start.x

    def line_function(self, x):
        if self.left <= x <= self.right:
            b = self.start.y - self.slope * self.start.x
            return x*self.slope + b
        else:
            return None
    
    def intersection_line(self, line):
        if self.slope == None and line.slope == None:
            return self.start.x == line.start.x and (self.bottom <= line.top) and (self.top >= line.bottom)
        if line.slope == None:
            return (self.left <= line.start.x <= self.right) and (line.bottom <= self.line_function(line.start.x) <= line.top)
        if self.slope == None:
            return (line.left <= self.start.x <= line.right) and (self.bottom <= line.line_function(self.start.x) <= self.top)
            
        if self.slope == line.slope:
            return self._cutY == line._cutY and (self.left <= line.right) and (self.right >= line.left)
        
        cut_point = (line._cutY - self._cutY) / (self.slope - line.slope)
        return (self.left < cut_point < self.right) and (line.left < cut_point < line.right)

    def discretize_line(self, n:int):
        domain = self.right - self.left
        increment = domain/n

        self.equally_spaced_points = []
        if domain == 0:
            increment = (self.top - self.bottom) / n
            x=self.right
            for i in range(1, n+1):
                y = self.bottom + increment*i
                self.equally_spaced_points.append( Point(x,y) )
        else:
            for i in range(1, n+1):
                x = self.left + increment * i
                y = self.line_function(x)
                self.equally_spaced_points.append( Point(x,y) ) 

        return self.equally_spaced_points
    
    def angle(self, line):
        if self.start.compare(line.start):
            first_vector = self.start.make_vector(self.end)
            second_vector = line.star.make_vector(line.end)
        elif self.start.compare(line.end):
            first_vector = self.start.make_vector(self.end)
            second_vector = line.end.make_vector(line.start)
        elif self.end.compare(line.start):
            first_vector = self.end.make_vector(self.start)
            second_vector = line.start.make_vector(line.end)
        elif self.end.compare(line.end):
            first_vector = self.end.make_vector(self.start)
            second_vector = line.end.make_vector(line.start)
        else: return "No conection"

        product = first_vector[0]*second_vector[0] + first_vector[1]*second_vector[1]
        return math.degrees(math.acos(product /(self.lenght * line.lenght)))




class Shape():
    def __init__(self, vertices: list, edges:list) -> None:
        self.vertices = vertices
        self.edges = edges
        self.inner_angles = []
        self.compute_inner_angles()
        self.is_regular = self.__compute_is_regular()
        self.area = self.compute_area()
        self.perimeter = self.compute_perimeter()
    
    def compute_area(self):
        pass
    def compute_perimeter(self):
        return sum([edge.lenght for edge in self.edges])
    def compute_inner_angles(self):
        for i in range(0, len(self.edges)):
            self.inner_angles.append( self.edges[i-1].angle(self.edges[i])     )
    def __compute_is_regular(self):
        for i in range(len(self.inner_angles)-1):
            if not self.inner_angles[i] == self.inner_angles[i+1]:
                return False
        for j in range(len(self.edges)-1):
            if not self.edges[j].lenght == self.edges[j+1].lenght:
                return False
        return True

    def compute_interference_point(self, point:Point) -> bool:

        for start in self.vertices:
            main_vector = start.make_vector(point, 0) #Hacer vector entre cada esquina y el punto
            for vertex in self.vertices:
                line_vector = start.make_vector(vertex, 0)
                product = line_vector[0] * main_vector[0] + line_vector[1] * main_vector[1] #producto punto
                if not (product >= 0):
                    return False #La proyección debe quedar sobre el lado, si no(negativo) está por fuera
        return True

    
    def compute_interference_line(self, line):
        
        if self.compute_interference_point(line.start) or self.compute_interference_point(line.end):
            return True
        
        for i in range(len(self.edges)):
            if self.edges[i].intersection_line(line):
                return True
        return False
    
    def get_caracteristics(self):
        print("Width:", self.width)
        print("Height:", self.height)
        print("Perimeter:", self.perimeter)
        print("Area:", self.area)
        print("Points:", *[str(x) for x in self.vertices])
        print("Angles:", self.inner_angles)
        print("Is regular:", self.is_regular)
