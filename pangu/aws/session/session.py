from typing import Optional, Dict, Union, Any, List
from pangu.particle.log.log_stream import LogStream
from pangu.particle.log.log_group import LogGroup

import boto3



class Session:

    """
    PARAMETERS:
        access_key (string): AWS access key ID
        secret_key (string): AWS secret access key
        token (string): AWS temporary session token
        region_name (string): Default region when creating new connections
        botocore_session (botocore.session.Session): Use this Botocore session instead of creating a new default one.
        profile_name (string): The name of a profile to use. If not given, then the default profile is used.
        aws_account_id (string): AWS account ID
        
    """

    def __init__(
        self, 
        access_key=None,
        secret_key=None,
        session_token=None,
        botocore_session=None,
        aws_account_id=None,
        profile_name=None,
        region_name=None,
        log_group: Optional[LogGroup] = None,
        **kwargs: Optional[Dict[str, Any]],
    ):
        params = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "aws_session_token": session_token,
            "botocore_session": botocore_session,
            "aws_account_id": aws_account_id,
            "profile_name": profile_name,
            "region_name": region_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        self.session = boto3.Session(
            **params,
        )
        self.plugin = {}
        self.account_id = aws_account_id
        self.region_name = region_name
        
        self.class_name = self.__class__.__name__.lower()
        self.log_stream = LogStream(
            name=f"{self.class_name}:{self.region_name}:{self.account_id}",
        )
        if log_group:
            self.log_group = log_group
            self.log_stream = self.log_group.register_stream(self.log_stream)
        else:
            self.log_group = None
        
    def list_regions(
        self,
        service_name: Optional[str],
        partition_name: Optional[str] = "aws",
    ) -> list:
        return self.session.get_available_regions(
            service_name=service_name,
            partition_name=partition_name,
        )

    def list_partitions(self) -> list:
        return self.session.get_available_partitions()
    
    def list_services(self) -> list:
        return self.session.get_available_services()
    
    def get_credentials(self):
        credential = self.session.get_credentials()
        return {
            "access_key": credential.access_key,
            "secret_key": credential.secret_key,
            "token": credential.token,
        }