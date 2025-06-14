import math
def square(side):
    pl = side*side
    if pl % 1 == 0:
     print("Площадь квадрата =", pl)  
    else:
     print("Площадь квадрата =", math.ceil(pl))  

side = float(input("Введите сторону квадрата: "))
square(side)