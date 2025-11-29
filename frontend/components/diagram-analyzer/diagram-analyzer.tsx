'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileImage, Loader2, AlertCircle, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { DiagramResults } from './diagram-results'
import { useToast } from '@/lib/use-toast'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const ACCEPTED_IMAGE_TYPES = {
  'image/png': ['.png'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'image/svg+xml': ['.svg']
}

export function DiagramAnalyzer() {
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    // File size limit: 50MB
    if (file.size > 50 * 1024 * 1024) {
      toast({
        title: 'File Too Large',
        description: 'Maximum file size is 50MB',
        variant: 'destructive'
      })
      return
    }

    setImageFile(file)

    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setImagePreview(e.target?.result as string)
    }
    reader.readAsDataURL(file)

    toast({
      title: 'Image Loaded',
      description: `${file.name} ready for analysis`
    })
  }, [toast])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_IMAGE_TYPES,
    maxFiles: 1,
    multiple: false
  })

  const handleAnalyze = async () => {
    if (!imageFile) {
      toast({
        title: 'No Image',
        description: 'Please upload an architecture diagram first',
        variant: 'destructive'
      })
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const formData = new FormData()
      formData.append('file', imageFile)

      const response = await fetch(`${API_URL}/api/v1/analyze/diagram`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`)
      }

      const data = await response.json()
      setAnalysisResult(data)

      toast({
        title: 'Analysis Complete',
        description: `Identified ${data.components?.length || 0} components`
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to analyze diagram'
      setError(errorMessage)
      toast({
        title: 'Analysis Failed',
        description: errorMessage,
        variant: 'destructive'
      })
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleClear = () => {
    setImageFile(null)
    setImagePreview(null)
    setAnalysisResult(null)
    setError(null)
  }

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <div className="rounded-lg border bg-card p-6">
        <div className="mb-4">
          <h2 className="text-2xl font-bold">Architecture Diagram Analysis</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Upload your infrastructure or application architecture diagram for security assessment
          </p>
        </div>

        {!imagePreview ? (
          <div
            {...getRootProps()}
            className={`
              cursor-pointer rounded-lg border-2 border-dashed p-12 text-center transition-colors
              ${isDragActive ? 'border-primary bg-primary/5' : 'border-muted-foreground/25 hover:border-primary/50'}
            `}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-4">
              <div className="rounded-full bg-primary/10 p-6">
                <Upload className="h-12 w-12 text-primary" />
              </div>
              <div>
                <p className="text-lg font-semibold">
                  {isDragActive ? 'Drop your diagram here' : 'Drag & drop your diagram'}
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  or click to browse files
                </p>
              </div>
              <div className="flex gap-2 text-xs text-muted-foreground">
                <span className="rounded bg-muted px-2 py-1">PNG</span>
                <span className="rounded bg-muted px-2 py-1">JPG</span>
                <span className="rounded bg-muted px-2 py-1">SVG</span>
              </div>
              <p className="text-xs text-muted-foreground">Maximum file size: 50MB</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative rounded-lg border bg-muted/50 p-4">
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-2 top-2"
                onClick={handleClear}
              >
                <X className="h-4 w-4" />
              </Button>

              <div className="flex flex-col items-center gap-4">
                <FileImage className="h-12 w-12 text-primary" />
                <div className="text-center">
                  <p className="font-semibold">{imageFile?.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(imageFile?.size || 0) / 1024 > 1024
                      ? `${((imageFile?.size || 0) / 1024 / 1024).toFixed(2)} MB`
                      : `${((imageFile?.size || 0) / 1024).toFixed(2)} KB`}
                  </p>
                </div>
              </div>

              {/* Image Preview */}
              <div className="mt-4 max-h-96 overflow-hidden rounded-lg">
                <img
                  src={imagePreview}
                  alt="Architecture diagram preview"
                  className="mx-auto max-h-96 object-contain"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={handleClear}>
                Clear
              </Button>
              <Button onClick={handleAnalyze} disabled={isAnalyzing} size="lg">
                {isAnalyzing ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <FileImage className="mr-2 h-5 w-5" />
                    Analyze Diagram
                  </>
                )}
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="rounded-lg border border-destructive bg-destructive/10 p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-destructive mt-0.5" />
            <div>
              <h3 className="font-semibold text-destructive">Analysis Error</h3>
              <p className="text-sm text-destructive/90 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {analysisResult && <DiagramResults result={analysisResult} />}
    </div>
  )
}
