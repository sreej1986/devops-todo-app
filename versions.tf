# versions.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  # Configure Terraform Cloud as the backend for state management
  cloud {
    organization = "your-github-sreej1986-devops" # Replace with your Terraform Cloud organization name
    workspace    = "todo-app-infra" # Match the workspace name you created
  }
}
