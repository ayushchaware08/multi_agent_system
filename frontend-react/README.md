# Multi-Agent Research AI - React Frontend

A modern, minimalistic React frontend for an AI-powered research assistant platform.

## Features

- 🔍 **Multi-Agent Query System** - Ask questions that are intelligently routed to specialized AI agents
- 📄 **PDF Upload & Analysis** - Upload research papers for RAG-based Q&A
- 📚 **ArXiv Search** - Search academic papers directly
- 🌐 **Web Search** - Get answers from the web when needed
- 🎨 **Modern UI** - Dark theme with smooth animations

## Tech Stack

- **React** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Query** - Server state management
- **Framer Motion** - Animations
- **Lucide Icons** - Icon library
- **React Dropzone** - File upload
- **React Markdown** - Markdown rendering

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd frontend-react

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
frontend-react/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Sidebar.jsx      # Navigation sidebar
│   │   ├── QueryInput.jsx   # Search input field
│   │   ├── FileUpload.jsx   # PDF upload component
│   │   ├── Suggestions.jsx  # Query suggestion chips
│   │   ├── AnswerCard.jsx   # Result display card
│   │   ├── AgentInfo.jsx    # Agent information display
│   │   ├── LoadingSkeleton.jsx  # Loading states
│   │   ├── ErrorMessage.jsx # Error handling
│   │   └── index.js         # Component exports
│   │
│   ├── pages/               # Page components
│   │   ├── Home.jsx         # Main page
│   │   └── index.js
│   │
│   ├── services/            # API integration
│   │   └── api.js           # Axios API client
│   │
│   ├── App.jsx              # Root component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
│
├── index.html               # HTML template
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── postcss.config.js        # PostCSS configuration
└── package.json             # Dependencies
```

## API Integration

The frontend connects to a FastAPI backend with these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check / wake backend |
| `/health` | GET | Health status |
| `/ask` | POST | Submit query to multi-agent system |
| `/upload` | POST | Upload PDF for RAG processing |
| `/logs` | GET | Get decision logs |

### Example API Usage

```javascript
import { submitQuery, uploadPDF, healthCheck } from './services/api'

// Submit a query
const result = await submitQuery('What are the latest papers on AI safety?')

// Upload a PDF
const formData = new FormData()
formData.append('file', pdfFile)
await uploadPDF(formData)

// Check backend health
const status = await healthCheck()
```

## Available Scripts

```bash
# Development
npm run dev          # Start dev server at localhost:3000

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
```

## Design System

### Colors

- **Primary**: Indigo (#6366f1)
- **Secondary**: Violet (#8b5cf6)
- **Success**: Emerald (#10b981)
- **Warning**: Amber (#f59e0b)
- **Error**: Red (#ef4444)

### Agent Colors

- **ArXiv Agent**: Blue
- **PDF RAG Agent**: Emerald
- **Web Search Agent**: Amber
- **LLM Router**: Violet

## License

MIT
