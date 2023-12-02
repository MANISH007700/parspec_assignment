from transformers import BertTokenizer, BertForSequenceClassification
import torch

def make_pred(model, tokenizer, input_clean_text) -> str:

    id2label = {0: "Not a Lighting Pdf", 1: "Lighting pdf"}

    inputs = tokenizer(input_clean_text, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    output_class = predictions.argmax().item()

    print("Pred class from model -> ", id2label[output_class])
    
    return {"category": id2label[output_class], "id": output_class}
