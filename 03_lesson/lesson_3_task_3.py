from Address import Address
from mailing import Mailing # type: ignore

to_address = Address("426035", "Ижевск", "Льва Толстого", "17", "33")
from_address = Address("427000", "Сарапул", "Ленина", "170", "23")
mailing = Mailing(to_address, from_address, 426, "AFJ345")

print(f"Отправление {mailing.track} из {mailing.from_address.index}, {mailing.from_address.city},"
      f" {mailing.from_address.street}, {mailing.from_address.house} - {mailing.from_address.apartament} "
      f"в {mailing.to_address.index}, {mailing.to_address.city}, {mailing.to_address.street}, "
      f"{mailing.to_address.house} - {mailing.to_address.apartament}. Стоимость {mailing.cost} рублей.")