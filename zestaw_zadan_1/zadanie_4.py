import random

class CalendarDate:
    def __init__(self, year, month, day):
        self.date = {
            'day': day,
            'month': month,
            'year': year
        }

    def __eq__(self, other):
        if not isinstance(other, CalendarDate):
            raise TypeError(f"Expected a CalendarDate, got {type(other)}")
        if self.date["year"] != other.date["year"]:
            return False
        if self.date["month"] != other.date["month"]:
            return False
        if self.date["day"] != other.date["day"]:
            return False
        return True

    def __lt__(self, other):
        if not isinstance(other, CalendarDate):
            raise TypeError(f"Expected a CalendarDate, got {type(other)}")
        if self.date["year"] != other.date["year"]:
            return self.date["year"] < other.date["year"]
        if self.date["month"] != other.date["month"]:
            return self.date["month"] < other.date["month"]
        if self.date["day"] != other.date["day"]:
            return self.date["day"] < other.date["day"]
        return False

    def __gt__(self, other):
        if not isinstance(other, CalendarDate):
            raise TypeError(f"Expected a CalendarDate, got {type(other)}")
        return not (self.__lt__(other) or self.__eq__(other))

def bubble_sort(elements: list) -> list:
    """sortowanie listy poprzez wykorzystanie sortownia bąbelkowego

    :param elements: list - elementy do posortowania
    :return: list - posortowane elementy
    """
    n = len(elements)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            if elements[j] > elements[j+1]:
                elements[j], elements[j+1] = elements[j+1], elements[j]
                swapped = True
        if not swapped:
            break
    return elements

def generate_random_dates(n: int) -> list[CalendarDate]:
    """Generuj n-dat

    :param n: liczba losowych dat do wygenerowania
    :return: list of CalendarDate object - lista n losowych dat
    """
    random_dates = []
    thirty_one_days = [1,3,5,7,8,10,12]
    for _ in range(n):
        year = random.randint(0, 2023)
        month = random.randint(1, 12)

        if month == 2:
            if leap_year(year):
                day = random.randint(1, 29)
            else:
                day = random.randint(1, 28)
        elif month in thirty_one_days:
            day = random.randint(1,31)
        else:
            day = random.randint(1,30)

        random_dates.append(CalendarDate(year, month, day))

    return random_dates

def leap_year(year: int) -> bool:
    """sprawdzanie czy dany rok jest parzysty

    :param year: rok
    :return: bool - zwraca True jeśli rok jest przestępny, w przeciwnym wypadku False
    """
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False

if __name__ == "__main__":
    dates = generate_random_dates(20)
    print("Wszystkie daty: ")
    for element in dates:
        day, month, year = element.date.values()
        print(f"{year}-{month}-{day}")

    print("\nPosortowane daty: ")
    for element in bubble_sort(dates):
        day, month, year = element.date.values()
        print(f"{year}-{month}-{day}")
