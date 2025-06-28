# main.tf
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1" # Or your preferred AWS region that has free tier instances
}

# Data source for the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group to allow HTTP (port 80) and SSH (port 22)
resource "aws_security_group" "todo_app_sg" {
  name        = "todo_app_sg"
  description = "Allow HTTP and SSH traffic to To-Do app"

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Be careful with 0.0.0.0/0 in production. Restrict to known IPs.
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "todo-app-sg"
  }
}

# EC2 Instance for the To-Do App
resource "aws_instance" "todo_app_instance" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro" # Free tier eligible
  security_groups = [aws_security_group.todo_app_sg.name]

  # User data script to install Docker, pull image, and run container
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              chkconfig docker on
              # Allow some time for Docker service to be fully ready
              sleep 10
              # Pull the latest image (replace YOUR_DOCKER_USERNAME)
              docker pull sreej1986/devops-todo-backend:latest
              # Run the container, mapping port 80 (HTTP) to port 8000 (Flask app)
              docker run -d --restart=always -p 80:8000 sreej1986/devops-todo-backend:latest
              EOF

  tags = {
    Name = "DevOpsTodoAppInstance"
  }
}

# Output the public IP address of the instance
output "public_ip" {
  value = aws_instance.todo_app_instance.public_ip
  description = "The public IP address of the To-Do app instance."
}

output "instance_id" {
  value = aws_instance.todo_app_instance.id
  description = "The ID of the EC2 instance."
}
