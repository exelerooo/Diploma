import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    GPT2Config,
    GPT2LMHeadModel
)

class DistilledModel(nn.Module):
    def __init__(self, vocab_size, hidden_size=256, num_layers=4):
        super().__init__()
        self.config = GPT2Config(
            vocab_size=vocab_size,
            n_embd=hidden_size,
            n_layer=num_layers,
            n_head=8
        )
        self.model = GPT2LMHeadModel(self.config)
        
    def forward(self, input_ids, attention_mask=None):
        return self.model(input_ids, attention_mask=attention_mask)

def distill_model(teacher_model_name, train_dataset, output_dir, 
                  batch_size=16, num_epochs=3, learning_rate=5e-5):
    # Загружаем модель-учитель
    teacher_tokenizer = AutoTokenizer.from_pretrained(teacher_model_name)
    teacher_model = AutoModelForCausalLM.from_pretrained(teacher_model_name)
    teacher_model.eval()  # Переводим в режим оценки
    
    # Создаем уменьшенную модель-ученик
    student_model = DistilledModel(
        vocab_size=teacher_tokenizer.vocab_size,
        hidden_size=256,  # Уменьшенный размер скрытого состояния
        num_layers=4      # Уменьшенное количество слоев
    )
    
    # Подготовка данных
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Оптимизатор и функция потерь
    optimizer = torch.optim.AdamW(student_model.parameters(), lr=learning_rate)
    kl_loss = nn.KLDivLoss(reduction='batchmean')
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    teacher_model.to(device)
    student_model.to(device)
    
    # Цикл обучения
    for epoch in range(num_epochs):
        student_model.train()
        total_loss = 0
        
        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            
            # Получаем логиты от учителя
            with torch.no_grad():
                teacher_outputs = teacher_model(input_ids, attention_mask=attention_mask)
                teacher_logits = teacher_outputs.logits
            
            # Получаем логиты от ученика
            student_outputs = student_model(input_ids, attention_mask=attention_mask)
            student_logits = student_outputs.logits
            
            # Вычисляем потери дистилляции
            loss = kl_loss(
                torch.log_softmax(student_logits/1.0, dim=-1),
                torch.softmax(teacher_logits/1.0, dim=-1)
            )
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(train_loader)
        print(f'Epoch {epoch+1}/{num_epochs}, Average Loss: {avg_loss:.4f}')
    
    # Сохраняем модель
    student_model.save_pretrained(output_dir)
    teacher_tokenizer.save_pretrained(output_dir)
    
    return student_model, teacher_tokenizer

# Пример использования:
"""
teacher_model_name = "gpt2"  # или другая модель
train_dataset = ...  # ваш набор данных для обучения
output_dir = "distilled_model"

distilled_model, tokenizer = distill_model(
    teacher_model_name=teacher_model_name,
    train_dataset=train_dataset,
    output_dir=output_dir
)
"""
