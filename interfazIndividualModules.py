from individualModules.triangle import *
from individualModules.rectangle import *

def point_request(txt="Enter point, componets separed by ',': "):
    return Point(*[float(x) for x in input(txt).split(",")])


def inicio():
    print("""What do you want to create?
    1. Rectangle.
    2. Square.
    3. Triangle.
    4. Line
    0. Exit""")

    select = int(input("Enter the number of your selection: "))
    if select == 1:
        print("""Choose a method:
        Method 1: Bottom-left corner(Point) + width and height
        Method 2: Center(Point) + width and height
        Method 3: Two opposite corners (Points) e.g. Bottom-left and Upper-right
        Method 4: Four lines that collide """)
        method = int(input("Number of the method: "))
        if method == 1:
            bottom_left = point_request("Enter bottom left, componets separed by ',': ")
            width = float(input("Enter width: "))
            height = float(input("Enter height: "))
            return Rectangle(1, [bottom_left, width, height])
        elif method == 2:
            center = point_request("Enter center, componets separed by ',': ")
            width = float(input("Enter width: "))
            height = float(input("Enter height: "))
            return Rectangle(2, [center, width, height])
        elif method == 3:
            corner1 = point_request("Enter corner 1, componets separed by ',': ")
            corner2 = point_request("Enter corner 2, componets separed by ',': ")
            return Rectangle(3, [corner1, corner2])
        elif method == 4:
            lines = []
            for i in range(4):
                print(f"Line {i+1}: ")
                lines.append(Line(point_request("Enter point 1, components separated by ',': "), point_request("Enter point 2, components separated by ',': ")))
            return Rectangle(4, lines)
        else:
            print("Try again")
            return inicio()

        
    elif select == 2:
        center = Point(*[float(x) for x in input("Enter center, componets separed by ',': ").split(",")])
        width = float(input("Enter width/height: "))
        return Square(center, width)
    
    elif select == 3:
        print("""Choose a type:
        1. Equiratelal triangle (Point, width)
        2. Isoceles triangle (Point, width, height)
        3. Scalene triangle (Three points)
        4. Right triangle (Points of hypotenuse)""")
        tri = int(input("Enter the number of your selection: "))
        if tri == 1:
            point = point_request("Enter left bottom point, components separated by ',': ")
            width = float(input("Enter width: "))
            return Equilateral(point, width)
        if tri ==2:
            point = point_request("Enter left bottom point, components separated by ',': ")
            width = float(input("Enter width: "))
            height = float(input("Enter height: "))
            return Isosceles(point, width, height)
        if tri == 3:
            points = [point_request(f"Enter point {i+1}, components separated by ',': ") for i in range(3)]
            return Scalene(*points)
        if tri == 4:
            point1 = point_request("Enter point 1 of the hypotenuse, components separated by ',': ")
            point2 = point_request("Enter point 2 of the hypotenuse, components separated by ',': ")
            return TriRectangle(point1, point2)
        

    elif select == 4:
        start = Point(*[float(x) for x in input("Enter first point, components separed by ',': ").split(",")])
        end = Point(*[float(x) for x in input("Enter second point, components separed by ',': ").split(",")])
        return Line(start, end)

    elif select == 0:
        exit()
    
    print("Try again")
    return inicio()



def bucle(figure):
    running = True

    while running:
        print("""What do you want to do?
    1. Define a figure.
    2. Get the characteristics of the figure.
    3. Get area.
    4. Get perimeter.
    5. Calculate interference point
    6. Calculate interference line
    7. Discretize line (Only for lines)
    0. Exit""")
        select = int(input("Enter the number of your selection: "))
        if select == 1:
            figure = inicio()
        elif select == 2:
            figure.get_caracteristics()
            if isinstance(figure, Rectangle): print("Center: ", figure.center)
        elif select == 3:
            print("Area:", figure.compute_area())
        elif select == 4:
            print("Perimeter:", figure.compute_perimeter())
        elif select == 5:
            point = point_request()
            print("The point" + (" interferes" if figure.compute_interference_point(point) else " does not interfer") + " with the " + figure.type ) 
        elif select == 6:
            point1 = point_request("Enter first point, components separed by ',': ")
            point2 = point_request("Enter second point, components separed by ',': ")
            print("The line" + (" interferes" if figure.compute_interference_line(Line(point1, point2)) else " does not interfer") + " with the " + figure.type)
        elif select == 7:
            if isinstance(figure, Line):
                points = figure.discretize_line(int(input("Number of points: ")))
                print( *[str(x) for x in points])
        elif select == 0:
            running = False
        
        print("\n-------------------\n")

def main():
    figure = inicio()
    bucle(figure)

if __name__ == "__main__":
    main()
