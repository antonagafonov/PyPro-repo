class Rectangle:
    def __init__(self,c,w,l):
        self.width=w
        self.lenght=l
        self.color=c
    def area(self):
        self.area=self.width*self.lenght
        return self.area

c1='red'
w1=3
l1=4
rect1=Rectangle(c1,w1,l1)
# print('Rectangle 1 is:',rect1.color,'width length',rect1.width,rect1.lenght)
areaRect1=rect1.area()
print(areaRect1)
