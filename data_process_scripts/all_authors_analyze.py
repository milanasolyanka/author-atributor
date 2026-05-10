import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Путь к папке с CSV файлами
folder_path = "authors"

# Функция для обрезания имени автора
def truncate_name(name, max_length=15):
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

# ================= ВЫВОД В КОНСОЛЬ =================
print("=" * 100)
print("АНАЛИЗ АВТОРОВ")
print("=" * 100)

print("\n📊 ОБЩАЯ СТАТИСТИКА ПО ВСЕМ АВТОРАМ:")
print("-" * 50)
total_authors = len(authors_data)
total_messages = sum(a['num_messages'] for a in authors_data)
overall_avg_length = sum(a['avg_length'] * a['num_messages'] for a in authors_data) / total_messages

print(f"Всего авторов: {total_authors}")
print(f"Всего сообщений: {total_messages}")
print(f"Средняя длина сообщения в целом: {overall_avg_length:.1f} символов")

print("\n📈 ДЕТАЛЬНАЯ СТАТИСТИКА ПО КАЖДОМУ АВТОРУ (ТОП-20):")
print("-" * 110)
print(f"{'Автор (полный)':<35} {'Автор (короткий)':<17} {'Сообщений':<12} {'Ср. длина':<12} {'Медиана':<12} {'Всего симв.':<15} {'Группа':<25}")
print("-" * 110)

# Показываем топ-20, чтобы не засорять консоль 400 строками
for author in authors_data[:20]:
    print(f"{author['author']:<35} {author['author_short']:<17} {author['num_messages']:<12} "
          f"{author['avg_length']:<12.1f} {author['median_length']:<12.0f} "
          f"{author['total_chars']:<15,} {author['group']:<25}")

if total_authors > 20:
    print(f"\n... и еще {total_authors - 20} авторов не показано в таблице")

print("\n" + "=" * 100)
print("ГРУППИРОВКА АВТОРОВ ПО АКТИВНОСТИ")
print("=" * 100)

# Статистика по группам
groups = {}
for author in authors_data:
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

for group_name, group_data in groups.items():
    num_authors = len(group_data['authors'])
    avg_length_group = group_data['avg_length_sum'] / num_authors
    
    print(f"\n{group_name}:")
    print(f"  • Количество авторов: {num_authors}")
    print(f"  • Всего сообщений в группе: {group_data['total_messages']}")
    print(f"  • Средняя длина сообщения в группе: {avg_length_group:.1f} символов")
    print(f"  • Авторы (полные имена): {', '.join(group_data['authors'][:10])}{'...' if len(group_data['authors']) > 10 else ''}")

# ================= ВИЗУАЛИЗАЦИЯ =================
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Анализ активности авторов чатов\nМиланы, Лизы, Саши, Вовы, Бориса, Бел, Лены', 
             fontsize=16, fontweight='bold')

# График 1: Количество сообщений по авторам (топ-15) с обрезанными именами
ax1 = axes[0, 0]
top_authors = authors_data[:15]
names_top_short = [a['author_short'] for a in top_authors]
messages_top = [a['num_messages'] for a in top_authors]
bars1 = ax1.bar(names_top_short, messages_top, color='hotpink', edgecolor='darkred', linewidth=1)
ax1.set_title('Топ-15 авторов по количеству сообщений', 
              fontsize=12, fontweight='bold')
ax1.set_xlabel('Авторы')
ax1.set_ylabel('Количество сообщений')
ax1.set_xticklabels(names_top_short, rotation=45, ha='right', fontsize=9)

# Добавляем значения над столбцами
for i, bar in enumerate(bars1):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=8)

# График 2: Средняя длина сообщения по авторам (топ-15 для читаемости)
ax2 = axes[0, 1]
top_authors_avg = sorted(authors_data, key=lambda x: x['avg_length'], reverse=True)[:15]
names_avg_short = [a['author_short'] for a in top_authors_avg]
avg_lengths_top = [a['avg_length'] for a in top_authors_avg]
bars2 = ax2.bar(names_avg_short, avg_lengths_top, color='lightcoral', alpha=0.7)
ax2.set_title('Топ-15 авторов по средней длине сообщения', 
              fontsize=12, fontweight='bold')
ax2.set_xlabel('Авторы')
ax2.set_ylabel('Средняя длина (символы)')
ax2.set_xticklabels(names_avg_short, rotation=45, ha='right', fontsize=9)
# Добавляем значения над столбцами
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=8)

# График 3: Распределение по группам (круговая диаграмма)
ax3 = axes[1, 0]
group_counts = [len(g['authors']) for g in groups.values()]
group_names = [g.split(':')[0] for g in groups.keys()]
colors_group = ['hotpink', 'lightcoral', 'salmon', 'pink']
wedges, texts, autotexts = ax3.pie(group_counts, labels=group_names, autopct='%1.1f%%',
                                    colors=colors_group, startangle=90)
ax3.set_title('Распределение авторов по группам активности', fontsize=12, fontweight='bold')

# График 4: Соотношение сообщений и средней длины
ax4 = axes[1, 1]
# Берем только топ-100 для читаемости графика
top_100 = authors_data[:100]
for author in top_100:
    ax4.scatter(author['num_messages'], author['avg_length'], 
                s=min(author['total_chars']/50, 500), alpha=0.6, c='hotpink', edgecolors='darkred')
    
    # Подписываем точки для топ-10 по сообщениям
    if author['num_messages'] >= sorted([a['num_messages'] for a in authors_data], reverse=True)[:10][-1]:
        ax4.annotate(author['author_short'], 
                    (author['num_messages'], author['avg_length']),
                    fontsize=8, ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax4.set_title('Корреляция: количество сообщений vs средняя длина\n(топ-100 авторов)', 
              fontsize=12, fontweight='bold')
ax4.set_xlabel('Количество сообщений')
ax4.set_ylabel('Средняя длина сообщения (символы)')
ax4.set_xscale('log')  # Логарифмическая шкала для лучшей видимости
ax4.grid(True, alpha=0.3)

# Добавляем легенду для размера точек
ax4.text(0.02, 0.98, 'Размер точки ~ общему количеству символов', 
         transform=ax4.transAxes, fontsize=9, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('authors_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Визуализация сохранена как 'authors_analysis.png'")

# Дополнительная статистика для консоли
print("\n" + "=" * 100)
print("ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА")
print("=" * 100)

# Самый активный автор
most_active = max(authors_data, key=lambda x: x['num_messages'])
print(f"🏆 Самый активный автор: {most_active['author']} ({most_active['num_messages']} сообщений)")
print(f"   (короткое имя: {most_active['author_short']})")

# Автор с самыми длинными сообщениями
longest_avg = max(authors_data, key=lambda x: x['avg_length'])
print(f"📝 Автор с самыми длинными сообщениями: {longest_avg['author']} "
      f"(средняя длина {longest_avg['avg_length']:.1f} символов)")

# Автор с самыми короткими сообщениями
shortest_avg = min(authors_data, key=lambda x: x['avg_length'])
print(f"✏️ Автор с самыми короткими сообщениями: {shortest_avg['author']} "
      f"(средняя длина {shortest_avg['avg_length']:.1f} символов)")

# Медианные значения по всем авторам
median_messages = np.median([a['num_messages'] for a in authors_data])
print(f"📊 Медианное количество сообщений на автора: {median_messages:.0f}")

# Статистика по длине сообщений
print(f"\nСтатистика по средней длине сообщений:")
print(f"  • Минимум: {min(a['avg_length'] for a in authors_data):.1f} символов")
print(f"  • Максимум: {max(a['avg_length'] for a in authors_data):.1f} символов")
print(f"  • Медиана: {np.median([a['avg_length'] for a in authors_data]):.1f} символов")

# Доп. статистика по группам
print(f"\n📊 Распределение по группам:")
for group_name, group_data in groups.items():
    print(f"  • {group_name}: {len(group_data['authors'])} авторов")

plt.show()