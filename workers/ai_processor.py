from transformers import pipeline
import re

class AIProcessor:
    
    def __init__(self):
        print("Carregando modelo de sumarização...")
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        print("Modelo de sumarização carregado com sucesso!")
    
    def analyze_sentiment(self, text: str):
        """
        Analisa o sentimento do texto
        
        Returns:
            tuple: (sentiment_type, score)
        """
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            
            label = result['label']
            stars = int(label.split()[0])
            
            if stars >= 4:
                sentiment = "positive"
                score = 0.5 + (stars - 4) * 0.5
            elif stars <= 2:
                sentiment = "negative"
                score = -0.5 - (2 - stars) * 0.5
            else:
                sentiment = "neutral"
                score = 0.0
            
            return sentiment, score
            
        except Exception as e:
            print(f"Erro na analise de sentimento: {e}")
            return "neutral", 0.0
    
    def detect_spam(self, text: str):
        """
        Detecta se a mensagem é spam
        
        Returns:
            int: 1 se spam, 0 se não spam
        """
        spam_patterns = [
            r'clique aqui',
            r'ganhe dinheiro',
            r'promoção imperdível',
            r'compre agora',
            r'oferta limitada',
            r'viagra',
            r'bitcoin',
            r'investimento garantido',
        ]
        
        text_lower = text.lower()
        
        for pattern in spam_patterns:
            if re.search(pattern, text_lower):
                return 1 
        
        if len(text) > 10:
            uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
            if uppercase_ratio > 0.7:
                return 1
        
        return 0 


ai_processor = AIProcessor()