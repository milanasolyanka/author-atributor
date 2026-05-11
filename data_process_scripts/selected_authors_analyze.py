import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# ================= КОНФИГУРАЦИЯ =================
FOLDER_PATH = "authors"  # Папка с CSV файлами авторов
SELECTED_AUTHORS_PATH = "./../selected_authors.py"  # Путь к файлу со списком авторов
MAX_NAME_LENGTH = 10  # Максимальная длина имени для отображения

# ================= ЗАГРУЗКА СПИСКА ВЫБРАННЫХ АВТОРОВ =================
def load_selected_authors():
    """Загружает список выбранных авторов из файла selected_authors.py"""
    # Добавляем родительскую папку в путь для импорта
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(parent_dir)  # Поднимаемся на уровень выше
    
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    try:
        # Импортируем selected_authors из файла
        from selected_authors import selected_authors
        return set(selected_authors)  # Используем set для быстрого поиска
    except ImportError as e:
        print(f"❌ Ошибка импорта selected_authors: {e}")
        print(f"   Ищем файл по пути: {os.path.join(parent_dir, 'selected_authors.py')}")
        return None

# ================= ФУНКЦИИ =================
def truncate_name(name, max_length=MAX_NAME_LENGTH):
    """Обрезает длинное имя"""
    if len(name) > max_length:
        return name[:max_length-3] + "..."
    return name

def load_author_data(author_name, folder_path):
    """Загружает данные одного автора из CSV файла"""
    file_path = os.path.join(folder_path, f"{author_name}.csv")
    
    if not os.path.exists(file_path):
        print(f"⚠️ Файл не найден: {file_path}")
        return None
    
    try:
        df = pd.read_csv(file_path)
        
        # Проверяем наличие колонки 'text'
        if 'text' not in df.columns:
            print(f"⚠️ В файле {author_name}.csv нет колонки 'text'")
            return None
        
        # Количество сообщений
        num_messages = len(df)
        
        # Рассчитываем длину каждого сообщения
        message_lengths = df['text'].astype(str).str.len()
        
        # Статистика
        avg_length = message_lengths.mean()
        median_length = message_lengths.median()
        total_chars = message_lengths.sum()
        max_length_msg = message_lengths.max()
        min_length_msg = message_lengths.min()
        std_length = message_lengths.std()
        
        return {
            'author': author_name,
            'author_short': truncate_name(author_name),
            'num_messages': num_messages,
            'avg_length': avg_length,
            'median_length': median_length,
            'total_chars': total_chars,
            'max_length': max_length_msg,
            'min_length': min_length_msg,
            'std_length': std_length
        }
        
    except Exception as e:
        print(f"❌ Ошибка при чтении {author_name}.csv: {e}")
        return None

# ================= ОСНОВНАЯ ЛОГИКА =================
def main():
    print("=" * 100)
    print("АНАЛИЗ ТОЛЬКО ВЫБРАННЫХ АВТОРОВ")
    print("=" * 100)
    
    # Загружаем список выбранных авторов
    selected_authors = load_selected_authors()
    
    if selected_authors is None:
        print("\n❌ Не удалось загрузить список авторов из selected_authors.py")
        print("   Убедитесь, что файл существует и содержит переменную selected_authors")
        return
    
    print(f"\n📋 Загружено выбранных авторов: {len(selected_authors)}")
    print(f"   Список: {', '.join(list(selected_authors)[:10])}{'...' if len(selected_authors) > 10 else ''}")
    
    # Загружаем данные только для выбранных авторов
    authors_data = []
    not_found_authors = []
    
    print("\n⏳ Загрузка данных...")
    for author in selected_authors:
        data = load_author_data(author, FOLDER_PATH)
        if data:
            authors_data.append(data)
            print(f"✅ Загружен: {author}")
        else:
            not_found_authors.append(author)
    
    print(f"\n📊 Успешно загружено авторов: {len(authors_data)} из {len(selected_authors)}")
    
    if not_found_authors:
        print(f"⚠️ Не найдены файлы для авторов: {', '.join(not_found_authors)}")
    
    if len(authors_data) == 0:
        print("\n❌ Нет данных для анализа!")
        return
    
    # Сортируем по количеству сообщений
    authors_data.sort(key=lambda x: x['num_messages'], reverse=True)
    
    # Определяем группы для выбранных авторов
    def get_group(num_messages):
        if num_messages < 10:
            return "Группа 1: Очень мало сообщений (<10)"
        elif 10 <= num_messages < 50:
            return "Группа 2: Мало сообщений (10-49)"
        elif 50 <= num_messages < 200:
            return "Группа 3: Средняя активность (50-199)"
        else:
            return "Группа 4: Высокая активность (200+)"
    
    for author in authors_data:
        author['group'] = get_group(author['num_messages'])
    
    # ================= ВЫВОД В КОНСОЛЬ =================
    print("\n" + "=" * 100)
    print("СТАТИСТИКА ПО ВЫБРАННЫМ АВТОРАМ")
    print("=" * 100)
    
    # Общая статистика
    total_messages = sum(a['num_messages'] for a in authors_data)
    overall_avg_length = sum(a['avg_length'] * a['num_messages'] for a in authors_data) / total_messages if total_messages > 0 else 0
    
    print("\n📊 ОБЩАЯ СТАТИСТИКА:")
    print("-" * 50)
    print(f"Всего выбранных авторов: {len(authors_data)}")
    print(f"Всего сообщений: {total_messages}")
    print(f"Средняя длина сообщения в целом: {overall_avg_length:.1f} символов")
    
    # Детальная таблица
    print("\n📈 ДЕТАЛЬНАЯ СТАТИСТИКА ПО КАЖДОМУ АВТОРУ:")
    print("-" * 130)
    print(f"{'Автор (полный)':<35} {'Автор (короткий)':<17} {'Сообщений':<12} {'Ср. длина':<12} {'Медиана':<12} {'Всего симв.':<15} {'Группа':<25}")
    print("-" * 130)
    
    for author in authors_data:
        print(f"{author['author']:<35} {author['author_short']:<17} {author['num_messages']:<12} "
              f"{author['avg_length']:<12.1f} {author['median_length']:<12.0f} "
              f"{author['total_chars']:<15,} {author['group']:<25}")
    
    # Группировка
    print("\n" + "=" * 100)
    print("ГРУППИРОВКА ВЫБРАННЫХ АВТОРОВ ПО АКТИВНОСТИ")
    print("=" * 100)
    
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
        print(f"  • Всего символов в группе: {group_data['total_chars']:,}")
        print(f"  • Авторы: {', '.join(group_data['authors'])}")
    
    # ================= ВИЗУАЛИЗАЦИЯ =================
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Анализ активности выбранных авторов\n(только авторы из selected_authors.py)', 
                 fontsize=14, fontweight='bold')
    
    # График 1: Количество сообщений
    ax1 = axes[0, 0]
    names_short = [a['author_short'] for a in authors_data]
    messages = [a['num_messages'] for a in authors_data]
    bars1 = ax1.bar(range(len(names_short)), messages, color='hotpink', edgecolor='darkred', linewidth=1)
    ax1.set_title(f'Количество сообщений по выбранным авторам\n(всего {len(authors_data)} авторов)', 
                  fontsize=12, fontweight='bold')
    ax1.set_xlabel('Авторы')
    ax1.set_ylabel('Количество сообщений')
    ax1.set_xticks(range(len(names_short)))
    ax1.set_xticklabels(names_short, rotation=45, ha='right', fontsize=9)
    
    # Добавляем значения над столбцами
    for bar, count in zip(bars1, messages):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    # График 2: Средняя длина сообщения
    ax2 = axes[0, 1]
    avg_lengths = [a['avg_length'] for a in authors_data]
    bars2 = ax2.bar(range(len(names_short)), avg_lengths, color='lightcoral', alpha=0.7, edgecolor='darkred', linewidth=1)
    ax2.set_title('Средняя длина сообщения по выбранным авторам', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Авторы')
    ax2.set_ylabel('Средняя длина (символы)')
    ax2.set_xticks(range(len(names_short)))
    ax2.set_xticklabels(names_short, rotation=45, ha='right', fontsize=9)
    
    for bar, length in zip(bars2, avg_lengths):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{length:.0f}', ha='center', va='bottom', fontsize=8)
    
    # График 3: Круговая диаграмма по группам
    ax3 = axes[1, 0]
    group_counts = [len(groups.get("Группа 1: Очень мало сообщений (<10)", {'authors': []})['authors']),
                    len(groups.get("Группа 2: Мало сообщений (10-49)", {'authors': []})['authors']),
                    len(groups.get("Группа 3: Средняя активность (50-199)", {'authors': []})['authors']),
                    len(groups.get("Группа 4: Высокая активность (200+)", {'authors': []})['authors'])]
    
    group_labels = ['Группа 1\n(<10)', 'Группа 2\n(10-49)', 'Группа 3\n(50-199)', 'Группа 4\n(200+)']
    colors_pie = ['#FFB6C1', '#FF69B4', '#FF1493', '#C71585']
    
    non_zero_groups = [(label, count, color) for label, count, color in zip(group_labels, group_counts, colors_pie) if count > 0]
    if non_zero_groups:
        labels, sizes, colors_used = zip(*non_zero_groups)
        wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
                                            colors=colors_used, startangle=90)
        ax3.set_title('Распределение выбранных авторов по группам активности', fontsize=12, fontweight='bold')
    
    # График 4: Соотношение количества и средней длины
    ax4 = axes[1, 1]
    colors_group_map = {'Группа 1: Очень мало сообщений (<10)': 'lightgray',
                        'Группа 2: Мало сообщений (10-49)': 'lightcoral',
                        'Группа 3: Средняя активность (50-199)': 'hotpink',
                        'Группа 4: Высокая активность (200+)': 'darkred'}
    
    for author in authors_data:
        color = colors_group_map.get(author['group'], 'gray')
        ax4.scatter(author['num_messages'], author['avg_length'], 
                    s=min(author['total_chars']/50, 800), alpha=0.6, 
                    c=color, edgecolors='black', linewidth=0.5)
        
        ax4.annotate(author['author_short'], 
                    (author['num_messages'], author['avg_length']),
                    fontsize=8, ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax4.set_title('Корреляция: количество сообщений vs средняя длина', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Количество сообщений')
    ax4.set_ylabel('Средняя длина сообщения (символы)')
    ax4.set_xscale('log')
    ax4.grid(True, alpha=0.3)
    
    # Легенда
    legend_elements = [Patch(facecolor='lightgray', alpha=0.6, label='Группа 1 (<10)'),
                       Patch(facecolor='lightcoral', alpha=0.6, label='Группа 2 (10-49)'),
                       Patch(facecolor='hotpink', alpha=0.6, label='Группа 3 (50-199)'),
                       Patch(facecolor='darkred', alpha=0.6, label='Группа 4 (200+)')]
    ax4.legend(handles=legend_elements, loc='upper left', fontsize=8)
    
    plt.tight_layout()
    
    # Сохраняем график
    output_filename = "selected_authors_analysis.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\n✅ Визуализация сохранена как '{output_filename}'")
    
    plt.show()
    
    # Дополнительная статистика
    print("\n" + "=" * 100)
    print("ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА")
    print("=" * 100)
    
    if authors_data:
        most_active = max(authors_data, key=lambda x: x['num_messages'])
        print(f"🏆 Самый активный автор: {most_active['author']} ({most_active['num_messages']} сообщений)")
        
        longest_avg = max(authors_data, key=lambda x: x['avg_length'])
        print(f"📝 Автор с самыми длинными сообщениями: {longest_avg['author']} "
              f"(средняя длина {longest_avg['avg_length']:.1f} символов)")

if __name__ == "__main__":
    main()