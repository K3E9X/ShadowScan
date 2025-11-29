# ShadowScan Infrastructure - AWS
# Terraform configuration for deploying ShadowScan to AWS

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  backend "s3" {
    bucket         = "shadowscan-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "shadowscan-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ShadowScan"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# VPC Configuration
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway   = true
  enable_vpn_gateway   = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Flow Logs for security monitoring
  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project_name}-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Cluster encryption
  cluster_encryption_config = {
    resources        = ["secrets"]
    provider_key_arn = aws_kms_key.eks.arn
  }

  # Cluster endpoint configuration
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

  # OIDC Provider for IRSA
  enable_irsa = true

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      min_size     = 2
      max_size     = 10
      desired_size = 3

      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }

      taints = []

      update_config = {
        max_unavailable_percentage = 33
      }
    }

    compute = {
      min_size     = 1
      max_size     = 20
      desired_size = 2

      instance_types = ["c6i.2xlarge"]
      capacity_type  = "SPOT"

      labels = {
        role = "compute"
        workload = "analysis"
      }

      taints = [{
        key    = "workload"
        value  = "analysis"
        effect = "NoSchedule"
      }]
    }
  }
}

# RDS PostgreSQL
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.project_name}-postgres"

  engine               = "postgres"
  engine_version       = "16.1"
  family              = "postgres16"
  major_engine_version = "16"
  instance_class       = "db.t3.large"

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_encrypted     = true
  kms_key_id           = aws_kms_key.rds.arn

  db_name  = "shadowscan"
  username = "shadowscan"
  port     = 5432

  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [aws_security_group.rds.id]

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  backup_retention_period = 30
  skip_final_snapshot     = false
  deletion_protection     = true

  performance_insights_enabled    = true
  performance_insights_kms_key_id = aws_kms_key.rds.arn
}

# ElastiCache Redis
module "redis" {
  source  = "terraform-aws-modules/elasticache/aws"
  version = "~> 1.0"

  cluster_id           = "${var.project_name}-redis"
  engine              = "redis"
  engine_version      = "7.0"
  node_type           = "cache.t3.medium"
  num_cache_nodes     = 2
  parameter_group_family = "redis7"

  subnet_group_name = module.vpc.elasticache_subnet_group_name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token_enabled        = true

  automatic_failover_enabled = true
  multi_az_enabled          = true

  snapshot_retention_limit = 7
  snapshot_window         = "03:00-05:00"
}

# S3 Bucket for storage
resource "aws_s3_bucket" "storage" {
  bucket = "${var.project_name}-storage-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_versioning" "storage" {
  bucket = aws_s3_bucket.storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage" {
  bucket = aws_s3_bucket.storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "storage" {
  bucket = aws_s3_bucket.storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# KMS Keys
resource "aws_kms_key" "eks" {
  description             = "EKS Secret Encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_key" "rds" {
  description             = "RDS Encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_key" "s3" {
  description             = "S3 Encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

# Security Groups
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "redis" {
  name        = "${var.project_name}-redis-sg"
  description = "Security group for ElastiCache Redis"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {}

# Outputs
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = module.redis.configuration_endpoint_address
  sensitive   = true
}

output "s3_bucket" {
  description = "S3 storage bucket"
  value       = aws_s3_bucket.storage.id
}
