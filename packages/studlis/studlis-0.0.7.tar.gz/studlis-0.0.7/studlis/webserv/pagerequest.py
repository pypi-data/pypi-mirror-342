#from mako.template import Template
import os
from mako.lookup import TemplateLookup
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import json
router = APIRouter()

template_dir = os.path.join(os.path.dirname(__file__), '..', 'webui')
mylookup = TemplateLookup(directories=[template_dir ], module_directory='tmp/mako_modules',cache_enabled = False)
global_variants={}


def serve_template(templatename, **kwargs):
    global global_variants
    mytemplate = mylookup.get_template(templatename)
 
    return mytemplate.render(global_variants=json.dumps(global_variants),**kwargs)


@router.get("/", response_class=HTMLResponse)
async def root():
    global jsvars

    try:
        return HTMLResponse(serve_template("main.html"), media_type="text/html")
    except Exception as e:return HTMLResponse(e.args)