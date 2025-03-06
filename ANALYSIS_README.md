# V2EX Post Analysis

This project provides tools to analyze V2EX post data by applying LLM-based analysis to each chunk of text within the JSON files. It adds the analysis results to each chunk and writes the modified data to new JSON files.

## Files

- `analyze_posts.py`: The main script that processes the JSON files.
- `analyze_posts_colab.ipynb`: A Google Colab notebook that runs the script in the cloud.

## Local Usage

If you have sufficient computational resources, you can run the script locally:

```bash
# Install dependencies
pip install torch transformers tqdm

# Run the script
python analyze_posts.py
```

### Command-line Arguments

The script accepts the following command-line arguments:

- `--input_dir`: Directory containing input JSON files (default: "docs/posts_json")
- `--output_dir`: Directory to write output JSON files (default: "docs/posts_json_analyzed")
- `--model_name`: Model name to use (default: "Qwen/Qwen2.5-1.5B-Instruct")
- `--force`: Overwrite existing output files
- `--limit`: Limit the number of files to process

Example:

```bash
# Process only 5 files
python analyze_posts.py --limit 5

# Use a different model
python analyze_posts.py --model_name "different/model"

# Process files from a different directory
python analyze_posts.py --input_dir "path/to/input" --output_dir "path/to/output"
```

## Google Colab Usage

If your local machine lacks the necessary resources, you can run the analysis on Google Colab:

1. Upload the `analyze_posts_colab.ipynb` notebook to Google Colab.
2. Run the cells in order.
3. The notebook will:
   - Install the required dependencies
   - Clone your repository to get the script and JSON files
   - Run the analysis script
   - Allow you to examine the results
   - Download the results to your local machine

### Customizing the Colab Notebook

You may need to modify the notebook to match your repository:

1. Update the repository URL in the "Download Files" cell:

   ```python
   !git clone https://github.com/yourusername/v2ex-digest-pages.git
   ```

2. Adjust the limit parameter in the "Run Analysis" cell based on your available resources:
   ```python
   !python analyze_posts.py --limit 5
   ```

## How It Works

The script performs the following steps:

1. Loads each JSON file from the input directory.
2. For each file, it processes each block and chunk.
3. For each chunk, it applies LLM-based analysis to the English and Chinese text.
4. It adds the analysis results to each chunk.
5. It writes the modified data to a new JSON file in the output directory.

The analysis uses the Qwen2.5-1.5B-Instruct model to analyze the English text based on the Chinese text. For each token in the English text, it predicts the top candidates that could have been generated at that position, along with their probabilities.

## Output Format

The output JSON files have the same structure as the input files, but with an additional `analysis` field in each chunk:

```json
{
  "id": 1013250,
  "blocks": [
    {
      "chunks": [
        {
          "zh": "简历里要不要写自己的折腾经历",
          "en": "Should you write your own tinkering experiences in your resume",
          "analysis": {
            "analysis": [
              {
                "token": "Should",
                "candidates": [
                  {"token": "Should", "probability": 0.1234},
                  {"token": "Do", "probability": 0.0567},
                  ...
                ]
              },
              ...
            ]
          }
        },
        ...
      ],
      "type": "title"
    },
    ...
  ]
}
```

## Requirements

- Python 3.6+
- PyTorch
- Transformers
- tqdm

## Troubleshooting

- **Out of memory errors**: Reduce the number of files processed at once using the `--limit` parameter.
- **Slow processing**: The analysis is computationally intensive. Consider using a GPU if available.
- **Model loading errors**: Ensure you have a stable internet connection when loading the model for the first time.
