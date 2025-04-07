import requests
from bs4 import BeautifulSoup


class QuizParser:
    def __init__(self):
        self.all_answers = 0
        self.right_answers = 0
        self.base_url = "https://baza-otvetov.ru/quiz"
        self.session = requests.Session()
        # Устанавливаем заголовки, чтобы имитировать браузер
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def get_new_question(self):
        """Получить новый вопрос викторины"""
        url = f"{self.base_url}/ask"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Извлекаем вопрос и его ID
            question_tag = soup.find('h3', class_='q_id')
            if not question_tag:
                return None
            self.question_id = question_tag.get('id')
            question_text = question_tag.get_text(strip=True)
            # Извлекаем варианты ответов
            answers = [h4.get_text(strip=True) for h4 in soup.find_all('h4')]
            return {
                'question_id': self.question_id,
                'question_text': question_text,
                'answers': answers
            }
        except Exception as e:
            print(f"Ошибка при получении вопроса: {e}")
            return None

    def check_answer(self, answer):
        """Проверить ответ на вопрос"""
        url = f"{self.base_url}/check"
        try:
            data = {
                'q_id': self.question_id,
                'answer': answer
            }
            response = self.session.post(url, data=data)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            result_tag = soup.find('h3', style=True)
            if not result_tag:
                return {'correct': False, 'message': 'Не удалось определить результат'}
            self.all_answers += 1
            result_tag = soup.find('h3', style=True)
            result_text = result_tag.get_text(strip=True)
            # Проверяем, правильный ли ответ
            correct = None
            if 'Правильно!' in result_text:
                correct_answer = result_tag.get_text('\n', strip=True).split('\n')[-1]
                self.right_answers += 1
                correct = True
            else:
                correct = False
                correct_answer_tag = soup.find('span', style="color:#339966")
                correct_answer = correct_answer_tag.get_text(strip=True)
            return {
                'correct': correct,
                'correct_answer': correct_answer,
                'statistics': f'Правильных ответов: {self.right_answers} из {self.all_answers}'
            }
        except Exception as e:
            print(f"Ошибка при проверке ответа: {e}")
            return {'correct': False, 'message': f'Ошибка: {e}'}
