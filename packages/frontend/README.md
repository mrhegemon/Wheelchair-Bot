# Frontend Package

This package contains the web-based user interface for the Wheelchair Bot project.

## Features

- React-based UI
- Real-time status monitoring
- Movement controls
- Responsive design

## Development

### Setup

```bash
cd packages/frontend
npm install
```

### Running the development server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building for production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview production build

```bash
npm run preview
```

## Configuration

The frontend is configured to proxy API requests to `http://localhost:8000`. Update `vite.config.js` to change this.
