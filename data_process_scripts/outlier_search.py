import os
import pandas as pd
import numpy as np

# Путь к папке с CSV файлами
folder_path = "authors"

# Список для хранения данных по авторам с выбросами
authors_with_outliers = []

# Проходим по всем CSV файлам в папке
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
print(f"Найдено CSV файлов: {len(files)}")
print("=" * 100)

for file in files:
    file_path = os.path.join(folder_path, file)
    author_name = file.replace('.csv', '')
    
    try:
        # Читаем CSV файл
        df = pd.read_csv(file_path)
        
        # Проверяем, есть ли колонка 'text'
        if 'text' not in df.columns:
            print(f"Предупреждение: в файле {file} нет колонки 'text', пропускаем")
            continue
        
        # Количество сообщений
        num_messages = len(df)
        
        # Рассчитываем длину каждого сообщения
        message_lengths = df['text'].astype(str).str.len()
        
        # Средняя длина сообщения
        avg_length = message_lengths.mean()
        
        # Проверяем, является ли автор выбросом (средняя длина > 900)
        if avg_length > 900 and 50 <= num_messages < 200:  # Группа 3: 50-199 сообщений
            authors_with_outliers.append({
                'author': author_name,
                'num_messages': num_messages,
                'avg_length': avg_length,
                'median_length': message_lengths.median(),
                'max_length': message_lengths.max(),
                'min_length': message_lengths.min(),
                'std_length': message_lengths.std(),
                'total_chars': message_lengths.sum(),
                'message_lengths': message_lengths.tolist(),
                'df': df  # Сохраняем DataFrame для детального анализа
            })
            
    except Exception as e:
        print(f"Ошибка при чтении {file}: {e}")

# Выводим результаты
print("\n" + "=" * 100)
print("🔍 ПОИСК ВЫБРОСОВ В ГРУППЕ 3 (средняя длина сообщения > 900 символов)")
print("=" * 100)

if len(authors_with_outliers) == 0:
    print("\n❌ Не найдено авторов в группе 3 со средней длиной сообщения > 900 символов.")
    print("   Возможно, выброс в другой группе или порог нужно изменить.")
else:
    print(f"\n✅ Найдено авторов-выбросов: {len(authors_with_outliers)}")
    
    for idx, author_data in enumerate(authors_with_outliers, 1):
        print("\n" + "=" * 100)
        print(f"📊 ВЫБРОС #{idx}: {author_data['author']}")
        print("=" * 100)
        
        print(f"\n📈 ОСНОВНАЯ СТАТИСТИКА:")
        print(f"  • Количество сообщений: {author_data['num_messages']}")
        print(f"  • Средняя длина сообщения: {author_data['avg_length']:.1f} символов")
        print(f"  • Медианная длина сообщения: {author_data['median_length']:.1f} символов")
        print(f"  • Максимальная длина сообщения: {author_data['max_length']} символов")
        print(f"  • Минимальная длина сообщения: {author_data['min_length']} символов")
        print(f"  • Стандартное отклонение: {author_data['std_length']:.1f}")
        print(f"  • Общее количество символов: {author_data['total_chars']:,}")
        
        # Анализ распределения длин сообщений
        lengths = author_data['message_lengths']
        print(f"\n📊 РАСПРЕДЕЛЕНИЕ ДЛИН СООБЩЕНИЙ:")
        print(f"  • 25-й перцентиль: {np.percentile(lengths, 25):.1f} символов")
        print(f"  • 50-й перцентиль (медиана): {np.percentile(lengths, 50):.1f} символов")
        print(f"  • 75-й перцентиль: {np.percentile(lengths, 75):.1f} символов")
        print(f"  • 90-й перцентиль: {np.percentile(lengths, 90):.1f} символов")
        print(f"  • 95-й перцентиль: {np.percentile(lengths, 95):.1f} символов")
        print(f"  • 99-й перцентиль: {np.percentile(lengths, 99):.1f} символов")
        
        # Находим самые длинные сообщения
        print(f"\n📝 ТОП-5 САМЫХ ДЛИННЫХ СООБЩЕНИЙ:")
        df_copy = author_data['df'].copy()
        df_copy['length'] = df_copy['text'].astype(str).str.len()
        top_messages = df_copy.nlargest(5, 'length')[['text', 'length']]
        
        for i, (idx_row, row) in enumerate(top_messages.iterrows(), 1):
            print(f"\n  {i}. Длина: {row['length']} символов")
            # Показываем первые 200 символов сообщения
            message_preview = row['text'][:200] + "..." if len(row['text']) > 200 else row['text']
            print(f"     Текст: {message_preview}")
        
        # Анализируем, почему средняя такая высокая
        print(f"\n🔍 АНАЛИЗ ВЫБРОСА:")
        if author_data['max_length'] > author_data['avg_length'] * 3:
            print(f"  • Обнаружены экстремально длинные сообщения (максимум в {author_data['max_length']/author_data['avg_length']:.1f} раз больше среднего)")
        
        if author_data['median_length'] < author_data['avg_length'] * 0.7:
            print(f"  • Средняя сильно смещена из-за нескольких длинных сообщений (медиана значительно ниже среднего)")
        
        # Показываем гистограмму распределения (если нужно)
        print(f"\n📊 СТАТИСТИКА ПО ДИАПАЗОНАМ ДЛИН:")
        ranges = [(0, 100, "Короткие (0-100)"),
                  (100, 500, "Средние (100-500)"),
                  (500, 1000, "Длинные (500-1000)"),
                  (1000, float('inf'), "Очень длинные (1000+)")]
        
        for min_len, max_len, label in ranges:
            if max_len == float('inf'):
                count = sum(1 for l in lengths if l >= min_len)
            else:
                count = sum(1 for l in lengths if min_len <= l < max_len)
            percentage = (count / len(lengths)) * 100
            print(f"  • {label}: {count} сообщений ({percentage:.1f}%)")
        
        # Сохраняем подробную информацию в CSV для этого автора
        output_file = f"outlier_analysis_{author_data['author']}.csv"
        df_copy[['text', 'length']].to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 Детальная информация сохранена в файл: {output_file}")

# Если нужно найти и в других группах
print("\n" + "=" * 100)
print("🔍 ДОПОЛНИТЕЛЬНЫЙ ПОИСК ВО ВСЕХ ГРУППАХ")
print("=" * 100)

# Анализируем всех авторов для контекста
all_authors_stats = []

for file in files:
    file_path = os.path.join(folder_path, file)
    author_name = file.replace('.csv', '')
    
    try:
        df = pd.read_csv(file_path)
        if 'text' not in df.columns:
            continue
            
        num_messages = len(df)
        message_lengths = df['text'].astype(str).str.len()
        avg_length = message_lengths.mean()
        
        # Определяем группу
        if num_messages < 10:
            group = "Группа 1"
        elif 10 <= num_messages < 50:
            group = "Группа 2"
        elif 50 <= num_messages < 200:
            group = "Группа 3"
        else:
            group = "Группа 4"
        
        all_authors_stats.append({
            'author': author_name,
            'group': group,
            'num_messages': num_messages,
            'avg_length': avg_length,
            'max_length': message_lengths.max(),
            'median_length': message_lengths.median()
        })
    except:
        continue

# Сортируем по средней длине сообщения
all_authors_stats.sort(key=lambda x: x['avg_length'], reverse=True)

print("\n🏆 ТОП-10 АВТОРОВ ПО СРЕДНЕЙ ДЛИНЕ СООБЩЕНИЯ (ВСЕ ГРУППЫ):")
print("-" * 100)
print(f"{'Автор':<30} {'Группа':<12} {'Сообщений':<10} {'Ср. длина':<12} {'Медиана':<12} {'Максимум':<12}")
print("-" * 100)

for author in all_authors_stats[:10]:
    print(f"{author['author']:<30} {author['group']:<12} {author['num_messages']:<10} "
          f"{author['avg_length']:<12.1f} {author['median_length']:<12.0f} {author['max_length']:<12}")

# Проверяем, есть ли автор с выбросом в топе
if authors_with_outliers:
    outlier_author = authors_with_outliers[0]['author']
    print(f"\n🎯 ВАШ ВЫБРОС: {outlier_author}")
    print(f"   Этот автор имеет среднюю длину сообщения {authors_with_outliers[0]['avg_length']:.1f} символов")
    print(f"   при {authors_with_outliers[0]['num_messages']} сообщениях в группе 3.")
    
    # Сохраняем полный отчет
    with open('outlier_report.txt', 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ О ВЫБРОСЕ В ГРУППЕ 3\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Автор: {authors_with_outliers[0]['author']}\n")
        f.write(f"Количество сообщений: {authors_with_outliers[0]['num_messages']}\n")
        f.write(f"Средняя длина: {authors_with_outliers[0]['avg_length']:.1f} символов\n")
        f.write(f"Медианная длина: {authors_with_outliers[0]['median_length']:.1f} символов\n")
        f.write(f"Максимальная длина: {authors_with_outliers[0]['max_length']} символов\n")
        f.write(f"Стандартное отклонение: {authors_with_outliers[0]['std_length']:.1f}\n\n")
        
        f.write("ТОП-5 САМЫХ ДЛИННЫХ СООБЩЕНИЙ:\n")
        f.write("-" * 50 + "\n")
        df_copy = authors_with_outliers[0]['df'].copy()
        df_copy['length'] = df_copy['text'].astype(str).str.len()
        top_messages = df_copy.nlargest(5, 'length')[['text', 'length']]
        for i, (idx, row) in enumerate(top_messages.iterrows(), 1):
            f.write(f"\n{i}. Длина: {row['length']} символов\n")
            f.write(f"   Текст: {row['text'][:500]}...\n")
    
    print(f"\n📄 Полный отчет сохранен в файл: outlier_report.txt")

print("\n" + "=" * 100)
print("✅ Анализ завершен!")