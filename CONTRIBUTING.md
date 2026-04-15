# Contributing to ChordMaker

Thank you for your interest in contributing to ChordMaker! We welcome contributions from the community. This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and inclusive. We're committed to providing a welcoming and inspiring community for all.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/ChordMaker/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Node version, browser, etc.)

### Suggesting Features

1. Check [Issues](https://github.com/yourusername/ChordMaker/issues) for similar suggestions
2. Create a new issue with:
   - Clear, descriptive title
   - Detailed feature description
   - Use cases and benefits
   - Possible implementation approaches (optional)

### Code Contributions

1. **Fork** the repository
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/chord-diagram-improvement
   ```
3. **Make your changes** following code standards
4. **Write tests** for new functionality
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add: Interactive chord diagram improvements"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/chord-diagram-improvement
   ```
7. **Create a Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/demos if UI changes

## Code Standards

### Style Guide

- Use consistent indentation (2 spaces)
- Follow ESLint configuration in the project
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Commit Messages

```
[Type]: Brief description

- Detail 1
- Detail 2
```

Types: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`

Example:
```
Fix: Chord diagram rendering on mobile devices

- Fixed responsive layout issues
- Improved touch interaction
- Updated media queries
```

## Development Workflow

1. **Install dependencies**: `npm install`
2. **Start dev server**: `npm run dev`
3. **Run tests**: `npm test`
4. **Build**: `npm run build`
5. **Lint**: `npm run lint`

## Testing

- Write unit tests for new features
- Ensure all tests pass: `npm test`
- Maintain or improve code coverage

## Documentation

- Update README.md if adding new features
- Add inline code comments for complex logic
- Update relevant docs in `/docs` folder
- Include usage examples

## Pull Request Process

1. Update documentation and tests
2. Ensure all tests pass locally
3. Rebase on latest `main` branch
4. Create descriptive PR with screenshots if applicable
5. Address feedback from reviewers
6. Maintainers will merge when approved

## Areas for Contribution

- 🎸 New chord variations and fingerings
- 🎯 Improved chord diagram UI/UX
- 🌍 Translations and localization
- 📱 Mobile responsiveness
- 🐛 Bug fixes
- 📚 Documentation
- ✨ New features and improvements

## Questions?

- Open an issue with tag `question`
- Check existing discussions
- Comment on related issues

---

Thank you for making ChordMaker better! 🎸
