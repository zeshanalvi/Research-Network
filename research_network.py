import requests
from bs4 import BeautifulSoup
import networkx as nx
import plotly.graph_objects as go
from collections import defaultdict

class Scholarnet:
    def __init__(self,dblp_url="https://dblp.org/pid/232/1606.html"):
        self.dblp_url=dblp_url
        self.graph=nx.Graph()
    def author_short(self,full_name):
        first_letters = ""
        for word in full_name.split():
            if word:
                first_letters+=word[0]
        return first_letters

    def extract_graph(self):
        response = requests.get(self.dblp_url)
        soup = BeautifulSoup(response.text, "html.parser")
        papers = soup.find_all("li", class_="entry")
        edge_weights = defaultdict(int)
        author_papers = defaultdict(int)
        main_author = soup.find("title").text.split("::")[0].strip()

        for paper in papers:
            authors = [a.text for a in paper.find_all("span", itemprop="author")]
            for author in authors:
                author_papers[author] += 1
            # Count co-author pair frequencies
            for i in range(len(authors)):
                for j in range(i+1, len(authors)):
                    pair = tuple(sorted([authors[i], authors[j]]))
                    edge_weights[pair] += 1
        for author, count in author_papers.items():
            if(author in main_author):
                self.graph.add_node(author,label=self.author_short(author),title=f"{author}\nTotal Papers: {count}", size=10+count*2, color="red")
            else:
                self.graph.add_node(author,label=self.author_short(author),title=f"{author}\nPapers with me: {count}", size=10+count*2, color="#1f78b4")
        for (a, b), w in edge_weights.items():
            self.graph.add_edge(a, b, weight=w*3, color="#B1C3EB2C")
        
    def show(self,height="600px",width="100%",bg_color="#ECE9E9",font_color="#636060"):
        # Create Pyvis network
        net = Network(notebook=True, height=height, width=width, bgcolor=bg_color, font_color=font_color)
        net.from_nx(self.graph)
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
        # Save and show
        net.show("research_network.html")

# pip install pyvis
import networkx as nx
from pyvis.network import Network
#net=Scholarnet(dblp_url="https://dblp.org/pid/290/7993.html")
#net=Scholarnet()
#net.extract_graph()
#net.show()

url="https://scholar.google.com/citations?user=vpcMBkEAAAAJ&hl=en"
response = requests.get(url)
print(response.text)
soup = BeautifulSoup(response.text, "html.parser")
papers = soup.find_all("a", class_="gsc_a_t")
print(papers)
