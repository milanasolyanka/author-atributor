import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Функция для обрезания имени автора
def truncate_name(name, max_length=15):
    if len(name) > max_length:
        return name[:max_length-3] + "..."
    return name

# Читаем CSV файл
# Получаем путь к папке, где находится текущий скрипт
current_dir = os.path.dirname(os.path.abspath(__file__))

# Поднимаемся на уровень вверх (в папку проекта) и заходим в results
project_dir = os.path.dirname(current_dir)
file_path = os.path.join(project_dir, "results", "global_summary.csv")
df = pd.read_csv(file_path)

# Сортируем по mean_similarity по убыванию
df_sorted = df.sort_values('mean_similarity', ascending=False)

# Подготавливаем данные (обрезаем имена)
authors_full = df_sorted['author'].tolist()
authors_short = [truncate_name(a) for a in authors_full]
mean_similarities = df_sorted['mean_similarity'].tolist()

# Создаем график
plt.figure(figsize=(14, 8))

# Строим столбчатую диаграмму
bars = plt.bar(authors_short, mean_similarities, color='hotpink', edgecolor='darkred', linewidth=1)

# Настройка внешнего вида
plt.title('Средняя схожесть (mean_similarity) по авторам\n(сортировка по убыванию)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Авторы', fontsize=12)
plt.ylabel('Mean Similarity', fontsize=12)

# Поворачиваем подписи авторов для лучшей читаемости
plt.xticks(rotation=45, ha='right', fontsize=9)

# Добавляем значения над столбцами
for bar, value, full_name, short_name in zip(bars, mean_similarities, authors_full, authors_short):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{value:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Если имя было обрезано, добавляем маленькую подпись с полным именем
    if short_name != full_name:
        plt.text(bar.get_x() + bar.get_width()/2., -max(mean_similarities)*0.02,
                full_name, ha='center', va='top', fontsize=6, rotation=45, alpha=0.7)

# Добавляем сетку
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Автоматическая регулировка отступов
plt.tight_layout()

# Сохраняем график
output_filename = "mean_similarity_chart.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"✅ График сохранен как {output_filename}")

# Показываем график
plt.show()

# Выводим результаты в консоль
print("\n" + "=" * 80)
print("РЕЗУЛЬТАТЫ ПО ВСЕМ АВТОРАМ (сортировка по mean_similarity)")
print("=" * 80)
print(f"{'№':<4} {'Автор':<40} {'Mean Similarity':<18} {'Windows Count':<15}")
print("-" * 80)

for i, (idx, row) in enumerate(df_sorted.iterrows(), 1):
    print(f"{i:<4} {row['author']:<40} {row['mean_similarity']:<18.2f} {row['windows_count']:<15}")

# Дополнительная статистика
print("\n" + "=" * 80)
print("СТАТИСТИКА")
print("=" * 80)
print(f"Всего авторов: {len(df)}")
print(f"Средний mean_similarity: {df['mean_similarity'].mean():.2f}")
print(f"Медианный mean_similarity: {df['mean_similarity'].median():.2f}")
print(f"Стандартное отклонение: {df['mean_similarity'].std():.2f}")
print(f"Минимальный mean_similarity: {df['mean_similarity'].min():.2f} (автор: {df.loc[df['mean_similarity'].idxmin(), 'author']})")
print(f"Максимальный mean_similarity: {df['mean_similarity'].max():.2f} (автор: {df.loc[df['mean_similarity'].idxmax(), 'author']})")