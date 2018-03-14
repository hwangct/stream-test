#!/usr/bin/python -u
import boto3
import json
import time
from hashlib import sha256


stream = 'kinesis-demo'
shardId = 'shardId-000000000000'


# Create a Kinesis client
kinesis = boto3.client('kinesis')

# Get the shard position from which to begin reading data records
response = kinesis.get_shard_iterator(StreamName=stream, ShardId=shardId, ShardIteratorType='LATEST')
shardIter = response['ShardIterator']

header = None
while True:
    # Fetch available data records
    try:
        response = kinesis.get_records(ShardIterator=shardIter)
        timeOfLastRead = time.time()
    except kinesis.exceptions.ProvisionedThroughputExceededException:
        print('Kinesis provisioned throughput exceeded. Will try again in 1 second.')
        time.sleep(1)
        continue

    for record in response['Records']:
        if header is None:
            # Search for next payload header record and write to file
            try:
                header = json.loads(record['Data'])
                numSegments = header['payload']['segments']
                numSegmentsRcvd = 0
                sha256sum = sha256()
                headerFile = header['payload']['id'] + '.json'
                with open(headerFile, 'w+') as f:
                    f.write(record['Data'])
                    print('wrote %d bytes (header)' % len(record['Data']))
            except ValueError:
                continue
            except KeyError:
                header = None
                continue
        else:
            # Append payload data segment to output file
            numSegmentsRcvd += 1
            sha256sum.update(record['Data'])
            payloadFile = header['payload']['id'] + '.bin'
            with open(payloadFile, 'ab+') as f:
                f.write(record['Data'])
                print('wrote %d bytes (segment %d)' % (len(record['Data']), numSegmentsRcvd-1))

            if numSegmentsRcvd == numSegments:
                # Validate checksum
                if header['payload']['checksum'] != sha256sum.hexdigest():
                    print('checksum failure')
                    os.remove(headerFile)
                    os.remove(payloadFile)
                else:
                    # add to s3
                    # data = {"Writing some sample data": []}
                    # s3 = boto3.resource('s3')

                    # Put s3 object in bucket
                    # obj = s3.Object('kinesis-spark-bucket', payloadFile)
                    # obj.put(Body=json.dumps(data))
                    print('transfer complete')
                header = None


    # Update the shard position
    shardIter = response['NextShardIterator']

    # Throttle reads to 1 per second
    time.sleep(max(timeOfLastRead + 1 - time.time(), 0))
