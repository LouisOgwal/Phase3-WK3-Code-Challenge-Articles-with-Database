from database.connection import get_connection

class Author:
    def __init__(self, id, name):
        if isinstance(name, str) and len(name) > 0:
            self._id = id
            self._name = name
            self._save_to_db()
        else:
            raise ValueError("Name must be a non-empty string")

    def _save_to_db(self):
        connection = get_connection()
        cursor = connection.cursor()

        # Check if the author already exists
        cursor.execute("SELECT id FROM authors WHERE id = ?", (self._id,))
        existing_author = cursor.fetchone()

        if not existing_author:
            # Author doesn't exist, so insert a new one
            cursor.execute("INSERT INTO authors (id, name) VALUES (?, ?)", (self._id, self._name))
        else:
            print(f"Author with ID {self._id} already exists.")

        connection.commit()
        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    # Object Relationship Methods
    def articles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def magazines(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* 
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        magazines = cursor.fetchall()
        connection.close()
        return magazines