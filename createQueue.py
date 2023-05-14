import os

teams_name = ['Vitality', 'PGNAT', 'OutPlayed']

for name in teams_name:
    os.system('aws sqs create-queue --queue-name '+ name +' --endpoint-url=http://localhost:4566')

os.system('aws sqs list-queues --endpoint-url=http://localhost:4566')
#os.system('aws sqs get-queue-attributes --queue-url http://localhost:4566/000000000000/Vitality --attribute-name QueueArn')


os.system(r'aws iam create-role --role-name lambdarole --assume-role-policy-document file://C:\Users\Daniele\IdeaProjects\SoftairAssistant\role_policy.json --query '+"\'"+'Role.Arn'+"\'"+' --endpoint-url=http://localhost:4566')



os.system(r'cd C:\Users\Daniele\IdeaProjects\SoftairAssistant')



os.system('aws lambda create-function --function-name saveGPSfunc --zip-file fileb://saveGPSfunc.zip --handler saveGPSfunc.lambda_handler --runtime python3.10 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566')

os.system('aws lambda create-event-source-mapping --function-name saveGPSfunc --batch-size 4 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:eu-west-2:000000000000:Vitality --endpoint-url=http://localhost:4566')
