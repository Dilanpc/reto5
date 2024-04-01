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




class Rectangle(Shape):
    def __init__(self, method:int, args: list) -> None:
        if method == 1:
            self.method1(*args)
            self.__define_edges()
        elif method == 2:
            self.method2(*args)
            self.__define_edges()
        elif method == 3:
            self.method3(*args)       
            self.__define_edges()
        elif method == 4:
            self.method_line(*args)
        else: print("no method")
        
        self.type = "Rectangle"

        super().__init__(self.vertices, self.edges)
        
        

    def method1(self, bottom_left, width, height):
        self.width = width
        self.height = height
        self.bottom_left = bottom_left

        self.center = Point( bottom_left.x + self.width/2, bottom_left.y + self.height/2   )
        self.bottom_right = Point(self.bottom_left.x+width, self.bottom_left.y)
        self.top_left = Point(self.bottom_left.x, self.bottom_left.y+height)
        self.top_right = Point(self.bottom_right.x, self.top_left.y)

        self.vertices = [self.bottom_left, self.top_left, self.top_right, self.bottom_right]


    def method2(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height
        self.bottom_left = Point(self.center.x-(self.width/2), self.center.y-(self.height/2))
        self.bottom_right = Point(self.bottom_left.x+width, self.bottom_left.y)
        self.top_left = Point(self.bottom_left.x, self.bottom_left.y+height)
        self.top_right = Point(self.bottom_right.x, self.top_left.y)

        self.vertices = [self.bottom_left, self.top_left, self.top_right, self.bottom_right]

    def method3(self, first_point, second_point):
        left = min(first_point.x, second_point.x)
        bottom = min(first_point.y, second_point.y)
        self.width = abs(first_point.x - second_point.x)
        self.height = abs(first_point.y - second_point.y)
        self.center = Point( left + self.width/2, bottom + self.height/2  )
        self.bottom_left = Point(left, bottom)
        self.bottom_right = Point(self.bottom_left.x+self.width, self.bottom_left.y)
        self.top_left = Point(self.bottom_left.x, self.bottom_left.y+self.height)
        self.top_right = Point(self.bottom_right.x, self.top_left.y)

        self.vertices = [self.bottom_left, self.top_left, self.top_right, self.bottom_right]

    def method_line(self, *lines):
        if len(lines) != 4:
            return False
        self.edges = lines

        self.width = lines[0].lenght 
        if self.width != lines[1].lenght:
            self.height = lines[2].lenght
        else:
            self.height = lines[1].lenght

        mostleft = lines[0].left
        mostright = lines[0].right
        mosttop = lines[0].top
        mostbottom = lines[0].bottom

        self.vertices = [line.start for line in self.edges]
        for line in self.edges:
            if mostleft > line.left:
                mostleft = line.left
            if mostright < line.right:
                mostright = line.right
            if mosttop < line.top:
                mosttop = line.top
            if mostbottom > line.bottom:
                mostbottom = line.bottom

            
        self.center = Point( mostleft + (mostright - mostleft)/2,  mostbottom + (mosttop - mostbottom)/2  )
        

    def __define_edges(self):
        self.left = self.center.x - self.width/2
        self.right = self.center.x + self.width/2
        self.top = self.center.y + self.height/2
        self.bottom = self.center.y - self.height/2
        self.edges = [Line(self.bottom_left, self.top_left), Line(self.top_left, self.top_right), Line(self.top_right, self.bottom_right), Line(self.bottom_right, self.bottom_left)]


    def compute_area(self) -> float:
        return self.width * self.height
    
    def compute_perimeter(self) -> float:
        return super().compute_perimeter()


class Square(Rectangle):
    def __init__(self, center:Point, width: float) -> None:
        super().__init__(2, [center, width, width])
        self.type = "Square"

class Triangle(Shape):
    def __init__(self, first_point:Point, second_point:Point, thrid_point:Point) -> None:
        self.vertices = [first_point, second_point, thrid_point]
        self.edges = [Line(self.vertices[0], self.vertices[1]), Line(self.vertices[1], self.vertices[2]), Line(self.vertices[2], self.vertices[0])]
        self.type = "triangle"

        super().__init__(self.vertices, self.edges)

    def compute_perimeter(self):
        return super().compute_perimeter()
    def compute_area(self):
        first_vector = self.vertices[0].make_vector(self.vertices[1])
        second_vector = self.vertices[0].make_vector(self.vertices[2])
        cross = first_vector[0] * second_vector[1] - first_vector[1] * second_vector[0]
        return abs(cross/2)
    
    def compute_interference_point(self, point: Point) -> bool:
        p = self.vertices[0].make_vector(point)
        #Expresar punto en términos de dos vectores del triángulo (lados)
        u = self.vertices[0].make_vector(self.vertices[1])
        v = self.vertices[0].make_vector(self.vertices[2])

        #t*u + q*v -> u y v vectores, t y q escalares (solucionar sistema lineal)
        q = (p[1]*u[0]**2 - u[0]*u[1]*p[0]) / (v[1]*u[0]**2 - u[0]*u[1]*v[0])
        t = (p[0] - q*v[0]) / u[0]

        return q >= 0 and t >= 0 and q+t <= 1
    
class Isosceles(Triangle):
    def __init__(self, left_bottom: Point, width:float, height:float) -> None:
        self.width = width
        self.height = height
        vertices = [left_bottom, Point(  left_bottom.x + width/2 , height + left_bottom.y  ), Point(left_bottom.x + width, left_bottom.y)]
        super().__init__(*vertices)
        

class Equilateral(Triangle):
    def __init__(self, left_bottom: Point, width:float) -> None:
        self.width = width
        self.height = (width**2 - (width**2)/4)**0.5
        vertices = [left_bottom, Point(left_bottom.x + width/2, left_bottom.y + self.height  ),  Point(left_bottom.x + width, left_bottom.y)]
        super().__init__(*vertices)
        self.is_regular = True
        

class Scalene(Triangle):
    def __init__(self, first_point: Point, second_point: Point, thrid_point: Point) -> None:
        super().__init__(first_point, second_point, thrid_point)
        self.width = max([edge.right for edge in self.edges]) - min([edge.left for edge in self.edges])
        self.height = max([edge.top for edge in self.edges]) - min([edge.bottom for edge in self.edges])

class TriRectangle(Triangle):
    def __init__(self, first_point: Point, second_point: Point) -> None:
        self.width = abs(first_point.x - second_point.x)
        self.height = abs(first_point.y - second_point.y)
        top_point = (first_point if first_point.y > second_point.y else second_point)
        bottom_point = (first_point if first_point.y <= second_point.y else second_point)

        other_point = Point(  top_point.x, bottom_point.y )
        super().__init__(top_point, bottom_point, other_point)




