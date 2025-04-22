import random
from typing import List

from .SynonymReplacer import SynonymReplacer
from .ContextualAugmenter import ContextualAugmenter
from .TextAugmenter import TextAugmenter

class EDA(TextAugmenter):
    """Класс для реализации простых методов аугментации текста."""

    def __init__(
        self,
        synonym_replacer: SynonymReplacer = None,
        contextual_augmenter: ContextualAugmenter = None,
        random_seed: int = 42
    ):
        """
        :param synonym_replacer: Экземпляр SynonymReplacer для работы с синонимами.
        :param contextual_augmenter: Экземпляр ContextualAugmenter для контекстной вставки/замены.
        :param random_seed: Случайный сид для воспроизводимости.
        """
        self.synonym_replacer = synonym_replacer
        self.contextual_augmenter = contextual_augmenter
        self.random_gen = random.Random(random_seed)

    def random_deletion(self, text: str, p: float = 0.1) -> str:
        """
        Удаление слов из текста с вероятностью p.

        :param text: Исходный текст.
        :param p: Вероятность удаления слова.
        :return: Текст после удаления слов.
        """
        words = text.split()
        if len(words) == 1:
            return text

        new_words = [word for word in words if self.random_gen.random() > p]
        if len(new_words) == 0:
            new_words = [self.random_gen.choice(words)]

        return ' '.join(new_words)

    def random_insertion(self, text: str, n: int = 1) -> str:
        """
        Вставка случайных синонимов в текст.

        :param text: Исходный текст.
        :param n: Количество вставок.
        :return: Текст после вставки слов.
        """

        if self.synonym_replacer is None:
            raise ValueError("Для synonym_insertion требуется экземпляр SynonymReplacer")

        words = text.split()
        for _ in range(n):
            word_to_insert, pos = self._select_random_word_with_pos(words)
            if not word_to_insert or not pos:
                continue

            parsed_word_to_insert = self.synonym_replacer.morph.parse(word_to_insert)[0]

            synonyms = self.synonym_replacer._get_neighbors(parsed_word_to_insert.normal_form)
            if synonyms:
                synonym = self.synonym_replacer._replace_word_with_synonym(parsed_word_to_insert, synonyms)

                insertion_index = self.random_gen.randint(0, len(words))
                words.insert(insertion_index, synonym)

        return ' '.join(words)

    def contextual_insertion(self, text: str, n: int = 1, top_k: int = 5) -> str:
        """
        Вставка контекстно-подходящих слов в случайные места текста.

        :param text: Исходный текст.
        :param n: Количество вставок.
        :param top_k: Количество топовых замен для выбора.
        :param contextual_augmenter: Экземпляр ContextualAugmenter.
        :return: Текст после вставки слов.
        """
        if self.contextual_augmenter is None:
            raise ValueError("Для contextual_insertion требуется экземпляр ContextualAugmenter")

        words = text.split()
        if len(words) < 2:  # Если слишком мало слов, не делаем вставки
            return text

        for _ in range(n):
            # Выбираем случайную позицию для вставки
            insertion_index = self.random_gen.randint(0, len(words))

            # Создаем текст с маской в месте вставки
            temp_words = words.copy()
            temp_words.insert(insertion_index, self.contextual_augmenter.tokenizer.mask_token)
            masked_text = " ".join(temp_words)

            # Получаем предсказание для маскированного токена
            if self.contextual_augmenter.model_type == "huggingface":
                result = self.contextual_augmenter.model(masked_text, top_k=top_k)
                top_k_tokens = [item["token_str"].strip() for item in result]
                top_k_probs = [item["score"] for item in result]
                print(masked_text)
                best_replacement = self.random_gen.choices(top_k_tokens, weights=top_k_probs, k=1)[0]
                print(best_replacement)
            elif self.contextual_augmenter.model_type == "custom":
                best_replacement = self.contextual_augmenter._predict_with_custom_model(masked_text, top_k=top_k)

            # Проверяем, что предсказание не является пунктуацией или пробелом
            if not self.contextual_augmenter.is_punctuation_or_space(best_replacement):
                words.insert(insertion_index, best_replacement)

        return " ".join(words)

    def swap_words(self, text: str, n: int = 1) -> str:
        """
        Перестановка двух случайных слов в тексте.

        :param text: Исходный текст.
        :param n: Количество перестановок.
        :return: Текст после перестановки слов.
        """
        words = text.split()
        for _ in range(n):
            if len(words) < 2:  # Если меньше двух слов, перестановка невозможна
                break
            idx1, idx2 = self.random_gen.sample(range(len(words)), 2)
            words[idx1], words[idx2] = words[idx2], words[idx1]
        return ' '.join(words)

    def _select_random_word_with_pos(self, words: List[str]) -> (str, str):
        """
        Выбрать случайное слово и его часть речи из списка слов.

        :param words: Список слов.
        :return: Кортеж из слова и его части речи.
        """

        valid_words = [word for word in words if word not in self.synonym_replacer.russian_stopwords]
        if not valid_words:
            return None, None

        word = self.random_gen.choice(valid_words)
        pos = self.synonym_replacer._get_pos_natasha(word) or self.synonym_replacer._get_pos_mystem(word)
        return word, pos

    def augment(self, text: str, methods: List[str], contextual_augmenter=None, **kwargs) -> str:
        """
        Применить выбранные методы аугментации к тексту.

        :param text: Исходный текст.
        :param methods: Список методов для применения ('random_deletion', 'random_insertion', 'swap_words', 'contextual_insertion').
        :param contextual_augmenter: Экземпляр ContextualAugmenter для контекстной вставки слов.
        :param kwargs: Дополнительные параметры для каждого метода.
        :return: Аугментированный текст.
        """
        augmented_text = text
        for method in methods:
            if method == "random_deletion":
                augmented_text = self.random_deletion(augmented_text, **kwargs)
            elif method == "random_insertion":
                augmented_text = self.random_insertion(augmented_text, **kwargs)
            elif method == "swap_words":
                augmented_text = self.swap_words(augmented_text, **kwargs)
            elif method == "contextual_insertion":
                augmented_text = self.contextual_insertion(augmented_text,
                                                           **kwargs)
            else:
                raise ValueError(f"Метод '{method}' не поддерживается.")
        return augmented_text