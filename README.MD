# Quick Python script to generate and then destroy some AWS objects 

* VPC
* 2 Subnets 
* 2 EC2 T2.Micro instances of Amazon Linux 
* Internet Gateway


**Purpose**: train a model of user behaviour to enable anomaly detection

**Usage**: export environment variables (or use ~/.aws/credentials) 
* AWS_DEFAULT_REGION (must be us-west-1 or change the ImageId)
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

python 
 
 NB - a bunch of stuff I coped from [this](https://gist.github.com/vernhart/c6a0fc94c0aeaebe84e5cd6f3dede4ce) GitHub Gist
