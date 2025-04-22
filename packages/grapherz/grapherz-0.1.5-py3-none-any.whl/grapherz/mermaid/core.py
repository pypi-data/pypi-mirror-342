 
import re
import networkx as nx
from typing import Dict, List, Tuple, Optional, Union

class MermaidNetworkX:
    """
    SDK for converting between Mermaid graph TD format and NetworkX.
    
    This class provides two main functionalities:
    1. Convert Mermaid graph TD syntax to NetworkX DiGraph
    2. Convert NetworkX DiGraph to Mermaid graph TD syntax
    """
    
    @staticmethod
    def mermaid_to_networkx(mermaid_code: str) -> nx.DiGraph:
        """
        Convert Mermaid graph TD syntax to NetworkX DiGraph
        
        Args:
            mermaid_code (str): Mermaid code in graph TD format
            
        Returns:
            nx.DiGraph: A NetworkX directed graph representing the Mermaid diagram
        """
        G = nx.DiGraph()
        
        # Remove the header (graph TD) and extract only the connections
        lines = mermaid_code.strip().split('\n')
        content_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip header line and empty lines
            if line.startswith('graph TD') or line.startswith('graph TB') or not line:
                continue
            # Skip comment lines
            if line.startswith('%%'):
                continue
            content_lines.append(line)
            
        # Process each connection line
        for line in content_lines:
            # Handle connections with labels
            label_match = re.search(r'(\w+)\s*--\s*(.+?)\s*-->\s*(\w+)', line)
            if label_match:
                source, label, target = label_match.groups()
                G.add_edge(source, target, label=label)
                continue
                
            # Handle simple connections
            simple_match = re.search(r'(\w+)\s*-->\s*(\w+)', line)
            if simple_match:
                source, target = simple_match.groups()
                G.add_edge(source, target)
                continue
                
            # Handle node definitions
            node_match = re.search(r'(\w+)\[(.+?)\]', line)
            if node_match:
                node_id, node_label = node_match.groups()
                # Add node with label as attribute
                G.add_node(node_id, label=node_label)
                
        return G
    
    @staticmethod
    def networkx_to_mermaid(G: nx.DiGraph) -> str:
        """
        Convert NetworkX DiGraph to Mermaid graph TD syntax
        
        Args:
            G (nx.DiGraph): NetworkX directed graph
            
        Returns:
            str: Mermaid code in graph TD format
        """
        mermaid_code = ["graph TD"]
        
        # Add node definitions
        for node, attrs in G.nodes(data=True):
            if 'label' in attrs:
                mermaid_code.append(f"    {node}[{attrs['label']}]")
            else:
                mermaid_code.append(f"    {node}[{node}]")
        
        # Add edges
        for source, target, attrs in G.edges(data=True):
            if 'label' in attrs:
                mermaid_code.append(f"    {source} -- {attrs['label']} --> {target}")
            else:
                mermaid_code.append(f"    {source} --> {target}")
        
        return '\n'.join(mermaid_code)
    
    @staticmethod
    def visualize_networkx(G: nx.DiGraph) -> None:
        """
        Visualize NetworkX graph using matplotlib
        
        Args:
            G (nx.DiGraph): NetworkX directed graph
        """
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_size=700)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, arrowsize=20)
            
            # Draw labels
            node_labels = {node: attrs.get('label', node) for node, attrs in G.nodes(data=True)}
            nx.draw_networkx_labels(G, pos, labels=node_labels)
            
            # Draw edge labels if they exist
            edge_labels = {(source, target): attrs.get('label', '') 
                          for source, target, attrs in G.edges(data=True) 
                          if 'label' in attrs}
            if edge_labels:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            
            plt.axis('off')
            plt.title("NetworkX Graph Visualization")
            plt.show()
        except ImportError:
            print("Matplotlib is required for visualization. Please install it using 'pip install matplotlib'")

