import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ================= КОНФИГУРАЦИЯ =================
# Пути и названия файлов
RESULTS_DIR = "results"  # Папка с результатами относительно папки проекта
INPUT_FILENAME = "graphematic_summary.csv"  # Имя входного файла
OUTPUT_FILENAME = "graphematic_mean_similarity_chart.png"  # Имя выходного файла для графика

# Настройки графика
FIGURE_SIZE = (14, 8)  # Размер графика (ширина, высота)
CHART_COLOR = 'hotpink'  # Цвет столбцов
EDGE_COLOR = 'darkred'  # Цвет границы столбцов
LINE_WIDTH = 1  # Толщина границы
DPI = 300  # Разрешение при сохранении

# Настройки подписей
MAX_NAME_LENGTH = 15  # Максимальная длина имени автора (для обрезания)
TITLE_TEXT = 'Средняя схожесть (mean_similarity) по авторам\n(сортировка по убыванию)'
X_LABEL = 'Авторы'
Y_LABEL = 'Mean Similarity'
ROTATION_ANGLE = 45  # Угол поворота подписей авторов

# Настройки сетки
GRID_ALPHA = 0.3  # Прозрачность сетки
GRID_LINESTYLE = '--'  # Стиль линий сетки

# Настройки отображения значений над столбцами
VALUE_OFFSET = 0.5  # Смещение значения над столбцом
VALUE_FONTSIZE = 8  # Размер шрифта значений
VALUE_FONTWEIGHT = 'bold'  # Жирность шрифта значений

# Настройки подписей обрезанных имен
FULLNAME_OFFSET = -0.02  # Смещение полного имени (отрицательное = вниз)
FULLNAME_FONTSIZE = 6  # Размер шрифта полного имени
FULLNAME_ALPHA = 0.7  # Прозрачность полного имени

# Настройки вывода в консоль
SHOW_STATISTICS = True  # Показывать статистику в консоли
SHOW_TABLE = True  # Показывать таблицу в консоли
SHOW_PLOT = True  # Показывать график в отдельном окне

# ================= ФУНКЦИИ =================
def truncate_name(name, max_length=MAX_NAME_LENGTH):
    """Обрезает имя автора, если оно превышает максимальную длину"""
    if len(name) > max_length:
        return name[:max_length-3] + "..."
    return name

def get_file_path():
    """Формирует путь к файлу на основе конфигурации"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, RESULTS_DIR, INPUT_FILENAME)

def load_data(file_path):
    """Загружает данные из CSV файла"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    return pd.read_csv(file_path)

def prepare_data(df):
    """Подготавливает данные для визуализации"""
    df_sorted = df.sort_values('mean_similarity', ascending=False)
    authors_full = df_sorted['author'].tolist()
    authors_short = [truncate_name(a) for a in authors_full]
    mean_similarities = df_sorted['mean_similarity'].tolist()
    return df_sorted, authors_full, authors_short, mean_similarities

def create_chart(authors_short, authors_full, mean_similarities):
    """Создает столбчатую диаграмму"""
    plt.figure(figsize=FIGURE_SIZE)
    
    # Строим столбчатую диаграмму
    bars = plt.bar(authors_short, mean_similarities, 
                   color=CHART_COLOR, 
                   edgecolor=EDGE_COLOR, 
                   linewidth=LINE_WIDTH)
    
    # Настройка внешнего вида
    plt.title(TITLE_TEXT, fontsize=14, fontweight='bold', pad=20)
    plt.xlabel(X_LABEL, fontsize=12)
    plt.ylabel(Y_LABEL, fontsize=12)
    
    # Поворачиваем подписи авторов
    plt.xticks(rotation=ROTATION_ANGLE, ha='right', fontsize=9)
    
    # Добавляем значения над столбцами
    for bar, value, full_name, short_name in zip(bars, mean_similarities, authors_full, authors_short):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + VALUE_OFFSET,
                 f'{value:.1f}', ha='center', va='bottom', 
                 fontsize=VALUE_FONTSIZE, fontweight=VALUE_FONTWEIGHT)
        
        # Если имя было обрезано, добавляем маленькую подпись с полным именем
        if short_name != full_name:
            plt.text(bar.get_x() + bar.get_width()/2., 
                    max(mean_similarities) * FULLNAME_OFFSET,
                    full_name, ha='center', va='top', 
                    fontsize=FULLNAME_FONTSIZE, rotation=ROTATION_ANGLE, 
                    alpha=FULLNAME_ALPHA)
    
    # Добавляем сетку
    plt.grid(axis='y', alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE)
    
    # Автоматическая регулировка отступов
    plt.tight_layout()
    
    return plt

def save_chart(plt_obj):
    """Сохраняет график в файл"""
    plt_obj.savefig(OUTPUT_FILENAME, dpi=DPI, bbox_inches='tight')
    print(f"✅ График сохранен как {OUTPUT_FILENAME}")

def print_table(df_sorted):
    """Выводит таблицу с результатами в консоль"""
    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ ПО ВСЕМ АВТОРАМ (сортировка по mean_similarity)")
    print("=" * 80)
    print(f"{'№':<4} {'Автор':<40} {'Mean Similarity':<18} {'Windows Count':<15}")
    print("-" * 80)
    
    for i, (idx, row) in enumerate(df_sorted.iterrows(), 1):
        print(f"{i:<4} {row['author']:<40} {row['mean_similarity']:<18.2f} {row['windows_count']:<15}")

def print_statistics(df):
    """Выводит статистику в консоль"""
    print("\n" + "=" * 80)
    print("СТАТИСТИКА")
    print("=" * 80)
    print(f"Всего авторов: {len(df)}")
    print(f"Средний mean_similarity: {df['mean_similarity'].mean():.2f}")
    print(f"Медианный mean_similarity: {df['mean_similarity'].median():.2f}")
    print(f"Стандартное отклонение: {df['mean_similarity'].std():.2f}")
    print(f"Минимальный mean_similarity: {df['mean_similarity'].min():.2f} "
          f"(автор: {df.loc[df['mean_similarity'].idxmin(), 'author']})")
    print(f"Максимальный mean_similarity: {df['mean_similarity'].max():.2f} "
          f"(автор: {df.loc[df['mean_similarity'].idxmax(), 'author']})")

# ================= ОСНОВНАЯ ЛОГИКА =================
def main():
    """Главная функция"""
    try:
        # Загрузка данных
        file_path = get_file_path()
        print(f"Загрузка данных из: {file_path}")
        df = load_data(file_path)
        print(f"✅ Данные загружены. Найдено {len(df)} авторов")
        
        # Подготовка данных
        df_sorted, authors_full, authors_short, mean_similarities = prepare_data(df)
        
        # Создание и сохранение графика
        plt_obj = create_chart(authors_short, authors_full, mean_similarities)
        save_chart(plt_obj)
        
        # Вывод результатов в консоль
        if SHOW_TABLE:
            print_table(df_sorted)
        
        if SHOW_STATISTICS:
            print_statistics(df)
        
        # Показ графика
        if SHOW_PLOT:
            plt_obj.show()
        
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        print(f"Текущая директория: {os.getcwd()}")
        print(f"Ожидаемый путь: {get_file_path()}")
    except KeyError as e:
        print(f"❌ Ошибка: В файле отсутствует колонка {e}")
        print(f"Доступные колонки: {df.columns.tolist() if 'df' in locals() else 'неизвестно'}")
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")

# Запуск скрипта
if __name__ == "__main__":
    main()