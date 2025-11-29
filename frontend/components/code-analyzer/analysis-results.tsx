'use client'

import { AlertTriangle, CheckCircle, Info, XCircle } from 'lucide-react'
import { getSeverityColor } from '@/lib/utils'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'

interface AnalysisResultsProps {
  result: any
}

export function AnalysisResults({ result }: AnalysisResultsProps) {
  const { vulnerabilities, summary, compliance, dependencies, secrets } = result

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard
          title="Total Issues"
          value={summary?.total_issues || 0}
          icon={<Info className="h-5 w-5" />}
        />
        <StatCard
          title="Critical"
          value={summary?.critical || 0}
          icon={<XCircle className="h-5 w-5 text-critical" />}
          severity="critical"
        />
        <StatCard
          title="High"
          value={summary?.high || 0}
          icon={<AlertTriangle className="h-5 w-5 text-high" />}
          severity="high"
        />
        <StatCard
          title="Medium/Low"
          value={(summary?.medium || 0) + (summary?.low || 0)}
          icon={<Info className="h-5 w-5 text-medium" />}
          severity="medium"
        />
      </div>

      {/* Vulnerabilities */}
      {vulnerabilities && vulnerabilities.length > 0 && (
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-4 text-xl font-bold">Security Vulnerabilities</h3>
          <Accordion type="single" collapsible className="space-y-2">
            {vulnerabilities.map((vuln: any, index: number) => (
              <AccordionItem key={index} value={`vuln-${index}`}>
                <AccordionTrigger className="hover:no-underline">
                  <div className="flex w-full items-center justify-between pr-4">
                    <div className="flex items-center gap-3">
                      <span className={`severity-badge ${getSeverityColor(vuln.severity)}`}>
                        {vuln.severity}
                      </span>
                      <span className="font-semibold">{vuln.title}</span>
                    </div>
                    <span className="text-sm text-muted-foreground">
                      {vuln.location?.file}:{vuln.location?.line}
                    </span>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <div className="space-y-4 pt-4">
                    <div>
                      <h4 className="mb-2 font-semibold">Description</h4>
                      <p className="text-sm text-muted-foreground">{vuln.description}</p>
                    </div>

                    {vuln.location?.snippet && (
                      <div>
                        <h4 className="mb-2 font-semibold">Code Snippet</h4>
                        <pre className="rounded bg-muted p-3 text-sm overflow-x-auto">
                          <code>{vuln.location.snippet}</code>
                        </pre>
                      </div>
                    )}

                    <div>
                      <h4 className="mb-2 font-semibold">Impact</h4>
                      <p className="text-sm text-muted-foreground">{vuln.impact}</p>
                    </div>

                    <div>
                      <h4 className="mb-2 font-semibold">Remediation</h4>
                      <p className="text-sm text-muted-foreground">{vuln.remediation}</p>
                    </div>

                    {vuln.secure_code && (
                      <div>
                        <h4 className="mb-2 font-semibold">Secure Code Example</h4>
                        <pre className="rounded bg-muted p-3 text-sm overflow-x-auto">
                          <code>{vuln.secure_code}</code>
                        </pre>
                      </div>
                    )}

                    {vuln.references && vuln.references.length > 0 && (
                      <div>
                        <h4 className="mb-2 font-semibold">References</h4>
                        <ul className="list-inside list-disc text-sm text-muted-foreground">
                          {vuln.references.map((ref: string, i: number) => (
                            <li key={i}>{ref}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-semibold">CWE ID:</span> {vuln.id}
                      </div>
                      <div>
                        <span className="font-semibold">Confidence:</span>{' '}
                        {Math.round((vuln.confidence || 0) * 100)}%
                      </div>
                      <div>
                        <span className="font-semibold">Exploitability:</span>{' '}
                        {vuln.exploitability}
                      </div>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      )}

      {/* Secrets Detection */}
      {secrets && secrets.length > 0 && (
        <div className="rounded-lg border border-critical bg-critical/10 p-6">
          <h3 className="mb-4 text-xl font-bold text-critical">
            <XCircle className="mr-2 inline-block h-5 w-5" />
            Secrets Detected
          </h3>
          <div className="space-y-2">
            {secrets.map((secret: any, index: number) => (
              <div key={index} className="rounded bg-background p-3">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-sm">{secret.type}</span>
                  <span className="text-sm text-muted-foreground">
                    Line {secret.line}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dependencies */}
      {dependencies && dependencies.length > 0 && (
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-4 text-xl font-bold">Dependency Vulnerabilities</h3>
          <div className="space-y-2">
            {dependencies.map((dep: any, index: number) => (
              <div key={index} className="rounded border p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-semibold">{dep.name}</span>
                    <span className="ml-2 text-sm text-muted-foreground">
                      v{dep.version}
                    </span>
                  </div>
                  {dep.vulnerabilities > 0 && (
                    <span className="severity-badge severity-high">
                      {dep.vulnerabilities} vulnerabilities
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Compliance */}
      {compliance && (
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-4 text-xl font-bold">Compliance Status</h3>
          <div className="grid gap-3 md:grid-cols-2">
            {Object.entries(compliance).map(([framework, status]: [string, any]) => (
              <div key={framework} className="flex items-center justify-between rounded border p-3">
                <span className="font-medium">{framework}</span>
                {status.compliant ? (
                  <CheckCircle className="h-5 w-5 text-low" />
                ) : (
                  <XCircle className="h-5 w-5 text-critical" />
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Issues Found */}
      {(!vulnerabilities || vulnerabilities.length === 0) &&
        (!secrets || secrets.length === 0) && (
          <div className="rounded-lg border border-low bg-low/10 p-8 text-center">
            <CheckCircle className="mx-auto mb-4 h-12 w-12 text-low" />
            <h3 className="mb-2 text-xl font-bold">No Critical Issues Found</h3>
            <p className="text-muted-foreground">
              Your code passed the security analysis. Keep following security best practices!
            </p>
          </div>
        )}
    </div>
  )
}

function StatCard({
  title,
  value,
  icon,
  severity
}: {
  title: string
  value: number
  icon: React.ReactNode
  severity?: string
}) {
  return (
    <div className="stats-card">
      <div className="mb-2 flex items-center justify-center text-muted-foreground">
        {icon}
      </div>
      <div className="mb-1 text-3xl font-bold">{value}</div>
      <div className="text-sm text-muted-foreground">{title}</div>
    </div>
  )
}
