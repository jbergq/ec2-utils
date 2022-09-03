import boto3

ec2 = boto3.resource("ec2")

name = "test-boto3-instance"

# Create a new EC2 instance.
instances = ec2.create_instances(
    ImageId="ami-0b1b702a76781d077",
    MinCount=1,
    MaxCount=1,
    InstanceType="t3.micro",
    KeyName="ec2-key-pair",
    SecurityGroupIds=["sg-09b92788c9f34f587"],
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [
                {"Key": "Name", "Value": name},
            ],
        }
    ],
)
