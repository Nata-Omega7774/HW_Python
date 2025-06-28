employee_list = ["Jonh Snow", "Piter Pen",
                 "Drakula", "IvanIV", "Moana", "Juilet"]

print(employee_list[1] + ", " + employee_list[-2])




def dev_by_three(number):
    return "Да" if number % 3 == 0 else "Нет"

num = int(input("Введите число: "))
result = dev_by_three(num)
print(f"Делится ли на три {num}? - {result}")





import math

def min_boxes(items):
    return math.ceil(items / 5)

num_items = int(input("Введите количество предметов: "))
print(f"Минимальное количество коробок: {min_boxes(num_items)}")



n = int(input("Введите число:"))


def check_divisibility(n):
    for i in range(1, n + 1):
        if i % 4 == 0:
            print(f"{i} - Делится и на 2, и на 4")
        elif i % 2 == 0:
            print(f"{i} - Делится на 2, но не на 4")
        else:
            print(i)


check_divisibility(n)






def quarter_of_year(month):
    if 1 <= month <= 3:
        return "I квартал"
    elif 4 <= month <= 6:
        return "II квартал"
    elif 7 <= month <= 9:
        return "III квартал"
    elif 10 <= month <= 12:
        return "IV квартал"
    else:
        return "Неверный номер месяца"

try:
    month = int(input("Введите номер месяца (1-12): "))
    print(quarter_of_year(month)) 
except ValueError:
    print("Пожалуйста, введите целое число от 1 до 12.")



    lst = [17, 34, 9, 21, 13, 48, 24, 7, 81, 29, 16, 12, 42]

result = [x for x in lst if x > 15 and x % 3 == 0]

print(result)







my_list = list(range(25, 0, -5))

print(my_list)




var_1 = 50
var_2 = 5

temp = var_1
var_1 = var_2
var_2 = temp

print("var_1 =", var_1)
print("var_2 =", var_2)


var_1 = 50
var_2 = 5

var_1, var_2 = var_2, var_1

print("var_1 =", var_1)




