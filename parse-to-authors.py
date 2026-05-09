import os
import csv
import re
from collections import defaultdict

# Исходный файл
INPUT_CSV = "messages_liza_chat.csv"
# Папка для выходных файлов
OUTPUT_DIR = "./authors"

def sanitize_filename(name):
    """Заменяет недопустимые для имени файла символы на подчеркивания."""
    # Недопустимые символы в Windows/Linux: \ / : * ? " < > | и пробел
    # Также заменим все символы, кроме букв, цифр, точки, дефиса, подчеркивания
    sanitized = re.sub(r'[\\/*?:"<>|\s]', '_', name)
    # Убираем точку в конце (некоторые ОС не любят)
    sanitized = sanitized.rstrip('.')
    return sanitized

def main():
    # Проверяем, существует ли исходный файл
    if not os.path.exists(INPUT_CSV):
        print(f"Файл {INPUT_CSV} не найден.")
        return

    # Создаём папку для выходных файлов, если её нет
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Собираем сообщения по авторам
    author_messages = defaultdict(list)

    # Читаем исходный CSV
    with open(INPUT_CSV, 'r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        header = next(reader, None)  # пропускаем заголовок (author, text)
        for row in reader:
            if len(row) >= 2:
                author, text = row[0], row[1]
                author_messages[author].append(text)

    # Для каждого автора записываем/дописываем его файл
    for author, texts in author_messages.items():
        safe_name = sanitize_filename(author)
        out_file = os.path.join(OUTPUT_DIR, f"{safe_name}.csv")

        # Открываем файл в режиме добавления (a)
        with open(out_file, 'a', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            # Если файл только что создан, запишем заголовок
            if os.path.getsize(out_file) == 0:
                writer.writerow(["text"])

            # Записываем все сообщения автора
            for text in texts:
                writer.writerow([text])

        print(f"Дописано {len(texts)} сообщений для автора {author} -> {out_file}")

    print("Готово. Все сообщения распределены по авторам.")

if __name__ == "__main__":
    main()