# ChordMaker Setup Guide

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ChordMaker.git
cd ChordMaker
```

### 2. Install Dependencies

```bash
npm install
```

Or with yarn:

```bash
yarn install
```

### 3. Set Up Environment Variables

Copy the example environment file and configure it for your setup:

```bash
cp .env.example .env
```

Edit `.env` with your configuration settings.

## Development

### Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Run Tests

```bash
npm test
```

## Project Structure

- **`/src`** - Main application source code
  - `components/` - Reusable UI components
  - `pages/` - Page components
  - `utils/` - Utility functions
  - `data/` - Chord database and data files
  
- **`/docs`** - Documentation
  - `architecture.md` - System architecture
  - `api.md` - API documentation
  
- **`/tests`** - Test files
  
- **`/public`** - Static assets (images, icons, etc.)
  
- **`/data`** - Chord data in JSON format

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```
NODE_ENV=development
REACT_APP_API_URL=http://localhost:3000
REACT_APP_DEBUG=true
```

## Troubleshooting

### Common Issues

**Issue**: Dependencies fail to install
- **Solution**: Try clearing npm cache and reinstalling
  ```bash
  npm cache clean --force
  npm install
  ```

**Issue**: Development server won't start
- **Solution**: Check if port 3000 is already in use
  ```bash
  # Find and kill the process on port 3000
  netstat -ano | findstr :3000  # Windows
  lsof -i :3000                 # macOS/Linux
  ```

## Next Steps

- Read the [README.md](README.md) for project overview
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Explore the `/docs` directory for detailed documentation

## Getting Help

If you run into issues:
1. Check existing [GitHub Issues](https://github.com/yourusername/ChordMaker/issues)
2. Create a new issue with detailed information about your problem
3. Join our community discussions

---

Happy coding! 🎸
