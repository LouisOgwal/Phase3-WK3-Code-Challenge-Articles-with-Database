import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'models')))

from models.Author import Author
from models.Magazine import Magazine
from models.Article import Article
from database.setup import create_tables

# Initialize the database tables
create_tables()

# Create instances
author1 = Author(1, "John Doe")
magazine1 = Magazine(1, "Tech Monthly", "Technology")
article1 = Article(author1, magazine1, "The Future of AI")

# Testing methods
print(author1.articles())
print(magazine1.articles())
print(magazine1.article_titles())