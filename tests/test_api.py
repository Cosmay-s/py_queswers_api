import httpx
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_api():
    """
    Полный тест API с проверкой CRUD операций и базовой валидации.

    Проверяет:
    - создание, получение, удаление вопросов и ответов;
    - предотвращение дубликатов вопросов;
    - бизнес-правила (ответы к несуществующим вопросам, каскадное удаление);
    - валидацию коротких ответов.
    """
    print("🧪 Тестируем API с валидацией...")

    time.sleep(1)

    with httpx.Client(timeout=30.0) as client:
        try:
            print("=== Основные операции ===")

            question_data = {"text": "Что такое Python?"}
            response = client.post(f"{BASE_URL}/questions/",
                                   json=question_data)
            assert response.status_code == 201
            question = response.json()
            question_id = question["id"]
            print("✅ Создание валидного вопроса")

            duplicate_question = {"text": "  что такое python?  "}
            response = client.post(f"{BASE_URL}/questions/",
                                   json=duplicate_question)
            assert response.status_code == 400
            print("✅ Предотвращение дубликатов")

            answer_data = {
                "text": "Python — высокоуровневый язык программирования",
                "user_id": "user123"
            }
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer_data
            )
            assert response.status_code == 201
            answer = response.json()
            answer_id = answer["id"]
            print("✅ Создание валидного ответа")

            print("=== Проверка бизнес-правил ===")

            response = client.post(
                f"{BASE_URL}/answers/questions/9999/answers/", json=answer_data
            )
            assert response.status_code == 404
            print("✅ Нельзя создать ответ к несуществующему вопросу")

            another_answer = {
                "text": "Python отлично подходит для веб-разработки",
                "user_id": "user123"
            }
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=another_answer
            )
            assert response.status_code == 201
            print("✅ Один юзер может оставить несколько ответов")

            # Проверяем количество ответов до удаления
            response = client.get(f"{BASE_URL}/questions/{question_id}")
            question_data = response.json()
            assert len(question_data.get("answers",
                                         [])) >= 1, "Ожидалось минимум 1 ответ"

            response = client.delete(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200

            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 404
            print("✅ Каскадное удаление ответов работает")

            print("=== Валидация ===")

            valid_question = {"text": "Вопрос для проверки валидации"}
            response = client.post(f"{BASE_URL}/questions/",
                                   json=valid_question)
            new_question_id = response.json()["id"]

            invalid_answer = {"text": "No", "user_id": "test"}
            response = client.post(
                f"{BASE_URL}/answers/questions/{new_question_id}/answers/",
                json=invalid_answer
            )
            assert response.status_code == 422
            print("✅ Валидация короткого ответа")

            # Очистка
            delete_response = client.delete(
                f"{BASE_URL}/questions/{new_question_id}"
                )
            assert delete_response.status_code == 200

            print("🎉 Тест API с валидацией пройден успешно!")
            return True

        except Exception as e:
            import traceback
            print(f"❌ Тест провален: {e}")
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)
