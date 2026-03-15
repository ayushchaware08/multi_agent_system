import { motion } from 'framer-motion'
import { 
  Brain, 
  FileSearch, 
  Globe, 
  BookOpen, 
  Github, 
  Zap,
  Sparkles,
  Server
} from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import api from '../services/api'

/**
 * Sidebar component displaying system info and agents
 */
const Sidebar = () => {
  // Wake backend mutation
  const wakeMutation = useMutation({
    mutationFn: api,
    onSuccess: () => {
      console.log('Backend is awake!')
    },
    onError: (error) => {
      console.error('Failed to wake backend:', error)
    }
  })

  // Agent definitions with icons and colors - using brand colors
  const agents = [
    {
      name: 'Arxiv Agent',
      description: 'Searches academic papers',
      icon: BookOpen,
      color: 'text-brand-light',
      bgColor: 'bg-brand-teal/20',
    },
    {
      name: 'PDF RAG Agent',
      description: 'Analyzes uploaded documents',
      icon: FileSearch,
      color: 'text-brand-gold',
      bgColor: 'bg-brand-gold/20',
    },
    {
      name: 'Web Search Agent',
      description: 'Searches the internet',
      icon: Globe,
      color: 'text-brand-light',
      bgColor: 'bg-brand-teal/20',
    },
    {
      name: 'LLM Router',
      description: 'Routes queries intelligently',
      icon: Brain,
      color: 'text-brand-light',
      bgColor: 'bg-brand-dark/50',
    },
  ]

  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="w-72 h-screen bg-dark-800/40 border-r border-dark-700/50 flex flex-col"
    >
      {/* Logo & Title */}
      <div className="p-6 border-b border-dark-700/50">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-brand-teal rounded-lg">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-brand-light">Multi-Agent</h1>
            <p className="text-sm text-dark-500">Research AI</p>
          </div>
        </div>
      </div>

      {/* System Description */}
      <div className="p-6 border-b border-dark-700/50">
        <h2 className="text-xs font-bold text-dark-500 uppercase tracking-wider mb-3">
          System Architecture
        </h2>
        <p className="text-sm text-dark-400 leading-relaxed">
          An intelligent multi-agent system that routes your queries to specialized AI agents for research, analysis, and web search.
        </p>
      </div>

      {/* Agents List - Bento style */}
      <div className="flex-1 p-6 overflow-y-auto">
        <h2 className="text-xs font-bold text-dark-500 uppercase tracking-wider mb-4">
          Available Agents
        </h2>
        <div className="grid grid-cols-2 gap-2">
          {agents.map((agent, index) => (
            <motion.div
              key={agent.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bento-cell p-3 hover:border-brand-teal/30 transition-colors"
            >
              <div className={`p-2 rounded-md ${agent.bgColor} w-fit mb-2`}>
                <agent.icon className={`w-4 h-4 ${agent.color}`} />
              </div>
              <h3 className="text-xs font-bold text-brand-light">{agent.name}</h3>
              <p className="text-[10px] text-dark-500 mt-0.5">{agent.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Footer Actions */}
      <div className="p-6 border-t border-dark-700/50 space-y-3">
        {/* Wake Backend Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => wakeMutation.mutate()}
          disabled={wakeMutation.isPending}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-brand-teal hover:bg-brand-teal/80 rounded-lg text-sm font-bold text-white transition-all disabled:opacity-50"
        >
          {wakeMutation.isPending ? (
            <>
              <Server className="w-4 h-4 animate-pulse" />
              Waking Backend...
            </>
          ) : wakeMutation.isSuccess ? (
            <>
              <Zap className="w-4 h-4 text-brand-gold" />
              Backend Ready
            </>
          ) : (
            <>
              <Server className="w-4 h-4" />
              Wake Backend
            </>
          )}
        </motion.button>

        {/* GitHub Link */}
        <a
          href="https://github.com"
          target="_blank"
          rel="noopener noreferrer"
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-dark-800/80 hover:bg-dark-700 border border-dark-700 rounded-lg text-sm text-dark-400 hover:text-brand-light transition-all font-medium"
        >
          <Github className="w-4 h-4" />
          View on GitHub
        </a>
      </div>
    </motion.aside>
  )
}

export default Sidebar
