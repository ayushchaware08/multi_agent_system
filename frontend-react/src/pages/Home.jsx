import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useMutation } from '@tanstack/react-query'
import { 
  Sparkles, 
  Layers, 
  Search, 
  BookOpen, 
  FileSearch, 
  Globe, 
  Brain,
  Server,
  Zap,
  Github
} from 'lucide-react'
import {
  QueryInput,
  FileUpload,
  Suggestions,
  AnswerCard,
  LoadingSkeleton,
  ErrorMessage,
} from '../components'
import { submitQuery, healthCheck } from '../services/api'

/**
 * Home page - Full page layout with agents integrated
 */
const Home = () => {
  const [currentQuery, setCurrentQuery] = useState('')
  const [results, setResults] = useState([])

  // Wake backend mutation
  const wakeMutation = useMutation({
    mutationFn: healthCheck,
    onSuccess: () => console.log('Backend is awake!'),
    onError: (error) => console.error('Failed to wake backend:', error)
  })

  // Query mutation
  const queryMutation = useMutation({
    mutationFn: submitQuery,
    onSuccess: (data) => {
      setResults((prev) => [
        { query: currentQuery, result: data, timestamp: Date.now() },
        ...prev,
      ])
    },
    onError: (error) => console.error('Query failed:', error),
  })

  const handleSubmit = useCallback((query) => {
    setCurrentQuery(query)
    queryMutation.mutate(query)
  }, [queryMutation])

  const handleSuggestionSelect = useCallback((suggestion) => {
    handleSubmit(suggestion)
  }, [handleSubmit])

  const handleRetry = useCallback(() => {
    if (currentQuery) {
      queryMutation.mutate(currentQuery)
    }
  }, [currentQuery, queryMutation])

  // Agent definitions
  const agents = [
    { name: 'Arxiv', desc: 'Academic papers', icon: BookOpen, color: 'bg-blue-100 text-blue-600' },
    { name: 'PDF RAG', desc: 'Document analysis', icon: FileSearch, color: 'bg-amber-100 text-amber-600' },
    { name: 'Web Search', desc: 'Internet search', icon: Globe, color: 'bg-green-100 text-green-600' },
    { name: 'LLM Router', desc: 'Smart routing', icon: Brain, color: 'bg-purple-100 text-purple-600' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-teal-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-surface-300 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-brand-teal to-blue-600 rounded-lg shadow-lg">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-brand-darker">Multi-Agent Research</h1>
              <p className="text-xs text-surface-500">AI-powered search system</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => wakeMutation.mutate()}
              disabled={wakeMutation.isPending}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-brand-teal to-blue-600 hover:from-brand-teal/90 hover:to-blue-600/90 rounded-lg text-sm font-semibold text-white shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
            >
              {wakeMutation.isPending ? (
                <><Server className="w-4 h-4 animate-pulse" /> Waking...</>
              ) : wakeMutation.isSuccess ? (
                <><Zap className="w-4 h-4" /> Ready</>
              ) : (
                <><Server className="w-4 h-4" /> Wake Backend</>
              )}
            </motion.button>
            
            <a
              href="https://github.com/ayushchaware08/multi_agent_system"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-surface-500 hover:text-brand-darker transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-100 to-teal-100 border border-blue-200 rounded-full mb-4 shadow-sm">
            <Layers className="w-4 h-4 text-brand-teal" />
            <span className="text-sm font-semibold text-brand-teal">Multi-Agent System</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-brand-darker via-brand-teal to-blue-600 bg-clip-text text-transparent mb-4">
            Research Smarter, Not Harder
          </h2>
          <p className="text-lg text-surface-500 max-w-2xl mx-auto">
            Ask questions, upload PDFs, and get intelligent answers from specialized AI agents
          </p>
        </motion.div>

        {/* Agents Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8"
        >
          {agents.map((agent, index) => (
            <motion.div
              key={agent.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + index * 0.05 }}
              className="bg-white/80 backdrop-blur-sm rounded-xl border border-surface-300 p-4 shadow-lg hover:shadow-xl hover:scale-105 transition-all"
            >
              <div className={`w-10 h-10 rounded-lg ${agent.color} flex items-center justify-center mb-3 shadow-sm`}>
                <agent.icon className="w-5 h-5" />
              </div>
              <h3 className="font-semibold text-brand-darker text-sm">{agent.name}</h3>
              <p className="text-xs text-surface-500">{agent.desc}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Search Section */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4 mb-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="md:col-span-4"
          >
            <FileUpload />
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="md:col-span-8"
          >
            <div className="bg-white rounded-xl border border-surface-300 p-4 shadow-card h-full">
              <QueryInput 
                onSubmit={handleSubmit} 
                isLoading={queryMutation.isPending} 
              />
            </div>
          </motion.div>
        </div>

        {/* Suggestions */}
        <Suggestions 
          onSelect={handleSuggestionSelect}
          disabled={queryMutation.isPending}
        />

        {/* Results Section */}
        <div className="space-y-4 mt-8">
          <AnimatePresence mode="popLayout">
            {queryMutation.isPending && (
              <motion.div
                key="loading"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <LoadingSkeleton />
              </motion.div>
            )}

            {queryMutation.isError && !queryMutation.isPending && (
              <motion.div
                key="error"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <ErrorMessage 
                  message={queryMutation.error?.message} 
                  onRetry={handleRetry}
                />
              </motion.div>
            )}

            {results.map((item, index) => (
              <motion.div
                key={item.timestamp}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ delay: index * 0.05 }}
              >
                <AnswerCard 
                  result={item.result} 
                  query={item.query}
                />
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Empty State */}
          {!queryMutation.isPending && !queryMutation.isError && results.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="bg-gradient-to-br from-white to-blue-50 rounded-xl border-2 border-surface-300 p-16 text-center shadow-lg"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-brand-teal to-blue-600 rounded-full mb-4 shadow-lg">
                <Search className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-brand-darker mb-2">Ready to search</h3>
              <p className="text-surface-500">
                Ask a question or upload a PDF to get started
              </p>
            </motion.div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-surface-300 bg-white/50 backdrop-blur-sm mt-16">
        <div className="max-w-6xl mx-auto px-6 py-6 text-center text-sm text-surface-500">
          Multi-Agent Research AI — Powered by intelligent agents
        </div>
      </footer>
    </div>
  )
}

export default Home
