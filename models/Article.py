from database.connection import get_connection

class Article:
    def __init__(self, author, magazine, title):
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._author_id = author.id
            self._magazine_id = magazine.id
            self._title = title
            self._save_to_db()
        else:
            raise ValueError("Title must be a string between 5 and 50 characters")

    def _save_to_db(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)", (self._author_id, self._magazine_id, self._title))
        connection.commit()
        connection.close()

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self._author_id,))
        author = cursor.fetchone()
        connection.close()
        return author

    @property
    def magazine(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self._magazine_id,))
        magazine = cursor.fetchone()
        connection.close()
        return magazine