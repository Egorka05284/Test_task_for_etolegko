import argparse
import time

import requests


REQUEST_COUNT = 10


def measure_speed(url):
    total_bytes = 0
    request_times = []

    total_start = time.perf_counter()

    with requests.Session() as session:
        for i in range(REQUEST_COUNT):
            request_start = time.perf_counter()

            response = session.get(url, timeout=(10, 60))
            response.raise_for_status()

            request_time = time.perf_counter() - request_start

            # Размер загруженного тела ответа
            downloaded_bytes = len(response.content)

            total_bytes += downloaded_bytes
            request_times.append(request_time)

            print(
                f"Запрос {i + 1}: "
                f"{request_time:.2f} сек. | "
                f"{downloaded_bytes} байт"
            )

    total_time = time.perf_counter() - total_start

    average_time = sum(request_times) / REQUEST_COUNT

    # Скорость в мегабитах в секунду
    speed_mbps = (total_bytes * 8) / total_time / 1_000_000

    total_megabytes = total_bytes / 1_000_000

    print("\n--- Результаты ---")
    print(f"Среднее время запроса: {average_time:.2f} сек.")
    print(f"Общий объём данных: {total_megabytes:.2f} MB")
    print(f"Общее время: {total_time:.2f} сек.")
    print(f"Скорость скачивания: {speed_mbps:.2f} Mbps")


def main():
    parser = argparse.ArgumentParser(
        description="Измерение скорости скачивания данных"
    )
    parser.add_argument("url", help="URL для отправки запросов")

    args = parser.parse_args()

    try:
        measure_speed(args.url)
    except requests.RequestException as error:
        print(f"Ошибка при выполнении запроса: {error}")


if __name__ == "__main__":
    main()