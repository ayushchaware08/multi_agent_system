import { motion } from 'framer-motion'
import { AlertCircle, RefreshCw, WifiOff } from 'lucide-react'

/**
 * Error message component
 */
const ErrorMessage = ({ message, onRetry }) => {
  const isNetworkError = message?.toLowerCase().includes('network') || 
                         message?.toLowerCase().includes('connection') ||
                         message?.toLowerCase().includes('timeout')

  const IconComponent = isNetworkError ? WifiOff : AlertCircle

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-sm rounded-xl border-2 border-red-200 p-6 shadow-lg"
    >
      <div className="flex items-start gap-4">
        <div className="p-3 bg-gradient-to-br from-red-100 to-red-200 rounded-lg shrink-0 shadow-sm">
          <IconComponent className="w-6 h-6 text-red-600" />
        </div>

        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-bold text-brand-darker mb-1">Something went wrong</h3>
          <p className="text-sm text-surface-500 mb-4">
            {message || 'An unexpected error occurred. Please try again.'}
          </p>

          {onRetry && (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onRetry}
              className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-brand-teal to-blue-600 hover:from-brand-teal/90 hover:to-blue-600/90 rounded-lg text-sm font-bold text-white shadow-lg hover:shadow-xl transition-all"
            >
              <RefreshCw className="w-4 h-4" />
              Try Again
            </motion.button>
          )}
        </div>
      </div>

      {isNetworkError && (
        <div className="mt-4 pt-4 border-t border-surface-200">
          <p className="text-xs font-bold text-surface-500 uppercase tracking-wider mb-2">Troubleshooting</p>
          <ul className="text-xs text-surface-500 space-y-1">
            <li>• Check your internet connection</li>
            <li>• The backend server might be starting up</li>
            <li>• Click "Wake Backend" button to wake the server</li>
          </ul>
        </div>
      )}
    </motion.div>
  )
}

export default ErrorMessage
