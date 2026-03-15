import { motion } from 'framer-motion'
import { Brain, Sparkles } from 'lucide-react'

/**
 * Loading skeleton for answer cards
 */
const LoadingSkeleton = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-sm rounded-xl border border-surface-300 p-6 shadow-lg"
    >
      <div className="flex items-center gap-3 mb-6">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="p-2 bg-gradient-to-br from-brand-teal to-blue-600 rounded-lg shadow-lg"
        >
          <Brain className="w-5 h-5 text-white" />
        </motion.div>
        <div>
          <p className="text-sm text-brand-darker font-bold">Processing your query...</p>
          <p className="text-xs text-surface-500">AI agents are working on it</p>
        </div>
      </div>

      <div className="space-y-3">
        <SkeletonLine width="100%" delay={0} />
        <SkeletonLine width="95%" delay={0.1} />
        <SkeletonLine width="88%" delay={0.2} />
        <SkeletonLine width="92%" delay={0.3} />
        <SkeletonLine width="70%" delay={0.4} />
      </div>

      <div className="flex items-center gap-2 mt-6">
        <Sparkles className="w-4 h-4 text-surface-400" />
        <div className="flex gap-1">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
              className="w-1.5 h-1.5 bg-brand-teal rounded-full"
            />
          ))}
        </div>
      </div>
    </motion.div>
  )
}

const SkeletonLine = ({ width, delay }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay }}
      className="h-4 bg-surface-200 rounded animate-pulse"
      style={{ width }}
    />
  )
}

export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizeClasses = { sm: 'w-4 h-4', md: 'w-6 h-6', lg: 'w-8 h-8' }

  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      className={`${sizeClasses[size]} ${className}`}
    >
      <svg className="w-full h-full text-brand-teal" viewBox="0 0 24 24" fill="none">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
    </motion.div>
  )
}

export default LoadingSkeleton
