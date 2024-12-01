def appearance(intervals):
    # Извлекаем время начала и конца урока, интервалы ученика и учителя
    lesson_start, lesson_end = intervals['lesson']
    pupil_intervals = intervals['pupil']
    tutor_intervals = intervals['tutor']

    def convert_to_presence_array(intervals, start, end):
        # Создаем массив, представляющий каждую секунду урока
        # 0 - отсутствие, 1 - присутствие
        presence = [0] * (end - start + 1)

        # Обрабатываем интервалы попарно (время входа и выхода)
        for i in range(0, len(intervals), 2):
            # Проверяем, чтобы время не выходило за рамки урока
            entry = max(intervals[i], start) - start
            exit = min(intervals[i + 1], end) - start

            # Отмечаем присутствие единицами для каждой секунды в интервале
            for j in range(entry, exit):
                presence[j] = 1
        return presence

    # Преобразуем интервалы в массивы присутствия по секундам
    pupil_presence = convert_to_presence_array(pupil_intervals, lesson_start, lesson_end)
    tutor_presence = convert_to_presence_array(tutor_intervals, lesson_start, lesson_end)

    # Подсчитываем общее время, когда и ученик, и учитель присутствовали одновременно
    total_time = sum(p and t for p, t in zip(pupil_presence, tutor_presence))

    return total_time


# Тестовые примеры
if __name__ == "__main__":
    # Список тестовых случаев с входными интервалами и ожидаемыми ответами
    tests = [
        {
            'intervals': {
                'lesson': [1594663200, 1594666800],
                'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
            },
            'answer': 3117
        },
        {
            'intervals': {
                'lesson': [1594702800, 1594706400],
                'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                          1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                          1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                          1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                          1594706524, 1594706524, 1594706579, 1594706641],
                'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
            },
            'answer': 3577
        },
        {
            'intervals': {
                'lesson': [1594692000, 1594695600],
                'pupil': [1594692033, 1594696347],
                'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
            },
            'answer': 3565
        }
    ]

    # Запускаем тесты и выводим результаты
    for i, test in enumerate(tests, 1):
        result = appearance(test['intervals'])
        status = "OK" if result == test['answer'] else "FAIL"
        print(f"Тест #{i}: {status}")
        print(f"Получено: {result}")
        print(f"Ожидалось: {test['answer']}\n")

