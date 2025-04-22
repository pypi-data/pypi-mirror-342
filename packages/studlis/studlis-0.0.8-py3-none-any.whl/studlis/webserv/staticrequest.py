from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import HTTPException
from fastapi import APIRouter
import os
import pathlib
import logging
from pathlib import Path
router = APIRouter()

disable_cache=False

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.abspath(os.path.join(current_dir, "../static"))

@router.get("/static/{file_path:path}")
async def static(file_path):

    headers={"cache-control":"public, max-age=3600"}
    
    if disable_cache:
        # Set headers to disable cache
        headers={"cache-control":"no-store, no-cache, must-revalidate, max-age=0"}


    path = os.path.abspath(os.path.join(static_dir, file_path))
    

    # Check if static_dir is a prefix of path_a
    if not os.path.commonpath([path, static_dir]) == static_dir:
        raise HTTPException(status_code=403, detail="Access forbidden.")

#
    # check if file exists
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    # check if file is a file
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    # check if file is within the static directory


    # return file
    return FileResponse(path, headers=headers)
    
    """
    # Please note: This part has not been audited for security implications yet. 
    # Sanitize the file_path to avoid directory traversal
    safe_path = Path(file_path).parts
    safe_path = [part for part in safe_path if part != '..']

    # Create an absolute path to the static directory
    static_dir = Path(__file__).parent.parent / "static"
    # Join the sanitized path
    full_path = static_dir.joinpath(*safe_path).resolve() 
    
    # Make sure that the path is within the static directory
    if not str(full_path).startswith(str(static_dir)):
        raise HTTPException(status_code=403, detail="Access to this file is forbidden")

    # Check if the file exists and is a file (not a directory)
    if not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    """
    # Return the requested file

