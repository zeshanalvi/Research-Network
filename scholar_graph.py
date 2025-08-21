#!/usr/bin/env python3
# scholar_graph.py

import argparse
import sys
import re
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
import networkx as nx
from collections import defaultdict
from pyvis.network import Network
import matplotlib.colors as mcolors

class Scholarnet:
    def __init__(self, dblp_url: str):
        self.dblp_url = dblp_url
        self.graph = nx.Graph()
        self.main_author = None

    @staticmethod
    def author_short(full_name: str) -> str:
        return "".join(w[0] for w in full_name.split() if w)

    def extract_graph(self):
        """Build a co-author graph from a single DBLP author HTML page."""
        resp = requests.get(self.dblp_url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        papers = soup.find_all("li", class_="entry")
        edge_weights = defaultdict(int)
        author_papers = defaultdict(int)

        title_tag = soup.find("title")
        self.main_author = title_tag.text.split("::")[0].strip() if title_tag else "Author"

        # Count appearances and coauthor pair frequencies
        for paper in papers:
            authors = [a.text.strip() for a in paper.find_all("span", itemprop="author")]
            if not authors:
                continue
            for author in authors:
                author_papers[author] += 1
            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    pair = tuple(sorted((authors[i], authors[j])))
                    edge_weights[pair] += 1

        # Add nodes
        for author, count in author_papers.items():
            is_main = (author == self.main_author)
            color = "red" if is_main else "#1f78b4"
            title = (
                f"{author}\nTotal Papers: {count}"
                if is_main
                else f"{author}\nCo-authored with {self.main_author}: {count}"
            )
            self.graph.add_node(
                author,
                label=self.author_short(author),  # compact label on node
                title=title,                      # full text on hover
                size=10 + count * 2,
                color=color,
            )

        # Add edges (weighted)
        for (a, b), w in edge_weights.items():
            base_color = mcolors.to_rgb("#8BA4DA")
            norm = min(w / 10, 1.0)
            darkened = tuple([c * (1 - 0.7 * norm) for c in base_color])
            self.graph.add_edge(a, b, weight=w, color=mcolors.to_hex(darkened))

    def show(self, output="research_network.html",
             height="700px", width="100%", bg_color="#ECE9E9", font_color="#636060"):
        """Save interactive PyVis HTML."""
        net = Network(notebook=False, height=height, width=width, bgcolor=bg_color, font_color=font_color)
        net.from_nx(self.graph)

        # Physics tuned for collaboration graphs
        net.set_options("""
        var options = {
        "physics": {
            "enabled": true,
            "stabilization": {
            "enabled": true,
            "iterations": 500
            },
            "barnesHut": {      
            "springLength": 200,
            "springConstant": 0.02,
            "damping": 0.3
            }
        }
        }
        """)

        net.save_graph(output)
        return output


def find_dblp_profile_by_name(name: str) -> str | None:
    """Find first DBLP author profile URL by name via the author search HTML."""
    search_url = f"https://dblp.org/search/author?q={quote_plus(name)}"
    r = requests.get(search_url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Prefer the standard "entry author" list item
    li = soup.find("li", class_="entry author")
    if li:
        a = li.find("a", href=True)
        if a and "/pid/" in a["href"]:
            return a["href"]

    # Fallback: any link containing /pid/
    a_any = soup.find("a", href=re.compile(r"/pid/"))
    if a_any:
        return a_any["href"]

    return None


def cli():
    parser = argparse.ArgumentParser(description="Build an interactive co-author graph from a DBLP author page.")
    sub = parser.add_subparsers(dest="command", required=True)

    b = sub.add_parser("build", help="Build co-author graph from a DBLP author name or profile URL")
    b.add_argument("query", help='Author name (e.g., "Zeshan Khan") OR DBLP URL (e.g., https://dblp.org/pid/232/1606.html)')
    b.add_argument("--depth", type=int, default=1, help="Graph depth (current implementation uses depth=1 from a single page)")
    b.add_argument("--out", default="research_network.html", help="Output HTML file (default: research_network.html)")
    b.add_argument("--height", default="700px", help="Graph height (default: 700px)")
    b.add_argument("--width", default="100%", help="Graph width (default: 100%)")

    args = parser.parse_args()

    if args.command == "build":
        # Resolve query to a DBLP URL
        if args.query.startswith("http"):
            dblp_url = args.query
        else:
            dblp_url = find_dblp_profile_by_name(args.query)
            if not dblp_url:
                print(f'Could not find a DBLP profile for "{args.query}".', file=sys.stderr)
                sys.exit(1)

        if args.depth > 1:
            print("Note: current implementation builds from a single DBLP page (depth=1). Ignoring --depth>1.", file=sys.stderr)

        net = Scholarnet(dblp_url=dblp_url)
        net.extract_graph()
        out = net.show(output=args.out, height=args.height, width=args.width)
        print(f"Saved interactive graph to: {out}")


if __name__ == "__main__":
    cli()
