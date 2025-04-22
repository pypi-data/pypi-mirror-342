from .TextAugmenter import TextAugmenter
import random
import math
import re
import requests
from typing import List
from gensim.models import KeyedVectors
from pymorphy3.analyzer import Parse
from pymystem3 import Mystem
from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, Doc
import pymorphy3

class SynonymReplacer(TextAugmenter):
    """Класс для замены слов синонимами."""

    mystem_to_ud = {
        'A': 'ADJ', 'ADV': 'ADV', 'ADVPRO': 'ADV', 'ANUM': 'ADJ', 'APRO': 'DET',
        'COM': 'ADJ', 'CONJ': 'SCONJ', 'INTJ': 'INTJ', 'NONLEX': 'X', 'NUM': 'NUM',
        'PART': 'PART', 'PR': 'ADP', 'S': 'NOUN', 'SPRO': 'PRON', 'UNKN': 'X', 'V': 'VERB'
    }

    def __init__(self,
                 model_path: str = None,
                 russian_stopwords: List[str] = None,
                 use_api: bool = False,
                 api_model: str = 'ruwikiruscorpora_upos_cbow_300_10_2021',
                 api_format: str = 'csv',
                 random_seed: int = 42):
        """
        :param model_path: Путь к модели Word2Vec.
        :param russian_stopwords: Список стоп-слов.
        :param use_api: Использовать API RusVectores вместо локальной модели.
        :param api_model: Название модели для RusVectores API.
        :param api_format: Формат ответа от RusVectores API.
        :param random_seed: Случайный сид для воспроизводимости.
        """
        self.use_api = use_api
        self.api_model = api_model
        self.api_format = api_format

        self.model = None
        if not use_api and model_path:
            self.model = KeyedVectors.load_word2vec_format(model_path, binary=True)

        self.random_gen = random.Random(random_seed)

        self.mystem = Mystem()
        self.morph = pymorphy3.MorphAnalyzer()
        self.segmenter = Segmenter()
        self.embedding = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.embedding)

        self.russian_stopwords = russian_stopwords or []

        self._get_neighbors = self._get_neighbors_with_api if use_api else self._get_neighbors_with_word2vec

    def _check_english(self, word: str) -> bool:
        """Проверяет, является ли слово английским."""
        return bool(re.search('[a-zA-Z]', word))

    def _get_pos_natasha(self, word: str) -> str:
        """Получить часть речи слова через Natasha."""
        if self._check_english(word):
            return None

        doc = Doc(word)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)

        if not doc.tokens:
            return None

        return doc.tokens[0].pos

    def _get_pos_mystem(self, word: str) -> str:
        """Получить часть речи слова через Mystem."""
        if self._check_english(word):
            return None

        processed = self.mystem.analyze(word)
        if not processed or 'analysis' not in processed[0] or not processed[0]['analysis']:
            return None

        mystem_tag = processed[0]['analysis'][0]['gr'].split(',')[0].split('=')[0].strip()
        return self.mystem_to_ud.get(mystem_tag, None)

    def _get_neighbors_with_api(self, word: str) -> List[str]:
        """Получить синонимы через RusVectores API."""
        pos = self._get_pos_natasha(word)
        word_with_pos = f"{word}_{pos}"
        url = f"https://rusvectores.org/{self.api_model}/{word_with_pos}/api/{self.api_format}/"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка API RusVectores: {e}")
            return []

        neighbors = []
        for line in response.text.split('\n'):
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                token, _ = parts[:2]
                token_word, token_pos = token.split('_', 1)
                if token_word != word and token_pos == pos:
                    neighbors.append(token_word)
        return neighbors

    def _get_neighbors_with_word2vec(self, word: str) -> List[str]:
        """Получить синонимы через локальную модель Word2Vec."""
        pos = self._get_pos_natasha(word)

        word_with_pos = f"{word}_{pos}"
        try:
            neighbors_sim = self.model.most_similar(word_with_pos)
        except KeyError:
            try:
                pos = self._get_pos_mystem(word)
                neighbors_sim = self.model.most_similar(f"{word}_{pos}")
            except KeyError:
                return []

        return [
            token.split('_', 1)[0]
            for token, _ in neighbors_sim
            if token.split('_', 1)[0] != word and token.split('_', 1)[1] == pos
        ]

    def _replace_word_with_synonym(self, parsed_word: Parse, synonyms: List[str]) -> str:
        """Заменить слово его синонимом с правильным склонением."""
        synonym = self.random_gen.choice(synonyms)
        parsed_synonym = self.morph.parse(synonym)[0]

        tags = {tag for tag in parsed_word.tag.grammemes if parsed_synonym.inflect({tag})}
        inflected_synonym = parsed_synonym.inflect(tags)

        return inflected_synonym.word if inflected_synonym else parsed_synonym.normal_form

    def augment(self, text: str, part: float = 0.5) -> str:
        """
        Заменить часть слов в тексте их синонимами.

        :param text: Исходный текст.
        :param part: Доля заменяемых слов (от 0 до 1).
        :return: Текст с замененными словами.
        """
        words = text.split()

        unique_words = sorted(list(set(word for word in words if word not in self.russian_stopwords)))
        self.random_gen.shuffle(unique_words)

        num_words_to_replace = math.trunc(len(unique_words) * part)
        words_to_replace = unique_words[:num_words_to_replace]

        new_words = words.copy()
        for word in words_to_replace:
            parsed_word = self.morph.parse(word)[0]
            synonyms = self._get_neighbors(parsed_word.normal_form)

            if synonyms:
                synonym = self._replace_word_with_synonym(parsed_word, synonyms)
                print("word: " + word + " synonym: " + synonym)
                indexes = [index for index, value in enumerate(new_words) if value == word]
                for index in indexes:
                    new_words[index] = synonym

        return ' '.join(new_words)
