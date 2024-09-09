# Boto3 Paginator Wrapper

`boto3-paginator-wrapper` is a Python library that provides a simplified interface for handling AWS service pagination using `boto3`. This wrapper automatically or manually manages paginated results, making it easier to work with large datasets returned by AWS API operations.

## Features

- **Automatic Pagination**: Automatically combines paginated results into a single list.
- **Manual Pagination**: Provides paginators for manual control over paginated results.
- **Dynamic Operation Handling**: Automatically detects whether an operation supports pagination.

## Installation

You can install `boto3-paginator-wrapper` from PyPI using pip:

```bash
pip install boto3-paginator-wrapper
```

# boto3-paginator-wrapper


## Usage

### Initialize the Wrapper
Create an instance of the wrapper by specifying the AWS service name. Optionally, provide a profile name and region name.

```python
from boto3_paginator_wrapper import Boto3PaginatorWrapper

# Initialize the wrapper for S3
s3_wrapper = Boto3PaginatorWrapper('s3')

# Initialize the wrapper for EC2 with optional profile and region
ec2_wrapper = Boto3PaginatorWrapper('ec2', profile_name='myprofile', region_name='us-west-1')
```

### Automatic Pagination
Use the `get_resources` method to retrieve a list of resources from an AWS service operation. The wrapper will automatically handle pagination and return a single list.

```python
# Get a list of S3 buckets
buckets = s3_wrapper.get_resources('list_buckets')

# Get a list of EC2 instances
instances = ec2_wrapper.get_resources('describe_instances', Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
```

### Manual Pagination
If you need more control over pagination, use the `get_paginator` method to retrieve a paginator object. You can then manually iterate over the paginated results.

```python
# Get a paginator for S3 list_objects_v2
objects_paginator = s3_wrapper.get_paginator('list_objects_v2', Bucket='my-bucket')

# Iterate over the paginated results
for page in objects_paginator.paginate():
    for obj in page['Contents']:
        print(obj['Key'])
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull reques