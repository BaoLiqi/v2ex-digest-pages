from matplotlib.colors import to_hex
import matplotlib.pyplot as pyplot


def generate_javascript_color_palette(colormap_name='viridis', num_colors=100):
    """
    Generates a JavaScript-ready (array of hex colors) from a matplotlib colormap.
    """
    cmap = pyplot.get_cmap(colormap_name)
    colors = [cmap(i / (num_colors - 1)) for i in range(num_colors)]
    hex_colors = [to_hex(color) for color in colors]
    js_array_string = ",\n        ".join(f'"{color}"' for color in hex_colors)
    return f"""      const colorPalette = [
        {js_array_string},
      ]; """


if __name__ == "__main__":
    js_palette = generate_javascript_color_palette(num_colors=20)
    print(js_palette)
