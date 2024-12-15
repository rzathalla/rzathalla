# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12uOlCub2NmJ06pDBxwhbYy_-vgbsjtNw
"""

from google.colab import files
uploaded = files.upload()  # Pilih file untuk diunggah

import pandas as pd

# 1. Load dataset dengan pemisah titik koma
file_path = '/content/bbc_news 2r.csv'
data = pd.read_csv(file_path, sep=';', engine='python')

# 2. Tampilkan informasi dataset
print("Jumlah baris dan kolom:", data.shape)
print("Kolom dalam dataset:", data.columns.tolist())

# 3. Tampilkan 5 baris pertama untuk verifikasi
print(data.head())

import pandas as pd

# 1. Load dataset
file_path = '/content/bbc_news 2r.csv'  # Ganti dengan nama file Anda
data = pd.read_csv(file_path, sep=';', engine='python')

# 2. Hapus kolom yang tidak diinginkan
columns_to_drop = ['Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11']
data = data.drop(columns=[col for col in columns_to_drop if col in data.columns])

# 3. Kurangi jumlah baris menjadi 7.000 (sampling secara acak)
data_sampled = data.sample(n=7000, random_state=42)  # Pilih 7000 baris secara acak

# 4. Tampilkan informasi dataset untuk verifikasi
print("Jumlah baris dan kolom setelah sampling:", data_sampled.shape)
print("Kolom dalam dataset setelah penghapusan:", data_sampled.columns.tolist())

# 5. Simpan dataset hasil ke file baru
data_sampled.to_csv('sampled_data.csv', index=False)
print("Dataset telah disimpan ke 'sampled_data.csv'")

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# 1. Unduh resource NLTK (dijalankan satu kali)
nltk.download('punkt')
nltk.download('stopwords')

# 2. Load dataset
file_path = 'sampled_data.csv'  # Ganti dengan nama file hasil sampling Anda
data = pd.read_csv(file_path)

# 3. Fungsi untuk membersihkan teks
def clean_text(text):
    # 3.1 Ubah teks menjadi huruf kecil
    text = text.lower()
    # 3.2 Hapus angka, simbol, dan tanda baca
    text = re.sub(r'[^a-z\s]', '', text)
    # 3.3 Tokenisasi (memisahkan teks menjadi kata-kata)
    tokens = word_tokenize(text)
    # 3.4 Hapus stop words (kata umum yang tidak memiliki banyak arti)
    stop_words = set(stopwords.words('indonesian'))  # Ganti 'indonesian' jika teks dalam bahasa lain
    tokens = [word for word in tokens if word not in stop_words]
    # Gabungkan kembali token menjadi teks
    return ' '.join(tokens)

# 4. Terapkan fungsi pembersihan teks
# Ganti 'kolom_teks' dengan nama kolom teks pada dataset Anda
if 'kolom_teks' in data.columns:  # Pastikan kolom teks ada di dataset
    data['cleaned_text'] = data['kolom_teks'].apply(clean_text)

# 5. Simpan dataset yang sudah dibersihkan
data.to_csv('cleaned_data.csv', index=False)
print("Dataset telah dibersihkan dan disimpan ke 'cleaned_data.csv'")

print(data.columns)

# Drop rows with missing values in the "title" column
data_cleaned = data.dropna(subset=['title']).reset_index(drop=True)

# Define initial categories and keywords for labeling
categories = {
    "Politics": ["Trump", "Biden", "government", "election", "Putin", "minister"],
    "Technology": ["TikTok", "AI", "technology", "robot", "Netflix"],
    "Health": ["health", "vaccine", "disease", "hospital", "COVID"],
    "Sports": ["football", "champion", "Olympics", "medal", "match"],
    "Others": []
}

# Assign categories based on keyword matching in the title
def label_category(title):
    for category, keywords in categories.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return category
    return "Others"

# Apply the labeling function
data_cleaned['category'] = data_cleaned['title'].apply(label_category)

# Check the distribution of categories
data_cleaned['category'].value_counts()

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
file_path = "cleaned BBCnews_data.csv"  # Ganti dengan nama file Anda
data = pd.read_csv(file_path)

# Drop rows with missing values in the "title" column
data_cleaned = data.dropna(subset=['title']).reset_index(drop=True)

# Define initial categories and keywords for labeling
categories = {
    "Politics": ["Trump", "Biden", "government", "election", "Putin", "minister"],
    "Technology": ["TikTok", "AI", "technology", "robot", "Netflix"],
    "Health": ["health", "vaccine", "disease", "hospital", "COVID"],
    "Sports": ["football", "champion", "Olympics", "medal", "match"],
    "Others": []
}

# Assign categories based on keyword matching in the title
def label_category(title):
    for category, keywords in categories.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return category
    return "Others"

# Apply the labeling function
data_cleaned['category'] = data_cleaned['title'].apply(label_category)

# Prepare labels
y = data_cleaned['category']

# Split data into training and testing sets
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    data_cleaned['title'], y, test_size=0.2, random_state=42
)

# Bag of Words (BoW) Vectorizer
bow_vectorizer = CountVectorizer(max_features=5000)
X_train_bow = bow_vectorizer.fit_transform(X_train_raw)
X_test_bow = bow_vectorizer.transform(X_test_raw)

# TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train_raw)
X_test_tfidf = tfidf_vectorizer.transform(X_test_raw)

# Train and evaluate models for BoW
print("=== Bag of Words (BoW) ===")
model_bow = MultinomialNB()
model_bow.fit(X_train_bow, y_train)
y_pred_bow = model_bow.predict(X_test_bow)
print("Classification Report (BoW):")
print(classification_report(y_test, y_pred_bow))
print(f"Accuracy (BoW): {accuracy_score(y_test, y_pred_bow):.2f}")

# Train and evaluate models for TF-IDF
print("\n=== TF-IDF ===")
model_tfidf = MultinomialNB()
model_tfidf.fit(X_train_tfidf, y_train)
y_pred_tfidf = model_tfidf.predict(X_test_tfidf)
print("Classification Report (TF-IDF):")
print(classification_report(y_test, y_pred_tfidf))
print(f"Accuracy (TF-IDF): {accuracy_score(y_test, y_pred_tfidf):.2f}")

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
file_path = "cleaned BBCnews_data.csv"  # Ganti dengan nama file Anda
data = pd.read_csv(file_path)

# Drop rows with missing values in the "title" column
data_cleaned = data.dropna(subset=['title']).reset_index(drop=True)

# Define initial categories and keywords for labeling
categories = {
    "Politics": ["Trump", "Biden", "government", "election", "Putin", "minister"],
    "Technology": ["TikTok", "AI", "technology", "robot", "Netflix"],
    "Health": ["health", "vaccine", "disease", "hospital", "COVID"],
    "Sports": ["football", "champion", "Olympics", "medal", "match"],
    "Others": []
}

# Assign categories based on keyword matching in the title
def label_category(title):
    for category, keywords in categories.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return category
    return "Others"

# Apply the labeling function
data_cleaned['category'] = data_cleaned['title'].apply(label_category)

# Prepare labels
y = data_cleaned['category']

# Split data into training and testing sets
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    data_cleaned['title'], y, test_size=0.2, random_state=42
)

# TF-IDF Vectorizer (Recommended for text classification)
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train_raw)
X_test_tfidf = tfidf_vectorizer.transform(X_test_raw)

# Train Naive Bayes Classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Predict on test set
y_pred = model.predict(X_test_tfidf)

# Evaluation
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Optional: Predict on new titles
new_titles = [
    "Government announces new policies for healthcare reform",
    "AI technology is revolutionizing industries",
    "Football championship finals held in Tokyo",
    "President addresses the nation on economic policies"
]
new_titles_tfidf = tfidf_vectorizer.transform(new_titles)
predictions = model.predict(new_titles_tfidf)
print("\nPredictions for New Titles:")
for title, category in zip(new_titles, predictions):
    print(f"Title: {title} --> Predicted Category: {category}")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Load dataset
file_path = "cleaned BBCnews_data.csv"  # Ganti dengan nama file Anda
data = pd.read_csv(file_path)

# Drop rows with missing values in the "title" column
data_cleaned = data.dropna(subset=['title']).reset_index(drop=True)

# Define initial categories and keywords for labeling
categories = {
    "Politics": ["Trump", "Biden", "government", "election", "Putin", "minister"],
    "Technology": ["TikTok", "AI", "technology", "robot", "Netflix"],
    "Health": ["health", "vaccine", "disease", "hospital", "COVID"],
    "Sports": ["football", "champion", "Olympics", "medal", "match"],
    "Others": []
}

# Assign categories based on keyword matching in the title
def label_category(title):
    for category, keywords in categories.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return category
    return "Others"

# Apply the labeling function
data_cleaned['category'] = data_cleaned['title'].apply(label_category)

# Simulate predictions (for simplicity, use the same label_category function)
y_test = data_cleaned['category']
y_pred = data_cleaned['title'].apply(label_category)

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred, labels=list(categories.keys()))

# Plot Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=categories.keys(), yticklabels=categories.keys())
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Distribution of Actual vs Predicted Categories
plt.figure(figsize=(10, 6))
actual_counts = pd.Series(y_test).value_counts().sort_index()
predicted_counts = pd.Series(y_pred).value_counts().sort_index()

width = 0.4  # Bar width
categories = actual_counts.index
x = range(len(categories))

plt.bar(x, actual_counts, width=width, label="Actual", align='center', alpha=0.7)
plt.bar([p + width for p in x], predicted_counts, width=width, label="Predicted", align='center', alpha=0.7)
plt.xticks([p + width / 2 for p in x], categories, rotation=45)
plt.title("Distribution of Actual vs Predicted Categories")
plt.xlabel("Category")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.show()