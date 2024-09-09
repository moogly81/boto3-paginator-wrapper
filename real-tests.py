from boto3_paginator_wrapper import Boto3PaginatorWrapper


# list iam roles
iam_client = Boto3PaginatorWrapper('iam')
all_roles = iam_client.list_roles()

for role in all_roles['Roles']:
    print(role['RoleName'])

# list s3 buckets
buckets = Boto3PaginatorWrapper('s3', profile_name='pco-root_auditors').list_buckets()
for bucket in buckets['Buckets']:
    print(bucket['Name'])

# get bucket policy
bucket_policy = Boto3PaginatorWrapper('s3', profile_name='pco-root_auditors').get_bucket_policy(Bucket='tooling-pco-root')

print(bucket_policy)