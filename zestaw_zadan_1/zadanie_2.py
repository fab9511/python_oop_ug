def friendly_numbers(bottom_threshold, top_threshold):
    """ Wypisz zaprzyjaźnione liczby z danego zakresu

    :param bottom_threshold: int - dolny zakres
    :param top_threshold: int - górny zakres
    :return: list of tuples - para liczb zaprzyjaźnionych
    """
    result = []
    if not isinstance(bottom_threshold, int) or not isinstance(top_threshold, int):
        raise ValueError("The input is not an integer")
    if bottom_threshold > top_threshold:
        raise ValueError("The bottom threshold is not greater than the top threshold")


    for num_1 in range(bottom_threshold, top_threshold):
        num_2 = sum_of_dividers(num_1)
        if num_1 == sum_of_dividers(num_2) and num_1 < num_2 <= top_threshold:
            result.append((num_1, num_2))

    return result

def sum_of_dividers(number):
    """Sumuje wszystkie dzielniki liczby.

    :param number: int - sprawdzana liczba
    :return: int - suma dzielnikiów
    """
    if not isinstance(number, int):
        raise ValueError("The input is not an integer")

    sum_div = 0

    for i in range(1, number):
        if number % i == 0:
            sum_div += i
    return sum_div

print("Program wypisze zaprzyjaźnione liczby z danego zakresu: ")
print("Podaj zakres dolny: ")
bottom = int(input())
print("Podaj górny zakres: ")
top = int(input())
print(friendly_numbers(bottom, top))
