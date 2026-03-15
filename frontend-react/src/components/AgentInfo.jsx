import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, Brain, BookOpen, FileSearch, Globe, Info } from 'lucide-react'

const getAgentConfig = (agentType) => {
  const normalizedType = agentType?.toLowerCase() || ''
  
  if (normalizedType.includes('arxiv')) {
    return {
      name: 'Arxiv Agent',
      icon: BookOpen,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      borderColor: 'border-blue-200',
      description: 'Searched academic papers on arXiv',
    }
  }
  
  if (normalizedType.includes('pdf') || normalizedType.includes('rag')) {
    return {
      name: 'PDF RAG Agent',
      icon: FileSearch,
      color: 'text-amber-600',
      bgColor: 'bg-amber-100',
      borderColor: 'border-amber-200',
      description: 'Analyzed your uploaded documents',
    }
  }
  
  if (normalizedType.includes('web') || normalizedType.includes('search')) {
    return {
      name: 'Web Search Agent',
      icon: Globe,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      borderColor: 'border-green-200',
      description: 'Searched the web for information',
    }
  }
  
  return {
    name: 'LLM Router',
    icon: Brain,
    color: 'text-purple-600',
    bgColor: 'bg-purple-100',
    borderColor: 'border-purple-200',
    description: 'Processed with AI reasoning',
  }
}

const AgentInfo = ({ agentUsed, reasoning }) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const config = getAgentConfig(agentUsed)
  const IconComponent = config.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4"
    >
      <div className="flex items-center gap-3 mb-2">
        <span className="text-xs font-bold text-surface-500 uppercase tracking-wider">Agent Used</span>
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg ${config.bgColor} ${config.borderColor} border`}>
          <IconComponent className={`w-4 h-4 ${config.color}`} />
          <span className={`text-sm font-bold ${config.color}`}>{config.name}</span>
        </div>
      </div>

      {reasoning && (
        <div className="mt-3">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-2 text-sm text-surface-500 hover:text-brand-darker transition-colors font-medium"
          >
            <Info className="w-4 h-4" />
            <span>Agents used & rationale</span>
            <motion.div animate={{ rotate: isExpanded ? 180 : 0 }} transition={{ duration: 0.2 }}>
              <ChevronDown className="w-4 h-4" />
            </motion.div>
          </button>

          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="mt-3 p-4 bg-surface-100 border border-surface-200 rounded-lg">
                  <p className="text-sm text-surface-500 leading-relaxed">{reasoning}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}
    </motion.div>
  )
}

export default AgentInfo
