from fastapi import FastAPI, Path, Query, HTTPException # type: ignore

import json

def load_data(): 
    with open('patients.json','r') as f:
        data=json.load(f)
    return data
    
    

app=FastAPI()

@app.get('/')

def hello():
    return {'message':'Patient management system API'}


@app.get('/about')
def about():
    return {'message':'Fully Functional API manage patient record'}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def patient_view(patient_id:str=Path(..., description='Id of the patient in db,example:P003')):
    # load all the patient
    data=load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    return {'error': 'id not found'}


@app.get('/sort')
def sort_patient(sort_by:str=Query(..., description='sort on the basis of height,weight, bmi'),
order:str=Query('asc',description='sort asc or desc order')):
    
    valid_fields=['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid field select from {valid_fields}')    
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid order select from asc or desc')
    
    data=load_data()
    
    sort_order= True if order=='desc' else False
    
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data
