from matplotlib.colors import to_hex
import matplotlib.pyplot as pyplot


def generate_typescript_color_palette(colormap_name='viridis', num_colors=100):
    """
    Generates a TypeScript-ready (array of hex colors) from a matplotlib colormap.
    """
    cmap = pyplot.get_cmap(colormap_name)
    colors = [cmap(i / (num_colors - 1)) for i in range(num_colors)]
    hex_colors = [to_hex(color) for color in colors]
    ts_array_string = ",\n  ".join(f'"{color}"' for color in hex_colors)
    return f"""export const colorPalette = [
  {ts_array_string},
];
"""


if __name__ == "__main__":
    ts_palette = generate_typescript_color_palette(num_colors=20)
    with open("src/components/colorPalette.ts", "w") as f:
        f.write(ts_palette)
    print("TypeScript color palette generated at src/components/colorPalette.ts")
