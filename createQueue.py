import os

teams_name = ['Vitality', 'PGNAT', 'OutPlayed']

for name in teams_name:
    os.system('aws sqs create-queue --queue-name '+ name +' --endpoint-url=http://localhost:4566')

os.system('aws sqs list-queues --endpoint-url=http://localhost:4566')
