key-pair:
	python create_key_pair.py && chmod 400 ec2-key-pair.pem
ec2-create:
	python create_ec2_instance.py
