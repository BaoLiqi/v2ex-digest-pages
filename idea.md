I have structured post data, as you can see in the typed_post.py file and the JSON files located in the public/posts_json/ directory. Additionally, I have an LLM-based analysis script (analyze_text_example.py) that can generate data from a single chunk of text containing both English and Chinese.

I want to create a script that iterates through all of the JSON files, then iterates through each chunk within those files, and inserts the analysis results into each chunk. Finally, it should write the modified data to a new JSON file (one for each original post JSON file). Since my local machine lacks the resources, I plan to run this script on Google Colab.

---

I need another board for my fake forum project. it is almost the same logic as we handle posts in public/posts_json, but now we are handling public/posts_json_analyzed/
We can add a colorful analysis for every chunk. the data is already in the json.

the json files are like:

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

and the logic is like what we do in color/

we need to generate a ts color array using python, and use it in our site.
write the render logic in react component.
