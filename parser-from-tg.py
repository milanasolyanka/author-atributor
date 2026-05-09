import os
import csv
from glob import glob
from bs4 import BeautifulSoup

# Глобальная переменная с именем папки
FOLDER_NAME = "messages start-20260228"

def is_forwarded(message_div):
    """Проверяет, является ли сообщение пересланным (репостом)."""
    # Ищем div с классом 'forwarded' (может быть 'forwarded body' или просто 'forwarded')
    if message_div.find('div', class_='forwarded'):
        return True
    # Также проверим наличие любого элемента с классом 'forwarded'
    if message_div.find(class_='forwarded'):
        return True
    return False

def parse_html_file(file_path):
    """Извлекает из HTML-файла обычные сообщения (не репосты) длиной >= 100 символов."""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Ошибка чтения {file_path}: {e}")
        return results

    # Ищем все блоки сообщений
    messages = soup.find_all('div', class_='message')
    for msg in messages:
        # Пропускаем служебные сообщения
        if 'service' in msg.get('class', []):
            continue

        # Пропускаем репосты (пересланные сообщения)
        if is_forwarded(msg):
            continue

        body = msg.find('div', class_='body')
        if not body:
            continue

        # Автор сообщения
        from_name_div = body.find('div', class_='from_name')
        if not from_name_div:
            continue
        author = from_name_div.get_text(strip=True)

        # Текст сообщения
        text_div = body.find('div', class_='text')
        if not text_div:
            continue

        text = text_div.get_text(strip=True)
        if len(text) >= 100:
            results.append((author, text))

    return results

def main():
    if not os.path.isdir(FOLDER_NAME):
        print(f"Папка '{FOLDER_NAME}' не найдена.")
        return

    # Ищем все .html файлы в папке
    html_files = glob(os.path.join(FOLDER_NAME, "*.html"))
    if not html_files:
        print(f"В папке '{FOLDER_NAME}' нет HTML-файлов.")
        return

    all_messages = []
    for file_path in sorted(html_files):
        print(f"Обработка: {os.path.basename(file_path)}")
        all_messages.extend(parse_html_file(file_path))

    # Запись в CSV
    output_file = "messages.csv"
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["author", "text"])
        writer.writerows(all_messages)

    print(f"Готово. Сохранено {len(all_messages)} сообщений в файл {output_file}")

if __name__ == "__main__":
    main()