import random
from typing import List

import torch
import re
import string

import torch.nn.functional as f
from transformers import AutoTokenizer, pipeline
import sys
import os

from .TextAugmenter import TextAugmenter

project_dir = os.path.abspath("RuLeanALBERT/src")
sys.path.insert(0, project_dir)

class ContextualAugmenter(TextAugmenter):
    """Класс для контекстной замены слов с использованием моделей Masked Language Model (MLM)."""

    def __init__(self,
                 model_type: str = "huggingface",
                 model_name: str = "ai-forever/ruRoberta-large",
                 russian_stopwords: List[str] = None,
                 random_seed: int = 42):
        """
        :param model_type: Тип модели ('huggingface' или 'custom').
        :param model_name: Имя модели для Hugging Face.
        :param russian_stopwords: Список стоп-слов.
        :param random_seed: Случайный сид для воспроизводимости.
        """
        self.random_gen = random.Random(random_seed)
        self.model_type = model_type

        self.russian_stopwords = russian_stopwords or []

        if model_type == "huggingface":
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length=512)
            self.model = pipeline("fill-mask", model=model_name, tokenizer=self.tokenizer)
        elif model_type == "custom":
            current_dir = os.path.dirname(__file__)
            rulean_albert_path = os.path.join(current_dir, "RuLeanALBERT")
            tokenizer_path = os.path.join(rulean_albert_path, "tokenizer")

            self._load_custom_model(rulean_albert_path, tokenizer_path)

        self.PUNCTUATION_WHITESPACE = string.punctuation + string.whitespace + '—' + '-'

    def _load_custom_model(self, model_path: str, tokenizer_path: str):
        """Загрузка кастомной модели."""
        from .RuLeanALBERT.src.models import LeanAlbertForPreTraining, LeanAlbertConfig
        import os

        os.environ["LEAN_USE_JIT"] = "0"

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

        config = LeanAlbertConfig.from_pretrained(f"{model_path}/config.json")
        self.model = LeanAlbertForPreTraining(config)

        checkpoint = torch.load(f"{model_path}/state.pth", map_location="cpu", weights_only=True)["model"]
        self.model.load_state_dict(checkpoint)
        self.model.eval()

    def is_punctuation_or_space(self, target_string: str) -> bool:
        """Проверяет, является ли строка пунктуацией или пробелом."""
        return target_string in self.PUNCTUATION_WHITESPACE

    def augment(self, text: str, part: float = 0.5, top_k: int = 2) -> str:
        """
        Аугментация текста с контекстной заменой слов.

        :param text: Текст для аугментации.
        :param part: Доля слов, которые будут заменены.
        :param top_k: Количество топовых замен для выбора.
        :return: Аугментированный текст.
        """
        split_text = text.split()
        indexes = set(index for index, word in enumerate(split_text) if word not in self.russian_stopwords)
        indexes_count = round(len(indexes) * part)
        modified_text = split_text[:]
        count_replacements = 0

        while count_replacements < indexes_count:
            if len(indexes) == 0:
                break

            index = self.random_gen.choice(list(indexes))
            indexes.remove(index)

            token = modified_text[index]
            modified_text[index] = self.tokenizer.mask_token

            joined_text = " ".join(modified_text)

            if self.model_type == "huggingface":
                result = self.model(joined_text, top_k=top_k)
                print(result)
                top_k_tokens = [item["token_str"].strip() for item in result]
                top_k_probs = [item["score"] for item in result]

                best_replacement = self.random_gen.choices(top_k_tokens, weights=top_k_probs, k=1)[0]
            elif self.model_type == "custom":
                best_replacement = self._predict_with_custom_model(joined_text, top_k=top_k)

            if not self.is_punctuation_or_space(best_replacement):
                modified_text[index] = best_replacement
                count_replacements += 1
            else:
                modified_text[index] = token

        new_text = " ".join(modified_text)
        new_text = re.sub(r'\s+', ' ', new_text).strip()
        return new_text

    def _predict_with_custom_model(self, masked_text: str, top_k: int) -> str:
        """Прогноз маскированного токена с кастомной моделью, выбирая пропорционально вероятностям."""
        inputs = self.tokenizer(masked_text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.prediction_logits

        mask_token_tensor = torch.tensor(self.tokenizer.mask_token_id)
        mask_token_index = torch.where(inputs.input_ids == mask_token_tensor)[1]

        mask_logits = logits[0, mask_token_index, :]

        top_k_probs = f.softmax(torch.topk(mask_logits, k=top_k).values[0], dim=-1)
        top_k_tokens = torch.topk(mask_logits, k=top_k).indices[0].tolist()

        chosen_token_id = self.random_gen.choices(top_k_tokens, weights=top_k_probs.tolist(), k=1)[0]

        return self.tokenizer.decode([chosen_token_id]).strip()
