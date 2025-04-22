from pangu.aws.session import Session


session = Session(
    access_key="AKIA3BIBAYW7B7HGRVOA",
    secret_key="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",
    #aws_session_token="",
    aws_account_id="758600746430",
    region_name="ap-southeast-2",
    #profile_name="default",
)

print(session.list_regions(service_name="s3"))
print(session.get_credentials())