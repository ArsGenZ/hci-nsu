import itertools
import os
import string
import time

# Попытка подключить tqdm для красивого прогресс-бара
try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("[!] Для красивого прогресс-бара установите: pip install tqdm\n")


def calculate_combinations(charset_size, min_length, max_length):
    """Считает общее количество комбинаций."""
    total = 0
    for length in range(min_length, max_length + 1):
        total += charset_size**length
    return total


def format_size(bytes_count):
    """Человекочитаемый размер файла."""
    for unit in ["Б", "КБ", "МБ", "ГБ", "ТБ"]:
        if bytes_count < 1024:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.2f} ПБ"


def generate_wordlist(
    output_file="wordlist.txt", min_length=1, max_length=4, charset=None
):
    """
    Генерация словаря паролей и запись в файл.

    :param output_file: путь к выходному файлу
    :param min_length: минимальная длина пароля
    :param max_length: максимальная длина пароля
    :param charset: набор символов (по умолчанию a-z + A-Z + 0-9)
    """
    if charset is None:
        charset = string.ascii_letters + string.digits  # 62 символа

    charset_size = len(charset)
    total_combinations = calculate_combinations(charset_size, min_length, max_length)

    # Прикидываем размер файла: средняя длина строки + символ перевода строки
    avg_line_length = (min_length + max_length) / 2 + 1  # +1 для \n
    estimated_size = total_combinations * avg_line_length

    print("=" * 60)
    print(" ПАРАМЕТРЫ ГЕНЕРАЦИИ")
    print("=" * 60)
    print(f" Алфавит ({charset_size} симв.): {charset}")
    print(f" Диапазон длин: от {min_length} до {max_length}")
    print(f" Всего комбинаций: {total_combinations:,}")
    print(f" Расчётный размер файла: ~{format_size(estimated_size)}")
    print(f" Выходной файл: {output_file}")
    print("=" * 60)

    # Предупреждение о больших файлах
    if estimated_size > 10 * 1024**3:  # больше 10 ГБ
        print("\n⚠️  ВНИМАНИЕ: файл будет очень большим!")
        print("    Убедитесь, что на диске достаточно свободного места.")
        confirm = input("    Продолжить? (y/n): ").strip().lower()
        if confirm != "y":
            print("Отменено.")
            return

    print("\n[*] Начинаю генерацию...\n")
    start_time = time.time()

    # Открываем файл в режиме дозаписи (или перезаписи)
    with open(output_file, "w", encoding="utf-8") as f:
        if HAS_TQDM:
            iterator = tqdm(
                _generate_combinations(charset, min_length, max_length),
                total=total_combinations,
                unit=" строк",
                desc="Генерация",
            )
        else:
            iterator = _generate_combinations(charset, min_length, max_length)

        written = 0
        for combo in iterator:
            f.write(combo + "\n")
            written += 1

            # Простой прогресс без tqdm
            if not HAS_TQDM and written % 1_000_000 == 0:
                elapsed = time.time() - start_time
                speed = written / elapsed
                print(
                    f"[*] Записано: {written:,} | "
                    f"Скорость: {speed:,.0f} строк/сек | "
                    f"Текущий: {combo}"
                )

    elapsed = time.time() - start_time
    actual_size = os.path.getsize(output_file)

    print("\n" + "=" * 60)
    print(" ГОТОВО!")
    print("=" * 60)
    print(f" Записано строк: {written:,}")
    print(f" Реальный размер файла: {format_size(actual_size)}")
    print(f" Затрачено времени: {elapsed:.2f} сек")
    print(f" Средняя скорость: {written / elapsed:,.0f} строк/сек")
    print(f" Файл сохранён: {os.path.abspath(output_file)}")
    print("=" * 60)


def _generate_combinations(charset, min_length, max_length):
    """Внутренний генератор комбинаций."""
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield "".join(combo)


# ============================================================
#  НАСТРОЙКИ — меняйте под свои задачи
# ============================================================
if __name__ == "__main__":
    # Пример 1: Только цифры, длина 4 (ПИН-коды)
    # generate_wordlist(
    #     output_file="pin_4digits.txt",
    #     min_length=4,
    #     max_length=4,
    #     charset=string.digits  # 10 символов, всего 10 000 комбинаций
    # )

    # Пример 2: Только строчные буквы, длина 1-6
    # generate_wordlist(
    #     output_file="lowercase_1-6.txt",
    #     min_length=1,
    #     max_length=6,
    #     charset=string.ascii_lowercase  # 26 символов
    # )

    # Пример 3: Полный алфавит (буквы + цифры), длина 1-4
    generate_wordlist(
        output_file="wordlist.txt",
        min_length=8,
        max_length=8,
        charset=string.ascii_letters + string.digits,  # 62 символа
    )
