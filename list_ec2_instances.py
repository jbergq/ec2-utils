import boto3

from create_ec2_instance import REGION


def main():
    ec2 = boto3.resource("ec2", region_name=REGION)

    # Get information for all running instances
    running_instances = ec2.instances.filter(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    if len(list(running_instances)) == 0:
        print("No instances active.")
        exit(0)

    print("Instances:\n")

    for instance in running_instances:
        print("-" * 30)

        name = "-"

        if instance.tags is not None:
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    name = tag["Value"]

        instance_info = {
            "Name": name,
            "Type": instance.instance_type,
            "State": instance.state["Name"],
            "Private IP": instance.private_ip_address,
            "Public IP": instance.public_ip_address,
            "Launch Time": instance.launch_time,
            "Public DNS Name": instance.public_dns_name,
        }

        for attr, instance_value in instance_info.items():
            print(f"{attr}: {instance_value}")
        print(f"SSH command: ssh ubuntu@{instance.public_dns_name}")


if __name__ == "__main__":
    main()
