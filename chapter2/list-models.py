import boto3

# 以下と同等
# aws bedrock list-foundation-models --region=us-east-1 --profile=private

session = boto3.Session(profile_name="private", region_name="us-east-1")

bedrock = session.client("bedrock")

result = bedrock.list_foundation_models()
print(result)
