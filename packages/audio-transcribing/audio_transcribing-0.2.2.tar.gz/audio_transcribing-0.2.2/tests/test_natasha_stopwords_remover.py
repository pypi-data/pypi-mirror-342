import unittest

from parameterized import parameterized

from audio_transcribing import NatashaStopwordsRemover


class TestNatashaStopwordsRemover(unittest.TestCase):
    def setUp(self):
        self.natasha_remover = NatashaStopwordsRemover()

    @parameterized.expand([
        ('Типа, сложно сказать, что там было.', 'сложно сказать, что там было.'),
        ('Какого типа этот треугольник?', 'Какого типа этот треугольник?'),
        ('', ''),
        ('Эм, ты серьезно?', 'ты серьезно?'),
        ('Я, короче, такую сплетню выцепила.', 'Я, такую сплетню выцепила.'),
        ('Ты короче меня.', 'Ты короче меня.'),
        ('Вообще-то, я лучше знаю.', 'я лучше знаю.'),
        ('Похоже, нам конец.', 'нам конец.'),
        ('Ну вот, а я говорила.', 'Ну, а я говорила.'),
        ('Блин, ты обещал.', 'ты обещал.'),
        ('Такой вкусный блин!', 'Такой вкусный блин!'),
        ('Бля, я не знала, прости.', 'я не знала, прости.'),
        ('Блять, я не знала, прости.', 'я не знала, прости.'),
        ('Это такой пиздец.', 'Это такой пиздец.'),
        ('Ахуеть, я в шоке.', 'я в шоке.'),
    ])
    def test_remove_stopwords(self, text, expected):
        with self.subTest(text=text, expected=expected):
            self.assertEqual(self.natasha_remover.remove_stopwords(text), expected)

    def test_remove_words(self):
        text = 'Я так люблю тебя, моя сладкая.'
        words = ['ЛюБлю ', '  моя']
        expected_text = 'Я так тебя, сладкая.'
        self.assertEqual(self.natasha_remover.remove_words(text, words), expected_text)

if __name__ == '__main__':
    unittest.main()
