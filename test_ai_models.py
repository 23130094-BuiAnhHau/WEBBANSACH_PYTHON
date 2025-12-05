import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStore.settings")
django.setup()

from apps.book.models import Book, Review
from apps.user.models import User
from BookStore.utils.ai_models import (
    get_similar_books,
    recommend_books_for_user,
    analyze_review_sentiment,
)


print("=== Test Embedding ===")
book = Book.objects.first()
if book:
    print([b.title for b in get_similar_books(book.id)])

print("\n=== Test Recommendation ===")
user = User.objects.filter(is_customer=True).first()
if user:
    print([b.title for b in recommend_books_for_user(user.id)])

print("\n=== Test Sentiment ===")
review = Review.objects.first()
if review:
    print(analyze_review_sentiment(review.id))

print("\nAI DONE OK")
