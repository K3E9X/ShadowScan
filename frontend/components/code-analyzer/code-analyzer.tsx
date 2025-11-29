'use client'

import { useState } from 'react'
import { Upload, FileCode, Loader2, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { CodeEditor } from './code-editor'
import { AnalysisResults } from './analysis-results'
import { useToast } from '@/lib/use-toast'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function CodeAnalyzer() {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  const handleAnalyze = async () => {
    if (!code.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter some code to analyze',
        variant: 'destructive'
      })
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const response = await fetch(`${API_URL}/api/v1/analyze/code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          code,
          language
        })
      })

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`)
      }

      const data = await response.json()
      setAnalysisResult(data)

      toast({
        title: 'Analysis Complete',
        description: `Found ${data.summary?.total_issues || 0} security issues`
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to analyze code'
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

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
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

    try {
      const text = await file.text()
      setCode(text)

      // Detect language from file extension
      const ext = file.name.split('.').pop()?.toLowerCase()
      const langMap: Record<string, string> = {
        py: 'python',
        js: 'javascript',
        ts: 'typescript',
        jsx: 'javascript',
        tsx: 'typescript',
        java: 'java',
        go: 'go',
        rs: 'rust',
        c: 'c',
        cpp: 'cpp',
        php: 'php',
        rb: 'ruby',
        cs: 'csharp'
      }

      if (ext && langMap[ext]) {
        setLanguage(langMap[ext])
      }

      toast({
        title: 'File Loaded',
        description: `${file.name} loaded successfully`
      })
    } catch (err) {
      toast({
        title: 'File Read Error',
        description: 'Failed to read file',
        variant: 'destructive'
      })
    }
  }

  return (
    <div className="space-y-6">
      {/* Code Input Section */}
      <div className="rounded-lg border bg-card p-6">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Code Security Analysis</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Paste your code or upload a file to analyze for security vulnerabilities
            </p>
          </div>

          <div className="flex gap-2">
            <label htmlFor="file-upload">
              <Button variant="outline" asChild>
                <span className="cursor-pointer">
                  <Upload className="mr-2 h-4 w-4" />
                  Upload File
                </span>
              </Button>
            </label>
            <input
              id="file-upload"
              type="file"
              className="hidden"
              onChange={handleFileUpload}
              accept=".py,.js,.ts,.jsx,.tsx,.java,.go,.rs,.c,.cpp,.php,.rb,.cs"
            />
          </div>
        </div>

        <CodeEditor
          value={code}
          onChange={setCode}
          language={language}
          onLanguageChange={setLanguage}
        />

        <div className="mt-4 flex justify-end">
          <Button onClick={handleAnalyze} disabled={isAnalyzing} size="lg">
            {isAnalyzing ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <FileCode className="mr-2 h-5 w-5" />
                Analyze Code
              </>
            )}
          </Button>
        </div>
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
      {analysisResult && <AnalysisResults result={analysisResult} />}
    </div>
  )
}
