// Типы для работы с анализом тональности
interface SentimentResult {
  positivePercent: number;
  negativePercent: number;
  neutralPercent: number;
  adjustedNeutralPercent: number;
  sentiment: string;
  foundPositive: string[];
  foundNegative: string[];
  keywordsText: string;
}

// Навигация между страницами
document.addEventListener('DOMContentLoaded', function(): void {
  const navButtons: NodeListOf<HTMLButtonElement> = document.querySelectorAll('#main-nav button');
  const pages: NodeListOf<HTMLElement> = document.querySelectorAll('.page');
  
  navButtons.forEach(button => {
    button.addEventListener('click', function(this: HTMLButtonElement): void {
      const pageId: string | null = this.getAttribute('data-page');
      
      // Удаляем активный класс у всех кнопок и страниц
      navButtons.forEach(btn => btn.classList.remove('active'));
      pages.forEach(page => page.classList.remove('active'));
      
      // Добавляем активный класс выбранной кнопке и странице
      this.classList.add('active');
      if (pageId) {
        const targetPage: HTMLElement | null = document.getElementById(pageId);
        if (targetPage) {
          targetPage.classList.add('active');
        }
      }
    });
  });
  
  // Демонстрация анализа тональности
  const analyzeBtn: HTMLButtonElement | null = document.getElementById('analyze-btn') as HTMLButtonElement;
  const sentimentInput: HTMLTextAreaElement | null = document.getElementById('sentiment-input') as HTMLTextAreaElement;
  const demoResult: HTMLElement | null = document.getElementById('demo-result');
  
  if (analyzeBtn && sentimentInput) {
    analyzeBtn.addEventListener('click', function(): void {
      const text: string = sentimentInput.value.trim();
      if (text.length < 3) {
        alert('Пожалуйста, введите более длинный текст для анализа.');
        return;
      }
      
      // Имитация анализа (в реальном приложении здесь был бы запрос к API)
      analyzeSentiment(text);
    });
  }
});

// Функция имитации анализа тональности
function analyzeSentiment(text: string): void {
  // Простая имитация работы анализатора на основе ключевых слов
  // В реальном приложении здесь был бы вызов API или местной модели
  
  const positiveWords: string[] = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'best', 'beautiful', 'enjoy', 'fantastic', 'perfect', 'pleased', 'delighted', 'impressive'];
  const negativeWords: string[] = ['bad', 'terrible', 'awful', 'horrible', 'sad', 'hate', 'worst', 'ugly', 'disappointing', 'poor', 'negative', 'unfortunately', 'upset', 'annoying', 'failed'];
  
  const words: string[] = text.toLowerCase().match(/\b(\w+)\b/g) || [];
  let positiveCount: number = 0;
  let negativeCount: number = 0;
  
  const foundPositive: string[] = [];
  const foundNegative: string[] = [];
  
  words.forEach(word => {
    if (positiveWords.includes(word)) {
      positiveCount++;
      if (!foundPositive.includes(word)) foundPositive.push(word);
    }
    if (negativeWords.includes(word)) {
      negativeCount++;
      if (!foundNegative.includes(word)) foundNegative.push(word);
    }
  });
  
  const wordCount: number = words.length;
  const neutralCount: number = wordCount - positiveCount - negativeCount;
  
  // Расчет процентов
  const positivePercent: number = Math.round((positiveCount / Math.max(wordCount, 1)) * 100);
  const negativePercent: number = Math.round((negativeCount / Math.max(wordCount, 1)) * 100);
  const neutralPercent: number = 100 - positivePercent - negativePercent;
  
  // Коррекция чтобы сумма была 100%
  let totalPercent: number = positivePercent + negativePercent + neutralPercent;
  let adjustedNeutralPercent: number = neutralPercent;
  if (totalPercent !== 100) {
    adjustedNeutralPercent += (100 - totalPercent);
  }
  
  // Обновление интерфейса
  const positiveBar: HTMLElement | null = document.getElementById('positive-bar');
  const neutralBar: HTMLElement | null = document.getElementById('neutral-bar');
  const negativeBar: HTMLElement | null = document.getElementById('negative-bar');
  
  const positiveValue: HTMLElement | null = document.getElementById('positive-value');
  const neutralValue: HTMLElement | null = document.getElementById('neutral-value');
  const negativeValue: HTMLElement | null = document.getElementById('negative-value');
  
  const sentimentSummary: HTMLElement | null = document.getElementById('sentiment-summary');
  const keywords: HTMLElement | null = document.getElementById('keywords');
  const demoResult: HTMLElement | null = document.getElementById('demo-result');
  
  if (positiveBar) positiveBar.style.width = positivePercent + '%';
  if (neutralBar) neutralBar.style.width = adjustedNeutralPercent + '%';
  if (negativeBar) negativeBar.style.width = negativePercent + '%';
  
  if (positiveValue) positiveValue.textContent = positivePercent + '%';
  if (neutralValue) neutralValue.textContent = adjustedNeutralPercent + '%';
  if (negativeValue) negativeValue.textContent = negativePercent + '%';
  
  // Определение преобладающей тональности
  let sentiment: string = 'нейтральная';
  if (positivePercent > negativePercent && positivePercent > adjustedNeutralPercent) {
    sentiment = 'положительная';
  } else if (negativePercent > positivePercent && negativePercent > adjustedNeutralPercent) {
    sentiment = 'отрицательная';
  }
  
  if (sentimentSummary) {
    sentimentSummary.textContent = `Преобладающая тональность текста: ${sentiment}`;
  }
  
  let keywordsText: string = '';
  if (foundPositive.length > 0) {
    keywordsText += `Положительные: ${foundPositive.join(', ')}. `;
  }
  if (foundNegative.length > 0) {
    keywordsText += `Отрицательные: ${foundNegative.join(', ')}.`;
  }
  if (keywordsText === '') {
    keywordsText = 'В тексте не обнаружены явные эмоционально окрашенные слова из нашего словаря.';
  }
  
  if (keywords) keywords.textContent = keywordsText;
  if (demoResult) demoResult.style.display = 'block';
}
