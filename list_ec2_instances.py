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

    ec2info = {}
    for instance in running_instances:
        name = "-"

        if instance.tags is not None:
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    name = tag["Value"]

        # Add instance info to a dictionary
        instance_info = {
            "Name": name,
            "Type": instance.instance_type,
            "State": instance.state["Name"],
            "Private IP": instance.private_ip_address,
            "Public IP": instance.public_ip_address,
            "Launch Time": instance.launch_time,
            "Public DNS Name": instance.public_dns_name,
        }

        ec2info[instance.id] = instance_info

        for attr, instance_value in instance_info.items():
            print("{0}: {1}".format(attr, instance_value))

        print(f"\nSSH command: \nssh ubuntu@{instance.public_dns_name}")
        print("------")


if __name__ == "__main__":
    main()
