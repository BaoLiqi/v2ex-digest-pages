import json
from colorization.export_viridis import generate_javascript_color_palette


def generate_html_from_json(json_file, html_file):
    """
    Generates an HTML file with colored words based on probabilities from a JSON file.
    Adds click-to-show candidate functionality.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Token Probability Visualization</title>
  <style>
    #text-container {
      display: flex;
      flex-wrap: wrap;
    }
    .word {
      white-space: pre-wrap;
      cursor: pointer; /* Indicate clickable elements */
      position: relative; /* Needed for absolute positioning of tooltip */
    }
    .tooltip {
      display: none; /* Hidden by default */
      position: absolute;
      top: 100%;  /* Position below the word */
      left: 50%;
      transform: translateX(-50%); /* Center horizontally */
      background-color: rgba(0, 0, 0, 0.8); /* Semi-transparent black */
      color: white;
      padding: 5px;
      border-radius: 5px;
      white-space: nowrap; /* Prevent text wrapping in the tooltip */
      z-index: 10; /* Ensure tooltip is on top */
    }
    .word.active .tooltip {
      display: block;  /* Show tooltip when word has 'active' class*/
    }


  </style>
</head>
<body>
  <div id="text-container">"""

    for item in data['analysis']:
        token = item['token']
        candidates = item.get('candidates', [])

        probability = 0.0
        for candidate in candidates:
            if candidate['token'].strip() == token.strip():
                probability = candidate['probability']
                break

        # Create the tooltip content
        tooltip_content = ""
        if candidates:  # only create tooltip if there's content
            tooltip_content = "<div class='tooltip'>"
            for candidate in candidates:
                tooltip_content += f"<div>{candidate['token']}: {candidate['probability']:.4f}</div>"
            tooltip_content += "</div>"

        html_content += f'<span class="word" data-probability="{probability:.4f}">{token}{tooltip_content}</span>'

    html_content += """</div>
  <script>
      """ + generate_javascript_color_palette(num_colors=100) + """

      function probabilityToColor(probability) {
        const index = Math.floor(probability * (colorPalette.length - 1));
        return colorPalette[index];
      }

    const words = document.querySelectorAll(".word");
    words.forEach((word) => {
      const probability = parseFloat(word.dataset.probability);
      word.style.color = probabilityToColor(probability);

      word.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent clicks from bubbling up to the document

        // Toggle the 'active' class on the clicked word
        this.classList.toggle('active');

        // Hide tooltips of all other words
        words.forEach(otherWord => {
            if (otherWord !== this) {
                otherWord.classList.remove('active');
            }
        });
      });
    });

    // Clicking anywhere on the document closes all tooltips
    document.addEventListener('click', function() {
      words.forEach(word => {
        word.classList.remove('active');
      });
    });

  </script>
</body>
</html>
"""

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    json_file = 'colorization/analysis_result.json'
    html_file = 'colorization/analysis_result.html'
    generate_html_from_json(json_file, html_file)
    print(f"HTML file generated at: {html_file}")
