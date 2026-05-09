import os
import csv
import re
from glob import glob
from bs4 import BeautifulSoup

# Глобальная переменная с именем папки
FOLDER_NAME = "messages start-20260509"
OUTPUT_FILE_NAME = 'messages_milana_chat.csv'

def is_forwarded(message_div):
    """Проверяет, является ли сообщение пересланным (репостом)."""
    if message_div.find('div', class_='forwarded'):
        return True
    if message_div.find(class_='forwarded'):
        return True
    return False

def clean_text(raw_text):
    """
    Заменяет любые последовательности пробельных символов (включая переносы строк)
    на один пробел, удаляет начальные и конечные пробелы.
    """
    # Заменяем все виды пробелов (включая \n, \r, \t) на пробел
    cleaned = re.sub(r'\s+', ' ', raw_text)
    # Удаляем начальные и конечные пробелы
    cleaned = cleaned.strip()
    return cleaned

def parse_html_file(file_path):
    """Извлекает из HTML-файла обычные сообщения (не репосты) длиной >= 100 символов."""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Ошибка чтения {file_path}: {e}")
        return results

    messages = soup.find_all('div', class_='message')
    for msg in messages:
        if 'service' in msg.get('class', []):
            continue
        if is_forwarded(msg):
            continue

        body = msg.find('div', class_='body')
        if not body:
            continue

        from_name_div = body.find('div', class_='from_name')
        if not from_name_div:
            continue
        author = from_name_div.get_text(strip=True)

        text_div = body.find('div', class_='text')
        if not text_div:
            continue

        # Получаем текст с сохранением структуры, затем очищаем переносы
        text = text_div.get_text(separator=' ').strip()
        if len(text) >= 100:
            results.append((author, text))

    return results

def main():
    if not os.path.isdir(FOLDER_NAME):
        print(f"Папка '{FOLDER_NAME}' не найдена.")
        return

    html_files = glob(os.path.join(FOLDER_NAME, "*.html"))
    if not html_files:
        print(f"В папке '{FOLDER_NAME}' нет HTML-файлов.")
        return

    all_messages = []
    for file_path in sorted(html_files):
        print(f"Обработка: {os.path.basename(file_path)}")
        all_messages.extend(parse_html_file(file_path))

    output_file = OUTPUT_FILE_NAME
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["author", "text"])
        writer.writerows(all_messages)

    print(f"Готово. Сохранено {len(all_messages)} сообщений в файл {output_file}")

if __name__ == "__main__":
    main()