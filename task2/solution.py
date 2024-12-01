import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import re
from collections import Counter

BASE_URL = "https://ru.wikipedia.org"


async def fetch_page(session, url):
    """Асинхронно загружает страницу."""
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Failed to fetch page: {url} (status: {response.status})")
            return None


async def fetch_all_animals():
    """Парсит всех животных по алфавиту с нескольких страниц."""
    url = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"
    letter_counts = Counter()  # Счётчик для букв

    async with aiohttp.ClientSession() as session:
        while url:
            print(f"Processing page: {url}")
            page_content = await fetch_page(session, url)
            if not page_content:
                break

            soup = BeautifulSoup(page_content, "html.parser")

            # Парсинг животных на текущей странице
            animals = soup.select("div.mw-category-group ul li a")
            for animal in animals:
                animal_name = animal.text.strip()
                if animal_name:  # Проверяем, что строка не пуста
                    first_letter = animal_name[0].upper()
                    if re.match("[А-ЯЁ]", first_letter):  # Проверяем, что это кириллица
                        letter_counts[first_letter] += 1

            # Найти ссылку на следующую страницу
            next_page = soup.find("a", string="Следующая страница")
            if next_page:
                url = f"{BASE_URL}{next_page['href']}"
            else:
                url = None  # Нет следующей страницы
                print("Последняя страница достигнута.")

    return letter_counts


def save_to_csv(letter_counts, filename="beasts.csv"):
    """Сохраняет итоговые данные в файл CSV с учётом русского алфавита."""
    # Задаём порядок русского алфавита
    russian_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    # Сортируем буквы по порядку русского алфавита
    sorted_counts = sorted(
        letter_counts.items(),
        key=lambda item: russian_alphabet.index(item[0])
    )

    # Записываем в CSV
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(sorted_counts)

if __name__ == "__main__":
    # Асинхронно запускаем сбор данных
    loop = asyncio.get_event_loop()
    counts = loop.run_until_complete(fetch_all_animals())

    # Сохраняем в CSV
    save_to_csv(counts)
    print("Результат сохранён в файл beasts.csv")
