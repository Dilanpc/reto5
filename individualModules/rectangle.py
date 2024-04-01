from .shapes import *


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
