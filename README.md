# SecuVision - AI-Powered Security Analysis Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI/CD](https://github.com/secuvision/secuvision/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/secuvision/secuvision/actions)
[![Security Rating](https://img.shields.io/badge/security-A+-green.svg)](https://secuvision.dev)

**SecuVision** is a production-grade, AI-powered security analysis platform that provides comprehensive code security analysis and architecture diagram assessment using state-of-the-art AI models and security frameworks.

## 🚀 Features

### Code Security Analysis
- **Multi-Language Support**: Analyze code in Python, JavaScript, TypeScript, Java, Go, Rust, C/C++, PHP, Ruby, and more
- **Comprehensive Detection**:
  - OWASP Top 10 2025 vulnerabilities
  - CWE Top 25 2025 weaknesses
  - Secrets and credentials detection
  - Dependency vulnerabilities
  - Supply chain security risks
  - Business logic flaws
- **AI-Powered Insights**: Advanced analysis using Claude 3.5 Sonnet / GPT-4 Turbo
- **Secure Code Generation**: Automatic generation of secure code alternatives
- **Compliance Checking**: ISO 27001:2022, PCI DSS, HIPAA, GDPR alignment

### Architecture Diagram Analysis
- **Visual Analysis**: Upload PNG, JPG, or SVG architecture diagrams
- **Component Identification**: Automatic detection of infrastructure components
- **Security Assessment**: Comprehensive evaluation of architecture security posture
- **Zero Trust Recommendations**: Detailed proposals for implementing Zero Trust architecture
- **Secure-by-Design Guidance**: Actionable recommendations for security hardening
- **Compliance Gaps**: Identification of compliance issues with major frameworks

## 🏗️ Architecture

SecuVision follows a microservices architecture built on modern, secure, and scalable technologies:

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Next.js   │─────▶│   FastAPI    │─────▶│  AI Models  │
│  Frontend   │      │   Backend    │      │   (Claude)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                ┌────▼────┐   ┌───▼────┐
                │PostgreSQL│   │ Redis  │
                └──────────┘   └────────┘
```

**Technology Stack:**
- **Frontend**: Next.js 15, React Server Components, Tailwind CSS, TypeScript
- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL 16, Redis 7
- **AI**: Claude 3.5 Sonnet, GPT-4 Turbo (configurable)
- **Infrastructure**: Docker, Kubernetes, Terraform, AWS
- **CI/CD**: GitHub Actions, automated security scanning

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 📋 Prerequisites

- **Docker** 24+ and Docker Compose
- **Node.js** 20+
- **Python** 3.12+
- **AI API Keys**: Anthropic (Claude) or OpenAI (GPT-4)
- **Kubernetes** 1.28+ (for production deployment)
- **Terraform** 1.6+ (for cloud infrastructure)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secuvision.git
cd secuvision
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# AI API Keys (at least one required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=postgresql+asyncpg://secuvision:secuvision_password@postgres:5432/secuvision

# Redis
REDIS_URL=redis://:secuvision_redis_password@redis:6379/0

# Security
SECRET_KEY=your-super-secret-key-at-least-32-characters-long

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- Frontend on http://localhost:3000
- Backend API on http://localhost:8000
- PostgreSQL on localhost:5432
- Redis on localhost:6379
- NGINX reverse proxy on http://localhost

### 4. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/docs
- **API Health**: http://localhost:8000/health

## 🔧 Development Setup

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000 with hot reload.

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with auto-reload.

## 📝 Usage Examples

### Code Analysis via API

```bash
curl -X POST http://localhost:8000/api/v1/analyze/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SELECT * FROM users WHERE id = ' + user_id",
    "language": "python",
    "filename": "app.py"
  }'
```

### Diagram Analysis via API

```bash
curl -X POST http://localhost:8000/api/v1/analyze/diagram \
  -F "file=@architecture.png"
```

### Using the Web Interface

1. Navigate to http://localhost:3000
2. Click **"Start Analysis"**
3. Choose **Code Analysis** or **Diagram Analysis**
4. Paste code or upload a diagram
5. Click **"Analyze"** and wait for results
6. Review vulnerabilities, recommendations, and secure code examples

## 🔒 Security Features

### Application Security
- ✅ **Input Validation**: Pydantic v2 schemas with strict validation
- ✅ **Anti-SSRF Protection**: Prevents server-side request forgery
- ✅ **Rate Limiting**: 100 req/min per IP, 10 analyses/hour per user
- ✅ **SQL Injection Prevention**: ORM-based queries only
- ✅ **XSS Protection**: React automatic escaping + CSP headers
- ✅ **CSRF Protection**: Token-based validation
- ✅ **Secure Headers**: HSTS, X-Frame-Options, CSP, etc.
- ✅ **Secrets Management**: Environment variables + Kubernetes secrets

### Infrastructure Security
- ✅ **Container Security**: Non-root users, read-only filesystems
- ✅ **Network Policies**: Zero Trust network segmentation
- ✅ **Encryption**: TLS 1.3 in transit, AES-256 at rest
- ✅ **Pod Security**: Restricted PSS, AppArmor profiles
- ✅ **RBAC**: Least privilege access control
- ✅ **Audit Logging**: Comprehensive security event logging

## 🧪 Testing

### Run All Tests

```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test
npm run test:e2e
```

### Security Scanning

```bash
# Run Semgrep
semgrep --config=auto .

# Run Bandit (Python)
cd backend
bandit -r app/

# Run Trivy (containers)
trivy image secuvision/backend:latest
```

## 🚀 Production Deployment

### Kubernetes Deployment

```bash
# Create namespace
kubectl apply -f infrastructure/kubernetes/namespace.yaml

# Create secrets (update with your values)
kubectl create secret generic secuvision-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=redis-url='redis://...' \
  --from-literal=secret-key='...' \
  --from-literal=anthropic-api-key='...' \
  -n secuvision-prod

# Deploy application
kubectl apply -f infrastructure/kubernetes/ -n secuvision-prod

# Verify deployment
kubectl get pods -n secuvision-prod
kubectl get svc -n secuvision-prod
```

### Terraform Deployment (AWS)

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Plan infrastructure
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan

# Get outputs
terraform output
```

## 📊 Monitoring & Observability

### Metrics
- **Prometheus**: Metrics collection on `/metrics`
- **Grafana**: Dashboards for visualization
- **Application Metrics**: Request rates, latency, error rates
- **Business Metrics**: Analysis counts, vulnerability detection rates

### Logging
- **Structured Logging**: JSON format with correlation IDs
- **ELK Stack**: Centralized log aggregation
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Audit Logs**: Security-relevant events

### Tracing
- **Distributed Tracing**: Jaeger integration
- **Request Tracing**: End-to-end request flow
- **Performance Profiling**: Identify bottlenecks

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- **Python**: Black formatting, Ruff linting, type hints with mypy
- **TypeScript**: ESLint, Prettier, strict TypeScript
- **Commits**: Conventional Commits format
- **Tests**: Minimum 80% code coverage

## 📚 Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - System architecture and design decisions
- [API Documentation](http://localhost:8000/api/docs) - Interactive API documentation
- [Security Guide](docs/SECURITY.md) - Security best practices and threat model
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [AI Prompts](backend/app/services/prompts.py) - AI analysis prompts

## 🔐 Security & Compliance

### Standards Implemented
- ✅ OWASP Top 10 2025
- ✅ CWE Top 25 2025
- ✅ NIST 800-218 SSDF
- ✅ ISO 27001:2022
- ✅ NIS2 Directive
- ✅ CIS Benchmarks
- ✅ GDPR Compliance

### Vulnerability Disclosure

If you discover a security vulnerability, please email security@secuvision.dev. Do not open public issues for security vulnerabilities.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude AI models
- **OpenAI** for GPT-4 models
- **OWASP** for security frameworks
- **MITRE** for CWE database
- **NIST** for cybersecurity guidelines

## 📞 Support

- **Documentation**: [https://docs.secuvision.dev](https://docs.secuvision.dev)
- **Email**: support@secuvision.dev
- **Issues**: [GitHub Issues](https://github.com/yourusername/secuvision/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/secuvision/discussions)

---

**Built with ❤️ for the security community**

*SecuVision - Securing your code and infrastructure with AI intelligence*
