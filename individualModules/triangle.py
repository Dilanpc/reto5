from .shapes import *

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
