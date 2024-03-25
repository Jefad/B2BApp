import requests

product_endpoint = 'http://127.0.0.1:8000/api/products/create/'
login_endpoint = 'http://127.0.0.1:8000/api/auth/login/'

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NjA2OTU4LCJpYXQiOjE3MDg2MDU3NTgsImp0aSI6ImZmYmMzZGRlNDExNDQxZTJhNjg4MTFlMjM5ZTRhMjRjIiwidXNlcl9pZCI6Mn0.Ur8Im_mi0-mJCqCpI0pVzhMvMzv2hAw2lbQJqI_iqI4',
    'Content-Type': 'application/json'
}

product_data = {
    'name': 'PES 2015',
    'size': 111.4,
    'price': 65
}

product_list_data = [
    {
        'name': 'FIFA 2021',
        'size': 117.4,
        'price': 98
    },
    {
        'name': 'FIFA 2020',
        'size': 114.1,
        'price': 97
    }
]

user_data = {
    'username': 'appadmin',
    'password': '1376'
}

response = requests.post(product_endpoint, headers=headers, json=product_data)

if response.ok:
    data = response.json()
    print('Authenticated Response:', data)
else:
    print('HTTP error! Status:', response.status_code)
    print('Error:', response.text)
