class TextAugmenter:
    """Базовый класс для текстовой аугментации."""

    def augment(self, text: str) -> str:
        """Метод для реализации аугментации. Должен быть переопределен в подклассах."""
        raise NotImplementedError("Метод augment должен быть переопределен")
