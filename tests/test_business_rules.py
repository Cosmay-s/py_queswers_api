import httpx
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_business_rules():
    """
    Тест бизнес-правил приложения.

    Фокусируется только на проверке логики и требований к поведению:
    - Нельзя создать ответ к несуществующему вопросу;
    - Один юзер может создавать несколько ответов к одному вопросу;
    - При удалении вопроса все связанные ответы удаляются каскадно.

    Не проверяет базовые CRUD-операции, а только бизнес-логику.
    """
    print("🧪 Тестируем бизнес-правила...")

    time.sleep(1)

    with httpx.Client(timeout=30.0) as client:
        try:
            # 1. Нельзя создать ответ к несуществующему вопросу
            print(
                "== Тест 1: Нельзя создать ответ к несуществующему вопросу =="
            )
            answer_data = {
                "text": "Этот ответ не должен создаться",
                "user_id": "test_user",
            }
            response = client.post(
                f"{BASE_URL}/answers/questions/9999/answers/", json=answer_data
            )
            assert response.status_code == 404, "Должен вернуть статус 404"
            print("✅ Нельзя создать ответ к несуществующему вопросу")

            # 2. Один юзер может оставлять несколько ответов на один вопрос
            print(
                "== Тест 2: Один юзер может оставить несколько ответов "
                "к одному вопросу =="
            )

            # Создаем вопрос
            question_data = {
                "text": "Может ли один юзер оставить несколько ответов?"
            }
            response = client.post(
                f"{BASE_URL}/questions/",
                json=question_data
                )
            question_id = response.json()["id"]

            # Первый ответ от юзера
            answer1_data = {
                "text": "Первый ответ от юзера",
                "user_id": "same_user",
            }
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer1_data,
            )
            assert response.status_code == 201
            answer1_id = response.json()["id"]

            # Второй ответ от того же юзера
            answer2_data = {
                "text": "Второй ответ от того же юзера",
                "user_id": "same_user",
            }
            response = client.post(
                f"{BASE_URL}/answers/questions/{question_id}/answers/",
                json=answer2_data,
            )
            assert response.status_code == 201
            answer2_id = response.json()["id"]

            # Проверяем, что оба ответа создались
            response = client.get(f"{BASE_URL}/questions/{question_id}")
            question = response.json()
            assert len(question["answers"]) == 2
            assert question["answers"][0]["user_id"] == "same_user"
            assert question["answers"][1]["user_id"] == "same_user"
            print(
                "✅ Один юзер может оставить несколько ответов "
                "к одному вопросу"
            )

            # 3. Тест: Каскадное удаление ответов при удалении вопроса
            print(
                "=== Тест 3: Каскадное удаление при удалении вопроса ==="
                )

            # Удаляем вопрос
            response = client.delete(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200

            # Проверяем, что ответы удалились
            response = client.get(f"{BASE_URL}/answers/{answer1_id}")
            assert response.status_code == 404
            response = client.get(f"{BASE_URL}/answers/{answer2_id}")
            assert response.status_code == 404
            print("✅ Ответы удаляются каскадно при удалении вопроса")

            print("🎉 Все бизнес-правила работают корректно!")
            return True

        except Exception as e:
            print(f"❌ Тест бизнес-правил провален: {e}")
            import traceback

            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = test_business_rules()
    exit(0 if success else 1)
