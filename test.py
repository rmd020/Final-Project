###################################
#
#
###################################
class Shape:
    def __init__(self, l, w):
        self.length = l
        self.width = w

    def draw(self):
        for i in range(self.width):
            print("*" * self.length)
            
class Rectangle(Shape):
    def __init__(self, l, w):
        super().__init__(l, w)

class Square(Shape):
    def __init__(self, l):
        super().__init__(l, l)

class Triangle(Shape):
    def __init__(self, l):
        super().__init__(l, l)

    def draw(self):
        for i in range(self.width):
            print("* " * (self.width - i))

r1 = Rectangle(12, 4)
r1.draw()
print()
s1 = Square(6)
s1.draw()
print()
t1 = Triangle(7)
t1.draw()
