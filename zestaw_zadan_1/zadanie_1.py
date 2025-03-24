import math

def prime(number):
    """Zwraca n liczb pierwszych.

    :param number: int - liczba liczb pierwszych do znalezienia
    :return: int - n-liczb pierwszych
    """
    if not isinstance(number, int):
        raise ValueError("The input is not an integer")
    if number == 0:
        raise ValueError("there is no zeroth prime")

    count = 0
    num = 0
    primes_list = []

    while count < number:
        num += 1
        if is_prime(num):
            count+=1
            primes_list.append(num)

    return primes_list


def is_prime(number):
    """Sprawdza, czy liczba jest pierwsza.

    :param number: int - sprawdzana liczba
    :return: bool - zwraca True jeśli liczba jest pierwsza, False w przeciwnym wypadku
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
    print("Podaj ile liczb pierwszych wypisać: ")
    print(prime(int(input())))
