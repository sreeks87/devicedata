import requests

r=requests.post("http://127.0.0.1:8000/device/",json={"timestamp":"","reading":12.34,"device_id":"12333","customer_id":"323444"})

print(r.content)