import math

def prime(bottom_threshold,top_threshold):
    """Zwraca liczby pierwsze z danego zakresu .

    :param bottom_threshold: int - dolny zakres
    :param top_threshold: int - górny zakres
    :return: int - liczby pierwsze z danego zakresu
    """

    if not isinstance(bottom_threshold, int) or not isinstance(top_threshold, int):
        raise ValueError("The input is not an integer")
    if bottom_threshold > top_threshold:
        raise ValueError("The bottom threshold is not greater than the top threshold")

    primes_list = []

    for num in range(bottom_threshold,top_threshold+1):
        if is_prime(num):
            primes_list.append(num)

    return primes_list


def is_prime(number):
    """Sprawdza, czy liczba jest pierwsza.

    :param number: int - sprawdzana liczba
    :returzn: bool - zwraca True jeśli liczba jest pierwsza, False w przeciwnym wypadku
    """
    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    for i in range(5, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
    return True

if __name__ ==  "__main__":
    #testy programu
    print("Podaj zakres liczb pierwszych")

    print("Podaj zakres dolny: ")
    bottom = int(input())
    print("Podaj górny zakres: ")
    top = int(input())
    print(prime(bottom, top))
