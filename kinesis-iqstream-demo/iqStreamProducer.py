#!/usr/bin/python -u
import argparse
import boto3
import json
import math
import time
import uuid
from hashlib import sha256


stream = "kinesis-demo"
partitionKey = "shardId-000000000000"


# Parse command-line args
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Source IQ file')
parser.add_argument('-f', '--format', help='File format (default: cs16)', 
		choices=['cu8','cs8','cs16','cf32'], default='cs16')
parser.add_argument('-r', '--sample_rate', help='Sampling rate (default: 2MSPS)', 
		metavar='RATE', type=int, default=2000000)
parser.add_argument('-s', '--snapshot_size', help='IQ snapshot size (default: 100MB)', 
		metavar='BYTES', type=int, default=100*1024*1024)
parser.add_argument('-d', '--data_size', help='Kinesis max record data size (default: 1MB)', 
		metavar='BYTES', type=int, default=1024*1024)
args = parser.parse_args()


# For simplicity, assume the timestamp of first IQ sample is the current time
dataStartTime = time.time()

# Determine the IQ sample size
sampleSize = int(args.format[2:]) / 8

# Ensure the file snapshot size is an integer number of IQ samples
snapshotSize = int(args.snapshot_size / sampleSize) * sampleSize

# Create a Kinesis client
kinesis = boto3.client('kinesis')

with open(args.filename, 'rb') as f:
	while True:
		# Read a single snapshot of data (the payload)
		offset = f.tell()
		payload = f.read(snapshotSize)
		if not payload:
			break
		
		numSegments = int(math.ceil(len(payload) / float(args.data_size)))
		timestamp = dataStartTime + (float(offset) / sampleSize / args.sample_rate)
		
		# Create a message header to capture payload info
		header = json.dumps({
			'source': 'sampleStreamProducer',
			'payload': {
				'id': str(uuid.uuid4()),
				'length': len(payload),
				'segments': numSegments,
				'checksum': sha256(payload).hexdigest(),
				'meta': {
					'timestamp': timestamp,
					'sample_rate': args.sample_rate,
					'format': args.format }}})
		
		# Send payload header record
		while True:
			try:
				kinesis.put_record(StreamName=stream, Data=header, PartitionKey=partitionKey)
				print('sent %d bytes (header)' % len(header))
				break
			except kinesis.exceptions.ProvisionedThroughputExceededException:
				print('Kinesis provisioned throughput exceeded. Will try again in 20 ms.')
				time.sleep(0.02)
		
		# Limit data write rate to 1MB/sec
		time.sleep(len(header)/1024.0/1024.0)
		
		# Send segmented payload data
		for i in xrange(numSegments):
			data = payload[(i * args.data_size):(i * args.data_size + args.data_size)]
			while True:
				try:
					kinesis.put_record(StreamName=stream, Data=data, PartitionKey=partitionKey)
					print('sent %d bytes (segment %d)' % (len(data), i))
					break
				except kinesis.exceptions.ProvisionedThroughputExceededException:
					print('Kinesis provisioned throughput exceeded. Will try again in 20 ms.')
					time.sleep(0.02)
			
			# Limit data write rate to 1MB/sec
			time.sleep(len(data)/1024.0/1024.0)

