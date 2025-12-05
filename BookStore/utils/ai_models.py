import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
from django.db.models import Q
from apps.book.models import Book, Review
from apps.user.models import User
from apps.order.models import RecommendationEngine
import torch.nn.functional as F

# --- Device ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device set to use", device)

# -------------------------
# 1. Embedding Model
# -------------------------
# Sử dụng MiniLM từ HuggingFace cho embeddings
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
embedding_model = AutoModel.from_pretrained(embedding_model_name).to(device)
embedding_model.eval()

def get_book_embedding(text: str):
    """Trả về embedding tensor cho 1 đoạn text."""
    with torch.no_grad():
        encoded_input = embedding_tokenizer(text, padding=True, truncation=True, return_tensors="pt").to(device)
        model_output = embedding_model(**encoded_input)
        embeddings = model_output.last_hidden_state[:,0,:]  # CLS token
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.squeeze(0)

def get_similar_books(book_id, top_k=5):
    """Trả về danh sách Book tương tự dựa trên title + description."""
    all_books = list(Book.objects.all())
    target_book = Book.objects.get(id=book_id)
    target_text = f"{target_book.title}. {target_book.description}"
    target_embedding = get_book_embedding(target_text)

    similarities = []
    for book in all_books:
        text = f"{book.title}. {book.description}"
        emb = get_book_embedding(text)
        sim = torch.cosine_similarity(target_embedding, emb, dim=0)
        similarities.append(sim.item())

    # Lấy top_k index, loại bỏ bản thân sách
    sim_tensor = torch.tensor(similarities)
    sim_tensor[all_books.index(target_book)] = -1  # tránh sách gốc
    top_indices = sim_tensor.topk(top_k).indices.tolist()

    result_books = [all_books[i] for i in top_indices]
    return result_books

# -------------------------
# 2. Recommendation Model
# -------------------------
def recommend_books_for_user(user_id, top_k=5):
    """Gợi ý sách dựa trên lịch sử order của user."""
    user = User.objects.get(id=user_id)
    try:
        engine = RecommendationEngine.objects.get(user=user)
        history_books = list(engine.order_history.all())
    except RecommendationEngine.DoesNotExist:
        history_books = []

    # Nếu không có lịch sử, lấy top sách bán chạy
    if not history_books:
        return list(Book.objects.all().order_by("-sold")[:top_k])

    # Tính embedding trung bình của lịch sử
    hist_embeddings = torch.stack([get_book_embedding(f"{b.title}. {b.description}") for b in history_books])
    hist_mean = hist_embeddings.mean(dim=0)

    # Tính similarity với tất cả sách
    all_books = list(Book.objects.all())
    similarities = []
    for book in all_books:
        emb = get_book_embedding(f"{book.title}. {book.description}")
        sim = torch.cosine_similarity(hist_mean, emb, dim=0)
        similarities.append(sim.item())

    # Lấy top_k sách không có trong history
    sim_tensor = torch.tensor(similarities)
    for idx, b in enumerate(all_books):
        if b in history_books:
            sim_tensor[idx] = -1
    top_indices = sim_tensor.topk(top_k).indices.tolist()

    result_books = [all_books[i] for i in top_indices]
    return result_books

# -------------------------
# 3. Sentiment Model
# -------------------------
# Sử dụng model phân loại sentiment của HuggingFace
sentiment_model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name).to(device)
sentiment_model.eval()

def analyze_review_sentiment(review_id):
    """Trả về label (Positive/Negative) và score cho review."""
    review = Review.objects.get(id=review_id)
    text = review.content
    encoded_input = sentiment_tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        output = sentiment_model(**encoded_input)
        probs = torch.softmax(output.logits, dim=-1)
        score, label_idx = torch.max(probs, dim=1)
        label_idx = label_idx.item()
        score = score.item()

    # Nhãn model nlptown: 0-4 tương ứng 1-5 sao
    if label_idx >= 3:
        label = "Positive"
    else:
        label = "Negative"
    return label, score
