I have structured post data, as you can see in the typed_post.py file and the JSON files located in the public/posts_json/ directory. Additionally, I have an LLM-based analysis script (analyze_text_example.py) that can generate data from a single chunk of text containing both English and Chinese.

I want to create a script that iterates through all of the JSON files, then iterates through each chunk within those files, and inserts the analysis results into each chunk. Finally, it should write the modified data to a new JSON file (one for each original post JSON file). Since my local machine lacks the resources, I plan to run this script on Google Colab.

---

I need to create another board for my mock forum project. It uses almost the same logic as we use for handling posts in public/posts_json, but this time we're working with public/posts_json_analyzed/. We can add a colorful analysis for each chunk; the data is already present in the JSON.

The JSON files are structured like this:

```
{
  "id": 1014826,
  "blocks": [
    {
      "chunks": [
        {
          "en": "From an 18th-tier city to a new first-tier city, the salary was finally suppressed during negotiations",
          "zh": "从十八线到新一线，最后谈薪被压了",
          "analysis": [
            {
              "token": "From",
              "candidates": [
                {
                  "token": "From",
                  "probability": 0.9311
                },
                {
                  "token": "Moving",
                  "probability": 0.031
                },
// not complete json
```

The logic is similar to what we implement within the folder color/

We need to use Python to generate a TypeScript color array, which will then be used on our website. Please write the rendering logic within a React component.