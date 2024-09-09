import boto3
from typing import Any, Dict, List, Union

class Boto3PaginatorWrapper:
    def __init__(self, service_name: str, profile_name: str = None, region_name: str = None):
        session_args = {k: v for k, v in {'profile_name': profile_name, 'region_name': region_name}.items() if v}
        self.client = boto3.Session(**session_args).client(service_name)
        self.pagination_methods = getattr(self.client.meta.service_model, 'pagination', {})

    def _call(self, operation_name: str, auto_paginate: bool = False, **kwargs: Any) -> Union[List[Dict[str, Any]], Any]:
        if operation_name in self.pagination_methods:
            paginator = self.client.get_paginator(operation_name)
            if auto_paginate:
                result = []
                for page in paginator.paginate(**kwargs):
                    # IAM 'list_roles' response has 'Roles' key, so we extract from it
                    if 'Roles' in page:
                        result.extend(page['Roles'])
                    else:
                        result.append(page)
                return result
            return paginator.paginate(**kwargs)
        return getattr(self.client, operation_name)(**kwargs)

    def __getattr__(self, name: str) -> Any:
        return lambda auto_paginate=False, **kwargs: self._call(name, auto_paginate=auto_paginate, **kwargs)
