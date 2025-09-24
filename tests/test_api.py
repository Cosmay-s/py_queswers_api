import httpx
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_api():
    """
    Интеграционный тест API.

    Проверяет основные CRUD-операции с вопросами и ответами:
    - создание, получение и удаление вопросов и ответов;
    - базовую работоспособность эндпоинтов.

    Включает минимальную проверку бизнес-правил для базового уровня,
    но не углубляется в логику.
    """
    print("🧪 Тестируем API и бизнес-правила...")

    time.sleep(1)

    with httpx.Client(timeout=30.0) as client:
        try:
            # Базовые операции
            print("=== Основные операции с API ===")

            # Создаем вопрос
            question_data = {"text": "Тестовый вопрос?"}
            response = client.post(
                f"{BASE_URL}/questions/",
                json=question_data
                )
            assert response.status_code == 201
            question = response.json()
            question_id = question["id"]
            print(f"✅ Вопрос создан с id={question_id}")

            # Получаем список вопросов
            response = client.get(f"{BASE_URL}/questions/")
            assert response.status_code == 200
            print("✅ Список вопросов получен")

            # Получаем вопрос по id с ответами
            response = client.get(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200
            print(f"✅ Вопрос с id={question_id} получен")

            # Создаем ответ
            answer_data = {"text": "Тестовый ответ", "user_id": "user123"}
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer_data,
            )
            assert response.status_code == 201
            answer = response.json()
            answer_id = answer["id"]
            print(f"✅ Ответ создан с id={answer_id}")

            # Получаем ответ по id
            response = client.get(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 200
            print(f"✅ Ответ с id={answer_id} получен")

            # Удаляем ответ
            response = client.delete(f"{BASE_URL}/answers/{answer_id}")
            assert response.status_code == 200
            print(f"✅ Ответ с id={answer_id} удалён")

            # Проверка бизнес-правил
            print("=== Проверка бизнес-правил ===")

            # Нельзя создать ответ к несуществующему вопросу
            print("Проверка: нельзя создать ответ к несуществующему вопросу")
            response = client.post(
                f"{BASE_URL}/answers/questions/9999/answers/", json=answer_data
            )
            assert response.status_code == 404
            print("✅ Нельзя создать ответ к несуществующему вопросу")

            # Один юзер может оставлять несколько ответов к одному вопросу
            print(
                "Проверка: юзер может оставить несколько ответов"
                )
            answer1_data = {"text": "Ответ 1", "user_id": "multi_user"}
            answer2_data = {"text": "Ответ 2", "user_id": "multi_user"}

            resp1 = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer1_data
            )
            resp2 = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer2_data
            )
            assert resp1.status_code == 201
            assert resp2.status_code == 201

            response = client.get(f"{BASE_URL}/questions/{question_id}")
            question = response.json()
            assert len(question["answers"]) == 2
            print(
                "✅ Один юзер может оставить несколько ответов к одному вопросу"
                )

            # Каскадное удаление
            print("Проверка: каскадное удаление ответов при удалении вопроса")
            response = client.delete(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200

            # Проверяем, что вопросы и ответы удалены
            response = client.get(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 404
            print("✅ Вопрос и связанные ответы удалены каскадно")

            print("🎉 Тесты API и бизнес-правил пройдены успешно!")
            return True

        except Exception as e:
            print(f"❌ Тест провален: {e}")
            return False


if __name__ == "__main__":
    test_api()
