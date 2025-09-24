import httpx
import time
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_logging():
    """
    Тест логирования при обращении к API.

    Проверяет:
    - наличие папки logs и файла app.log;
    - создание записей в логах при создании вопроса и ответа;
    - наличие ключевых фраз в логе.
    """
    print("🧪 Тестируем логирование...")

    time.sleep(1)

    # Проверка наличия папки logs
    assert os.path.exists("logs"), "Папка logs должна существовать"
    print("✅ Папка logs создана")

    with httpx.Client(timeout=30.0) as client:
        try:
            print("=== Создание вопроса и ответа ===")

            question_data = {
                "text": "Тестовый вопрос для проверки логов"
            }
            response = client.post(
                f"{BASE_URL}/questions/",
                json=question_data
            )
            assert response.status_code == 201
            question_id = response.json()["id"]

            answer_data = {
                "text": "Тестовый ответ для логов",
                "user_id": "logger_test"
            }
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer_data
            )
            assert response.status_code == 201
            answer_id = response.json()["id"]

            print("✅ Вопрос и ответ успешно созданы")

            # Проверка файла лога
            log_file = "logs/app.log"
            assert os.path.exists(log_file), (
                f"Файл лога {log_file} должен существовать"
            )
            print("✅ Файл лога создан")

            # Чтение последних строк лога
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()[-10:]

            log_content = ''.join(lines)
            print("📋 Последние записи в логе:")
            for line in lines[-5:]:
                print(f"   {line.strip()}")

            # Проверка наличия ключевых фраз
            assert (
                "создание нового вопроса" in log_content.lower()
                or "создан вопрос" in log_content.lower()
            ), "В логах нет записи о создании вопроса"

            assert (
                "создание ответа" in log_content.lower()
                or "создан ответ" in log_content.lower()
            ), "В логах нет записи о создании ответа"

            print("✅ Ключевые события залогированы")

            # Очистка
            client.delete(f"{BASE_URL}/questions/{question_id}")

            print("🎉 Логирование работает корректно!")
            return True

        except Exception as e:
            print(f"❌ Тест логирования провален: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = test_logging()
    exit(0 if success else 1)
