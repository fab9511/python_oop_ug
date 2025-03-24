class JosephusProblem:
    def __init__(self, num_people):
        if not isinstance(num_people, int):
            raise TypeError('num_people must be an integer')
        self.people =  [num+1 for num in range(num_people)]
        self.index = 0

    def __eliminate(self):
        while len(self.people) > 1:
            self.index = (self.index + 1) % len(self.people)
            self.people.pop(self.index)

    def find_safe_position(self):
        self.__eliminate()
        return self.people[0]

if __name__ == "__main__":
    print("Podaj liczbę ludzi w okręgu: ")
    problem = JosephusProblem(int(input()))
    safe_position = problem.find_safe_position()
    print(f"Bezpieczna pozycja: {safe_position}")

