import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.tokenize import sent_tokenize


def is_huggingface_model(directory):
    """Check if the directory contains a fine-tuned Hugging Face model."""
    required_files = {
        "config.json",
        # "pytorch_model.bin",
    }  # or 'tf_model.h5' for TensorFlow models
    directory_files = set(os.listdir(directory))
    return required_files.issubset(directory_files)


def is_pytorch_model(directory):
    """Check if the directory contains a PyTorch model file."""
    pytorch_files = [
        file for file in os.listdir(directory) if file.endswith((".pt", ".pth"))
    ]
    return len(pytorch_files) > 0


def is_model_directory(directory):
    """Check if the directory contains a fine-tuned model of any known type."""
    if is_huggingface_model(directory):
        print("The directory contains a Hugging Face model.")
        return True
    elif is_pytorch_model(directory):
        print("The directory contains a PyTorch model.")
        return True
    else:
        print("The directory does not contain any recognized fine-tuned model.")
        return False


def get_important_sentences(df, field, n=100):
    # Step 1: split sentences
    df["sentences"] = df[field].apply(filter_sentences_by_words).str.split(".")

    # Step 2: Flatten the list of sentences
    sentences = df["sentences"].explode().dropna().str.strip()

    # Step 3: Use TF-IDF to compute sentence importance
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(sentences)

    # Step 4: Sum the TF-IDF scores for each sentence
    sentence_scores = tfidf_matrix.sum(axis=1).A1  # A1 converts to a 1D array

    # Step 5: Sort the sentences based on their scores
    sorted_indices = sentence_scores.argsort()[::-1]  # Sort in descending order
    sorted_sentences = sentences.iloc[sorted_indices[:]]

    # Step 6: Select top n sentences
    top_n_sentences = sorted_sentences.head(n)

    return top_n_sentences.tolist()


def filter_sentences_by_words(
    paragraph: str,
    related_words=["smoke", "smoking", "cigarette", "nicotine", "tobacco"],
):
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        # nltk.download("punkt") This is old version which consists in unsafe pickles
        nltk.download("punkt_tab")
        print("downloading nltk")
    sentences = sent_tokenize(paragraph)
    filtered_sentences = [
        sentence
        for sentence in sentences
        if any(
            re.search(rf"\b{word}\b", sentence, re.IGNORECASE) for word in related_words
        )
    ]
    return "\n".join(filtered_sentences)
