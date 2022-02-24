from requests import get, post, delete, put
from datetime import datetime

'''print(get('http://localhost:5000/api/jobs').json())
print(get('http://localhost:5000/api/jobs/2').json())
print(get('http://localhost:5000/api/jobs/15').json())
print(get('http://localhost:5000/api/jobs/qqqqqq').json())

print(post('http://localhost:5000/api/jobs',
           json={'id': 4,
                 'team_leader': 'Alan Walker',
                 'job': 'artist',
                 'work_size': 9,
                 'collaborators': "1, 2",
                 'is_finished': True}).json())

print(post('http://localhost:5000/api/jobs', # ошибочный запрос с существующим id
           json={'id': 1,
                 'team_leader': 'Alan Walker',
                 'job': 'artist',
                 'work_size': 9,
                 'collaborators': "1, 2",
                 'is_finished': True}).json())

print(post('http://localhost:5000/api/jobs', # ошибочный запрос с недостаточным кол-вом параметров
           json={'team_leader': 'Mark',
                 'job': 'engineer',
                 'work_size': 20,
                 'is_finished': False}).json())


print(post('http://localhost:5000/api/jobs', # ошибочный запрос с очень большим кол-вом параметров id
           json={'id': 6,
                 'team_leader': 'Alan Walker',
                 'job': 'artist',
                 'work_size': 9,
                 'collaborators': "1, 2",
                 'qwe': 'qwe',
                 'is_finished': True}).json())


print(delete('http://localhost:5000/api/jobs/2').json())

print(delete('http://localhost:5000/api/jobs/qqq').json()) # неверный id

print(delete('http://localhost:5000/api/jobs/111').json()) # неверный id

print(delete('http://localhost:5000/api/jobs/6').json()) '''

print(put('http://localhost:5000/api/jobs/1', # ошибочный запрос с очень большим кол-вом параметров id
           json={'id': 1,
                 'team_leader': 'Alan Walker',
                 'job': 'artist',
                 'work_size': 9,
                 'collaborators': "1, 2",
                 'is_finished': True}).json())
print(get('http://localhost:5000/api/jobs').json())

