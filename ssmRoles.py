from troposphere import (
    Join,
    Ref,
    Template,
    Output,
    GetAtt,
    Export
)
import troposphere.iam as iam
from cfn_flip import flip, to_yaml

t = Template()

def main():
    # Meta
    t.add_version("2010-09-09")
    t.add_description("SSM EC2 and SSM Automation roles")
    t.add_metadata({
        "Comments": "Development",
        "LastUpdated": "2017 02 16",
        "UpdatedBy": "Hamin Mousavi",
        "Version": "0.1",
    })

    # EC2 instance role
    ec2_role_for_ssm = t.add_resource(
        iam.Role(
            "AmazonEC2RoleforSSM",
            Path="/",
            AssumeRolePolicyDocument=
            {
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "ec2.amazonaws.com",
                            "ssm.amazonaws.com"
                            ]
                    },
                    "Action": ["sts:AssumeRole"]
                }
                ]
            },
            ManagedPolicyArns=[
                "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
            ],
        )
    )

    ec2_role_for_ssm_instance_profile = t.add_resource(iam.InstanceProfile(
        "InstanceProfile",
        Roles=[Ref("AmazonEC2RoleforSSM")]
    ))

    # Automation service role
    automation_service_role = t.add_resource(
        iam.Role(
            "AutomationServiceRole",
            Path="/",
            AssumeRolePolicyDocument=
            {
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "ec2.amazonaws.com",
                            "ssm.amazonaws.com"
                            ]
                    },
                    "Action": ["sts:AssumeRole", # TODO
                               "iam:PassRole"]   # Has to passrole to itself and the ec2-instance role
                                                 # http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sysman-ami-permissions.html
                }
                ]
            },
            ManagedPolicyArns=[
                "arn:aws:iam::aws:policy/service-role/AmazonSSMAutomationRole"
            ],
        )
    )

    # Maintenance window role
    maintenance_window_role = t.add_resource(
        iam.Role(
            "MaintenanceWindowRole",
            Path="/",
            AssumeRolePolicyDocument=
            {
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "ec2.amazonaws.com",
                            "ssm.amazonaws.com"
                            ]
                    },
                    "Action": ["sts:AssumeRole"]
                }
                ]
            },
            ManagedPolicyArns=[
                "arn:aws:iam::aws:policy/service-role/AmazonSSMMaintenanceWindowRole"
            ],
        )
    )


    print(to_yaml(t.to_json()))

if __name__ == '__main__':
    main()