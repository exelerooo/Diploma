import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    GPT2LMHeadModel
)
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Tuple
import spacy
import pandas as pd
from collections import defaultdict

class LanguageExerciseGenerator:
    def __init__(self, model_path: str, vocabulary_path: str):
        # Загружаем базовую языковую модель
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        
        # Загружаем spaCy для обработки текста
        self.nlp = spacy.load('en_core_web_sm')
        
        # Загружаем словарь
        self.vocabulary = pd.read_csv(vocabulary_path)
        self.vocab_words = set(self.vocabulary['word'].str.lower())
        
        # Кэш для определений
        self.definitions_cache = {}
        
    def get_dictionary_definition(self, word: str) -> str:
        """Получает определение слова из онлайн-словарей"""
        if word in self.definitions_cache:
            return self.definitions_cache[word]
            
        # Здесь должен быть код для обращения к API словарей
        # В реальном приложении нужно использовать официальные API
        # Cambridge и Oxford словарей
        url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
        # Добавьте proper headers и API ключи
        
        definition = "Sample definition"  # Заглушка
        self.definitions_cache[word] = definition
        return definition
        
    def generate_gap_fill(self, word: str) -> Dict:
        """Генерирует упражнение на заполнение пропусков"""
        prompt = f"Create a sentence using the word '{word}' and replace it with _____ : "
        
        # Генерируем предложение с помощью модели
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_length=100,
            num_return_sequences=1,
            temperature=0.7
        )
        
        sentence = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Обработка и форматирование предложения
        
        return {
            "type": "gap_fill",
            "sentence": sentence,
            "answer": word
        }
        
    def generate_paraphrase(self, sentence: str) -> Dict:
        """Генерирует упражнение на перефразирование"""
        prompt = f"Paraphrase this sentence: {sentence}"
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_length=100,
            num_return_sequences=1,
            temperature=0.7
        )
        
        paraphrase = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "type": "paraphrase",
            "original": sentence,
            "paraphrase": paraphrase
        }
        
    def generate_matching(self, words: List[str]) -> Dict:
        """Генерирует упражнение на соотнесение слов с определениями"""
        definitions = {}
        for word in words:
            definitions[word] = self.get_dictionary_definition(word)
            
        return {
            "type": "matching",
            "words": words,
            "definitions": definitions
        }
        
    def generate_translation(self, sentence: str, target_lang: str) -> Dict:
        """Генерирует упражнение на перевод"""
        # Здесь должен быть код для обращения к API перевода
        # В реальном приложении нужно использовать официальные API
        
        return {
            "type": "translation",
            "original": sentence,
            "target_language": target_lang
        }
        
    def analyze_essay(self, essay_text: str) -> Dict:
        """Анализирует эссе и находит использование слов из вокабуляра"""
        doc = self.nlp(essay_text.lower())
        
        # Находим совпадения со словарем
        matches = defaultdict(list)
        corrected_text = essay_text
        
        for sent in doc.sents:
            for token in sent:
                # Проверяем отдельные слова
                if token.text in self.vocab_words:
                    matches[token.text].append(str(sent))
                
                # Проверяем словосочетания
                if token.i < len(doc) - 1:
                    bigram = token.text + " " + doc[token.i + 1].text
                    if bigram in self.vocab_words:
                        matches[bigram].append(str(sent))
                        
        # Выделяем найденные слова в тексте
        for word, contexts in matches.items():
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            replacement = f"{word} (**{word}**)"
            corrected_text = pattern.sub(replacement, corrected_text)
            
        return {
            "corrected_text": corrected_text,
            "matches": dict(matches)
        }
        
    def generate_exercises(self, vocabulary: List[str]) -> Dict:
        """Генерирует полный набор упражнений для заданного вокабуляра"""
        exercises = {
            "gap_fill": [],
            "paraphrase": [],
            "matching": [],
            "translation": []
        }
        
        # Генерируем упражнения каждого типа
        for word in vocabulary:
            exercises["gap_fill"].append(self.generate_gap_fill(word))
            
        # Группируем слова для упражнения на соответствие
        chunk_size = 5
        for i in range(0, len(vocabulary), chunk_size):
            chunk = vocabulary[i:i + chunk_size]
            exercises["matching"].append(self.generate_matching(chunk))
            
        return exercises

# Пример использования:
"""
generator = LanguageExerciseGenerator(
    model_path="path_to_your_distilled_model",
    vocabulary_path="path_to_vocabulary.csv"
)

# Генерация упражнений
vocabulary = ["example", "word", "another", "test"]
exercises = generator.generate_exercises(vocabulary)

# Анализ эссе
essay = "This is a sample essay using some vocabulary words..."
analysis = generator.analyze_essay(essay)
"""
