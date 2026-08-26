# AWS Certified Developer - Associate (DVA-C02) — Compressed Guide

Source: AWS official Exam Guide (DVA-C02), version 2.1 (Dec 12, 2024).
Format: 65 questions (50 scored + 15 unscored), 130 min, pass 720/1000.
Question types: multiple choice (1 correct of 4), multiple response (2+ correct of 5+).

## Content domains and weightings

| # | Domain | Weight |
|---|--------|--------|
| 1 | Development with AWS Services | 32% |
| 2 | Security | 26% |
| 3 | Deployment | 24% |
| 4 | Troubleshooting and Optimization | 18% |

## Domain 1: Development with AWS Services

### Task 1.1: Develop code for applications hosted on AWS
- 1.1.1 Architectural patterns (event-driven, microservices, monolithic, choreography, orchestration, fanout)
- 1.1.2 Stateful vs stateless
- 1.1.3 Tightly vs loosely coupled components
- 1.1.4 Synchronous vs asynchronous patterns
- 1.1.5 Fault-tolerant and resilient apps (Java, C#, Python, JavaScript, TypeScript, Go)
- 1.1.6 Create/extend/maintain APIs (request/response transforms, validation, status codes)
- 1.1.7 Unit tests in dev environments (AWS SAM)
- 1.1.8 Use messaging services
- 1.1.9 Interact with AWS services via APIs and SDKs
- 1.1.10 Handle streaming data
- 1.1.11 Amazon Q Developer for dev assistance
- 1.1.12 Event-driven patterns with Amazon EventBridge
- 1.1.13 Resilient third-party integrations (retry logic, circuit breakers, error handling)

### Task 1.2: Develop code for AWS Lambda
- 1.2.1 Private resource access in VPCs from Lambda
- 1.2.2 Configure Lambda (memory, concurrency, timeout, runtime, handler, layers, extensions, triggers, destinations)
- 1.2.3 Event lifecycle and errors (Lambda Destinations, dead-letter queues)
- 1.2.4 Test code using AWS services and tools
- 1.2.5 Integrate Lambda with AWS services
- 1.2.6 Tune Lambda for performance
- 1.2.7 Lambda for near real-time data processing

### Task 1.3: Use data stores in application development
- 1.3.1 High-cardinality partition keys for balanced access
- 1.3.2 Consistency models (strongly vs eventually consistent)
- 1.3.3 Query vs scan operations
- 1.3.4 Amazon DynamoDB keys and indexing
- 1.3.5 Serialize/deserialize data
- 1.3.6 Use, manage, maintain data stores
- 1.3.7 Manage data lifecycles
- 1.3.8 Data caching services
- 1.3.9 Specialized data stores by access pattern (Amazon OpenSearch Service)

## Domain 2: Security

### Task 2.1: Authentication and authorization
- 2.1.1 Identity provider for federated access (Amazon Cognito, IAM)
- 2.1.2 Bearer tokens
- 2.1.3 Programmatic access to AWS
- 2.1.4 Authenticated calls to AWS services
- 2.1.5 Assume an IAM role
- 2.1.6 Permissions for IAM principals
- 2.1.7 Application-level authorization for fine-grained access
- 2.1.8 Cross-service authentication in microservices

### Task 2.2: Encryption
- 2.2.1 Encryption at rest and in transit
- 2.2.2 Certificate management (AWS Private CA)
- 2.2.3 Client-side vs server-side encryption
- 2.2.4 Use encryption keys to encrypt/decrypt data
- 2.2.5 Generate certificates and SSH keys for dev
- 2.2.6 Encryption across account boundaries
- 2.2.7 Enable/disable key rotation

### Task 2.3: Manage sensitive data in application code
- 2.3.1 Data classification (PII, PHI)
- 2.3.2 Encrypt env vars containing sensitive data
- 2.3.3 Secret management services
- 2.3.4 Sanitize sensitive data
- 2.3.5 Application-level data masking and sanitization
- 2.3.6 Data access patterns for multi-tenant apps

## Domain 3: Deployment

### Task 3.1: Prepare application artifacts
- 3.1.1 Manage dependencies (env vars, config files, container images)
- 3.1.2 Organize files and directory structure
- 3.1.3 Code repositories in dev environments
- 3.1.4 Application resource requirements (memory, cores)
- 3.1.5 Prepare app configs for specific environments (AWS AppConfig)

### Task 3.2: Test applications in dev environments
- 3.2.1 Test deployed code using AWS services/tools
- 3.2.2 Integration tests and mock APIs for external dependencies
- 3.2.3 Test using dev endpoints (API Gateway stages)
- 3.2.4 Deploy app stack updates (AWS SAM template to a different staging environment)
- 3.2.5 Test event-driven applications

### Task 3.3: Automate deployment testing
- 3.3.1 App test events (JSON payloads for Lambda, API Gateway, SAM)
- 3.3.2 Deploy API resources to various environments
- 3.3.3 App environments with approved versions (Lambda aliases, container image tags, Amplify branches, Copilot environments)
- 3.3.4 IaC templates (AWS SAM, CloudFormation)
- 3.3.5 Manage environments in individual AWS services (API Gateway stages: dev/test/prod)
- 3.3.6 Amazon Q Developer to generate automated tests

### Task 3.4: Deploy code using CI/CD services
- 3.4.1 Lambda deployment packaging options
- 3.4.2 API Gateway stages and custom domains
- 3.4.3 Update existing IaC templates (SAM, CloudFormation)
- 3.4.4 Manage app environments using AWS services
- 3.4.5 Deploy app version using deployment strategies
- 3.4.6 Commit code to invoke build/test/deploy actions
- 3.4.7 Orchestrated workflows across environments
- 3.4.8 App rollbacks using existing deployment strategies
- 3.4.9 Labels and branches for version/release management
- 3.4.10 Runtime configs for dynamic deployments (API Gateway staging variables in Lambda)
- 3.4.11 Deployment strategies (blue/green, canary, rolling)

## Domain 4: Troubleshooting and Optimization

### Task 4.1: Root cause analysis
- 4.1.1 Debug code to identify defects
- 4.1.2 Interpret metrics, logs, traces
- 4.1.3 Query logs to find relevant data
- 4.1.4 Custom metrics (CloudWatch Embedded Metric Format / EMF)
- 4.1.5 Review app health via dashboards and insights
- 4.1.6 Troubleshoot deployment failures via service output logs
- 4.1.7 Debug service integration issues

### Task 4.2: Instrument code for observability
- 4.2.1 Logging vs monitoring vs observability
- 4.2.2 Effective logging strategy
- 4.2.3 Emit custom metrics from code
- 4.2.4 Annotations for tracing services
- 4.2.5 Notification alerts (quota limits, deployment completions)
- 4.2.6 Tracing using AWS services/tools
- 4.2.7 Structured logging for events and user actions
- 4.2.8 Health checks and readiness probes

### Task 4.3: Optimize applications
- 4.3.1 Define concurrency
- 4.3.2 Profile app performance
- 4.3.3 Minimum memory/compute for an app
- 4.3.4 Subscription filter policies to optimize messaging
- 4.3.5 Cache content based on request headers
- 4.3.6 Application-level caching
- 4.3.7 Optimize app resource usage
- 4.3.8 Analyze app performance issues
- 4.3.9 Use app logs to identify performance bottlenecks

## Emerging topics (may appear as unscored pretest questions)
- AI-assisted dev tools (spec-driven code gen, automated reviews, intelligent completion, refactoring, security scanning)
- Security risks with AI integration (data privacy, access management, model input/output controls, agent security, log scrubbing)
- AWS AI tools for test generation and automation
- AWS AI tools for CI/CD (deployment approvals, environment provisioning, post-deployment validation)
- AWS AI tools for error analysis and troubleshooting suggestions
- AWS AI tools for optimization (bottleneck detection, resource optimization, code efficiency)

## In-scope AWS services

**Analytics:** Athena, Kinesis, OpenSearch Service
**Application Integration:** AppSync, EventBridge, SNS, SQS, Step Functions
**Compute:** EC2, Elastic Beanstalk, Lambda
**Containers:** ECR, ECS, EKS
**Database:** Aurora, DynamoDB, ElastiCache, RDS
**Developer Tools:** Amplify, CloudShell, CodeArtifact, CodeBuild, CodeDeploy, CodePipeline, X-Ray, Amazon Q Developer
**Management & Governance:** AppConfig, CDK, CloudFormation, CloudTrail, CloudWatch, CLI, Systems Manager
**Networking & Content Delivery:** API Gateway, CloudFront, ELB, Route 53, VPC
**Security, Identity, Compliance:** Cognito, IAM, KMS, Secrets Manager, STS, WAF
**Storage:** EBS, EFS, S3
