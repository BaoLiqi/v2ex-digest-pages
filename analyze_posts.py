import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import argparse
from typing import Dict, Any
import time
import logging
from pathlib import Path


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analyze_posts.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_model(model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
    """
    Set up the model and tokenizer.

    Args:
        model_name: The name of the model to use

    Returns:
        tuple: (tokenizer, model)
    """
    logger.info(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Clear CUDA cache before loading model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("Cleared CUDA cache before loading model")

    # Load model with better memory efficiency
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        low_cpu_mem_usage=True
    )
    model.eval()

    # Check if CUDA is available and move model to GPU if possible
    if torch.cuda.is_available():
        logger.info("CUDA is available. Moving model to GPU.")
        model = model.to("cuda")

    return tokenizer, model


def get_prompt(chinese_text: str, tokenizer):
    """
    Create a prompt for the model based on the Chinese text.

    Args:
        chinese_text: The Chinese text to translate
        tokenizer: The tokenizer to use

    Returns:
        str: The prompt text
    """
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


def get_next_word_candidates(input_ids, model, tokenizer, top_k=5, top_p=0.99):
    """
    Get the next word candidates based on the input ids.

    Args:
        input_ids: The input ids
        model: The model to use
        tokenizer: The tokenizer to use
        top_k: The number of top candidates to consider
        top_p: The cumulative probability threshold

    Returns:
        list: A list of candidate tokens with their probabilities
    """
    with torch.no_grad():
        # Ensure input_ids are LongTensor and on the same device as the model
        input_ids = input_ids.to(model.device).long()
        outputs = model(input_ids)

        # Get logits and immediately move to CPU to free GPU memory
        logits = outputs.logits
        next_token_logits = logits[0, -1, :].cpu()

        # Delete outputs to free memory
        del outputs
        del logits

        probs = torch.softmax(next_token_logits, dim=0)
        top_probs, top_indices = torch.topk(probs, top_k)
        cumulative_probs = torch.cumsum(top_probs, dim=0)

        # Find the index where cumulative probability exceeds top_p
        exceed_index = (cumulative_probs > top_p).nonzero()
        if len(exceed_index) > 0:
            # Include the index where it exceeds
            cutoff_index = exceed_index[0].item() + 1
        else:
            cutoff_index = top_k  # If no index exceeds, take all top_k

        top_p_indices = top_indices[:cutoff_index]
        top_p_probs = top_probs[:cutoff_index]

        suggestions = []
        for idx, prob in zip(top_p_indices, top_p_probs):
            token_str = tokenizer.decode([idx.item()])
            suggestions.append({"token": token_str.strip(),
                               "probability": round(prob.item(), 4)})

        # Clean up tensors
        del next_token_logits, probs, top_probs, top_indices, cumulative_probs

        return suggestions


def analyze_english_text(english_text: str, chinese_text: str, model, tokenizer):
    """
    Analyze the English text based on the Chinese text.

    Args:
        english_text: The English text to analyze
        chinese_text: The corresponding Chinese text
        model: The model to use
        tokenizer: The tokenizer to use

    Returns:
        list: The analysis results as a list of token analyses
    """
    prompt = get_prompt(chinese_text, tokenizer)
    input_ids = tokenizer.encode(
        english_text, return_tensors='pt', add_special_tokens=False)
    analysis = []
    cumulative_tokens = []

    for i in range(input_ids.size(1)):
        # Get the current token (shape [1,1])
        current_token_id = input_ids[:, i:i+1]
        # Decode for display (current_token_id[0] is a tensor containing one token)
        current_token_str = tokenizer.decode(current_token_id[0])

        # Create a tensor of shape [1, sequence_length]
        if not cumulative_tokens:
            prediction_input_ids = tokenizer.encode(
                prompt, return_tensors="pt", add_special_tokens=False)
        else:
            prediction_input_ids = tokenizer.encode(
                prompt + tokenizer.decode(cumulative_tokens), return_tensors="pt", add_special_tokens=False)

        candidates = get_next_word_candidates(
            prediction_input_ids, model, tokenizer)
        analysis.append({"token": current_token_str, "candidates": candidates})

        # Extend cumulative_tokens with the new token (convert tensor to list of ints)
        cumulative_tokens.extend(current_token_id.tolist()[0])

    return analysis


def process_chunk(chunk: Dict[str, str], model, tokenizer) -> Dict[str, Any]:
    """
    Process a single chunk by adding analysis to it.

    Args:
        chunk: The chunk to process
        model: The model to use
        tokenizer: The tokenizer to use

    Returns:
        dict: The processed chunk with analysis added
    """
    english_text = chunk["en"]
    chinese_text = chunk["zh"]

    # Create a new chunk with the original data
    new_chunk = {
        "en": english_text,
        "zh": chinese_text
    }

    # Add analysis to the chunk
    try:
        analysis = analyze_english_text(
            english_text, chinese_text, model, tokenizer)
        new_chunk["analysis"] = analysis
    except Exception as e:
        logger.error(f"Error analyzing chunk: {e}")
        new_chunk["analysis"] = {"error": str(e)}

    return new_chunk


def process_file(input_file: str, output_dir: str, model, tokenizer, force: bool = False) -> None:
    """
    Process a single JSON file.

    Args:
        input_file: The path to the input file
        output_dir: The directory to write the output file to
        model: The model to use
        tokenizer: The tokenizer to use
        force: Whether to overwrite existing output files
    """
    # Create output filename
    input_path = Path(input_file)
    output_filename = input_path.name.replace(".json", "_analyzed.json")
    output_path = Path(output_dir) / output_filename

    # Check if output file already exists
    if output_path.exists() and not force:
        logger.info(f"Output file {output_path} already exists. Skipping.")
        return

    # Load the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Error loading file {input_file}: {e}")
        return

    logger.info(f"Processing file: {input_file}")

    # Process each block in the file
    for block_idx, block in enumerate(data["blocks"]):
        logger.info(f"Processing block {block_idx+1}/{len(data['blocks'])}")

        # Process each chunk in the block
        new_chunks = []
        for chunk_idx, chunk in enumerate(tqdm(block["chunks"], desc=f"Block {block_idx+1}")):
            new_chunk = process_chunk(chunk, model, tokenizer)
            new_chunks.append(new_chunk)

        # Replace the chunks in the block
        block["chunks"] = new_chunks

    # Write the output file
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Wrote output file: {output_path}")
    except Exception as e:
        logger.error(f"Error writing file {output_path}: {e}")


def main():
    """
    Main function to process all JSON files.
    """
    parser = argparse.ArgumentParser(
        description="Analyze posts and add analysis to chunks.")
    parser.add_argument("--input_dir", type=str, default="docs/posts_json",
                        help="Directory containing input JSON files")
    parser.add_argument("--output_dir", type=str, default="docs/posts_json_analyzed",
                        help="Directory to write output JSON files")
    parser.add_argument("--model_name", type=str,
                        default="Qwen/Qwen2.5-1.5B-Instruct", help="Model name to use")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing output files")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit the number of files to process")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Set up model and tokenizer
    tokenizer, model = setup_model(args.model_name)

    # Get list of input files
    input_files = [os.path.join(args.input_dir, f) for f in os.listdir(
        args.input_dir) if f.endswith(".json")]

    # Limit the number of files if specified
    if args.limit is not None:
        input_files = input_files[:args.limit]

    logger.info(f"Found {len(input_files)} input files")

    # Process each file
    for file_idx, input_file in enumerate(input_files):
        logger.info(
            f"Processing file {file_idx+1}/{len(input_files)}: {input_file}")
        start_time = time.time()
        process_file(input_file, args.output_dir, model, tokenizer, args.force)
        elapsed_time = time.time() - start_time
        logger.info(f"Processed file in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
