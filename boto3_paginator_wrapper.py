import boto3
from botocore.exceptions import ClientError

class Boto3PaginatorWrapper:
    def __init__(self, service_name=None, profile_name=None, region_name=None):
        """
        Initialize the Boto3PaginatorWrapper with the specified AWS service.

        :param service_name: AWS service name (e.g., 's3', 'ec2') (positional argument).
        :param profile_name: AWS CLI profile to use (optional).
        :param region_name: AWS region to use (optional).
        """
        if isinstance(service_name, str):
            self.service_name = service_name
        else:
            raise ValueError("service_name must be provided as the first positional argument")
        
        session_args = {}
        if profile_name:
            session_args['profile_name'] = profile_name
        if region_name:
            session_args['region_name'] = region_name
        
        self.session = boto3.Session(**session_args)
        self.client = self.session.client(self.service_name)
        
        # Fetch supported paginators from the local boto3 service model
        self.pagination_methods = self._get_pagination_methods()

    def _get_pagination_methods(self):
        """
        Retrieves all operations that support pagination from the local boto3 service model.

        :return: List of operations that support pagination.
        """
        try:
            return self.client.meta.service_model.pagination
        except AttributeError:
            return {}

    def _call_paginated(self, operation_name, auto_paginate=False, **kwargs):
        """
        Call the specified operation with pagination support.

        :param operation_name: The AWS service method name (e.g., 'list_objects_v2').
        :param auto_paginate: If True, automatically paginate through all pages.
        :param kwargs: Arguments for the AWS operation.
        :return: The result from the operation (all pages if auto_paginate=True).
        """
        paginator = self.client.get_paginator(operation_name)
        if auto_paginate:
            result = []
            for page in paginator.paginate(**kwargs):
                for key, value in page.items():
                    if isinstance(value, list):
                        result.extend(value)
                        break
            return result
        else:
            return paginator.paginate(**kwargs)

    def _call_non_paginated(self, operation_name, **kwargs):
        """
        Call the specified operation without pagination.

        :param operation_name: The AWS service method name (e.g., 'list_objects_v2').
        :param kwargs: Arguments for the AWS operation.
        :return: The result from the operation.
        """
        operation = getattr(self.client, operation_name)
        return operation(**kwargs)

    def _call(self, operation_name, auto_paginate=False, **kwargs):
        """
        Determine whether to call a paginated or non-paginated method.

        :param operation_name: The AWS service method name (e.g., 'list_objects_v2').
        :param auto_paginate: If True, automatically paginate through all pages.
        :param kwargs: Arguments for the AWS operation.
        :return: The result from the operation.
        """
        try:
            if operation_name in self.pagination_methods:
                return self._call_paginated(operation_name, auto_paginate=auto_paginate, **kwargs)
            else:
                return self._call_non_paginated(operation_name, **kwargs)
        except ClientError as e:
            print(f"ClientError: {e}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise

    def __getattr__(self, name):
        """
        Handle dynamic method dispatch for AWS operations.

        :param name: AWS operation name.
        :return: A callable method for the specified operation.
        """
        def method(auto_paginate=False, *args, **kwargs):
            return self._call(name, auto_paginate=auto_paginate, **kwargs)
        return method
