# 🤝 Contributing to ShadowScan

Thank you for your interest in contributing to **ShadowScan**! We welcome contributions from the community.

## 🌟 How Can You Contribute?

- 🐛 **Report bugs** - Found a bug? [Open an issue](https://github.com/K3E9X/New-project/issues/new)
- 💡 **Suggest features** - Have an idea? [Start a discussion](https://github.com/K3E9X/New-project/discussions)
- 📝 **Improve documentation** - Help make our docs better
- 🔧 **Submit pull requests** - Fix bugs or add features
- ⭐ **Star the repo** - Show your support!

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/New-project.git
   cd New-project
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Set up the development environment**
   ```bash
   # Copy environment variables
   cp .env.example .env

   # Add your API keys to .env

   # Start with Docker
   docker-compose up -d
   ```

5. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

6. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest --cov=app

   # Frontend tests
   cd frontend
   npm run lint
   npm run type-check
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   We use [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

8. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

9. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Wait for review

## 📋 Pull Request Guidelines

- ✅ **One feature per PR** - Keep PRs focused
- ✅ **Update documentation** - If you change functionality
- ✅ **Add tests** - For new features
- ✅ **Follow code style** - Use existing patterns
- ✅ **Describe your changes** - Write a clear PR description
- ✅ **Link related issues** - Use "Fixes #123" syntax

## 🎨 Code Style

### Python (Backend)
```bash
# Format with Black
black app/

# Lint with Ruff
ruff check app/

# Type check with mypy
mypy app/
```

### TypeScript (Frontend)
```bash
# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

## 🧪 Testing

All code should be tested:

```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=html

# Frontend tests (when available)
cd frontend
npm run test
```

## 🔒 Security

- **Never commit secrets** - Use `.env` files (which are gitignored)
- **Report security issues privately** - Email security@shadowscan.dev
- **Follow security best practices** - See our [SECURITY.md](SECURITY.md)

## 📖 Documentation

- Update README.md if you add features
- Add comments for complex code
- Update API docs if you change endpoints
- Keep ARCHITECTURE.md in sync

## 💬 Community

- Be respectful and inclusive
- Help others learn and grow
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)

## 🏆 Recognition

Contributors will be added to our [Contributors](https://github.com/K3E9X/New-project/graphs/contributors) page!

## ❓ Questions?

- 💬 [GitHub Discussions](https://github.com/K3E9X/New-project/discussions)
- 🐛 [GitHub Issues](https://github.com/K3E9X/New-project/issues)
- 📧 Email: support@shadowscan.dev

---

**Thank you for contributing to ShadowScan! 🎉**
