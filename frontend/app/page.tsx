import Link from 'next/link'
import { ArrowRight, Code, Shield, FileSearch, Zap, Lock, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Navbar } from '@/components/layout/navbar'
import { Footer } from '@/components/layout/footer'

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      {/* Hero Section */}
      <section className="flex-1">
        <div className="container flex flex-col items-center gap-8 py-24 md:py-32">
          <div className="flex flex-col items-center gap-4 text-center">
            <div className="inline-flex items-center rounded-full border px-4 py-2 text-sm">
              <Shield className="mr-2 h-4 w-4" />
              <span>AI-Powered Security Analysis Platform</span>
            </div>

            <h1 className="max-w-4xl text-4xl font-bold tracking-tight sm:text-6xl">
              Secure Your Code and Architecture with{' '}
              <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                AI Intelligence
              </span>
            </h1>

            <p className="max-w-2xl text-lg text-muted-foreground">
              Comprehensive security analysis for your code and infrastructure diagrams.
              Detect vulnerabilities, analyze architectures, and get secure-by-design
              recommendations based on 2025 security standards.
            </p>

            <div className="flex gap-4 mt-4">
              <Button size="lg" asChild>
                <Link href="/analyze">
                  Start Analysis
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/docs">View Documentation</Link>
              </Button>
            </div>
          </div>

          {/* Features Grid */}
          <div className="mt-20 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <FeatureCard
              icon={<Code className="h-10 w-10" />}
              title="Code Security Analysis"
              description="Deep security analysis for any programming language. Detect OWASP Top 10, CWE Top 25, secrets, and supply chain vulnerabilities."
            />
            <FeatureCard
              icon={<FileSearch className="h-10 w-10" />}
              title="Architecture Analysis"
              description="Upload diagrams and get comprehensive security assessments with Zero Trust and Secure-by-Design recommendations."
            />
            <FeatureCard
              icon={<Zap className="h-10 w-10" />}
              title="AI-Powered Insights"
              description="Leverage advanced AI models to analyze code patterns, detect security issues, and generate secure code rewrites."
            />
            <FeatureCard
              icon={<Lock className="h-10 w-10" />}
              title="2025 Security Standards"
              description="Analysis based on OWASP 2025, CWE Top 25, NIST 800-218 SSDF, ISO 27001:2022, and NIS2 compliance."
            />
            <FeatureCard
              icon={<Shield className="h-10 w-10" />}
              title="Zero Trust Architecture"
              description="Get recommendations for implementing Zero Trust principles in your infrastructure and applications."
            />
            <FeatureCard
              icon={<CheckCircle className="h-10 w-10" />}
              title="Detailed Reports"
              description="Comprehensive reports with vulnerability details, risk levels, exploitability, and mitigation strategies."
            />
          </div>

          {/* Security Frameworks */}
          <div className="mt-20 w-full rounded-lg border bg-card p-8">
            <h3 className="mb-6 text-center text-2xl font-bold">
              Based on Industry-Leading Security Frameworks
            </h3>
            <div className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:grid-cols-6">
              <FrameworkBadge name="OWASP Top 10 2025" />
              <FrameworkBadge name="CWE Top 25 2025" />
              <FrameworkBadge name="NIST 800-218" />
              <FrameworkBadge name="ISO 27001:2022" />
              <FrameworkBadge name="NIS2" />
              <FrameworkBadge name="CIS Benchmarks" />
            </div>
          </div>

          {/* CTA Section */}
          <div className="mt-20 w-full rounded-lg border bg-gradient-to-r from-blue-600/10 to-cyan-600/10 p-12 text-center">
            <h2 className="mb-4 text-3xl font-bold">
              Ready to Secure Your Applications?
            </h2>
            <p className="mb-8 text-lg text-muted-foreground">
              Start analyzing your code and architecture diagrams today. No credit card
              required.
            </p>
            <Button size="lg" asChild>
              <Link href="/analyze">
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

function FeatureCard({
  icon,
  title,
  description
}: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <div className="card-elevated p-6 transition-all hover:shadow-xl">
      <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3 text-primary">
        {icon}
      </div>
      <h3 className="mb-2 text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  )
}

function FrameworkBadge({ name }: { name: string }) {
  return (
    <div className="rounded-lg border bg-background p-3 text-center text-sm font-medium">
      {name}
    </div>
  )
}
