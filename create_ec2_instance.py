import boto3

ec2 = boto3.resource("ec2")

# Create a new EC2 instance.
instances = ec2.create_instances(
    ImageId="ami-012ae45a4a2d92750",
    MinCount=1,
    MaxCount=1,
    InstanceType="t3.micro",
    KeyName="ec2-key-pair",
)
