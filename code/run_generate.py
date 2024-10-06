import torch
from transformers import GPT2Tokenizer
from Model import GatedTransformerDecoder, GPT2Wrapper
import json
from types import SimpleNamespace

def load_model(model_path, config_path):
    with open(config_path, 'r') as f:
        config = SimpleNamespace(**json.load(f))
    model = GatedTransformerDecoder(config, n_head=8, n_layers=6)
    model = torch.nn.DataParallel(model)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    return model

def generate_text(input_data, model_path, tokenizer_path, config_path):
    model = load_model(model_path, config_path)
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    wrapper_model = GPT2Wrapper(model)

    # 입력 데이터 준비
    encoded_input = tokenizer.encode(input_data, add_special_tokens=False, return_tensors="pt")
    batch_size, seq_len = encoded_input.shape
    
    # entity_ids, triple_ids, position_ids 준비
    entity_ids = torch.zeros_like(encoded_input)
    triple_ids = torch.zeros_like(encoded_input)
    position_ids = torch.arange(seq_len, dtype=torch.long).unsqueeze(0).repeat(batch_size, 1)

    # tgt_seq 준비 (시작 토큰으로 초기화)
    tgt_seq = torch.LongTensor([[tokenizer.bos_token_id]])

    # 생성
    with torch.no_grad():
        for _ in range(100):  # 최대 100 토큰 생성
            outputs = model(encoded_input, entity_ids, triple_ids, position_ids, tgt_seq)
            next_token_logits = outputs[:, -1, :]
            next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)
            tgt_seq = torch.cat([tgt_seq, next_token], dim=-1)
            if next_token.item() == tokenizer.eos_token_id:
                break

    generated_sequence = tgt_seq[0].tolist()
    text = tokenizer.decode(generated_sequence)
    
    return text

model_path = "../checkpoint_webnlg/checkpoint_finetune_sequence_head8_layer6_GPT2_maxfact12_from_ep14/model_ep30.pt"
tokenizer_path = "../GPT2_tokenizer"
config_path = "../GPT2_tokenizer/knowledge_config.json"

input_data_list = [
    "Alan Shepard Nationality United States . Alan Shepard Occupation Test pilot . Alan Shepard Awards Distinguished Service Medal . Alan Shepard Status Deceased .",
    "Marie Curie Nationality Poland . Marie Curie Occupation Physicist . Marie Curie Awards Nobel Prize in Physics . Marie Curie Status Deceased .",
    "Elon Musk Nationality South Africa . Elon Musk Occupation Entrepreneur . Elon Musk Company SpaceX . Elon Musk Status Alive .",
    "William Shakespeare Nationality England . William Shakespeare Occupation Playwright . William Shakespeare Work Hamlet . William Shakespeare Status Deceased .",
    "Malala Yousafzai Nationality Pakistan . Malala Yousafzai Occupation Activist . Malala Yousafzai Awards Nobel Peace Prize . Malala Yousafzai Status Alive ."
]

input_data = input_data_list[2];
generated_text = generate_text(input_data, model_path, tokenizer_path, config_path)
print(generated_text)