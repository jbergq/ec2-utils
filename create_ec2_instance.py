import argparse

import boto3


def put_cpu_alarm(instance_id):
    cloudwatch = boto3.client("cloudwatch")
    cloudwatch.put_metric_alarm(
        AlarmName=f"CPU_ALARM_{instance_id}",
        AlarmDescription="Alarm when server CPU does not exceed 10%",
        AlarmActions=["arn:aws:automate:eu-north-1:ec2:stop"],
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Statistic="Average",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        Period=900,
        EvaluationPeriods=3,
        Threshold=10,
        ComparisonOperator="LessThanOrEqualToThreshold",
        TreatMissingData="notBreaching",
    )


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", help="The name of the instance.", required=True)
    parser.add_argument(
        "-t",
        "--type",
        default="t3.micro",
        help="The type of instance you want to create. Use 't3.micro' "
        + "for a normal CPU instance and 'g4dn.xlarge' for a GPU instance.",
        choices=["t3.micro", "g4dn.xlarge"],
    )

    return parser.parse_args()


def main(args):
    ec2 = boto3.resource("ec2")

    # Create a new EC2 instance.
    instances = ec2.create_instances(
        ImageId="ami-0b1b702a76781d077",
        MinCount=1,
        MaxCount=1,
        InstanceType=args.type,
        KeyName="ec2-key-pair",
        SecurityGroupIds=["sg-09b92788c9f34f587"],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": args.name},
                ],
            }
        ],
    )

    for ec2_instance in instances:
        put_cpu_alarm(ec2_instance.id)


if __name__ == "__main__":
    args = parse_args()
    main(args)
