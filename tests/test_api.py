import httpx
import time
import os
import traceback

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_api():
    """
    Полный тест API с валидацией, логикой и проверкой логов.

    Проверяет:
    - создание, получение, удаление вопросов и ответов;
    - предотвращение дубликатов;
    - бизнес-правила (ответ к несуществующему вопросу, каскадное удаление);
    - базовую валидацию (короткий ответ);
    - логирование в файл logs/app.log.
    """
    print("🧪 Тестируем API с валидацией и логированием...")

    time.sleep(1)

    with httpx.Client(timeout=30.0) as client:
        try:
            print("=== Основные операции ===")

            question_data = {"text": "Что такое Python?"}
            response = client.post(
                f"{BASE_URL}/questions/", json=question_data
            )
            assert response.status_code == 201
            question = response.json()
            question_id = question["id"]
            print("✅ Создание валидного вопроса")

            duplicate_question = {"text": "  что такое python?  "}
            response = client.post(
                f"{BASE_URL}/questions/", json=duplicate_question
            )
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
                f"{BASE_URL}/answers/questions/9999/answers/",
                json=answer_data
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

            response = client.get(f"{BASE_URL}/questions/{question_id}")
            question_data = response.json()
            assert len(question_data.get("answers", [])) >= 1, (
                "Ожидалось минимум 1 ответ"
            )

            response = client.delete(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200

            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 404
            print("✅ Каскадное удаление ответов работает")

            print("=== Валидация ===")

            valid_question = {"text": "Вопрос для проверки валидации"}
            response = client.post(
                f"{BASE_URL}/questions/", json=valid_question
            )
            assert response.status_code == 201
            new_question_id = response.json()["id"]

            invalid_answer = {"text": "No", "user_id": "test"}
            response = client.post(
                f"{BASE_URL}/answers/questions/{new_question_id}/answers/",
                json=invalid_answer
            )
            assert response.status_code == 422
            print("✅ Валидация короткого ответа")

            delete_response = client.delete(
                f"{BASE_URL}/questions/{new_question_id}"
            )
            assert delete_response.status_code == 200

            print("=== Логирование ===")
            log_file = "logs/app.log"
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = f.read()

                assert (
                    "вопрос" in logs.lower() or "question" in logs.lower()
                ), "Логи не содержат записей о вопросах"

                assert (
                    "ответ" in logs.lower() or "answer" in logs.lower()
                ), "Логи не содержат записей об ответах"

                print("✅ Логирование работает корректно")
            else:
                print("⚠️ Логи не найдены (возможно, лог пишется в stdout)")

            print("🎉 Тест API пройден успешно!")
            return True

        except Exception as e:
            print(f"❌ Тест провален: {e}")
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)
