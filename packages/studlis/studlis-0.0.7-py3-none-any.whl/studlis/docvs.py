from .webserv.apirequest import default_request_handler
from .webserv.apirequest import stream_request_handler
from .webserv.apirequest import SimpleRequest
from .webserv.apirequest import ErrorResult
from docvs.util import path_valid
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from typing import AsyncIterator
from .authprovider import AuthPermission
import time
import json
import aiofiles
import sqlite3
router = APIRouter()
import os
import re
import aiohttp
from bs4 import BeautifulSoup

appmain=None
#

@router.post("/request/search")
async def create_search_handle(data:SimpleRequest):return await default_request_handler(data,search)

@router.get("/request/getpdf/{data}")
async def get_pdf(data: str):
    return await stream_request_handler(data, request_pdf_resource)

@router.post("/request/login")
async def login_route(data:SimpleRequest):return await default_request_handler(data,login)

@router.post("/request/edit_resource_load")
async def edit_resource_load_route(data:SimpleRequest):return await default_request_handler(data,edit_resource_load)

@router.post("/request/edit_resource_save")
async def edit_resource_save_route(data:SimpleRequest):return await default_request_handler(data,edit_resource_save)

@router.post("/request/load_wiki")
async def load_wiki_route(data:SimpleRequest):return await default_request_handler(data,load_wiki)

@router.post("/request/parse_wiki")
async def parse_wiki_route(data:SimpleRequest):return await default_request_handler(data,parse_wiki)

@router.post("/request/save_wiki")
async def save_wiki_route(data:SimpleRequest):return await default_request_handler(data,save_wiki)


async def search(data,parent):
    if data["query"] is None:
        return ErrorResult("No query provided")
    
    params = {}
    if "entity" in data:
        params["entity"] = data["entity"]
    if "edit_mode" in data: # editor search
        if appmain.has_permission(data, AuthPermission.EDITOR):
            params["edit_mode"] = True
        

    results = await appmain.index.search(data["query"],**params)

    # Return the results
    return results

async def load_wiki(data,parent):
    # if data["path"] is [a-zA-Z][a-zA-Z0-9_ :]{5,164}
    if not path_valid(data["path"]):
        return ErrorResult("Invalid path")
    return await appmain.wiki.get(data["path"])
    
async def parse_wiki(data,parent):
    if "text" not in data:
        return ErrorResult("No text provided")
    return appmain.wiki.parse_text(data["text"])

async def save_wiki(data,parent):
    if "path" not in data:
        return ErrorResult("No path provided")

    category,name,valid_path = appmain.parse_verify_path(data["path"]) # this also validates categoty
    if not appmain.has_category_edit_permission(data, category["path"]):
        return ErrorResult("Not enough permissions")
    await appmain.wiki.save(valid_path,data) # raises exception if not successful
    return {"success": True}



async def request_pdf_resource(id,parent):
    file_path = await appmain.index.get_resource_path(id);
    if not os.path.exists(file_path):
        return ErrorResult("File not found", status_code=404)



    async def iterfile() -> AsyncIterator[bytes]:
        async with aiofiles.open(file_path, mode="rb") as file_like:
            while chunk := await file_like.read(8192):
                yield chunk
    return StreamingResponse(iterfile(), media_type="application/pdf")

async def login(data,parent):
    if not await appmain.auth.needs_credentials():
        result= await appmain.auth.authenticate(appmain)
        if result is None:
            return ErrorResult("Invalid username or password")
        
        session_token =  appmain.session_manager.create_session(data=result)
        return {"token":session_token,"permission_groups":result["permission_groups"]}
    return ErrorResult("Invalid username or password")


async def edit_resource_load(data,parent):

    if not appmain.has_permission(data, AuthPermission.MODERATOR.value):
        return ErrorResult("Not enough permissions")

    path = data["path"].strip()
    path = path.replace('"', '') # windows path copy has quotes, and quotes are not valid anyway

    if path.isnumeric(): # if it is a number, it is an id
        cursor = await appmain.index.db.execute("SELECT id,name,search_words,path,description,type FROM items WHERE id = ?", (int(path),))
    else:
        cursor = await appmain.index.db.execute("SELECT id,name,search_words,path,description,type FROM items WHERE path = ?", (path,))
    
    result = await cursor.fetchone()
    await cursor.close()
    if result:
        return {"id": result[0], "name": result[1], "search_text": result[2], "path": result[3], "description": result[4], "type": result[5]}
   


    if path.startswith("http"):
        # This is a web resource, try get metadata
        async with aiohttp.ClientSession() as session:
            async with session.get(path) as response:
                if response.status != 200:
                    return ErrorResult("Failed to fetch the webpage", status_code=response.status)
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.title.string if soup.title else path
                description = soup.find('meta', attrs={'name': 'description'})
                description_content = description['content'] if description else ""
                return {"id": -1, "search_text": title+ " "+ description_content, "name": title, "path": path, "type": 2}
    else:
        if not os.path.exists(path):
            return ErrorResult(f"File {path} not found")

async def edit_resource_save(data,parent):  
    permission, session_data = appmain.has_permission(data, AuthPermission.MODERATOR.value)
    if not permission:
        return ErrorResult("Not enough permissions")
    name = data["name"].strip()
    search_text = data["search_text"].strip()
    path = data["path"].strip()
    path = path.replace('"', '') # windows path copy has quotes, and quotes are not valid anyway
    description = data["description"].strip()
    resource_type = data["type"]
    
    if int(data["id"]) <= 0:
        cursor = await appmain.db.execute("INSERT INTO items (name, search_words, path, description, type) VALUES (?, ?, ?, ?, ?)", (name, search_text, path, description, resource_type))
        await appmain.db.commit()
        data["id"] = cursor.lastrowid
    else:
        cursor = await appmain.db.execute("UPDATE items SET name = ?, search_words = ?, path = ?, description = ?, type = ? WHERE id = ?", (name, search_text, path, description, resource_type, data["id"]))
   
    await appmain.db.execute(
        "INSERT INTO changelog (resource_id, timestamp, new_content, user) VALUES (?, ?, ?, ?)",
        (data["id"], int(time.time()), json.dumps(data), session_data["user_id"])
    )
    await appmain.db.commit()
    await cursor.close()
    await appmain.index.update_item(data)
    return {"success": True}          



