import re


class WordsFinder:
    def __init__(self, *file_names):
        self.file_names = file_names  # Сохранение переданных названий файлов в виде кортежа

    def get_all_words(self):
        # Пустой словарь для хранения всех слов из файлов
        all_words = {}
        # Пунктуация для удаления из строк
        punctuation = [',', '.', '=', '!', '?', ';', ':', ' - ']

        # Перебор названий файлов
        for file_name in self.file_names:
            with open(file_name, 'r', encoding='utf-8') as file:
                text = file.read().lower()  # Чтение файла и приведение к нижнему регистру

                # Удаление пунктуации из текста
                for punct in punctuation:
                    text = text.replace(punct, '')
                # Избавление от тире обособленного пробелами
                text = re.sub(r' - ', ' ', text)

                words_list = text.split()  # Разбиение текста на слова
                all_words[file_name] = words_list  # Сохранение списка слов в словарь

        return all_words

    def find(self, word):
        # Приведение искомого слова к нижнему регистру
        search_word = word.lower()

        # Получение всех слов из файлов
        all_words = self.get_all_words()
        result = {}

        # Перебор элементов словаря all_words
        for name, words in all_words.items():
            try:
                # Поиск позиции первого вхождения слова в списке слов
                position = words.index(search_word) + 1  # Индексы начинаются с 0, поэтому добавляем 1
                result[name] = position
            except ValueError:
                # Если слово не найдено, не добавляем его в результат
                result[name] = None

        return result

    def count(self, word):
        # Приведение искомого слова к нижнему регистру
        search_word = word.lower()

        # Получение всех слов из файлов
        all_words = self.get_all_words()
        result = {}

        # Перебор элементов словаря all_words
        for name, words in all_words.items():
            # Подсчет количества вхождений слова в списке слов
            word_count = words.count(search_word)
            result[name] = word_count

        return result


# Пример использования класса WordsFinder
finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words())  # Все слова
print(finder2.find('TEXT'))  # Где находится первое вхождение слова "TEXT"
print(finder2.count('teXT'))  # Сколько раз слово "teXT" встречается в тексте