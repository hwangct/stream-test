# Set up AWS-cli
https://docs.aws.amazon.com/cli/latest/userguide/installing.html

# Write python module to generate Data (using code sample processInfo.py)

# Create default roles (necessary to create EMR cluster)
$ aws emr create-default-roles

# AWS-cli commands using cheapest configuration (need to change KeyName)
$ aws kinesis create-stream --stream-name kinesis-spark-demo --shard-count 1
$ aws emr create-cluster --applications Name=Ganglia Name=Hadoop Name=Hive Name=Hue Name=Mahout Name=Pig Name=Tez --ec2-attributes '{"KeyName":"ec2-ssh","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-97b6eedc","EmrManagedSlaveSecurityGroup":"sg-98657cec","EmrManagedMasterSecurityGroup":"sg-62110816"}' --service-role EMR_DefaultRole --enable-debugging --release-label emr-5.11.1 --log-uri 's3n://aws-logs-708241547068-us-east-1/elasticmapreduce/' --name 'My cluster' --instance-groups '[{"InstanceCount":2,"InstanceGroupType":"CORE","InstanceType":"m1.medium","Name":"Core Instance Group"},{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m1.medium","Name":"Master Instance Group"}]' --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region us-east-1

# Set up S3 bucket
$ aws s3api create-bucket --bucket kinesis-spark-bucket --region us-east-1

# Start python application to send random data to stream 
$ python generateRandom.py

# Copy application files to EMR master node
scp -i <path/to/ec2-ssh.pem> <path/to/files> hadoop@<ip-of-masternode>:

# Log onto master server and install Boto3, an AWS SDK
$ ssh -i <path/to/ec2-ssh.pem> hadoop@<ip-of-masternode>
$ sudo pip install boto3

# Run a Python application on a Spark standalone cluster.  Not sure if the packages are already in the classpath on the EMR cluster.
# https://spark.apache.org/docs/latest/submitting-applications.html
$ spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl:2.2.1 --master local processInfo.py 1000
