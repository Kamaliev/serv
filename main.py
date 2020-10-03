import time


class Messenger:
    def __init__(self):
        self.db = [
            {'text': 'Привет', 'author': 'Jack', 'time': time.time()},
            {'text': 'Приве!', 'author': 'Mary', 'time': time.time()},
        ]

    def send_message(self, text, author):
        if isinstance(text, str) and isinstance(author, str):
            self.db.append({
                'text': text,
                'author': author,
                'time': time.time()
            })
            print(text, author)
            return 'OK'
        else:
            return 'Not OK'

    def get_messages(self):
        return self.db
