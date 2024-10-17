import unittest
from tests_12_3 import RunnerTest, TournamentTest  # импортируйте ваши тестовые классы из вашего файла

# Создаем TestSuite
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(RunnerTest))
suite.addTest(unittest.makeSuite(TournamentTest))

# Создаем TestRunner и запускаем его
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)