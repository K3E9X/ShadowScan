'use client'

import { Shield, AlertTriangle, CheckCircle, Network, Database, Cloud } from 'lucide-react'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface DiagramResultsProps {
  result: any
}

export function DiagramResults({ result }: DiagramResultsProps) {
  const {
    components,
    security_assessment,
    weaknesses,
    zero_trust_proposal,
    secure_by_design,
    compliance
  } = result

  return (
    <div className="space-y-6">
      {/* Components Identified */}
      {components && components.length > 0 && (
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-4 text-xl font-bold">
            <Network className="mr-2 inline-block h-5 w-5" />
            Identified Components
          </h3>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {components.map((component: any, index: number) => (
              <div key={index} className="rounded border p-3">
                <div className="flex items-center gap-2">
                  {getComponentIcon(component.type)}
                  <div>
                    <div className="font-semibold">{component.name}</div>
                    <div className="text-xs text-muted-foreground">{component.type}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Security Assessment */}
      {security_assessment && (
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-4 text-xl font-bold">
            <Shield className="mr-2 inline-block h-5 w-5" />
            Security Assessment
          </h3>
          <div className="space-y-4">
            <div>
              <h4 className="mb-2 font-semibold">Overall Security Posture</h4>
              <p className="text-sm text-muted-foreground">
                {security_assessment.overall || 'Analysis in progress...'}
              </p>
            </div>
            {security_assessment.risk_level && (
              <div className="flex items-center gap-2">
                <span className="font-semibold">Risk Level:</span>
                <span
                  className={`severity-badge ${
                    security_assessment.risk_level === 'HIGH'
                      ? 'severity-high'
                      : security_assessment.risk_level === 'MEDIUM'
                      ? 'severity-medium'
                      : 'severity-low'
                  }`}
                >
                  {security_assessment.risk_level}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Weaknesses & Misconfigurations */}
      {weaknesses && weaknesses.length > 0 && (
        <div className="rounded-lg border border-high bg-high/10 p-6">
          <h3 className="mb-4 text-xl font-bold text-high">
            <AlertTriangle className="mr-2 inline-block h-5 w-5" />
            Security Weaknesses
          </h3>
          <Accordion type="single" collapsible className="space-y-2">
            {weaknesses.map((weakness: any, index: number) => (
              <AccordionItem key={index} value={`weakness-${index}`}>
                <AccordionTrigger>
                  <div className="flex items-center gap-3">
                    <span className={`severity-badge severity-${weakness.severity?.toLowerCase() || 'medium'}`}>
                      {weakness.severity || 'MEDIUM'}
                    </span>
                    <span className="font-semibold">{weakness.title}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="mb-2 font-semibold">Description</h4>
                      <p className="text-sm text-muted-foreground">{weakness.description}</p>
                    </div>
                    {weakness.affected_components && (
                      <div>
                        <h4 className="mb-2 font-semibold">Affected Components</h4>
                        <ul className="list-inside list-disc text-sm text-muted-foreground">
                          {weakness.affected_components.map((comp: string, i: number) => (
                            <li key={i}>{comp}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {weakness.recommendation && (
                      <div>
                        <h4 className="mb-2 font-semibold">Recommendation</h4>
                        <p className="text-sm text-muted-foreground">{weakness.recommendation}</p>
                      </div>
                    )}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      )}

      {/* Recommendations */}
      <Tabs defaultValue="zero-trust" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="zero-trust">Zero Trust Architecture</TabsTrigger>
          <TabsTrigger value="secure-design">Secure-by-Design</TabsTrigger>
        </TabsList>

        <TabsContent value="zero-trust" className="mt-6">
          {zero_trust_proposal && (
            <div className="rounded-lg border bg-card p-6">
              <h3 className="mb-4 text-xl font-bold">
                <Shield className="mr-2 inline-block h-5 w-5" />
                Zero Trust Architecture Proposal
              </h3>
              <div className="space-y-6">
                {zero_trust_proposal.network_segmentation && (
                  <Section
                    title="Network Segmentation"
                    content={zero_trust_proposal.network_segmentation}
                  />
                )}
                {zero_trust_proposal.identity_access && (
                  <Section
                    title="Identity & Access Management"
                    content={zero_trust_proposal.identity_access}
                  />
                )}
                {zero_trust_proposal.encryption && (
                  <Section title="Encryption Strategy" content={zero_trust_proposal.encryption} />
                )}
                {zero_trust_proposal.monitoring && (
                  <Section
                    title="Monitoring & Logging"
                    content={zero_trust_proposal.monitoring}
                  />
                )}
              </div>
            </div>
          )}
        </TabsContent>

        <TabsContent value="secure-design" className="mt-6">
          {secure_by_design && (
            <div className="rounded-lg border bg-card p-6">
              <h3 className="mb-4 text-xl font-bold">
                <CheckCircle className="mr-2 inline-block h-5 w-5" />
                Secure-by-Design Recommendations
              </h3>
              <div className="space-y-6">
                {secure_by_design.hardening && (
                  <Section title="Security Hardening" content={secure_by_design.hardening} />
                )}
                {secure_by_design.redundancy && (
                  <Section title="Redundancy & Resilience" content={secure_by_design.redundancy} />
                )}
                {secure_by_design.data_protection && (
                  <Section title="Data Protection" content={secure_by_design.data_protection} />
                )}
                {secure_by_design.best_practices && (
                  <Section title="Best Practices" content={secure_by_design.best_practices} />
                )}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {/* Compliance */}
      {compliance && (
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-4 text-xl font-bold">Compliance Assessment</h3>
          <div className="grid gap-3 md:grid-cols-2">
            {Object.entries(compliance).map(([framework, status]: [string, any]) => (
              <div key={framework} className="flex items-center justify-between rounded border p-3">
                <div>
                  <div className="font-medium">{framework}</div>
                  {status.issues && (
                    <div className="text-xs text-muted-foreground">
                      {status.issues} issue{status.issues !== 1 ? 's' : ''} found
                    </div>
                  )}
                </div>
                {status.compliant ? (
                  <CheckCircle className="h-5 w-5 text-low" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-high" />
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function Section({ title, content }: { title: string; content: string | string[] }) {
  return (
    <div>
      <h4 className="mb-2 font-semibold">{title}</h4>
      {Array.isArray(content) ? (
        <ul className="list-inside list-disc space-y-1 text-sm text-muted-foreground">
          {content.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-muted-foreground">{content}</p>
      )}
    </div>
  )
}

function getComponentIcon(type: string) {
  const iconMap: Record<string, React.ReactNode> = {
    database: <Database className="h-4 w-4 text-primary" />,
    cloud: <Cloud className="h-4 w-4 text-primary" />,
    network: <Network className="h-4 w-4 text-primary" />,
    default: <Shield className="h-4 w-4 text-primary" />
  }

  return iconMap[type.toLowerCase()] || iconMap.default
}
