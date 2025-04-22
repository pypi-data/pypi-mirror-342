import random

from deep_translator import GoogleTranslator
from transformers import MarianMTModel, MarianTokenizer
from typing import List

from .TextAugmenter import TextAugmenter

class BackTranslationAugmenter(TextAugmenter):
    """Класс для обратного перевода текста."""

    def __init__(self, method: str = "google", random_seed: int = 42):
        """
        :param method: Метод обратного перевода ('google' или 'neural').
        :param random_seed: Случайное сид для воспроизводимости.
        """
        self.method = method
        self.random_gen = random.Random(random_seed)

        self.marian_languages = {
            "af", "ar", "az", "be", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa",
            "fi", "fr", "gu", "he", "hi", "hr", "hu", "hy", "id", "is", "it", "ja", "ka", "kk", "ko", "lt",
            "lv", "mk", "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "pa", "pl", "ps", "pt", "ro",
            "ru", "si", "sk", "sl", "sq", "sr", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "uz",
            "vi", "xh", "zh", "zu", "ru"
        }
        self.supported_languages = self.marian_languages

        if method == "neural":
            self.models = {}
            self.tokenizers = {}

    def _get_marian_model_and_tokenizer(self, src_lang: str, tgt_lang: str):
        """Загрузка модели и токенайзера MarianMT для заданной пары языков."""
        pair = f"{src_lang}-{tgt_lang}"
        if pair not in self.models:
            model_name = f"Helsinki-NLP/opus-mt-{pair}"
            self.models[pair] = MarianMTModel.from_pretrained(model_name)
            self.tokenizers[pair] = MarianTokenizer.from_pretrained(model_name)
        return self.models[pair], self.tokenizers[pair]

    def _translate_with_neural(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Перевод текста с использованием модели MarianMT."""
        model, tokenizer = self._get_marian_model_and_tokenizer(src_lang, tgt_lang)
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = model.generate(**inputs)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text

    def _translate_with_google(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Перевод текста с использованием Deep Translator (Google Translate)."""
        return GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)

    def augment(self, text: str, languages: List[str]) -> str:
        """
        Выполнить бэктрансляцию текста через указанные языки.

        :param text: Исходный текст.
        :param languages: Список языков для бэктрансляции, где:
                          первый элемент — исходный язык,
                          последний элемент — язык, на который текст возвращается.
        :return: Текст после бэктрансляции.
        """
        if len(languages) < 2:
            raise ValueError("Необходимо указать минимум два языка для бэктрансляции.")

        for lang in languages:
            if lang not in self.supported_languages:
                raise ValueError(f"Язык '{lang}' не поддерживается. Доступные языки: {self.supported_languages}")

        current_text = text
        for i in range(len(languages) - 1):
            src_lang = languages[i]
            tgt_lang = languages[i + 1]

            if self.method == "google":
                current_text = self._translate_with_google(current_text, src_lang, tgt_lang)
            elif self.method == "neural":
                current_text = self._translate_with_neural(current_text, src_lang, tgt_lang)
            else:
                raise ValueError("Допустимые методы: 'google' или 'neural'.")

        return current_text
