import re


class CadastralValidator:
    """Утилита для нормализации и валидации кадастровых номеров."""

    @staticmethod
    def normalize(value: str) -> str:
        """Удаляет пробельные символы из кадастрового номера.

        Args:
            value: Кадастровый номер в виде строки.

        Returns:
            Нормализованная строка без пробелов.
        """
        return re.sub(r"\s+", "", value)

    @staticmethod
    def is_valid(value: str) -> bool:
        """Проверяет кадастровый номер на соответствие формату.

        Args:
            value: Кадастровый номер в виде строки.

        Returns:
            True, если кадастровый номер валиден. Иначе False.
        """
        if ":" not in value:
            return False
        parts_count = len(value.split(":"))
        patterns = {
            4: re.compile(r"\d{2}:\d{2}:\d{6,7}:\d{2,6}"),  # кадастровый номер нового образца
            6: re.compile(r"\d{2}:\d{2}:\d{6,7}:\d{2}:\d:\d"),  # кадастровый номер старого образца
        }
        pattern = patterns.get(parts_count)
        return bool(pattern and pattern.fullmatch(value))
