import os
import json
import aiosqlite
import sqlite3 as sqlite
from enum import Enum
import asyncio
import time
import csv
import tempfile
import io
import zipfile
from fastapi.responses import StreamingResponse
from typing import AsyncIterator
from openpyxl import Workbook
from datetime import datetime
class ProjectManager():
    def __init__(self,parent):
        self.appmain = parent

    async def refresh_projects(self):
      



        for project_root in self.appmain.configuration["project_roots"]:
            if "project.json" in os.listdir(project_root):
                await self.refresh_project(project_root)
                continue
            for root, dirs, files in os.walk(project_root):
                if 'project.json' in files:
                    await self.refresh_project(root)
    async def refresh_project(self,path):
        project = await load_project(path)
        if not project:return
        if project.name in self.appmain.projects:
            if self.appmain.projects[project.name].path != path:    
                print(f"Project {project.name} already exists in {self.appmain.projects[project.name].path}, skipping {path}")
        else:
                self.appmain.projects[project.name] = project
async def load_project(path):   

    try:
        return Project(path) # not async, but this is not done often TODO: make async
    except json.JSONDecodeError:
        print(f"Error loading project {path}: project.json is not a valid JSON.")
    except FileNotFoundError:
        print(f"Error loading project {path}: project.json not found.")
    except Exception as e:
        print(f"Error loading project {path}: {e}")



class FieldType(Enum):
    BOOL = "bool"
    MULTIBOOL = "multibool"
    SELECT = "select"
    INT = "int"
    DECIMAL = "decimal"
    CATEGORY = "category"
    TEXT = "text"



class Project():
    def __init__(self,path):
        
        self.path = path
        self.project_data = None
        self.fields={}
        self.study_count=0
        self.async_db = None
        
        self.load_project_data()
    def load_project_data(self):

        with open(os.path.join(self.path, 'project.json'), 'r') as project_file:
            
                self.configuration = json.load(project_file)
                self.name=self.configuration["name"]
                if "description" in self.configuration:
                    self.description=self.configuration["description"]
                else:
                    self.description=""




        db_path = os.path.join(self.path, 'data.db')
        self.db= sqlite.connect(db_path)
        self.init_db()        
        self.refresh_data()
        print(f"Loaded project {self.name} from {self.path}")
    
    def init_db(self):

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS studies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,                                
            name TEXT,          
            source TEXT,
            source_collection TEXT,
            source_id TEXT,
            doi TEXT,
            comment TEXT,
            abstract TEXT,
            fulltext TEXT,
            year INT,
            month INT,
            day INT,
            study_data TEXT,
            state INTEGER,    
            excluded_reason TEXT
            )
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_id ON studies (source_id)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source ON studies (source)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_collection ON studies (source_collection)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_source_id ON studies (source, source_id)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_year ON studies (year)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_state ON studies (state)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_excluded_reason ON studies (excluded_reason)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_doi ON studies (doi)
        ''')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT,
            caption TEXT,
            description TEXT,                
            type TEXT,
            reference TEXT,
            llm_query TEXT,
            style TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS validation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_id INTEGER,
                validator TEXT, 
                comment TEXT,
                ts INTEGER,
                data_changed INTEGER,
                data TEXT,               
                study_state INTEGER,
                confidence INTEGER,     /* If confidence is 0 no "are you sure you want to change data" is asked  */
                validation_state INTEGER,      /* -1 invalid/deprecated/deleted 1 valid, 10 revision requested */
                consensus INTEGER   /* 1 if at ts time all validations are the same, 0 otherwise */
            )
        ''')
        # consensus = the newest validation of each user is the same, checked on save, data equals data

        
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_study_id ON validation (study_id)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_validator ON validation (validator)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_ts ON validation (ts)
        ''')
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_validation_valid_state ON validation (validation_state)
        ''')



        self.db.commit()
    def refresh_data(self):

        # Refresh data that may have changed in the project.json file
        with open(os.path.join(self.path, 'project.json'), 'r') as project_file:
            conf = json.load(project_file)
            self.exclude_reasons = conf["exclude_reasons"]

        # Refresh data that may have changed in the database
        new_data = {}
        new_data_fields = {}
        cursor=self.db.execute('SELECT field_name, caption, description, type, reference, llm_query, style FROM fields')
        data=cursor.fetchall()

        for row in data:
            field_name, caption, description, type, reference, llm_query, style = row
            new_data[field_name] = {
                "name": field_name,
                "caption": caption,
                "description": description,
                "type": type,
                "reference": json.loads(reference),
                "llm_query": llm_query,
                "style": style
            }
            if type == FieldType.MULTIBOOL.value:
                for ref in json.loads(reference):
                    new_data_fields[f"{field_name}_{ref}"] = {
                        "name": f"{field_name}_{ref}",
                        "caption": caption,
                        "description": description,
                        "type": type,
                        "reference": json.loads(reference),
                        "llm_query": llm_query,
                        "style": style
                    }
            else:
                new_data_fields[field_name] = {
                    "name": field_name,
                    "caption": caption,
                    "description": description,
                    "type": type,
                    "reference": json.loads(reference),
                    "llm_query": llm_query,
                    "style": style
                }
        self.fields = new_data
        self.datafields = new_data_fields
        self.study_count = self.db.execute('SELECT COUNT(*) FROM studies').fetchone()[0]

    def register_field(self,field_name,caption="",description="",type=FieldType.DECIMAL,reference={},llm_query="",style=""):
    
        if len(caption)==0: caption=field_name
        cursor = self.db.execute('SELECT COUNT(*) FROM fields WHERE field_name = ?', (field_name,))
        if cursor.fetchone()[0] > 0:
            print(f"Field {field_name} already exists. Metadata updated.")
            self.db.execute('''
                UPDATE fields SET caption = ?, description = ?, type = ?, reference = ?, llm_query = ?, style = ? WHERE field_name = ?
            ''',(caption,description,type.value,json.dumps(reference),llm_query,style,field_name))
            self.db.commit()
            return
        
        self.db.execute('''
            INSERT INTO fields (field_name, caption, description, type, reference, llm_query, style)
            VALUES (?,?,?,?,?,?,?)
        ''',(field_name,caption,description,type.value,json.dumps(reference),llm_query,style))

        sqltype=None
        if type == FieldType.CATEGORY:
            sqltype = "TEXT"
        elif type=="bool":
            sqltype = "INTEGER"
        elif type == FieldType.SELECT:
            sqltype = "TEXT"
        
        elif type == FieldType.DECIMAL:
            sqltype = "REAL"
        elif type == FieldType.INT:
            sqltype = "INTEGER"
        elif type == FieldType.TEXT:
            sqltype = "TEXT"

        if sqltype:
            self.db.execute(f'''
                ALTER TABLE studies ADD COLUMN data_{field_name} {sqltype}
            ''')
        elif type == FieldType.MULTIBOOL:
            for ref in reference:
                self.db.execute(f'''
                    ALTER TABLE studies ADD COLUMN data_{field_name}_{ref} INTEGER
                ''')

        self.db.commit()
    def drop_field(self,field_name):
        cursor = self.db.execute('SELECT type FROM fields WHERE field_name = ?', (field_name,))
        ret=cursor.fetchone()
        if not ret:
            print(f"Field {field_name} does not exist.")
            return
        field_type = ret[0]
        if field_type == FieldType.MULTIBOOL.value:   
            cursor = self.db.execute("PRAGMA table_info(studies)")
            columns = [row[1] for row in cursor.fetchall()]
            for column in columns:
                if column.startswith(f"data_{field_name}_"):
                    self.db.execute(f'ALTER TABLE studies DROP COLUMN {column}')
        else:
            self.db.execute(f'''
                ALTER TABLE studies DROP COLUMN data_{field_name}
            ''')

        self.db.execute('DELETE FROM fields WHERE field_name = ?', (field_name,))
        
        self.db.commit()
        
    def register_pubmed(self, pid, type="journal_article",name="",abstract="",fulltext="",year=0,month=0,day=0,study_data="{}",state=0,excluded_reason=0,source_collection="default",doi=""):
        cursor=self.db.execute('SELECT COUNT(*) FROM studies WHERE source = ? AND source_id = ?', ("pubmed", pid))

        count = cursor.fetchone()
        if count[0] > 0:return

        self.db.execute('''
            INSERT INTO studies (type, name, source, source_id, comment, abstract, fulltext, year, month, day, study_data, state, excluded_reason,source_collection,doi)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',(type,name,"pubmed",pid,"",abstract,fulltext,year,month,day,study_data,state,excluded_reason,source_collection,doi))
        self.db.commit()

    def get_llm_metadata(self):
        cursor = self.db.execute('SELECT field_name,  type, reference, llm_query FROM fields')
        data = cursor.fetchall()
        ret = []
        for row in data:
            field_name, type, reference_str, llm_query = row
            reference=json.loads(reference_str)

            # MULTIBOOL behave like a list of single bools
            if type == FieldType.MULTIBOOL.value:
                
                for ref in reference:
                    if "llm_query" in reference[ref]:
                        ret.append(
                            {"fieldname":field_name+"_"+ref,
                             "options":reference[ref]["llm_options"],
                             "query":reference[ref]["llm_query"]})
                    else:
                        print(f"Field {field_name}.{ref} does not have a llm_query.")
            elif type == FieldType.SELECT.value:
                
                
                
                    if llm_query:
                   
                        ret.append( 
                                {"fieldname":field_name,
                                "options":",".join(f'"{k}"' for k in reference.keys()),
                                "query":llm_query})
                    else:
                        print(f"Field {field_name}.{ref} does not have a llm_query.")    


                
            elif type==FieldType.INT.value:
                if llm_query:
                     ret.append(
                            {"fieldname":field_name,
                             "options":"integer",
                             "query":llm_query})
                else:
                    print(f"Field {field_name} does not have a llm_query.")
        return ret
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "fields": self.fields,
            "study_count": self.study_count,
            "exclude_reasons": self.exclude_reasons
        }
    def get_study_list(self,q_from=0,limit=30):
        cursor = self.db.execute('SELECT * FROM studies LIMIT ? OFFSET ?', (limit,q_from))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]    
    
    async def get_study_list_async(self,data,session_data,limit=30,id_only=False):
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))
        where=""
        join =""
 
        order = "ORDER BY id DESC"
        if "order_mode" in data:
            if data["order_mode"] == "asc":
                order = "ORDER BY studies.id ASC"
            elif data["order_mode"] == "desc":
                order = "ORDER BY studies.id DESC"
            elif data["order_mode"] == "date_desc":
                order = "ORDER BY studies.year DESC, month DESC, day DESC"
            elif data["order_mode"] == "date_asc":
                order = "ORDER BY studies.year ASC, month ASC, day ASC"
            elif data["order_mode"] == "pseudorandom": # linear congruential generator
                uid=session_data["user_id"]
                order = f"ORDER BY abs((studies.id * 1103515245 + 12345 + {uid}) % 2147483647)"

        params = []

        if "from" in data:
            q_from = data["from"]
        else:
            q_from=0





        if "filter" in data:
            if "name" in data["filter"]:
                q_filter = data["filter"]["name"]
                if len(q_filter) >=3:
                    where = where + f" AND studies.name LIKE ?"
                    params.append(f"%{q_filter}%")

            if "included" in data["filter"]:
                if data["filter"]["included"]==1:
                    where = where + " AND studies.state >= 0 "
                else:
                    where = where + " AND studies.state < 0 "
        if id_only:
            selector="studies.id"
        else:
            selector="studies.*"
        
        if where != "":
            where = "WHERE 1 "+where

        if "validated_own" in data:
            if data["validated_own"]:
                join=join+f" INNER JOIN validation ON studies.id = validation.study_id AND validation.validator = ? "
                params.append(session_data["username"])
     
        params.append(limit)
        params.append(q_from)
        
#
        async with self.async_db.execute('SELECT '+selector+' FROM studies '+join+where+order+' LIMIT ? OFFSET ?', params) as cursor:
            rows = await cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            if not id_only:
                return [dict(zip(columns, row)) for row in rows]
            else:
                return [row[0] for row in rows]
    async def get_study_async(self,data):
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))
        ret = {}
        async with self.async_db.execute('SELECT * FROM studies WHERE id = ?', (data["study_id"],)) as cursor:
            row = await cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            ret["study"]= dict(zip(columns, row))
        async with self.async_db.execute('SELECT * FROM validation WHERE study_id = ? ORDER BY ts DESC', (data["study_id"],)) as cursor:
            rows = await cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            ret["validation"] = [dict(zip(columns, row)) for row in rows]
        ret["project"]=self.to_dict()

        return ret
    def get_study(self,study_id):
        ret = {}
        cursor=self.db.execute('SELECT * FROM studies WHERE id = ?', (study_id,))
        row = cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        ret["study"]= dict(zip(columns, row))
        cursor=self.db.execute('SELECT * FROM validation WHERE study_id = ? ORDER BY ts DESC', (study_id,))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        ret["validation"] = [dict(zip(columns, row)) for row in rows]
        ret["project"]=self.to_dict()
        return ret
    

    async def get_next_study_for_validation_async(self,data,session_data):
        data["amount"]=1
        studies = await self.get_studies_for_validation_async(data,session_data)
        if len(studies) == 0:return {"result":"no_studies"}
        return await self.get_study_async({"study_id":studies[0]["id"]})
    
    async def get_studies_for_validation_async(self,data,session_data):
        amount = data["amount"]
        username=session_data["username"]
        ret={}
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))
        studies = []
        async with self.async_db.execute('''
            SELECT studies.* FROM studies 
            LEFT JOIN validation ON studies.id = validation.study_id AND validation.validator = ?
            WHERE validation.study_id IS NULL
            ORDER BY RANDOM()
            LIMIT ?
        ''', (username, amount)) as cursor:
            rows = await cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            for row in rows:
                studies.append(dict(zip(columns, row)))
        return studies
        

    def get_studies_for_validation(self,username,amount=1):

        studies = []
        cursor=self.db.execute('''
            SELECT studies.* FROM studies 
            LEFT JOIN validation ON studies.id = validation.study_id AND validation.validator = ?
            WHERE validation.study_id IS NULL
            ORDER BY RANDOM()
            LIMIT ?
        ''', (username, amount)) 
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        for row in rows:
            studies.append(dict(zip(columns, row)))
        return studies
        


    async def update_validation_async(self,data,session_data):
        username=session_data["username"]
        study=await self.get_study_async(data)
        study_data=study["study"]
        new_validation_data=data["validation_data"]
        update_data={}
        changes = []
        for field in new_validation_data:
            if field not in self.datafields:
                raise ValueError(f"Field {field} does not exist in project {self.name}.")
            if study_data[f"data_{field}"] != new_validation_data[field]:
                update_data[f"data_{field}"] = new_validation_data[field]
                changes.append({
                    "name": field,
                    "old_value": study_data[f"data_{field}"],
                    "new_value": new_validation_data[field]
                })
        
        user_validation = None

        # Check if the user has already validated this study
        # If yes, check if data should be overwritten or not

        if len(study["validation"])>0:

            # Check if the user has already validated this study

            for validation in study["validation"]:
                if validation["validator"] == username:
                    user_validation = validation
                    break
        
            # Check if the last user that validated was confident
            if study["validation"][0]["confidence"] > data["confidence"]:

                # If the last user was confident, we need to ask for confirmation
                # Confirmation increases data["confidence"], 
                # if the updating user is at least as confident as the last user, data will be overwritten

                return {"result":"confidence_requested", "last_validation":study["validation"][0], "changes":changes}
                
                
        if len(update_data) == 0:
            return {"result":"nothing_changed"}
        
        update_query = "UPDATE studies SET "
        update_query += ", ".join([f"{key} = ?" for key in update_data.keys()])
        update_query += " WHERE id = ?"
        update_values = list(update_data.values())
        update_values.append(study_data["id"])
        await self.async_db.execute(update_query, update_values)

        update_values=[]
        update_values.append(json.dumps(new_validation_data))
        update_values.append(data["confidence"])
        update_values.append(time.time())
        update_values.append(study_data["id"])
        update_values.append(username)

        if user_validation:
            # Update the existing validation
            update_query = "UPDATE validation SET data = ?, confidence = ?,ts=?,validation_state=1"
            update_query += " WHERE study_id = ? AND validator = ?"
            await self.async_db.execute(update_query, update_values)
        else:
            # Insert a new validation
            update_query = "INSERT INTO validation (data, confidence,ts,study_id,validator,validation_state) VALUES (?,?,?,?,?,1)"
            await self.async_db.execute(update_query, update_values)
        await self.async_db.commit()
        return {"result":"saved"}


    def update_validation(self,study_id,data,username,confidence=0, lazy=False):
        study=self.get_study(study_id)
        study_data=study["study"]
        new_validation_data=data
        update_data={}
        changes = []
        for field in new_validation_data:

            if field not in self.datafields:
                if lazy:
                    continue
                raise ValueError(f"Field {field} does not exist in project {self.name}.")
            
            if self.datafields[field]["type"] == FieldType.MULTIBOOL.value:
                if new_validation_data[field] == True: new_validation_data[field] = 1
                if new_validation_data[field] == False: new_validation_data[field] = 0
                if not (new_validation_data[field] == 0 or new_validation_data[field]==1 or new_validation_data[field] is None):
                    if lazy:
                        print(f"Field {field} is not a valid boolean value.")
                        continue
                    raise ValueError(f"Field {field} is not a valid boolean value.")

            if study_data[f"data_{field}"] != new_validation_data[field]:
                update_data[f"data_{field}"] = new_validation_data[field]
                changes.append({
                    "name": field,
                    "old_value": study_data[f"data_{field}"],
                    "new_value": new_validation_data[field]
                })
        
        user_validation = None

        # Check if the user has already validated this study
        # If yes, check if data should be overwritten or not

        if len(study["validation"])>0:

            # Check if the user has already validated this study

            for validation in study["validation"]:
                if validation["validator"] == username:
                    user_validation = validation
                    break
        
            # Check if the last user that validated was confident
            if study["validation"][0]["confidence"] > confidence:
                if not lazy:
                    
                # If the last user was confident, we need to ask for confirmation
                # Confirmation increases data["confidence"], 
                # if the updating user is at least as confident as the last user, data will be overwritten

                    return {"result":"confidence_requested", "last_validation":study["validation"][0], "changes":changes}
                
                
        if len(update_data) == 0:
            return {"result":"nothing_changed"}
        
        update_query = "UPDATE studies SET "
        update_query += ", ".join([f"{key} = ?" for key in update_data.keys()])
        update_query += " WHERE id = ?"
        update_values = list(update_data.values())
        update_values.append(study_data["id"])
        self.db.execute(update_query, update_values)

        update_values=[]
        update_values.append(json.dumps(new_validation_data))
        update_values.append(confidence)
        update_values.append(time.time())
        update_values.append(study_data["id"])
        update_values.append(username)

        if user_validation:
            # Update the existing validation
            update_query = "UPDATE validation SET data = ?, confidence = ?,ts=?,validation_state=1"
            update_query += " WHERE study_id = ? AND validator = ?"
            self.db.execute(update_query, update_values)
        else:
            # Insert a new validation
            update_query = "INSERT INTO validation (data, confidence,ts,study_id,validator,validation_state) VALUES (?,?,?,?,?,1)"
            self.db.execute(update_query, update_values)
        self.db.commit()
        return {"result":"saved"}
    

    async def exclude_study_async(self,data,session_data):
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))
        username=session_data["username"]
        study_id=data["study_id"]
        reason=data["reason"]

        if len(reason)==0:
            await self.async_db.execute('UPDATE studies SET state = 1, excluded_reason = ? WHERE id = ?', (None,study_id))
            await self.async_db.commit()
            return True

        if reason not in self.exclude_reasons:
            raise ValueError(f"Reason {reason} does not exist in project {self.name}.")
        
        await self.async_db.execute('UPDATE studies SET state = -1, excluded_reason = ? WHERE id = ?', (reason,study_id))
        await self.async_db.commit()
        return True
    
    
    async def get_stats_async(self,data,session_data):
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))
        username = session_data["username"]
        user_id = session_data["user_id"]
        ret = {}

        # Incuded/Excluded studies

        cursor= await self.async_db.execute('SELECT COUNT(*) FROM studies')
        count = await cursor.fetchone()
        cursor = await self.async_db.execute('SELECT COUNT(*) FROM studies WHERE state >=0')
        included = await cursor.fetchone()


        ret ["included"] = included[0]
        ret ["count"] = count[0]
        validation_count_q="""
            SELECT validation_count, COUNT(*) AS num_studies
            FROM (
                SELECT study_id, COUNT(*) AS validation_count
                FROM validation
                WHERE validation_state = 1
                GROUP BY study_id
            ) AS valid_counts
            GROUP BY validation_count
            ORDER BY validation_count;
            """
        cursor= await self.async_db.execute(validation_count_q)
        rows = await cursor.fetchall()

        # Build validation counts indexed by validation_count
        validation_map = {row[0]: row[1] for row in rows}

        # Max validation count observed
        max_validation_count = max(validation_map.keys(), default=0)

        # Build the ret["validation"] list
        ret["validation"] = []
        for i in range(max_validation_count + 1):
            ret["validation"].append(validation_map.get(i, 0))

        # Ensure validation[0] is count[0] - sum of all other validations
        if ret["validation"]:
            ret["validation"][0] = ret["count"] - sum(ret["validation"][1:])

        # Get validations / count for this user
        cursor= await self.async_db.execute('SELECT COUNT(*) FROM validation WHERE validator = ? AND validation_state = 1', (username,))
        count = await cursor.fetchone()
        ret["user_validations"] = count[0]

        return ret
    


    async def stream_backup_async(self,data,session_data):
         # Fallback to temporary file
        db_path = os.path.join(self.path, 'data.db')
        json_path = os.path.join(self.path, 'project.json')
        tmp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        try:
            with zipfile.ZipFile(tmp_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                zf.write(db_path, arcname='data.db')
                zf.write(json_path, arcname='project.json')
            tmp_zip.flush()
            tmp_zip.close()
            zip_size = os.path.getsize(tmp_zip.name)
            async def iterfile() -> AsyncIterator[bytes]:
                with open(tmp_zip.name, mode='rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        yield chunk
                # Clean up the temp file after streaming
                os.remove(tmp_zip.name)
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            filename = f"studlis_{self.name}_{timestamp}.zip"
            return StreamingResponse(
                iterfile(),
                media_type='application/zip',
                headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Length': str(zip_size)
                }
            )
        except Exception:
            # Ensure temp file is removed on error
            try:
                os.remove(tmp_zip.name)
            except Exception:
                pass
            raise

    async def stream_csv(self, data, session_data):
        # Ensure database connection
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))

        # Query all rows from 'studies' table
        cursor = await self.async_db.execute("SELECT * FROM studies")
        columns = [col[0] for col in cursor.description]

        async def iter_csv() -> AsyncIterator[bytes]:
            # In-memory text buffer for CSV rows
            buffer = io.StringIO()
            writer = csv.writer(buffer)

            # Write header
            writer.writerow(columns)
            yield buffer.getvalue().encode()
            buffer.seek(0)
            buffer.truncate(0)

            # Write data rows
            async for row in cursor:
                writer.writerow(row)
                yield buffer.getvalue().encode()
                buffer.seek(0)
                buffer.truncate(0)

            await cursor.close()

        # Filename for download
        filename = f"studlis_{self.name}.csv"

        return StreamingResponse(
            iter_csv(),
            media_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )

    async def stream_xlsx(self, data, session_data):
        # Ensure database connection
        if not self.async_db:
            self.async_db = await aiosqlite.connect(os.path.join(self.path, 'data.db'))

        # Query all rows from 'studies' table
        cursor = await self.async_db.execute("SELECT * FROM studies")
        columns = [col[0] for col in cursor.description]

        # Build workbook
        wb = Workbook()
        ws = wb.active
        ws.append(columns)

        async for row in cursor:
            ws.append(list(row))
        await cursor.close()

        # Save to in-memory buffer
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        filename_xlsx = f"studlis_{self.name}.xlsx"
        return StreamingResponse(
            buf,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': f'attachment; filename="{filename_xlsx}"'
            }
        )