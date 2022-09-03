key-pair:
	python create_key_pair.py && chmod 400 .ssh/ec2-key-pair.pem
ec2-create:
	python create_ec2_instance.py
ec2-list:
	python list_ec2_instances.py
# ec2-connect:
