import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ExternalLink, Copy, Check } from 'lucide-react'
import { useState } from 'react'
import AgentInfo from './AgentInfo'

/**
 * Answer card component for displaying query results
 */
const AnswerCard = ({ result, query }) => {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.answer || result.response || '')
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const answerText = result.answer || result.response || result.result || ''
  const agentUsed = result.agent_used || result.agent || result.source || 'LLM'
  const reasoning = result.reasoning || result.rationale || result.explanation || ''
  const sources = result.sources || result.references || []

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-sm rounded-xl border border-surface-300 p-6 shadow-lg hover:shadow-xl transition-shadow"
    >
      <div className="mb-4 pb-4 border-b border-surface-200">
        <p className="text-xs font-bold text-surface-500 uppercase tracking-wider mb-1">Your question</p>
        <p className="text-brand-darker font-medium">{query}</p>
      </div>

      <AgentInfo agentUsed={agentUsed} reasoning={reasoning} />

      <div className="relative">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleCopy}
          className="absolute top-0 right-0 p-2 text-surface-400 hover:text-brand-teal transition-colors"
          title="Copy answer"
        >
          {copied ? (
            <Check className="w-4 h-4 text-green-600" />
          ) : (
            <Copy className="w-4 h-4" />
          )}
        </motion.button>

        <div className="markdown-content pr-10">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {answerText}
          </ReactMarkdown>
        </div>
      </div>

      {sources && sources.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-6 pt-4 border-t border-surface-200"
        >
          <p className="text-xs font-bold text-surface-500 uppercase tracking-wider mb-3">Sources</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {sources.map((source, index) => (
              <a
                key={index}
                href={source.url || source.link || '#'}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 p-3 bg-surface-100 hover:bg-brand-teal/10 border border-surface-200 hover:border-brand-teal rounded-lg transition-colors group"
              >
                <ExternalLink className="w-4 h-4 text-surface-400 group-hover:text-brand-teal transition-colors flex-shrink-0" />
                <span className="text-sm text-surface-500 group-hover:text-brand-darker transition-colors truncate font-medium">
                  {source.title || source.name || source.url || `Source ${index + 1}`}
                </span>
              </a>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}

export default AnswerCard
