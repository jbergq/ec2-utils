import argparse

import boto3

ec2 = boto3.resource("ec2")

name = "g4dn-boto3-instance"


def parse_args():
    parser = argparse.ArgumentParser()

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
                    {"Key": "Name", "Value": name},
                ],
            }
        ],
    )


if __name__ == "__main__":
    args = parse_args()
    main(args)
