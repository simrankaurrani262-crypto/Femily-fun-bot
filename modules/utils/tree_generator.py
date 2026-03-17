"""
Family Tree Image Generator using NetworkX and Matplotlib
Generates PNG images showing complete family structures
"""
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image, ImageDraw, ImageFont
import io
from database import db
import logging

logger = logging.getLogger(__name__)

# Node type definitions and colors
NODE_TYPES = {
    'USER': {'color': '#4e7ed3', 'emoji': '🧑', 'label': 'You'},
    'PARTNER': {'color': '#ef5a87', 'emoji': '❤️', 'label': 'Partner'},
    'PARENT': {'color': '#91d28b', 'emoji': '👪', 'label': 'Parent'},
    'CHILD': {'color': '#ffd966', 'emoji': '👶', 'label': 'Child'},
    'GRANDPARENT': {'color': '#b0a16e', 'emoji': '🧓', 'label': 'Grandparent'},
    'GRANDCHILD': {'color': '#e899d6', 'emoji': '👦', 'label': 'Grandchild'},
    'SIBLING': {'color': '#f4a460', 'emoji': '🤝', 'label': 'Sibling'},
}

class FamilyTreeGenerator:
    """Generate family tree images"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = db.get_user(user_id)
        self.family = db.get_family(user_id)
        self.graph = nx.DiGraph()
        self.positions = {}
        self.node_colors = {}
        self.labels = {}
    
    def build_graph(self):
        """Build NetworkX graph from family data"""
        if not self.user or not self.family:
            logger.warning(f"User {self.user_id} or family data not found")
            return False
        
        # Add USER node
        self._add_node(f'user_{self.user_id}', 'USER', self.user.get('username', 'User'))
        
        # Add PARTNER
        if self.family.get('partner'):
            partner_id = self.family['partner']
            partner = db.get_user(partner_id)
            self._add_node(f'user_{partner_id}', 'PARTNER', partner.get('username', 'Partner') if partner else 'Partner')
            self.graph.add_edge(f'user_{self.user_id}', f'user_{partner_id}')
        
        # Add PARENTS
        for parent_id in self.family.get('parents', []):
            parent = db.get_user(parent_id)
            self._add_node(f'user_{parent_id}', 'PARENT', parent.get('username', f'Parent{parent_id}') if parent else f'Parent')
            self.graph.add_edge(f'user_{parent_id}', f'user_{self.user_id}')
        
        # Add CHILDREN
        for child_id in self.family.get('children', []):
            child = db.get_user(child_id)
            self._add_node(f'user_{child_id}', 'CHILD', child.get('username', f'Child{child_id}') if child else 'Child')
            self.graph.add_edge(f'user_{self.user_id}', f'user_{child_id}')
        
        # Add GRANDPARENTS
        for gparent_id in self.family.get('grandparents', []):
            gparent = db.get_user(gparent_id)
            self._add_node(f'user_{gparent_id}', 'GRANDPARENT', gparent.get('username', 'Grandparent') if gparent else 'Grandparent')
            # Connect to parents
            for parent_id in self.family.get('parents', []):
                self.graph.add_edge(f'user_{gparent_id}', f'user_{parent_id}')
        
        # Add GRANDCHILDREN
        for gchild_id in self.family.get('grandchildren', []):
            gchild = db.get_user(gchild_id)
            self._add_node(f'user_{gchild_id}', 'GRANDCHILD', gchild.get('username', 'Grandchild') if gchild else 'Grandchild')
            # Connect from children
            for child_id in self.family.get('children', []):
                self.graph.add_edge(f'user_{child_id}', f'user_{gchild_id}')
        
        # Add SIBLINGS
        for sibling_id in self.family.get('siblings', []):
            sibling = db.get_user(sibling_id)
            self._add_node(f'user_{sibling_id}', 'SIBLING', sibling.get('username', 'Sibling') if sibling else 'Sibling')
        
        return True
    
    def _add_node(self, node_id, node_type, label):
        """Add node to graph"""
        self.graph.add_node(node_id, type=node_type)
        self.labels[node_id] = label
        self.node_colors[node_id] = NODE_TYPES[node_type]['color']
    
    def compute_layout(self):
        """Compute hierarchical layout"""
        if not self.graph.nodes():
            return False
        
        self.positions = self._hierarchy_pos(
            self.graph, 
            f'user_{self.user_id}',
            width=2.0,
            vert_gap=1.5
        )
        return True
    
    def _hierarchy_pos(self, G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
        """
        Create hierarchical tree layout
        """
        def _recursive_layout(G, root_node, width, vert_gap, vert_loc, xcenter, pos, parent_node=None):
            neighbors = list(G.successors(root_node))
            if not neighbors:
                pos[root_node] = (xcenter, vert_loc)
            else:
                dx = width / len(neighbors) if neighbors else 0
                nextx = xcenter - width/2 - dx/2
                for neighbor in neighbors:
                    nextx += dx
                    pos = _recursive_layout(
                        G, neighbor, dx, vert_gap,
                        vert_loc - vert_gap, nextx, pos,
                        root_node
                    )
                pos[root_node] = (xcenter, vert_loc)
            return pos
        
        return _recursive_layout(G, root, width, vert_gap, vert_loc, xcenter, {})
    
    def generate_image(self):
        """Generate matplotlib figure and return as PIL Image"""
        if not self.build_graph():
            logger.error("Failed to build graph")
            return None
        
        if not self.compute_layout():
            logger.error("Failed to compute layout")
            return None
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
        
        # Draw nodes
        colors = [self.node_colors.get(node, '#cccccc') for node in self.graph.nodes()]
        nx.draw_networkx_nodes(
            self.graph, self.positions,
            node_color=colors,
            node_size=2000,
            ax=ax
        )
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph, self.positions,
            edge_color='gray',
            arrows=True,
            arrowsize=20,
            width=2,
            ax=ax
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            self.graph, self.positions,
            labels=self.labels,
            font_size=9,
            font_weight='bold',
            ax=ax
        )
        
        # Add legend
        legend_elements = [
            mpatches.Patch(
                color=NODE_TYPES[node_type]['color'],
                label=NODE_TYPES[node_type]['label']
            )
            for node_type in NODE_TYPES
        ]
        ax.legend(handles=legend_elements, loc='upper left')
        
        ax.set_title(f"Family Tree: {self.user.get('username', 'User')}", fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        buf.seek(0)
        
        img = Image.open(buf)
        return img

def generate_family_tree(user_id):
    """
    Main function to generate family tree image
    Returns PIL Image or None if failed
    """
    try:
        generator = FamilyTreeGenerator(user_id)
        img = generator.generate_image()
        if img:
            logger.info(f"✅ Family tree generated for user {user_id}")
        return img
    except Exception as e:
        logger.error(f"❌ Error generating family tree: {e}")
        return None

def save_tree_to_file(user_id, filepath):
    """Save tree image to file"""
    img = generate_family_tree(user_id)
    if img:
        img.save(filepath)
        return True
    return False

def get_family_stats(user_id):
    """Get family statistics"""
    family = db.get_family(user_id)
    if not family:
        return None
    
    return {
        'partner': family.get('partner'),
        'children_count': len(family.get('children', [])),
        'parents_count': len(family.get('parents', [])),
        'siblings_count': len(family.get('siblings', [])),
        'grandparents_count': len(family.get('grandparents', [])),
        'grandchildren_count': len(family.get('grandchildren', [])),
        'total_family_members': len(family.get('children', [])) + len(family.get('parents', [])) + 
                                len(family.get('grandparents', [])) + len(family.get('grandchildren', [])) + 
                                len(family.get('siblings', [])) + (1 if family.get('partner') else 0) + 1
    }