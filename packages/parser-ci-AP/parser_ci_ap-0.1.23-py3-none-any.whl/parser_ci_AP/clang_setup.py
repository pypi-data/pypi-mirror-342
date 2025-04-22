from pathlib import Path
from clang.cindex import Config
import sys

def init_clang():
    """
    Инициализирует путь к libclang.dll, если он установлен вместе с clang.
    Рекурсивно ищет libclang.dll в папке site-packages виртуального окружения,
    а затем — в папке установленного пакета clang.
    """
    try:
        # Определяем корень виртуального окружения через sys.prefix
        venv = Path(sys.prefix)

        # Рекурсивный поиск libclang.dll в venv/Lib/site-packages
        site_pkgs = venv / "Lib" / "site-packages"
        if site_pkgs.is_dir():
            for dll_path in site_pkgs.rglob("libclang.dll"):
                Config.set_library_file(str(dll_path))
                return

        # Альтернатива: поиск в установленном модуле clang
        import clang
        clang_lib = Path(clang.__file__).parent / "lib" / "libclang.dll"
        if clang_lib.is_file():
            Config.set_library_file(str(clang_lib))
            return

        # Если не нашли ни там, ни там
        print("[!] Не удалось найти libclang.dll. Установите вручную с помощью Config.set_library_file().")

    except Exception as e:
        print(f"[!] Ошибка при настройке libclang: {e}")