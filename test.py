import requests
import json

data = {"unom" : 1, "incident_name" : "открыт колодец", "date" : "12.02.2022"}

res = requests.post(url = "http://localhost:8000/items", data=json.dumps(data))
print(res.json())