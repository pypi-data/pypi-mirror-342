import copy
import random
import string
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import boto3
from functools import lru_cache
from typing import List, Dict
import os

# Load environment variables once at startup
load_dotenv()

def generate_random_string(length=5):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

# Initialize FastMCP
mcp = FastMCP("Amazon Web Services Elastic Beanstalk Utility")

# Create a single reusable client
eb_client = boto3.client(
    "elasticbeanstalk",
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
)

@mcp.tool()
def aws_elasticBeanstalk_applications() -> List[Dict]:
    """
    Get the Elastic Beanstalk Applications and List them
    
    Returns:
        List[Dict]: List of Elastic Beanstalk Applications
    """
    response = eb_client.describe_applications()
    return response["Applications"]

@mcp.tool()
def aws_elasticBeanstalk_application(application_name: str) -> Dict:
    """
    Get the Elastic Beanstalk Application and Describe it

    Args:
        application_name (str): Name of the Elastic Beanstalk Application
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.describe_applications(
        ApplicationNames=[application_name]
    )
    return response["Applications"][0]

@mcp.tool()
def aws_elasticBeanstalk_environments(app_name: str) -> List[Dict]:
    """
    Get the Elastic Beanstalk Environments of an Application and List them

    Returns:
        List[Dict]: List of Elastic Beanstalk Environments
    """
    response = eb_client.describe_environments(ApplicationName=app_name)
    return response["Environments"]

@mcp.tool()
def aws_elasticBeanstalk_environment_describe(environment_name: str) -> Dict:
    """
    Get the Elastic Beanstalk Environment and Describe it

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.describe_environments(
        EnvironmentNames=[environment_name]
    )
    return response["Environments"][0]

@mcp.tool()
def aws_elasticBeanstalk_environment_restart(environment_name: str) -> Dict:
    """
    Restart the Elastic Beanstalk Environment

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.restart_app_server(
        EnvironmentName=environment_name
    )
    return response

@mcp.tool()
def aws_elasticBeanstalk_environment_clone(app_name: str, environment_name: str) -> Dict:
    """
    Clone the Elastic Beanstalk Environment

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """

    current_env_response = eb_client.describe_configuration_settings(
        EnvironmentName=environment_name,
        ApplicationName=app_name
    )

    option_settings = current_env_response["ConfigurationSettings"][0]
    filtered_settings = [option for option in option_settings["OptionSettings"] if "Value" in option]


    response = eb_client.create_environment(
        ApplicationName= current_env_response['ConfigurationSettings'][0]['ApplicationName'],
        EnvironmentName= current_env_response['ConfigurationSettings'][0]['EnvironmentName'] + '-clone-' + generate_random_string(),
        SolutionStackName= current_env_response['ConfigurationSettings'][0]['SolutionStackName'],
        OptionSettings=filtered_settings
    )

    return response

@mcp.tool()
def aws_elasticBeanstalk_environment_swap(source_environment_name: str, destination_environment_name: str) -> Dict:
    """
    Swap the Elastic Beanstalk Environment

    Args:
        source_environment_name (str): Name of the source Elastic Beanstalk Environment
        destination_environment_name (str): Name of the destination Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.swap_environment_cnames(
        SourceEnvironmentName=source_environment_name,
        DestinationEnvironmentName=destination_environment_name
    )
    return response

@mcp.tool()
def aws_elasticBeanstalk_environment_delete(environment_name: str) -> Dict:
    """
    Delete the Elastic Beanstalk Environment

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.terminate_environment(
        EnvironmentName=environment_name
    )
    return response

@mcp.tool()
def aws_elasticBeanstalk_environment_health(environment_name: str) -> Dict:
    """
    Get the Elastic Beanstalk Environment Health

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.describe_environment_health(
        EnvironmentName=environment_name
    )
    return response

@mcp.tool()
def aws_elasticBeanstalk_environment_resources(environment_name: str) -> Dict:
    """
    Get the Elastic Beanstalk Environment Resources

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.describe_environment_resources(
        EnvironmentName=environment_name
    )
    return response

@mcp.tool()
def aws_elasticBeanstalk_environment_instance(environment_name: str) -> Dict:
    """
    Get the Elastic Beanstalk Environment Instance

    Args:
        environment_name (str): Name of the Elastic Beanstalk Environment
    Returns:
        Dict: Response from the Elastic Beanstalk API
    """
    response = eb_client.describe_instances_health(
        EnvironmentName=environment_name,
        AttributeNames=[
            'HealthStatus',
            'InstanceType'
        ]
    )
    return response

if __name__ == "__main__":
    mcp.run(transport='stdio')
