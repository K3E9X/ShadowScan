'use client'

import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Navbar } from '@/components/layout/navbar'
import { CodeAnalyzer } from '@/components/code-analyzer/code-analyzer'
import { DiagramAnalyzer } from '@/components/diagram-analyzer/diagram-analyzer'
import { Code, FileImage } from 'lucide-react'

export default function AnalyzePage() {
  const [activeTab, setActiveTab] = useState('code')

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1 py-8">
        <div className="container">
          <div className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight">Security Analysis</h1>
            <p className="mt-2 text-muted-foreground">
              Analyze your code or architecture diagrams for security vulnerabilities
              and get AI-powered recommendations.
            </p>
          </div>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full max-w-md grid-cols-2">
              <TabsTrigger value="code" className="flex items-center gap-2">
                <Code className="h-4 w-4" />
                Code Analysis
              </TabsTrigger>
              <TabsTrigger value="diagram" className="flex items-center gap-2">
                <FileImage className="h-4 w-4" />
                Diagram Analysis
              </TabsTrigger>
            </TabsList>

            <TabsContent value="code" className="mt-6">
              <CodeAnalyzer />
            </TabsContent>

            <TabsContent value="diagram" className="mt-6">
              <DiagramAnalyzer />
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}
