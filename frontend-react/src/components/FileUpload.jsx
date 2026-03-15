import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { useMutation } from '@tanstack/react-query'
import { 
  Upload, 
  FileText, 
  Check, 
  Loader2,
  AlertCircle
} from 'lucide-react'
import { uploadPDF } from '../services/api'

/**
 * File upload component with drag-and-drop support
 */
const FileUpload = () => {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadedFile, setUploadedFile] = useState(null)

  const uploadMutation = useMutation({
    mutationFn: (file) => uploadPDF(file, setUploadProgress),
    onSuccess: (data) => {
      setUploadedFile(data.filename || data.message)
    },
    onError: () => {
      setUploadProgress(0)
    }
  })

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0]
    if (file) {
      setUploadProgress(0)
      setUploadedFile(null)
      uploadMutation.mutate(file)
    }
  }, [uploadMutation])

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxSize: 50 * 1024 * 1024,
    maxFiles: 1,
    disabled: uploadMutation.isPending
  })

  const resetUpload = () => {
    setUploadedFile(null)
    setUploadProgress(0)
    uploadMutation.reset()
  }

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-xl border border-surface-300 p-4 h-full shadow-lg">
      <h3 className="text-xs font-bold text-surface-500 uppercase tracking-wider mb-3 flex items-center gap-2">
        <Upload className="w-3 h-3" />
        Upload PDF
      </h3>

      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
          isDragActive 
            ? 'border-brand-teal bg-gradient-to-br from-blue-50 to-teal-50 scale-105' 
            : 'border-surface-300 hover:border-brand-teal/50 bg-gradient-to-br from-blue-50/30 to-white'
        } ${uploadMutation.isPending ? 'pointer-events-none opacity-70' : ''}shadow-md hover:shadow-lg`}
      >
        <input {...getInputProps()} />

        <AnimatePresence mode="wait">
          {uploadMutation.isSuccess && uploadedFile && (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center gap-2"
            >
              <div className="p-2 bg-green-100 rounded-lg">
                <Check className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-brand-darker font-bold text-sm">Uploaded</p>
                <p className="text-xs text-surface-500 mt-0.5 truncate max-w-[150px]">{uploadedFile}</p>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); resetUpload() }}
                className="text-xs text-brand-teal hover:text-brand-gold transition-colors font-medium"
              >
                Upload another
              </button>
            </motion.div>
          )}

          {uploadMutation.isPending && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center gap-2"
            >
              <Loader2 className="w-6 h-6 text-brand-teal animate-spin" />
              <div>
                <p className="text-brand-darker font-bold text-sm">Uploading...</p>
                <p className="text-xs text-surface-500 mt-0.5">{uploadProgress}%</p>
              </div>
              <div className="w-full max-w-[120px] h-1 bg-surface-200 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-brand-teal"
                  initial={{ width: 0 }}
                  animate={{ width: `${uploadProgress}%` }}
                />
              </div>
            </motion.div>
          )}

          {uploadMutation.isError && (
            <motion.div
              key="error"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center gap-2"
            >
              <div className="p-2 bg-red-100 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-600" />
              </div>
              <div>
                <p className="text-brand-darker font-bold text-sm">Failed</p>
                <p className="text-xs text-red-600 mt-0.5">{uploadMutation.error?.message || 'Error'}</p>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); resetUpload() }}
                className="text-xs text-brand-teal hover:text-brand-gold transition-colors font-medium"
              >
                Try again
              </button>
            </motion.div>
          )}

          {!uploadMutation.isPending && !uploadMutation.isSuccess && !uploadMutation.isError && (
            <motion.div
              key="default"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center gap-2"
            >
              <div className={`p-2 rounded-lg transition-colors ${isDragActive ? 'bg-brand-teal/10' : 'bg-surface-200'}`}>
                <FileText className={`w-5 h-5 ${isDragActive ? 'text-brand-teal' : 'text-surface-400'}`} />
              </div>
              <div>
                <p className="text-brand-darker font-bold text-sm">{isDragActive ? 'Drop here' : 'Drop PDF'}</p>
                <p className="text-xs text-surface-500 mt-0.5">or click • 50MB max</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {fileRejections.length > 0 && (
          <p className="text-xs text-red-600 mt-2">{fileRejections[0].errors[0].message}</p>
        )}
      </div>
    </div>
  )
}

export default FileUpload
