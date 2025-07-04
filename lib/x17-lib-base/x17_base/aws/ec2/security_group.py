from typing import Optional, Dict, Any, List

from x17_base.aws.base.aws_resource import AwsResource

class Ec2SecurityGroup(AwsResource):
    """
    Class to manage EC2 security groups.
    
    """
    
    def __init__(
        self,
        resource_id: Optional[str] = None,
        account_id: Optional[str] = None,
        region: Optional[str] = None,
        raw: Optional[Dict[str, Any]] = None,
        log_group: Optional[Any] = None,
    ):
        super().__init__(
            resource_id=resource_id,
            account_id=account_id,
            region=region,
            raw=raw,
            log_group=log_group,
        )
        
        
        
    
    
    
        
        