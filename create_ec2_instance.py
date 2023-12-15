import boto3
from PyInquirer import prompt


def put_cpu_alarm(instance_id):
    cloudwatch = boto3.client("cloudwatch")
    cloudwatch.put_metric_alarm(
        AlarmName=f"CPU_ALARM_{instance_id}",
        AlarmDescription="Alarm when server CPU does not exceed 10%",
        AlarmActions=["arn:aws:automate:eu-central-1:ec2:stop"],
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Statistic="Maximum",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        Period=900,
        EvaluationPeriods=3,
        Threshold=10,
        ComparisonOperator="LessThanOrEqualToThreshold",
        TreatMissingData="notBreaching",
    )


def main():
    ec2 = boto3.resource("ec2", region_name="eu-central-1")

    questions = [
        {
            "type": "input",
            "name": "instance_name",
            "message": "Instance name:",
            "default": "my_instance",
        },
        {
            "type": "list",
            "name": "ami_id",
            "message": "AMI (Amazon Machine Instance):",
            "choices": [
                {
                    "key": "ami-005b753c60d9b654c",
                    "name": "Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.1.0 (Ubuntu 20.04) 20231205",
                    "value": "ami-005b753c60d9b654c",
                }
            ],
            "default": 0,
        },
        {
            "type": "list",
            "name": "instance_type",
            "choices": ["t3.micro", "t3.medium", "g4dn.xlarge"],
            "message": "Instance type:",
            "default": "t3.micro",
        },
        {
            "type": "checkbox",
            "name": "security_groups",
            "choices": [
                {
                    "key": sg.id,
                    "name": sg.description,
                    "value": sg.id,
                }
                for sg in ec2.security_groups.all()
            ],
            "message": "Security groups:",
        },
        {
            "type": "list",
            "name": "key_pair",
            "choices": [kp.name for kp in ec2.key_pairs.all()],
            "message": "SSH key pair:",
        },
        {
            "type": "input",
            "name": "volume_size",
            "default": "50",
            "message": "Instance volume size:",
        },
    ]

    answers = prompt(questions)

    # Create a new EC2 instance.
    instances = ec2.create_instances(
        ImageId=answers["ami_id"],
        MinCount=1,
        MaxCount=1,
        InstanceType=answers["instance_type"],
        KeyName=answers["key_pair"],
        SecurityGroupIds=answers["security_groups"],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": answers["instance_name"]},
                ],
            }
        ],
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sda1",
                "Ebs": {
                    "VolumeSize": int(answers["volume_size"]),
                    "VolumeType": "standard",
                },
            }
        ],
    )

    for ec2_instance in instances:
        put_cpu_alarm(ec2_instance.id)


if __name__ == "__main__":
    main()
