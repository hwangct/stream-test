# Starting point
https://docs.aws.amazon.com/streams/latest/dev/fundamental-stream.html

# Set up AWS-cli
https://docs.aws.amazon.com/cli/latest/userguide/installing.html

# Install python packages
$ pip install boto3

# Start python application to consume IQ snapshots from stream and write out to files
$ python iqStreamConsumer.py

# Start python application to produce IQ shapshots from source IQ file and place on stream
$ python iqStreamProducer.py <sourceIQFile>
