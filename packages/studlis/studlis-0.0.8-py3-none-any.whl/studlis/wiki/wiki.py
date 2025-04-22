from docvs.wiki.wiki_parse import extract_markdown_titles_and_quotes
import time
import gzip
class WikiManager():
    def __init__(self, parent):
        self.parent = parent

    async def get(self, path):
        pathlower = path.lower().strip()
        cursor=await self.parent.wikidb.execute("SELECT path,content,search_words, index_mode FROM wiki WHERE path = ? ", (pathlower,))
        ret = await cursor.fetchone()
        return None if ret is None else {"path":ret[0],"content":ret[1],"searchwords":ret[2],"index_mode":ret[3]}

    async def save(self,valid_path,data):
        # Note: in contrast to other methods save() expects a verified and valid path

        # Verify content
        if not "content" in data:raise ValueError("No content provided")
    
        content = data["content"]
        if len(content)>self.parent.max_wiki_content_length:raise ValueError("Content too long (including images)")
        name=valid_path.split("/")[-1]
        search_words = data["searchwords"]
        index_mode = data["index_mode"] 

        if index_mode == "full":
            index_text = content + " " + search_words + " " + name
        elif index_mode == "default":
            titles, quotes = extract_markdown_titles_and_quotes(content)
            index_text= " ".join(titles) + " " + " ".join(quotes) + " " + search_words + " " + name
        elif index_mode == "name":
            index_text = name
        elif index_mode == "searchwords":
            index_text=search_words
        elif index_mode == "none":
            index_text = ""
        else:
            raise ValueError("Invalid index mode")
        
        if len(search_words)>self.parent.max_wiki_search_words_length:raise ValueError("Search words too long")

        existing = await self.get(valid_path)
        
        if existing is None:
            await self.parent.wikidb.execute("INSERT INTO wiki (name,path,content,search_words,last_changed) VALUES (?,?,?,?,?)", (valid_path.split("/")[-1], valid_path, content,search_words,time.time()))
        else:
            await self.parent.wikidb.execute("UPDATE wiki SET name = ?, content = ?, search_words = ?, last_changed=? WHERE path = ?", (valid_path.split("/")[-1], content, search_words, valid_path,time.time()))


        await self.parent.index.update_resource(path = valid_path, 
                                                search_text = index_text, 
                                                type = 1,
                                                updated_module="wiki",
                                                updated_module_version="0.1",
                                                search_keywords=":wiki")
        

                                                



    def parse_text(self, text):
        return parse(text)
    

