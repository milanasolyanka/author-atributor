# собирает все CSV файлы из папки results/graphematic_profiles в один общий файл

import os
import sys
import pandas as pd
from pathlib import Path

# ================= КОНФИГУРАЦИЯ =================
RESULTS_DIR = "results"
INPUT_SUBDIR = "graphematic_profiles"  # Папка с исходными CSV файлами
OUTPUT_FILENAME = "all_graphematic_profiles.csv"  # Имя итогового файла
ADD_FILENAME_AS_COLUMN = True  # Добавлять колонку с именем исходного файла
FILENAME_COLUMN_NAME = "source_file"  # Название колонки с именем файла
DELETE_EXISTING = True  # Удалять существующий выходной файл перед записью

# ================= ФУНКЦИИ =================
def get_project_dir():
    """Получает путь к корневой папке проекта"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def get_input_dir():
    """Получает путь к папке с входными CSV файлами"""
    return os.path.join(
        get_project_dir(),
        RESULTS_DIR,
        INPUT_SUBDIR
    )


def get_output_path():
    """Получает путь к выходному файлу"""
    return os.path.join(
        get_project_dir(),
        RESULTS_DIR,
        OUTPUT_FILENAME
    )


def find_csv_files(input_dir):
    """Находит все CSV файлы в указанной директории"""
    csv_files = []
    
    # Рекурсивный поиск всех CSV файлов
    for file_path in Path(input_dir).rglob("*.csv"):
        csv_files.append(file_path)
    
    # Сортировка для воспроизводимости
    csv_files.sort()
    
    return csv_files


def collect_csv_files(csv_files, input_dir):
    """Собирает все CSV файлы в один DataFrame"""
    all_data = []
    skipped_files = []
    
    for csv_file in csv_files:
        try:
            # Читаем CSV файл
            df = pd.read_csv(csv_file)
            
            # Добавляем колонку с именем файла (относительный путь от input_dir)
            if ADD_FILENAME_AS_COLUMN:
                # Получаем относительный путь от папки input_dir
                rel_path = csv_file.relative_to(input_dir)
                df[FILENAME_COLUMN_NAME] = str(rel_path)
            
            all_data.append(df)
            print(f"✅ Загружен: {rel_path if ADD_FILENAME_AS_COLUMN else csv_file.name} "
                  f"({len(df)} строк)")
            
        except Exception as e:
            print(f"❌ Ошибка при чтении {csv_file.name}: {e}")
            skipped_files.append(csv_file.name)
    
    return all_data, skipped_files


def merge_dataframes(all_data):
    """Объединяет все DataFrame в один"""
    if not all_data:
        return None
    
    # Объединяем все DataFrame
    merged_df = pd.concat(all_data, ignore_index=True)
    
    return merged_df


def save_merged_data(df, output_path):
    """Сохраняет объединенный DataFrame в CSV"""
    # Создаем директорию, если её нет
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Сохраняем в CSV
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Файл сохранен: {output_path}")
    print(f"   Всего строк: {len(df)}")
    print(f"   Всего колонок: {len(df.columns)}")


def print_statistics(df, csv_files, skipped_files, output_path):
    """Выводит статистику в консоль"""
    print("\n" + "=" * 80)
    print("СТАТИСТИКА СБОРА ДАННЫХ")
    print("=" * 80)
    
    print(f"\n📁 Исходная папка: {get_input_dir()}")
    print(f"📄 Найдено CSV файлов: {len(csv_files)}")
    print(f"✅ Успешно обработано: {len(csv_files) - len(skipped_files)}")
    
    if skipped_files:
        print(f"⚠️ Пропущено файлов: {len(skipped_files)}")
        for skipped in skipped_files:
            print(f"   - {skipped}")
    
    print(f"\n📊 Результирующий файл: {output_path}")
    print(f"📈 Всего строк в объединенном файле: {len(df)}")
    print(f"📋 Колонки: {', '.join(df.columns.tolist())}")
    
    # Статистика по авторам (если есть колонка author)
    if 'author' in df.columns:
        print(f"\n👥 Уникальных авторов: {df['author'].nunique()}")
        print(f"📊 Распределение по авторам (топ 10):")
        author_counts = df['author'].value_counts().head(10)
        for author, count in author_counts.items():
            print(f"   - {author}: {count} записей")
    
    # Статистика по исходным файлам (если добавлена колонка)
    if ADD_FILENAME_AS_COLUMN and FILENAME_COLUMN_NAME in df.columns:
        print(f"\n📁 Распределение по исходным файлам:")
        file_counts = df[FILENAME_COLUMN_NAME].value_counts()
        for file_name, count in file_counts.items():
            print(f"   - {file_name}: {count} записей")


# ================= ОСНОВНАЯ ЛОГИКА =================
def main():
    """Главная функция"""
    print("=" * 80)
    print("СБОРЩИК CSV ФАЙЛОВ ИЗ ПАПКИ graphematic_profiles")
    print("=" * 80)
    
    try:
        # Получаем пути
        input_dir = get_input_dir()
        output_path = get_output_path()
        
        # Проверяем существование входной папки
        if not os.path.exists(input_dir):
            print(f"❌ Папка не найдена: {input_dir}")
            print(f"\nТекущая структура:")
            print(f"  Папка проекта: {get_project_dir()}")
            print(f"  Ожидаемая папка: {input_dir}")
            
            # Проверяем, существует ли папка results
            results_dir = os.path.join(get_project_dir(), RESULTS_DIR)
            if os.path.exists(results_dir):
                print(f"\n✅ Папка {RESULTS_DIR} существует.")
                print(f"   Содержимое: {os.listdir(results_dir)}")
            else:
                print(f"\n❌ Папка {RESULTS_DIR} не существует!")
            
            return
        
        # Проверяем, нужно ли удалить существующий выходной файл
        if DELETE_EXISTING and os.path.exists(output_path):
            os.remove(output_path)
            print(f"🗑️ Удален существующий файл: {output_path}")
        
        # Находим все CSV файлы
        csv_files = find_csv_files(input_dir)
        print(f"\n📁 Поиск CSV файлов в: {input_dir}")
        print(f"📄 Найдено файлов: {len(csv_files)}")
        
        if not csv_files:
            print("❌ Нет CSV файлов для обработки!")
            return
        
        # Собираем все файлы
        print("\n⏳ Загрузка файлов...")
        all_data, skipped_files = collect_csv_files(csv_files, input_dir)
        
        if not all_data:
            print("❌ Нет данных для объединения!")
            return
        
        # Объединяем все DataFrame
        print("\n⏳ Объединение данных...")
        merged_df = merge_dataframes(all_data)
        
        # Сохраняем результат
        save_merged_data(merged_df, output_path)
        
        # Выводим статистику
        print_statistics(merged_df, csv_files, skipped_files, output_path)
        
        # Показываем первые строки результата
        print("\n" + "=" * 80)
        print("ПРЕВЬЮ ОБЪЕДИНЕННЫХ ДАННЫХ (первые 5 строк)")
        print("=" * 80)
        print(merged_df.head())
        
        print("\n✅ Скрипт успешно завершен!")
        
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        import traceback
        traceback.print_exc()


# Альтернативная версия с возможностью выбора, какие колонки сохранять
def main_with_column_filter(columns_to_keep=None):
    """
    Версия с фильтрацией колонок
    
    Args:
        columns_to_keep: список колонок, которые нужно сохранить (если None - сохраняем все)
    """
    print("=" * 80)
    print("СБОРЩИК CSV ФАЙЛОВ С ФИЛЬТРАЦИЕЙ КОЛОНОК")
    print("=" * 80)
    
    try:
        input_dir = get_input_dir()
        output_path = get_output_path()
        
        if not os.path.exists(input_dir):
            print(f"❌ Папка не найдена: {input_dir}")
            return
        
        csv_files = find_csv_files(input_dir)
        print(f"\n📄 Найдено файлов: {len(csv_files)}")
        
        all_data = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            
            # Фильтруем колонки, если нужно
            if columns_to_keep:
                existing_columns = [col for col in columns_to_keep if col in df.columns]
                df = df[existing_columns]
            
            if ADD_FILENAME_AS_COLUMN:
                rel_path = csv_file.relative_to(input_dir)
                df[FILENAME_COLUMN_NAME] = str(rel_path)
            
            all_data.append(df)
            print(f"✅ Загружен: {csv_file.name} ({len(df)} строк)")
        
        merged_df = pd.concat(all_data, ignore_index=True)
        merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Сохранен файл: {output_path}")
        print(f"   Всего строк: {len(merged_df)}")
        print(f"   Колонки: {merged_df.columns.tolist()}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    # Запуск основной версии
    main()
    
    # Если нужно сохранить только определенные колонки, раскомментируйте строку ниже:
    # main_with_column_filter(['author', 'mean_similarity', 'std_similarity'])