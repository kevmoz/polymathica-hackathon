# Contributing to POLYMATHICA

## Code Standards

All contributions must follow the engineering standards defined in [docs/ENGINEERING_STANDARDS.md](docs/ENGINEERING_STANDARDS.md).

**The most important rule**: No placeholders, no mock data, no incomplete code.

## Workflow

1. **Fork and Branch**
   ```bash
   git clone https://github.com/YOUR_USERNAME/polymathica-hackathon
   cd polymathica-hackathon
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow the code standards
   - Add tests for all new code
   - Update documentation
   - Ensure tests pass: `pytest`

3. **Validate**
   ```bash
   # Run tests
   pytest --cov=src
   
   # Check code style
   black src/
   flake8 src/
   mypy src/
   
   # Run linter
   pylint src/
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: description of your change"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

## Pull Request Requirements

- [ ] Code follows engineering standards
- [ ] No placeholders or mock data
- [ ] Tests added and passing (>80% coverage)
- [ ] Documentation updated
- [ ] Commit messages are descriptive
- [ ] No breaking changes without migration

## Testing

All code must have tests:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_module.py

# Run with coverage
pytest --cov=src --cov-report=html
```

## Documentation

- Add docstrings to all public functions
- Update relevant markdown files
- Include examples for new features
- Keep architecture docs in sync

## Questions?

Reach out to [@kevmoz](https://github.com/kevmoz) or open an issue.
