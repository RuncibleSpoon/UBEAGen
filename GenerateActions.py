import boto3
import time

SleepTime = 300
ec2 = boto3.resource('ec2')
ec2client = ec2.meta.client

# Set some variables
def create():
    # create VPC
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "Tiddles"}])
    print("VPC Created:", vpc.vpc_id)
    print("Waiting for VPC to become avaialble")
    vpc.wait_until_available()
    # create subnets
    subnet1 = ec2.create_subnet(CidrBlock = '10.0.1.0/24', VpcId = vpc.id, AvailabilityZone = 'us-west-2a')
    subnet2 = ec2.create_subnet(CidrBlock = '10.0.2.0/24', VpcId= vpc.id,  AvailabilityZone = 'us-west-2a')
    print("Subnets ", subnet1, ", ",subnet2," created")
    # create ec2 instances
    instances = ec2.create_instances(
        ImageId = 'ami-01f08ef3e76b957e5',
        MinCount = 1,
        MaxCount = 2,
        InstanceType = 't2.micro',
        KeyName = 'AAAPANKP',
        SubnetId = subnet1.subnet_id
    )
    print("Waiting for instances to come online")
    for instance in instances:
        instance.wait_until_running()
        print("Created instance ", instance.instance_id)

    print("Created EC2 Instances")
    # create an internet gateway and attach it to VPC
    internetgateway = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)
    print("Created internet gateway")
    print("Finished Create\n")
    return(vpc.vpc_id)


def cleanup(vpcid):
    print("Beginning Cleanup")
    vpc = ec2.Vpc(vpcid)
    #detach and delete all gateways associated with the vpc
    for gw in vpc.internet_gateways.all():
        vpc.detach_internet_gateway(InternetGatewayId=gw.id)
        gw.delete()
        print("Deleted internet Gateway")
    # delete ec2 instances in vpc
    instances = ec2.instances.filter(
        Filters=[{'Name': 'vpc-id', 'Values':[vpc.vpc_id]}]
    )
    for instance in instances:
        print("Terminating instance", instance.id)
        instance.terminate()
        print("Waiting for termination")
        instance.wait_until_terminated()
        print("Terminated")

    # delete subnets
    for subnet in vpc.subnets.all():
        print("Deleting subnet ", subnet.subnet_id)
        subnet.delete()
    # delete VPC
    print("Deleteing VPC ",vpcid)
    ec2client.delete_vpc(VpcId=vpcid)



def main(argv=None):
    print("Starting")
    vpcid = create()
    print("VPC Returned=", vpcid)
    print("Sleeping to allow Prisma Cloud to detect entities")
    time.sleep(SleepTime)
    cleanup(vpcid)

if __name__ == '__main__':
     main()