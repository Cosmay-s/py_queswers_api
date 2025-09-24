import httpx
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_api():
    """Тестирование API согласно требованиям задания"""
    print("🧪 Тестирование API согласно криериям")

    time.sleep(1)

    with httpx.Client(timeout=30.0) as client:
        try:
            # 1. Эндпоинты вопросов
            print("=== Тестирование Вопросов ===")

            # POST /questions/
            question_data = {"text": "Тестовый вопрос?"}
            response = client.post(
                f"{BASE_URL}/questions/",
                json=question_data)
            assert response.status_code == 201
            question = response.json()
            question_id = question["id"]
            print("✅ POST /questions/")

            # GET /questions/
            response = client.get(f"{BASE_URL}/questions/")
            assert response.status_code == 200
            print("✅ GET /questions/")

            # GET /questions/{id}
            response = client.get(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200
            print("✅ GET /questions/{id}")

            # 2. Эндпоинты ответов
            print("=== Тестирование Ответов ===")

            # POST /answers/questions/{id}/answers/
            answer_data = {"text": "Тестовый ответ", "user_id": "user123"}
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer_data
            )
            assert response.status_code == 201
            answer = response.json()
            answer_id = answer["id"]
            print("✅ POST /answers/questions/{id}/answers/")

            # GET /answers/{id}
            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 200
            print("✅ GET /answers/{id}")

            # DELETE /answers/{id}
            response = client.delete(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 200
            print("✅ DELETE /answers/{id}")

            # 3. Тест каскадного удаления
            print("=== Тестирование Каскадного Удаления ===")

            # Создание нового ответа для теста каскадного удаления
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer_data
            )
            answer_id = response.json()["id"]

            # DELETE /questions/{id} (должен каскадно удалить ответы)
            response = client.delete(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200
            print("✅ DELETE /questions/{id}")

            # Проверка каскадного удаления
            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 404
            print("✅ Каскадное удаление работает")

            print("🎉 Все эндпоинты API работают корректно!")
            return True

        except Exception as e:
            print(f"❌ Тест не пройден: {e}")
            return False


if __name__ == "__main__":
    test_api()
