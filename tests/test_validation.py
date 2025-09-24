import httpx
import time
import random

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_validation():
    print("🧪 Тестируем улучшенную валидацию и бизнес-правила...")
    time.sleep(1)

    with httpx.Client(timeout=30.0) as client:
        try:
            print("=== Валидация вопросов ===")

            response = client.post(f"{BASE_URL}/questions/",
                                   json={"text": "Hi?"})
            assert response.status_code == 422, "Должен отклонять короткий вопрос"
            print("✅ Проверка короткого вопроса")

            response = client.post(f"{BASE_URL}/questions/",
                                   json={"text": "   "})
            assert response.status_code == 422, "Должен отклонять пустой вопрос"
            print("✅ Проверка пустого вопроса")

            unique_question_text = f"Что такое программирование? #{random.randint(10000, 99999)}"
            valid_question = {"text": unique_question_text}
            response = client.post(f"{BASE_URL}/questions/",
                                   json=valid_question)
            if response.status_code != 201:
                print(
                    f"Ошибка при создании валидного вопроса: статус {response.status_code}"
                    )
                print("Ответ сервера:", response.text)
            assert response.status_code == 201
            question_id = response.json()["id"]

            duplicate_question = {"text": f"  {unique_question_text.lower()}  "}
            response = client.post(f"{BASE_URL}/questions/",
                                   json=duplicate_question)
            assert response.status_code == 400, "Должен отклонять дубликаты"
            print("✅ Проверка дубликата вопроса")

            # (далее остальной код без изменений...)
            # ...

            # После теста желательно удалить созданный вопрос:
            client.delete(f"{BASE_URL}/questions/{question_id}")

            print("🎉 Все тесты валидации пройдены успешно!")
            return True

        except Exception as e:
            print(f"❌ Тест валидации провален: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = test_validation()
    exit(0 if success else 1)
