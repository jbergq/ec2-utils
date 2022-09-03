import boto3

ec2 = boto3.resource("ec2")

# Create a file to store the key locally.
outfile = open("ec2-key-pair.pem", "w")

# Call the boto ec2 function to create a key pair.
key_pair = ec2.create_key_pair(KeyName="ec2-key-pair")

# Capture the key and store it in a file.
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)
