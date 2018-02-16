# Compatability check
# Make sure your versions of Java (8), Scala (2.10), Spark (2.11), AWS SDK are all compatible

# Set up AWS-cli
https://docs.aws.amazon.com/cli/latest/userguide/installing.html

# Write python module to generate Data (using code sample processInfo.py)

# Create default roles (necessary to create EMR cluster)
$ aws emr create-default-roles

# AWS-cli commands using cheapest configuration (need to change KeyName)
$ aws kinesis create-stream --stream-name kinesis-demo --shard-count 1
aws emr create-cluster --applications Name=Ganglia Name=Spark Name=Zeppelin --ec2-attributes '{"KeyName":"dean-ssh","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-dbb1e7bf","EmrManagedSlaveSecurityGroup":"sg-98657cec","EmrManagedMasterSecurityGroup":"sg-62110816"}' --service-role EMR_DefaultRole --enable-debugging --release-label emr-5.11.1 --name 'My cluster' --instance-groups '[{"InstanceCount":2,"InstanceGroupType":"CORE","InstanceType":"m1.medium","Name":"Core Instance Group"},{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m1.medium","Name":"Master Instance Group"}]' --configurations '[{"Classification":"spark","Properties":{"maximizeResourceAllocation":"true"},"Configurations":[]}]' --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region us-east-1

# Set up S3 bucket
$ aws s3api create-bucket --bucket kinesis-spark-bucket --region us-east-1

# Start python application to send random data to stream 
$ python simpleProducer.py

# Copy application files to EMR master node
scp -i <path/to/ec2-ssh.pem> <path/to/files> hadoop@<ip-of-masternode>:

# Log onto master server and install Boto3, an AWS SDK
$ ssh -i <path/to/ec2-ssh.pem> hadoop@<ip-of-masternode>
$ sudo pip install boto3

# Run a Python application on a Spark standalone cluster
# $ spark-submit --jars spark-streaming_2.11-2.2.1.jar --master local processInfo.py 1000

# OR Run a Python application on a AWS EMR cluster
$ spark-submit --deploy-mode cluster --master yarn --num-executors 5 --executor-cores 5 --executor-memory 20g –conf spark.yarn.submit.waitAppCompletion=false wordcount.py s3://inputbucket/input.txt s3://outputbucket/
