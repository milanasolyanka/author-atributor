import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Путь к папке с CSV файлами
folder_path = "authors"

# Функция для обрезания имени автора
def truncate_name(name, max_length=10):
    if len(name) > max_length:
        return name[:max_length-3] + "..."  # Обрезаем и добавляем многоточие
    return name

# Список для хранения данных по каждому автору
authors_data = []

# Проходим по всем CSV файлам в папке
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
print(f"Найдено CSV файлов: {len(files)}")

for file in files:
    file_path = os.path.join(folder_path, file)
    author_name = file.replace('.csv', '')
    author_name_short = truncate_name(author_name)
    
    try:
        # Читаем CSV файл
        df = pd.read_csv(file_path)
        
        # Количество сообщений (строк)
        num_messages = len(df)
        
        # Проверяем, есть ли колонка 'text'
        if 'text' not in df.columns:
            print(f"Предупреждение: в файле {file} нет колонки 'text', пропускаем")
            continue
            
        # Рассчитываем длину каждого сообщения
        message_lengths = df['text'].astype(str).str.len()
        
        # Средняя длина сообщения
        avg_length = message_lengths.mean()
        
        # Медианная длина для дополнительной статистики
        median_length = message_lengths.median()
        
        # Общее количество символов
        total_chars = message_lengths.sum()
        
        authors_data.append({
            'author': author_name,
            'author_short': author_name_short,
            'num_messages': num_messages,
            'avg_length': avg_length,
            'median_length': median_length,
            'total_chars': total_chars
        })
        
        if len(authors_data) % 50 == 0:
            print(f"Обработано {len(authors_data)} авторов...")
        
    except Exception as e:
        print(f"Ошибка при чтении {file}: {e}")

print(f"Успешно обработано авторов: {len(authors_data)}")

# Проверяем, есть ли данные
if len(authors_data) == 0:
    print("Нет данных для анализа! Проверьте путь к папке и наличие колонки 'text' в CSV файлах.")
    exit()

# Сортируем по количеству сообщений
authors_data.sort(key=lambda x: x['num_messages'], reverse=True)

# Функция для определения группы по количеству сообщений
def get_group(num_messages):
    if num_messages < 10:
        return "Группа 1: Очень мало сообщений (<10)"
    elif 10 <= num_messages < 50:
        return "Группа 2: Мало сообщений (10-49)"
    elif 50 <= num_messages < 200:
        return "Группа 3: Средняя активность (50-199)"
    else:
        return "Группа 4: Высокая активность (200+)"

# Добавляем информацию о группе
for author in authors_data:
    author['group'] = get_group(author['num_messages'])

# ФИЛЬТРУЕМ ТОЛЬКО ГРУППЫ 3 и 4 (исключаем группы 1 и 2)
filtered_authors = [author for author in authors_data 
                   if author['group'] not in ["Группа 1: Очень мало сообщений (<10)", 
                                               "Группа 2: Мало сообщений (10-49)"]]

print(f"\n✅ Отфильтровано: показаны только группы 3 и 4")
print(f"   (исключены авторы с менее чем 50 сообщениями)")
print(f"   Всего авторов после фильтрации: {len(filtered_authors)} из {len(authors_data)}")

# Если нет авторов в группах 3-4, выводим предупреждение
if len(filtered_authors) == 0:
    print("\n⚠️ ВНИМАНИЕ: Нет авторов с 50+ сообщениями!")
    print("   Попробуйте уменьшить порог или проверьте данные.")
    exit()

# ================= ВЫВОД В КОНСОЛЬ =================
print("=" * 100)
print("АНАЛИЗ АВТОРОВ (только группы 3 и 4 - 50+ сообщений)")
print("=" * 100)

# Статистика только по отфильтрованным авторам
total_messages_filtered = sum(a['num_messages'] for a in filtered_authors)
overall_avg_length_filtered = sum(a['avg_length'] * a['num_messages'] for a in filtered_authors) / total_messages_filtered if total_messages_filtered > 0 else 0

print("\n📊 ОБЩАЯ СТАТИСТИКА ПО ОТФИЛЬТРОВАННЫМ АВТОРАМ (группы 3-4):")
print("-" * 50)
print(f"Всего авторов: {len(filtered_authors)}")
print(f"Всего сообщений: {total_messages_filtered}")
print(f"Средняя длина сообщения в целом: {overall_avg_length_filtered:.1f} символов")

print("\n📈 ДЕТАЛЬНАЯ СТАТИСТИКА ПО КАЖДОМУ АВТОРУ:")
print("-" * 110)
print(f"{'Автор (полный)':<35} {'Автор (короткий)':<17} {'Сообщений':<12} {'Ср. длина':<12} {'Медиана':<12} {'Всего симв.':<15} {'Группа':<25}")
print("-" * 110)

# Показываем всех отфильтрованных авторов (их уже не так много)
for author in filtered_authors:
    print(f"{author['author']:<35} {author['author_short']:<17} {author['num_messages']:<12} "
          f"{author['avg_length']:<12.1f} {author['median_length']:<12.0f} "
          f"{author['total_chars']:<15,} {author['group']:<25}")

print("\n" + "=" * 100)
print("ГРУППИРОВКА АВТОРОВ ПО АКТИВНОСТИ (только группы 3 и 4)")
print("=" * 100)

# Статистика по группам (только для отфильтрованных авторов)
groups = {}
for author in filtered_authors:
    group = author['group']
    if group not in groups:
        groups[group] = {
            'authors': [],
            'authors_short': [],
            'total_messages': 0,
            'avg_length_sum': 0,
            'total_chars': 0
        }
    groups[group]['authors'].append(author['author'])
    groups[group]['authors_short'].append(author['author_short'])
    groups[group]['total_messages'] += author['num_messages']
    groups[group]['avg_length_sum'] += author['avg_length']
    groups[group]['total_chars'] += author['total_chars']

# Сортируем группы для вывода
for group_name in sorted(groups.keys()):
    group_data = groups[group_name]
    num_authors = len(group_data['authors'])
    avg_length_group = group_data['avg_length_sum'] / num_authors
    
    print(f"\n{group_name}:")
    print(f"  • Количество авторов: {num_authors}")
    print(f"  • Всего сообщений в группе: {group_data['total_messages']}")
    print(f"  • Средняя длина сообщения в группе: {avg_length_group:.1f} символов")
    print(f"  • Всего символов в группе: {group_data['total_chars']:,}")
    print(f"  • Авторы: {', '.join(group_data['authors'])}")

# ================= ВИЗУАЛИЗАЦИЯ =================
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Анализ активности авторов чатов (группы 3-4: 50+ сообщений)\nМиланы, Лизы, Саши, Вовы, Бориса, Бел, Лены', 
             fontsize=14, fontweight='bold')

# График 1: Количество сообщений по авторам (все из групп 3-4)
ax1 = axes[0, 0]
names_short = [a['author_short'] for a in filtered_authors]
messages = [a['num_messages'] for a in filtered_authors]
bars1 = ax1.bar(range(len(names_short)), messages, color='hotpink', edgecolor='darkred', linewidth=1)
ax1.set_title(f'Количество сообщений по авторам\n(все {len(filtered_authors)} авторов с 50+ сообщениями)', 
              fontsize=12, fontweight='bold')
ax1.set_xlabel('Авторы')
ax1.set_ylabel('Количество сообщений')
ax1.set_xticks(range(len(names_short)))
ax1.set_xticklabels(names_short, rotation=45, ha='right', fontsize=9)

# Добавляем значения над столбцами (только если их не слишком много)
if len(filtered_authors) <= 20:
    for bar, count in zip(bars1, messages):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)

# График 2: Сравнение групп 3 и 4 (boxplot)
ax2 = axes[0, 1]
group_3_lengths = [a['avg_length'] for a in filtered_authors if 'Группа 3' in a['group']]
group_4_lengths = [a['avg_length'] for a in filtered_authors if 'Группа 4' in a['group']]

if group_3_lengths and group_4_lengths:
    box_data = [group_3_lengths, group_4_lengths]
    box_labels = [f'Группа 3\n(50-199 сообщ.)\n(n={len(group_3_lengths)})', 
                  f'Группа 4\n(200+ сообщ.)\n(n={len(group_4_lengths)})']
    
    bp = ax2.boxplot(box_data, labels=box_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], ['hotpink', 'darkred']):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_title('Сравнение средней длины сообщения\nгруппы 3 vs группа 4', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Средняя длина сообщения (символы)')
    ax2.grid(True, alpha=0.3, axis='y')
elif group_4_lengths:
    # Только группа 4
    ax2.boxplot([group_4_lengths], labels=['Группа 4\n(200+ сообщ.)'], patch_artist=True)
    ax2.set_title('Распределение средней длины сообщения\n(только группа 4)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Средняя длина сообщения (символы)')
    ax2.grid(True, alpha=0.3, axis='y')
else:
    # Только группа 3
    ax2.boxplot([group_3_lengths], labels=['Группа 3\n(50-199 сообщ.)'], patch_artist=True)
    ax2.set_title('Распределение средней длины сообщения\n(только группа 3)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Средняя длина сообщения (символы)')
    ax2.grid(True, alpha=0.3, axis='y')

# График 3: Круговая диаграмма (группы 3 и 4) - ИСПРАВЛЕНАЯ ВЕРСИЯ
ax3 = axes[1, 0]
group_counts = [len(groups.get("Группа 3: Средняя активность (50-199)", {'authors': []})['authors']),
                len(groups.get("Группа 4: Высокая активность (200+)", {'authors': []})['authors'])]

# Формируем названия с проверкой на наличие авторов
group_3_label = f'Группа 3\n(50-199 сообщ.)\n{group_counts[0]} авт.' if group_counts[0] > 0 else 'Группа 3'
group_4_label = f'Группа 4\n(200+ сообщ.)\n{group_counts[1]} авт.' if group_counts[1] > 0 else 'Группа 4'

group_names_simple = [group_3_label, group_4_label]
colors_group = ['hotpink', 'darkred']

# Убираем группы с нулевым количеством
non_zero_groups = [(name, count, color) for name, count, color 
                   in zip(group_names_simple, group_counts, colors_group) if count > 0]
if non_zero_groups:
    labels, sizes, colors_used = zip(*non_zero_groups)
    wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors_used, startangle=90)
    ax3.set_title('Распределение авторов по группам\n(только группы 3-4)', fontsize=12, fontweight='bold')

# График 4: Соотношение сообщений и средней длины
ax4 = axes[1, 1]
for author in filtered_authors:
    # Разный цвет для разных групп
    if 'Группа 3' in author['group']:
        color = 'hotpink'
        size_factor = 100
    else:
        color = 'darkred'
        size_factor = 150
    
    ax4.scatter(author['num_messages'], author['avg_length'], 
                s=min(author['total_chars']/size_factor, 800), alpha=0.6, 
                c=color, edgecolors='black', linewidth=0.5)
    
    # Подписываем всех авторов (их немного)
    ax4.annotate(author['author_short'], 
                (author['num_messages'], author['avg_length']),
                fontsize=8, ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7, 
                         edgecolor='black', linewidth=0.5))

ax4.set_title('Корреляция: количество сообщений vs средняя длина\n(цвет по группам активности)', 
              fontsize=12, fontweight='bold')
ax4.set_xlabel('Количество сообщений')
ax4.set_ylabel('Средняя длина сообщения (символы)')
ax4.set_xscale('log')
ax4.grid(True, alpha=0.3)

# Добавляем легенду для цветов
legend_elements = []
if group_3_lengths:
    legend_elements.append(Patch(facecolor='hotpink', alpha=0.6, label=f'Группа 3 (50-199 сообщ, n={len(group_3_lengths)})'))
if group_4_lengths:
    legend_elements.append(Patch(facecolor='darkred', alpha=0.6, label=f'Группа 4 (200+ сообщ, n={len(group_4_lengths)})'))
if legend_elements:
    ax4.legend(handles=legend_elements, loc='upper left', fontsize=8)

ax4.text(0.02, 0.98, 'Размер точки ~ общему количеству символов', 
         transform=ax4.transAxes, fontsize=8, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('authors_analysis_groups_3_4.png', dpi=300, bbox_inches='tight')
print("\n✅ Визуализация сохранена как 'authors_analysis_groups_3_4.png'")

# Дополнительная статистика для консоли (только отфильтрованные)
print("\n" + "=" * 100)
print("ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА (только группы 3 и 4)")
print("=" * 100)

if filtered_authors:
    # Самый активный автор
    most_active = max(filtered_authors, key=lambda x: x['num_messages'])
    print(f"🏆 Самый активный автор: {most_active['author']} ({most_active['num_messages']} сообщений)")
    
    # Автор с самыми длинными сообщениями
    longest_avg = max(filtered_authors, key=lambda x: x['avg_length'])
    print(f"📝 Автор с самыми длинными сообщениями: {longest_avg['author']} "
          f"(средняя длина {longest_avg['avg_length']:.1f} символов)")
    
    # Автор с самыми короткими сообщениями
    shortest_avg = min(filtered_authors, key=lambda x: x['avg_length'])
    print(f"✏️ Автор с самыми короткими сообщениями: {shortest_avg['author']} "
          f"(средняя длина {shortest_avg['avg_length']:.1f} символов)")
    
    # Медианные значения по отфильтрованным авторам
    median_messages = np.median([a['num_messages'] for a in filtered_authors])
    median_length = np.median([a['avg_length'] for a in filtered_authors])
    print(f"📊 Медианное количество сообщений на автора: {median_messages:.0f}")
    print(f"📊 Медианная средняя длина сообщения: {median_length:.1f} символов")
    
    # Дополнительная статистика по группам
    if group_3_lengths:
        print(f"\n📊 Статистика по группе 3 (50-199 сообщений, n={len(group_3_lengths)}):")
        print(f"   • Средняя длина (среднее): {np.mean(group_3_lengths):.1f} символов")
        print(f"   • Медиана длины: {np.median(group_3_lengths):.1f} символов")
        print(f"   • Диапазон: {min(group_3_lengths):.1f} - {max(group_3_lengths):.1f} символов")
    
    if group_4_lengths:
        print(f"\n📊 Статистика по группе 4 (200+ сообщений, n={len(group_4_lengths)}):")
        print(f"   • Средняя длина (среднее): {np.mean(group_4_lengths):.1f} символов")
        print(f"   • Медиана длины: {np.median(group_4_lengths):.1f} символов")
        print(f"   • Диапазон: {min(group_4_lengths):.1f} - {max(group_4_lengths):.1f} символов")

# Статистика по тому, сколько авторов было исключено
excluded_count = len(authors_data) - len(filtered_authors)
if excluded_count > 0:
    print(f"\n⚠️ Исключено авторов с менее чем 50 сообщениями (группы 1-2): {excluded_count}")
    print(f"   Всего авторов в группах 1-2: {excluded_count}")

plt.show()