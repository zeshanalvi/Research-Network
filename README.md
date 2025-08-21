# Scholar Graph

**Scholar Graph** is a lightweight CLI tool that fetches co-author data from **DBLP** and visualizes it as an **interactive graph**.  
The tool allows you to explore academic collaboration networks directly from the terminal, with results displayed in an HTML graph that can be zoomed, dragged, and explored interactively.

---

## 🚀 Features

- Fetches co-author data from [DBLP](https://dblp.org/).
- Visualizes authors and co-authors as a **draggable, interactive graph**.
- Supports **depth control** for graph exploration.
- CLI-based usage with simple commands.
- Outputs graphs as HTML (open in browser for interactive visualization).
- Edge widths and node sizes scale based on number of joint publications.

---

## 📦 Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/zeshanalvi/Research_Network.git
cd Research_Network
pip install -r requirements.txt
```

## Requirements

Python >= 3.8

## Dependencies:
`requests`
`beautifulsoup4`
`pyvis`
Install them with:
```bash
pip install requests beautifulsoup4 pyvis
```
## Usage

Run the CLI command:
```bash
python scholar_graph.py build "Author Name" --depth 2
```
### Example:

```bash 
python scholar_graph.py build "Zeshan Khan" --depth 2
```

This will:
Fetch Zeshan Khan’s DBLP profile.
Parse co-authors and co-authors-of-co-authors (depth = 2).
Generate an interactive HTML graph.
Save it as scholar_graph.html in the current directory.

Open the file in a browser:
```bash
This will:

Fetch Zeshan Khan’s DBLP profile.
Parse co-authors and co-authors-of-co-authors (depth = 2).
Generate an interactive HTML graph.
Save it as scholar_graph.html in the current directory.
Open the file in a browser:

```bash
open scholar_graph.html   # macOS
xdg-open scholar_graph.html  # Linux
start scholar_graph.html  # Windows
```
## Graph Features
Nodes → Authors.
Edges → Co-authorships.
Node size → Number of collaborations.
Edge width → Number of joint papers.
Hover tooltip → Shows author name and publication count.
Interactive → Drag, zoom, and explore relationships.

## CLI Options

The tool provides a simple command-line interface (CLI) to build and visualize co-author graphs from DBLP.

| Option          | Type    | Description                                                                 | Example                           |
|-----------------|---------|-----------------------------------------------------------------------------|-----------------------------------|
| `build`         | Command | Builds the co-author graph for the given author name.                       | `python scholar_graph.py build "Zeshan Khan"` |
| `--depth`       | int     | Depth of co-author expansion (default: `1`). Higher values show more layers.| `--depth 2`                       |
| `--output`      | string  | Output HTML file name for visualization (default: `graph.html`).            | `--output zeshan_graph.html`      |
| `--max-authors` | int     | Maximum number of co-authors to expand per author (default: unlimited).     | `--max-authors 20`                |
| `--open`        | flag    | Automatically open the output HTML graph in the browser after generation.   | `--open`                          |

### Example Usage

```bash
# Build a co-author graph of depth 2 for Zeshan Khan
python scholar_graph.py build "Zeshan Khan" --depth 2 --output my_graph.html --open


## Project Structure

```bash
scholar-graph/
│
├── scholar_graph.py      # Main CLI tool
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
```

## Contributing

Contributions are welcome!
If you'd like to improve parsing, add new data sources (like Google Scholar), or extend visualization features:
Fork the repo.
Create a new branch (feature-x).
Submit a pull request.

#License

MIT License. Feel free to use, modify, and share.
```pgsql
Would you like me to also generate a **sample `requirements.txt`** and a **short usage example (with screenshots / code snippets)** so you can directly drop them into your repo?
```
