import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Путь к папке с CSV файлами
folder_path = "authors"

# Список для хранения (имя файла, количество строк)
file_row_counts = []

# Проходим по всем CSV файлам в папке
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        
        # Читаем CSV файл
        try:
            df = pd.read_csv(file_path)
            # Получаем количество строк (без учета заголовка, если он есть)
            # Используем len(df) для учета всех строк данных
            row_count = len(df)
            file_row_counts.append((file, row_count))
        except Exception as e:
            print(f"Ошибка при чтении {file}: {e}")

# Сортируем по убыванию количества строк
file_row_counts.sort(key=lambda x: x[1], reverse=True)

# Берем топ-10
top_10 = file_row_counts[:10]

# Подготавливаем данные для графика
file_names = [name.replace('.csv', '') for name, count in top_10]  # Убираем .csv
row_counts = [count for name, count in top_10]

# Создаем столбчатую диаграмму
plt.figure(figsize=(12, 7))
bars = plt.bar(file_names, row_counts, color='hotpink', edgecolor='darkred', linewidth=1)

# Настройка внешнего вида
plt.title("Топ-10 авторов сообщений размеров 100+ символов в чатах Миланы, Лизы, Саши, Вовы, Бориса, Бел, Лены", 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel("Авторы", fontsize=12)
plt.ylabel("Количество сообщений", fontsize=12)

# Поворачиваем подписи на 45 градусов для лучшей читаемости
plt.xticks(rotation=45, ha='right', fontsize=9)

# Добавляем значения над столбцами
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# Добавляем сетку для удобства чтения
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Автоматическая регулировка отступов
plt.tight_layout()

# Сохраняем диаграмму
output_filename = "top_10_authors_chart.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Диаграмма сохранена как {output_filename}")

# Показываем диаграмму (опционально)
plt.show()

# Выводим результаты в консоль
print("\nТоп-10 файлов по количеству строк:")
for i, (file_name, count) in enumerate(top_10, 1):
    print(f"{i}. {file_name.replace('.csv', '')}: {count} строк")