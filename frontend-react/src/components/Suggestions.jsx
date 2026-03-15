import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'

/**
 * Suggestion chips for common queries
 */
const Suggestions = ({ onSelect, disabled }) => {
  const suggestions = [
    'Recent papers on AI safety',
    'Summarize my uploaded PDF',
    'Find papers about reinforcement learning',
    'Latest developments in AI 2025',
    'Explain transformer architecture',
    'Research on large language models',
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.3 }}
      className="mb-6"
    >
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="w-4 h-4 text-amber-500" />
        <span className="text-xs font-bold text-surface-500 uppercase tracking-wider">Try asking</span>
      </div>
      
      <div className="flex flex-wrap gap-2">
        {suggestions.map((suggestion) => (
          <motion.button
            key={suggestion}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(suggestion)}
            disabled={disabled}
            className="px-4 py-2 bg-gradient-to-r from-white to-blue-50 hover:from-blue-50 hover:to-teal-50 border border-surface-300 hover:border-brand-teal rounded-lg text-sm text-surface-600 hover:text-brand-teal cursor-pointer transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
          >
            {suggestion}
          </motion.button>
        ))}
      </div>
    </motion.div>
  )
}

export default Suggestions
