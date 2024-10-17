import unittest

class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name
        return False


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        # Мы изменим логику, сортируя участников по скорости для правильного подсчета
        self.participants.sort(key=lambda x: -x.speed)
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    # Пока мы итерации по списку, нельзя его модифицировать: создаем копию
                    temp_participants = self.participants[:]
                    temp_participants.remove(participant)
                    self.participants = temp_participants
        return finishers

class TournamentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner('Усэйн', 10)
        self.andrey = Runner('Андрей', 9)
        self.nick = Runner('Ник', 3)

    @classmethod
    def tearDownClass(cls):
        for result in cls.all_results.values():
            print({k: str(v) for k, v in result.items()})

    def test_usain_and_nick(self):
        tournament = Tournament(90, self.usain, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_usain_and_nick'] = results
        self.assertTrue(list(results.values())[-1] == 'Ник')

    def test_andrey_and_nick(self):
        tournament = Tournament(90, self.andrey, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_andrey_and_nick'] = results
        self.assertTrue(list(results.values())[-1] == 'Ник')

    def test_usain_andrey_and_nick(self):
        tournament = Tournament(90, self.usain, self.andrey, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_usain_andrey_and_nick'] = results
        self.assertTrue(list(results.values())[-1] == 'Ник')


if __name__ == '__main__':
    unittest.main()