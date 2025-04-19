# pip install nltk gensim scikit-learn transformers sentencepiece

# Прочитайте текстовый файл: (Стругацкие) Тестовая_2 вместе.txt. Проведите векторизацию текста используя различные методы, в том числе предобученные модели, word2vec, Skip-Gram

import re
import nltk
import gensim
import torch
import numpy as np

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models import Word2Vec
from transformers import AutoModel, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')      # токенизация
nltk.download('stopwords')  # стоп-слова

# --- 1. Чтение файла ---
with open("(Стругацкие) Тестовая_2 вместе.txt", "r", encoding="utf-8") as f:
    text = f.read()

# --- 2. Предварительная обработка ---
# Пример: убираем лишние символы, приводим к нижнему регистру, разбиваем на предложения
text_clean = re.sub(r"[^а-яА-ЯёЁa-zA-Z0-9\s]", " ", text)  # только буквы/цифры/пробел
text_clean = re.sub(r"\s+", " ", text_clean)               # многократные пробелы -> один
text_clean = text_clean.strip().lower()

sentences = sent_tokenize(text_clean, language="russian")  # получаем список предложений
russian_stopwords = set(stopwords.words("russian"))

# Для упрощения — разбиваем каждое предложение на токены, убираем стоп-слова
all_tokens = []
for sent in sentences:
    tokens = word_tokenize(sent, language="russian")
    tokens = [t for t in tokens if t not in russian_stopwords and t.isalpha()]
    all_tokens.append(tokens)

# Если нужно — можно тут же провести лемматизацию (например, через pymorphy2 или Stanza).
# Ниже просто оставлено как комментарий-напоминание:
# from pymorphy2 import MorphAnalyzer
# morph = MorphAnalyzer()
# tokens_lemma = [morph.parse(t)[0].normal_form for t in tokens]

# --- 3. TF-IDF (мешок слов) ---
# Нужно соединить все предложения обратно, чтобы TfidfVectorizer мог работать
sentences_for_tfidf = [" ".join(toks) for toks in all_tokens if len(toks) > 0]

vectorizer = TfidfVectorizer(
    max_features=5000,   # ограничим количество фич (по частоте)
)
tfidf_matrix = vectorizer.fit_transform(sentences_for_tfidf)
print("TF-IDF shape:", tfidf_matrix.shape)
# tfidf_matrix — это разреженная матрица (число_предложений x число_признаков)

# --- 4. Word2Vec (пример с Skip-Gram) ---
# Допустим, хотим обучить свою модель:
# `sg=1` означает Skip-Gram; `sg=0` было бы CBOW
w2v_model = Word2Vec(
    all_tokens,    # список предложений, каждое предложение — список токенов
    vector_size=100,
    window=5,
    min_count=2,
    sg=1,
    epochs=10
)
word_vectors = w2v_model.wv

# Пример: получаем вектор для слова "альпинист"
if "альпинист" in word_vectors:
    vec_alpinist = word_vectors["альпинист"]
    print("Вектор 'альпинист':", vec_alpinist[:10], "...")

# Чтобы получить вектор для целого предложения, можно усреднить вектора всех токенов
def sentence_vector_w2v(tokens, word_vecs):
    valid_vecs = []
    for t in tokens:
        if t in word_vecs:
            valid_vecs.append(word_vecs[t])
    if len(valid_vecs) == 0:
        return np.zeros(w2v_model.vector_size)
    else:
        return np.mean(valid_vecs, axis=0)

example_sent = all_tokens[0]  # пусть возьмём первое предложение
example_sent_vec = sentence_vector_w2v(example_sent, word_vectors)
print("Пример вектора предложения (Word2Vec):", example_sent_vec[:10], "...")

# --- 5. Предобученные трансформеры (пример: 'bert-base-multilingual-cased') ---
# Можно взять любую подходящую модель, напр. для русского 'DeepPavlov/rubert-base-cased'
model_name = "DeepPavlov/rubert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)
bert_model.eval()

# Вариант: для каждой фразы делаем embedding CLS-токена
def encode_sentence_transformer(sent: str):
    # Токенизируем
    inputs = tokenizer(sent, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Обычно embedding CLS-токена лежит в outputs.last_hidden_state[:, 0, :]
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return cls_embedding

# Пример: берём первое предложение и переводим в BERT-вектор
example_sent_str = " ".join(example_sent)
example_bert_vec = encode_sentence_transformer(example_sent_str)
print("Shape BERT-вектора:", example_bert_vec.shape)
