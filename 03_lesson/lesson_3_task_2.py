from smartphone import Smartphone

catalog = []
phone1 = Smartphone("Apple", "IPhone 13", "+79124452053")
phone2 = Smartphone("Google", "Pixel 7 pro", "+79128956523")
phone3 = Smartphone("Xiaomi", "Mi 10T Pro", "+79128788482")
phone4 = Smartphone("Samsung", "Galaxy S23", "+79196335597")
phone5 = Smartphone("OnePlus", "9 Pro", "+79127658939")
catalog.append(phone1)
catalog.append(phone2)
catalog.append(phone3)
catalog.append(phone4)
catalog.append(phone5)


for phone in catalog:
    print(f"{phone.brand} {phone.model}, {phone.phone_number}")