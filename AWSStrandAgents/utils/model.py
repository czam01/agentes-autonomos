import boto3
from strands.models import BedrockModel

class ModelSelector:
    def __init__(self, model):
        self.model = model
        self.session = boto3.Session(
                region_name='us-east-1',
                profile_name='ccamp' 
            )

    def get_model(self):
        if self.model == 'Sonnet3.7':
            

            # Create a Bedrock model with the custom session
            bedrock_model = BedrockModel(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                boto_session=self.session,
            )

            return bedrock_model
        elif self.model == 'AmazonNovaPro':
            # Create a Bedrock model with the custom session
            bedrock_model = BedrockModel(
                model_id="amazon.nova-pro-v1:0",
                boto_session=self.session,
            )
            return bedrock_model
            
