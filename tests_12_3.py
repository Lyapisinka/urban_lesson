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
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)
        return finishers


def skip_if_frozen(method):
    def wrapper(*args, **kwargs):
        cls = args[0].__class__
        if cls.is_frozen:
            raise unittest.SkipTest('Тесты в этом кейсе заморожены')
        return method(*args, **kwargs)

    return wrapper


class RunnerTest(unittest.TestCase):
    is_frozen = False

    def setUp(self):
        self.runner = Runner('TestRunner', 10)

    @skip_if_frozen
    def test_run(self):
        self.runner.run()
        self.assertEqual(self.runner.distance, 20)

    @skip_if_frozen
    def test_walk(self):
        self.runner.walk()
        self.assertEqual(self.runner.distance, 10)

    @skip_if_frozen
    def test_challenge(self):
        self.runner.run()
        self.runner.walk()
        self.assertEqual(self.runner.distance, 30)


class TournamentTest(unittest.TestCase):
    is_frozen = True

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

    @skip_if_frozen
    def test_first_tournament(self):
        tournament = Tournament(90, self.usain, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_first_tournament'] = results
        self.assertTrue(list(results.values())[-1] == 'Ник')

    @skip_if_frozen
    def test_second_tournament(self):
        tournament = Tournament(90, self.andrey, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_second_tournament'] = results
        self.assertTrue(list(results.values())[-1] == 'Ник')

    @skip_if_frozen
    def test_third_tournament(self):
        tournament = Tournament(90, self.usain, self.andrey, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_third_tournament'] = results
        self.assertTrue(list(results.values())[-1] == 'Ник')


if __name__ == '__main__':
    unittest.main()