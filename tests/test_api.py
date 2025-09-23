import httpx
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_api():
    """Тест основных endpoints API"""
    print("🧪 Testing API endpoints...")

    # Даем серверу время запуститься
    time.sleep(2)

    with httpx.Client(timeout=30.0) as client:
        try:
            # 1. Создаем вопрос
            question_data = {"text": "What is FastAPI?"}
            response = client.post(f"{BASE_URL}/questions/",
                                   json=question_data)
            print(f"✅ Create question: {response.status_code}")
            if response.status_code != 201:
                print(f"Error: {response.text}")
                return

            question = response.json()
            question_id = question["id"]

            # 2. Получаем список вопросов
            response = client.get(f"{BASE_URL}/questions/")
            print(f"✅ Get questions: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
                return

            # 3. Получаем конкретный вопрос
            response = client.get(f"{BASE_URL}/questions/{question_id}")
            print(f"✅ Get question: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
                return

            question_detail = response.json()
            print(f"Question details: {json.dumps(question_detail,
                                                  indent=2,
                                                  default=str)}")

            # 4. Добавляем ответ
            answer_data = {"text": "FastAPI is a modern web framework",
                           "user_id": "test_user"}

            response = client.post(
                f"{BASE_URL}/questions/{question_id}/answers",
                json=answer_data)
            print(f"✅ Create answer: {response.status_code}")
            if response.status_code != 201:
                print(f"Error: {response.text}")
                return

            answer = response.json()
            answer_id = answer["id"]

            # 5. Получаем ответ
            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            print(f"✅ Get answer: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
                return

            # 6. Удаляем вопрос (должны удалиться и ответы)
            response = client.delete(f"{BASE_URL}/questions/{question_id}")
            print(f"✅ Delete question: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
                return

            # 7. Проверяем что ответ удалился каскадно
            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            print(
                f"✅ Cascade delete: {response.status_code} (should be 404)")

            print("🎉 API test completed!")

        except Exception as e:
            print(f"❌ Exception during test: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_api()
