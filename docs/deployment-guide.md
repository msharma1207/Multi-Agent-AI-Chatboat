# Deployment Guide

## Docker

1. Build and start the stack:
   - `docker compose up --build`
2. Access the API:
   - `http://localhost:8000/docs`
3. Access the local data services:
   - PostgreSQL: `localhost:5432`
   - Redis: `localhost:6379`
   - Qdrant: `localhost:6333`

## AWS

- Use ECS or EC2 for the API service.
- Run PostgreSQL with RDS, Redis with ElastiCache, and file storage via S3.
- Place the application behind an ALB with SSL and CloudFront.
- Store secrets in AWS Secrets Manager and configure IAM roles.
