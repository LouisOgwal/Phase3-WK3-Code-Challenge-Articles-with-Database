from database.connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        # Validate the name and category
        if isinstance(name, str) and 2 <= len(name) <= 16:
            if isinstance(category, str) and len(category) > 0:
                self._id = id
                self._name = name
                self._category = category
                self._save_to_db()
            else:
                raise ValueError("Category must be a non-empty string")
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    def _save_to_db(self):
        connection = get_connection()
        cursor = connection.cursor()

        # Check if the magazine ID already exists
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self._id,))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"Magazine with ID {self._id} already exists.")
        else:
            cursor.execute("INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)", 
                           (self._id, self._name, self._category))
            connection.commit()
            print(f"Magazine '{self._name}' added to database.")

        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    # Object Relationship Methods
    def articles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def contributors(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* 
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._id,))
        contributors = cursor.fetchall()
        connection.close()
        return contributors

    # Aggregate Methods
    def article_titles(self):
        articles = self.articles()
        return [article[1] for article in articles] if articles else None

    def contributing_authors(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._id,))
        authors = cursor.fetchall()
        connection.close()
        return authors if authors else None