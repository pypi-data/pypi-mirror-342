from typing import Optional, List
from pathlib import Path
from clang.cindex import Cursor


class DefineInfo:
    def __init__(self, cursor: Cursor, encoding: str):
        self._cursor = cursor
        self.name: str = cursor.spelling
        self.location: Path = (
            Path(cursor.location.file.name).resolve()
            if cursor.location.file
            else Path()
        )
        try:
            self._usr: str = cursor.get_usr()
        except (AttributeError, TypeError, UnicodeDecodeError):
            self._usr = f"{self.name}@{self.location}"
        self.encoding = encoding

        self._raw_line: str
        self.params: Optional[List[str]]
        self.value: str
        self.comment: str
        self.is_system: bool

        self._raw_line = self._read_raw_line()
        self.params = self._extract_params()
        self.value = self._extract_value()
        self.comment = self._extract_comment_after()
        self.is_system = self._detect_system_define()  # Дефайны которые не используются кодом напрямую

    def _detect_system_define(self) -> bool:
        """
        Определяет, является ли define системным:
        - начинается с '_'
        - или у него отсутствует значение (value)
        """
        return self.name.startswith("_") or not self.value

    def _read_raw_line(self) -> str:
        """
        Считывает строку исходника, содержащую #define.
        """
        try:
            line_num = self._cursor.location.line
            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()
                return lines[line_num - 1].strip()
        except Exception as e:
            return f"[!] Ошибка чтения строки define {self.name}: {e}"

    def _extract_params(self) -> Optional[List[str]]:
        """
        Пытается извлечь параметры, если define является макросом с параметрами.
        Пример: #define MAX(a, b) ((a) > (b) ? (a) : (b))
        """
        try:
            after_name = self._raw_line.split(self.name, 1)[1].lstrip()
            if after_name.startswith("("):
                end_idx = after_name.find(")")
                if end_idx != -1:
                    param_str = after_name[1:end_idx]
                    params = [p.strip() for p in param_str.split(",") if p.strip()]
                    return params
        except Exception:
            pass
        return None

    def _extract_value(self) -> str:
        """
        Извлекает значение define (до начала комментария, если он есть).
        """
        try:
            parts = self._raw_line.split(None, 2)
            if len(parts) < 3:
                return ""

            value_part = parts[2]
            # обрезаем комментарий (если есть)
            for comment_start in ["//", "/*"]:
                if comment_start in value_part:
                    value_part = value_part.split(comment_start, 1)[0].strip()
            return value_part.strip()
        except Exception:
            return ""

    def _extract_comment_after(self) -> str:
        """
        Извлекает комментарий после значения define (если он есть).
        """
        try:
            for marker in ["//", "/*"]:
                if marker in self._raw_line:
                    return self._raw_line.split(marker, 1)[1].strip()
            return ""
        except Exception:
            return ""

    def describe(self) -> str:
        loc_str = f"{self.location}:{self._cursor.location.line}"
        system_flag = "[system] " if self.is_system else ""
        if self.params:
            return f"{system_flag}#define {self.name}({', '.join(self.params)}) {self.value}  // from {loc_str}"
        return f"{system_flag}#define {self.name} {self.value}  // from {loc_str}"

    def __str__(self) -> str:
        return self.describe()

    def __eq__(self, other):
        if not isinstance(other, DefineInfo):
            return False
        return self._usr == other._usr

    def __hash__(self):
        return hash(self._usr)
