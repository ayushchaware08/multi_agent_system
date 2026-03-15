import { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Send, Loader2 } from 'lucide-react'

/**
 * Query input component for submitting research questions
 * @param {Object} props
 * @param {function} props.onSubmit - Callback when query is submitted
 * @param {boolean} props.isLoading - Whether a query is in progress
 */
const QueryInput = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (query.trim() && !isLoading) {
      onSubmit(query.trim())
    }
  }

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="h-full flex flex-col justify-center">
      <div className="relative">
        <div className="absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none">
          <Search className="w-5 h-5 text-surface-400" />
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a research question..."
          disabled={isLoading}
          className="w-full bg-white border-2 border-surface-300 rounded-xl pl-12 pr-14 py-4 text-brand-darker text-lg font-medium placeholder:text-surface-400 focus:outline-none focus:border-brand-teal focus:ring-4 focus:ring-brand-teal/10 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md"
        />

        <motion.button
          type="submit"
          disabled={!query.trim() || isLoading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 rounded-lg bg-gradient-to-r from-brand-teal to-blue-600 hover:from-brand-teal/90 hover:to-blue-600/90 disabled:bg-surface-300 disabled:cursor-not-allowed transition-all shadow-lg"
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 text-white animate-spin" />
          ) : (
            <Send className="w-5 h-5 text-white" />
          )}
        </motion.button>
      </div>

      <p className="text-xs text-surface-400 mt-2 text-center">
        Press <kbd className="px-1.5 py-0.5 bg-surface-200 rounded text-surface-500 font-mono">Ctrl</kbd> + <kbd className="px-1.5 py-0.5 bg-surface-200 rounded text-surface-500 font-mono">Enter</kbd> to submit
      </p>
    </form>
  )
}

export default QueryInput
