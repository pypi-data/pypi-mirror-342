from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
import re
from docvs.util import ensure_valid_name
grammar = Grammar(r"""
    content  = (link / text)*
    link     = "[[" path "]]"
    path     = ~r"[^\[]*" # Due to greedyness we need to validate the path in the visitor              
    linktext = ~r"[^\]]*"
    text     = ~r"[^\[]+"
""")
# ("|" linktext)? "]]" path      =  (&relativepath value) / (&fullpath value) / invalidpath
class WikiLinkVisitor(NodeVisitor):
    def __init__(self,current_category):
        self.current_category=current_category
    def visit_content(self, node, visited_children):
        """Concatenate the first element from each visited child node into a single string."""
        return ''.join(child[0] for child in visited_children)

    def visit_link(self, node, visited_children):
        # visited_children structure:
        # If custom link text: ["[[", key, [ "|" , linktext ], "]]"]
        # Otherwise: ["[[", key, "]]"]
        key = visited_children[1]
        
        #if key.startswith(":invalid"):
        #    return f"[Invalid Link:{key}]"

        if len(visited_children) == 4:
            if len(visited_children[2])>0:
                if len(visited_children[2][0][1])>0:
                    linktext = visited_children[2][0][1]
                else:
                    linktext = key
            else:
                linktext = key
        else:
            # No custom link text provided, so use the key
            linktext = key
            
        return f'<a onclick="" path="{key}">{linktext}</a>'

    #def visit_path(self, node, visited_children):
    #    return node.text
    def visit_path(self, node, visited_children):
        path = node.text.strip()
        if len(path)==0: return "Invalid Link"
        if not path.startswith("/"): # Relative path
            path = ensure_valid_name(path)
            if len(path)>128:return "Invalid Link"
            path = f"{self.current_category}/{path}"

        return path
    def visit_linktext(self, node, visited_children):
        return node.text.strip("|")  # Remove the leading "|" before processing

    def visit_text(self, node, visited_children):
        return node.text
    



    def generic_visit(self, node, visited_children):
        return visited_children or node.text



def parse(text,category):
    
    tree = grammar.parse(text)
    visitor = WikiLinkVisitor(category)
    return visitor.visit(tree)


# Example Usage:
#html = "First [[xysoe.s#]] Second [[/asdad/hallo|My Link Text]] Third [[asdasd]]"
html = "First [[xysoe.s]] Second [[/asdad/hallo]] Third [[asdasd]]"
parsed_html = parse(html,"/metavision/")
print(parsed_html)