from .webserv.apirequest import default_request_handler
from .webserv.apirequest import stream_request_handler
from .webserv.apirequest import SimpleRequest
from .webserv.apirequest import ErrorResult
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Query
import sqlite3
router = APIRouter()
import os
import re
# Define routes
@router.post("/request/categories_and_licences")
async def get_regions_handle(data:SimpleRequest):return await default_request_handler(data,categories_and_licences)

# Define routes
@router.post("/request/create_icon")
async def create_icon_handle(data:SimpleRequest):return await default_request_handler(data,create_icon)

@router.post("/request/update_icon")
async def create_update_icon(data:SimpleRequest):return await default_request_handler(data,update_icon)


@router.post("/request/icons")
async def icons_handle(data:SimpleRequest):return await default_request_handler(data,icon)

@router.post("/request/categories")
async def categories_handle(data:SimpleRequest):return await default_request_handler(data,categories)

@router.post("/request/update_variant")
async def update_variant_handle(data:SimpleRequest):return await default_request_handler(data,update_variant)

@router.post("/request/variants")
async def variants_handle(data:SimpleRequest):return await default_request_handler(data,variants)

@router.post("/request/icon_variants")
async def icon_variants_handle(data:SimpleRequest):return await default_request_handler(data,icon_variants)

@router.post("/request/update_icon_variant")
async def update_icon_variant_handle(data:SimpleRequest):return await default_request_handler(data,update_icon_variant)

@router.get("/request/download_icons")
async def download_icons_handle(data: str = Query(...)):
    return await stream_request_handler(data,download_icons)





# Path to the directory of main.py
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the database, relative to the directory of main.py
db_path = os.path.join(base_dir, "data", "data.db")

# Connect to the database using an absolute path
resource_conn = sqlite3.connect(db_path)


async def categories(data,parent):
    res=resource_conn.execute("SELECT categories.*, COUNT(icons.id) AS icon_count FROM categories LEFT JOIN icons ON icons.category = categories.id GROUP BY categories.id;")
    columns = [description[0] for description in res.description]
    return [dict(zip(columns, row)) for row in res.fetchall()]

async def variants(data,parent):
    res=resource_conn.execute("SELECT variants.*, COUNT(icon_variants.id) AS icon_count FROM variants LEFT JOIN icon_variants ON icon_variants.variant = variants.id GROUP BY variants.id;")
    columns = [description[0] for description in res.description]
    return [dict(zip(columns, row)) for row in res.fetchall()]

async def update_icon_variant(data,parent):
    if data["active"]:
        resource_conn.execute("INSERT INTO icon_variants (icon, variant) VALUES (?,?)",(data["icon_id"],data["variant_id"]))
    else:
        resource_conn.execute("DELETE FROM icon_variants WHERE icon=? AND variant=?",(data["icon_id"],data["variant_id"]))
    cnt=resource_conn.execute("SELECT COUNT(id) as cnt FROM icon_variants WHERE icon=? GROUP BY icon",(data["icon_id"],)).fetchone()
    return cnt[0] if cnt else 0

async def icon_variants(data,parent):
    global variants_cache
    if variants_cache is None:
        res=resource_conn.execute("SELECT * FROM variants")
        columns = [description[0] for description in res.description]
        variants_cache= [dict(zip(columns, row)) for row in res.fetchall()]


    data=resource_conn.execute("SELECT variant FROM icon_variants WHERE icon=?",(data["icon_id"],)).fetchall()
   
    return {"variants_active":data,"variants":variants_cache}


async def categories_and_licences(data,parent):
    res=resource_conn.execute("SELECT * FROM licenses")
    columns = [description[0] for description in res.description]
    licences= [dict(zip(columns, row)) for row in res.fetchall()]

    res=resource_conn.execute("SELECT * FROM categories")
    columns = [description[0] for description in res.description]
    categories= [dict(zip(columns, row)) for row in res.fetchall()]

    return {"categories":categories,"licenses":licences}

categories_cache=None # speed up request for searching
variants_cache=None
async def icon(data,parent):

    global categories_cache
    if categories_cache is None:
        res=resource_conn.execute("SELECT * FROM categories")
        columns = [description[0] for description in res.description]
        categories_cache= [dict(zip(columns, row)) for row in res.fetchall()]



    if len(data["filter"])>0:
        res=resource_conn.execute("SELECT icons.id as id, icons.name as name, icons.category as category , icons.data as data,COUNT(icon_variants.id) as variant_count FROM icons LEFT JOIN icon_variants ON icon_variants.icon = icons.id  WHERE icons.name LIKE ? GROUP BY icon_variants.icon;",(data["filter"],))
    else:
        res=resource_conn.execute("SELECT icons.id as id, icons.name as name, icons.category as category, icons.data as data,COUNT(icon_variants.id) as variant_count FROM icons LEFT JOIN icon_variants ON icon_variants.icon = icons.id GROUP BY icon_variants.icon;")


    columns = [description[0] for description in res.description]
    icons= [dict(zip(columns, row)) for row in res.fetchall()]

    return {"categories":categories_cache,"icons":icons,"variants":variants_cache}




async def create_icon(data,parent):

    # Verify entry valid

    if not re.match(r'^[a-zA-Z0-9 _]{2,48}$', data["name"]):return ErrorResult("Invalid name [a-zA-Z0-9 ]{2,48}")
    if not resource_conn.execute("SELECT * FROM categories WHERE id=?",(int(data["category_id"]),)).fetchone():return ErrorResult("Invalid category")
    if not resource_conn.execute("SELECT * FROM licenses WHERE id=?",(int(data["license_id"]),)).fetchone():return ErrorResult("Invalid license")
    if not len(data["data"])>10 or len(data["data"])>100000: return ErrorResult("Icon empty or invalid")

    # Verify name unique

    if resource_conn.execute("SELECT * FROM icons WHERE name LIKE ?",(data["name"],)).fetchone():return ErrorResult("Icon name already exists")


    # Save new entry
    cursor = resource_conn.cursor()
    cursor.execute("INSERT INTO icons (name,category,license,data) VALUES (?,?,?,?)",(data["name"], data["category_id"],data["license_id"],data["data"]))
    icon_id=cursor.lastrowid
    cursor.execute("INSERT INTO icon_variants (icon, variant) SELECT ?, id FROM variants WHERE is_default=1;",(icon_id,))
    resource_conn.commit();
    return True

async def update_icon(data,parent):
    # Verify entry valid
    icon_id=int(data["icon_id"])
    if not re.match(r'^[a-zA-Z0-9 _]{2,48}$', data["name"]):return ErrorResult("Invalid name [a-zA-Z0-9 ]{2,48}")
    if not resource_conn.execute("SELECT * FROM categories WHERE id=?",(int(data["category_id"]),)).fetchone():return ErrorResult("Invalid category")


    # Verify name unique
    if resource_conn.execute("SELECT * FROM icons WHERE id <> ? AND name LIKE ?",(icon_id,data["name"],)).fetchone():return ErrorResult("Icon name already exists")

    # Save new entry
    cursor = resource_conn.cursor()
    cursor.execute("UPDATE icons SET name=?,category=? WHERE id=?",(data["name"], data["category_id"],icon_id))
    resource_conn.commit();
    return True


async def update_variant(data,parent):
    # Verify entry valid
    variant_id=int(data["variant_id"])
    if not re.match(r'^[a-zA-Z0-9 _]{2,48}$', data["name"]):
        return ErrorResult("Invalid name [a-zA-Z0-9 _]{2,48}")
    if not re.match(r'^[a-zA-Z0-9 _]{0,3}$', data["abbreviation"]):
        return ErrorResult("Invalid abbreviation [a-zA-Z0-9 _]{0,3}")
    if not re.match(r'^[a-zA-Z0-9 _]{0,16}$',data["prefix"]):
        return ErrorResult("Invalid prefix [a-zA-Z0-9 _]{0,16}")
    if not re.match(r'^[a-zA-Z0-9 _]{0,16}$', data["postfix"]):
        return ErrorResult("Invalid postfix [a-zA-Z0-9 _]{0,16}")
    if not (1 <= int(data["height"]) <= 512):
        return ErrorResult("Invalid height [1-512]")
    if not (1 <= int(data["width"]) <= 512):
        return ErrorResult("Invalid width [1-512]")
    if not (-1 <=variant_id <=1000000):
        return ErrorResult("Unexpected id")
    if (len(data["prefix"])+ len(data["postfix"]))==0: return ErrorResult("pre or postfix must be set")
    # Verify uniqueness
    cursor = resource_conn.cursor()
    
    if variant_id == -1: # new
        if cursor.execute("SELECT * FROM variants WHERE name LIKE ?",(data["name"],)).fetchone():return ErrorResult("Variant name already exists")
        if cursor.execute("SELECT * FROM variants WHERE prefix LIKE ? AND postfix LIKE ?",(data["prefix"],data["postfix"])).fetchone():return ErrorResult("Variant pre/postfix not unique")
    else:
        if cursor.execute("SELECT * FROM variants WHERE id <> ? AND name LIKE ?",(variant_id,data["name"])).fetchone():return ErrorResult("Variant name already exists")
        if cursor.execute("SELECT * FROM variants WHERE id <> ? AND prefix LIKE ? AND postfix LIKE ?",(variant_id,data["prefix"],data["postfix"])).fetchone():return ErrorResult("Variant pre/postfix not unique")
   
    # Insert or Update
    if variant_id == -1: # new
        cursor.execute("INSERT INTO variants (name,width,height,color,prefix,postfix,is_default) VALUES (?,?,?,?,?,?,?)",(data["name"],int(data["width"]),int(data["height"]),data["color"],data["prefix"],data["postfix"],(1 if data["is_default"] else 0)))
        inserted_id = cursor.lastrowid
        if data["is_default"]:
            cursor.execute("INSERT INTO icon_variants (icon, variant) SELECT id, ? FROM icons;",(inserted_id,))
    else:
        cursor.execute("UPDATE variants SET name=?, width=?, height=?, color=?, prefix=?, postfix=?, is_default=? WHERE id=?", (data["name"], int(data["width"]), int(data["height"]), data["color"], data["prefix"], data["postfix"], (1 if data["is_default"] else 0), variant_id))
    resource_conn.commit()
    global variants_cache
    variants_cache=None
    return True
async def download_icons(data,parent):
    if "icon_id" in data:
        res=resource_conn.execute("SELECT icons.name as name,icons.data as data, categories.name as category, variants.width as width, variants.height as height, variants.color as color, variants.prefix as prefix, variants.postfix as postfix FROM icon_variants  LEFT JOIN icons ON icons.id = icon_variants.icon  LEFT JOIN variants ON variants.id = icon_variants.variant LEFT JOIN categories  ON icons.category=categories.id WHERE icons.id=?",(data["icon_id"],))
    else:
        res = resource_conn.execute("SELECT icons.name as name,icons.data as data, categories.name as category, variants.width as width, variants.height as height, variants.color as color, variants.prefix as prefix, variants.postfix as postfix FROM icon_variants  LEFT JOIN icons ON icons.id = icon_variants.icon  LEFT JOIN variants ON variants.id = icon_variants.variant LEFT JOIN categories  ON icons.category=categories.id")
   

    #res=resource_conn.execute("SELECT icons.name as name,icons.data as data, categories.name as category FROM icons LEFT JOIN categories  ON icons.category=categories.id")
    columns = [description[0] for description in res.description]
    icons = [dict(zip(columns, row)) for row in res.fetchall()]


    import xml.etree.ElementTree as ET
    import cairosvg
    from zipfile import ZipFile, ZIP_DEFLATED
    import io
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}

    buffer = io.BytesIO()
    with ZipFile(buffer, 'w', ZIP_DEFLATED) as zip_file:

        for icon in icons:
            # Parse the SVG file
            root = ET.fromstring(icon["data"])
        #root = tree.getroot()

            if len(icon["color"])==7:
                # Find elements to change color 
                for element in root.findall('.//*[@fill]', namespaces):
                    element.set('fill', icon["color"])
                for element in root.findall('.//*[@stroke]', namespaces):
                    element.set('stroke', icon["color"])


            svg_data = ET.tostring(root, encoding='unicode')

            png_bytes = cairosvg.svg2png(bytestring=svg_data, output_width=icon["width"], output_height=icon["height"])

            # Write PNG to zip
            output_file = f"{icon['category']}/{icon['prefix']}{icon['name']}{icon['postfix']}.png"
            zip_file.writestr(output_file, png_bytes)

    # Important: Seek to the beginning of the BytesIO buffer
    buffer.seek(0)

    return StreamingResponse(io.BytesIO(buffer.getvalue()), media_type="application/octet-stream")