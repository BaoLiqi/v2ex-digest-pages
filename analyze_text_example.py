import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()


def get_prompt(chinese_text):
    translation_marker = "<TRANSLATION>"
    messages = [
        {"role": "system", "content": "You are a helpful assistant that translates Chinese to English. Only Output the translation."},
        {"role": "user", "content": f"{chinese_text}"},
        {"role": "assistant", "content": translation_marker}
    ]

    text_prefix = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False
    )

    start_index = text_prefix.find(translation_marker)

    if start_index == -1:
        raise ValueError(
            f"The marker '{translation_marker}' was not found in the text_prefix.")
    else:
        return text_prefix[0:start_index]



def get_next_word_candidates(input_ids, top_k=10, top_p=0.99):
    with torch.no_grad():
        # Ensure input_ids are LongTensor and on the same device as the model
        input_ids = input_ids.to(model.device).long()
        outputs = model(input_ids)  # Use the model directly, not model.forward
    logits = outputs.logits
    next_token_logits = logits[0, -1, :]
    probs = torch.softmax(next_token_logits, dim=0)
    top_probs, top_indices = torch.topk(probs, top_k)
    cumulative_probs = torch.cumsum(top_probs, dim=0)

    # Find the index where cumulative probability exceeds top_p
    exceed_index = (cumulative_probs > top_p).nonzero()
    if len(exceed_index) > 0:
        cutoff_index = exceed_index[0].item() + 1  # Include the index where it exceeds
    else:
        cutoff_index = top_k  # If no index exceeds, take all top_k

    top_p_indices = top_indices[:cutoff_index]
    top_p_probs = top_probs[:cutoff_index]


    suggestions = []
    for idx, prob in zip(top_p_indices, top_p_probs):
        token_str = tokenizer.decode([idx.item()])
        suggestions.append({"token": token_str.strip(), "probability": round(prob.item(), 4)})
    return suggestions



def analyze_english_text(english_text, chinese_text):
    prompt = get_prompt(chinese_text)
    # prompt_ids = tokenizer.encode(prompt, return_tensors='pt', add_special_tokens=False)

    # Tokenize the full text. (The Chinese text isn't used in this snippet, but it might be used in the full prompt.)
    input_ids = tokenizer.encode(english_text, return_tensors='pt', add_special_tokens=False)
    analysis = []
    cumulative_tokens = []

    for i in range(input_ids.size(1)):
        # Get the current token (shape [1,1])
        current_token_id = input_ids[:, i:i+1]
        # Decode for display (current_token_id[0] is a tensor containing one token)
        current_token_str = tokenizer.decode(current_token_id[0])

        # Create a tensor of shape [1, sequence_length]
        if not cumulative_tokens:
            prediction_input_ids = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=False)
        else:
             prediction_input_ids = tokenizer.encode(prompt + tokenizer.decode(cumulative_tokens), return_tensors="pt", add_special_tokens=False)

        candidates = get_next_word_candidates(prediction_input_ids)
        analysis.append({"token": current_token_str, "candidates": candidates})

        # Extend cumulative_tokens with the new token (convert tensor to list of ints)
        cumulative_tokens.extend(current_token_id.tolist()[0])

    return {"analysis": analysis}


if __name__ == "__main__":
    english_text = "Despite the torrential downpour and the mounting traffic congestion that threatened to derail their carefully planned schedule, the group of intrepid hikers, armed with waterproof gear and a determined spirit, pressed onward through the muddy trails, their sights set on reaching the summit before nightfall."
    chinese_text = "尽管倾盆大雨倾泻而下，交通拥堵日益严重，几乎要打乱他们精心安排的行程，但这群勇敢的徒步旅行者，装备着防水装备，怀着坚定的精神，仍然在泥泞的小路上奋勇前进，他们的目标是在天黑前到达山顶。"
    analysis_result = analyze_english_text(english_text, chinese_text)

    # Save to JSON file
    with open("analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(analysis_result, f, indent=4, ensure_ascii=False)

    print("Analysis saved to analysis_result.json")