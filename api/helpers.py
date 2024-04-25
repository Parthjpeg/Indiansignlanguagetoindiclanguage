from ultralytics import YOLO
import os
from openai import OpenAI
import requests

model = YOLO("best.pt")

def gettextfromvideo():
    directory_path = 'C:/personal/finalyearproject2024/cv/videotoimage/isltoil/data'
    l = []
    cnt = 0
    for x in os.listdir("C:/personal/finalyearproject2024/cv/videotoimage/isltoil/data"):
        print(x)
        a = []
        if x.endswith(".jpg"):
            comp = "C:/personal/finalyearproject2024/cv/videotoimage/isltoil/data/"+x
            print(comp)
            try:
                
                a.append(x)
                results = model.predict(comp)
                result = results[0]
                box = result.boxes
                class_id = box.cls.item()
                class_id = result.names[box.cls[0].item()]
                print(class_id)
                a.append(class_id)
                l.append(a)
            except:
                print("cannot classify")

    sorted_data = sorted(l, key=lambda x: int(x[0][5:-4]))
    print(sorted_data)
    s = ""
    cnt = 0
    for i in sorted_data:
        if(cnt == 0 ):
            word = i[1]
            cnt = cnt+1
            s = s+" "+i[1]
        elif(word!=i[1]):
            word = i[1]
            cnt = cnt+1
            s = s+" "+i[1]
    return s

def generativetranslate(s):
    client = OpenAI()
    l = [{"role": "system", "content": "your job is to help people who have cant talk i will give you a sentence your job is to refactor the sentence for the user"} , {"role":"user" , "content":s}]
    response = client.chat.completions.create(
        model="gpt-4",
      messages=l
      )

    totranslate = response.choices[0].message.content
    return totranslate


def translatetext(text , language):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "0ELDJvqbaDLzAGPIR1Dfv38ehE21HkMjxWkXYWq-Mk1bajlyyxXMyHGpwb3lD2cz"
    }
    payload = {
       "inputData": {
        "input": [
            {
                "source": text
            }
        ]
        },
        "pipelineTasks":[
        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": "en",
                    "targetLanguage": language
                },
                "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
            }
        }
        ]
        }
    response = requests.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", headers=headers, json=payload)
    return (response.json().get('pipelineResponse')[0].get('output')[0].get('target'))

#supported languages
# as
# bn
# brx
# gu
# hi
# kn
# ml
# mni
# mr
# or
# pa
# ta
# te