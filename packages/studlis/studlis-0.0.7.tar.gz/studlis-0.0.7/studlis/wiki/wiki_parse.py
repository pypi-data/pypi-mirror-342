from docvs.util import ensure_valid_name
import re
import markdown



def extract_markdown_titles_and_quotes(markdown_text):
    # Extract all headings (titles)
    headings = re.findall(r'^(#{1,6})\s*(.*)', markdown_text, re.MULTILINE)
    
    # Extract quoted text (lines starting with >)
    quotes = re.findall(r'^\s*>+\s*(.*)', markdown_text, re.MULTILINE)
    
    # Format results
    headings = [f"{h[1]}" for h in headings]
    quotes = [q.strip() for q in quotes]

    return headings, quotes



def parse_old(text,category):
    def replace_link(match):
        parts = match.group(1).split('|')
        link = parts[0]
        link_text = parts[1] if len(parts) > 1 else link
        
        if len(link)==0: return "Invalid Link"
        if not link.startswith("/"): # Relative path
            path = ensure_valid_name(link)
            if len(path)>128:return "Invalid Link"
            path = f"{category}/{path}"
        else:
            path = link
        
        #return f'<span class="wiki-link" onclick="wiki_link(\'{path}\')">{link_text}</span>'

    return re.sub(r'\[\[([^\]]+)\]\]', replace_link, text)
    

#print(parse("This is a [[link|linktext]]", "/category"))