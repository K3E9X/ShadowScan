import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/layout/theme-provider'
import { Toaster } from '@/components/ui/toaster'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono'
})

export const metadata: Metadata = {
  title: 'ShadowScan - AI-Powered Security Analysis Platform',
  description:
    'Comprehensive code security analysis and architecture diagram assessment using AI. Detect vulnerabilities, analyze architectures, and get secure-by-design recommendations.',
  keywords: [
    'security analysis',
    'code security',
    'SAST',
    'vulnerability detection',
    'architecture analysis',
    'OWASP',
    'CWE',
    'Zero Trust',
    'secure-by-design'
  ],
  authors: [{ name: 'ShadowScan Team' }],
  creator: 'ShadowScan',
  publisher: 'ShadowScan',
  robots: {
    index: true,
    follow: true
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://shadowscan.dev',
    title: 'ShadowScan - AI-Powered Security Analysis Platform',
    description:
      'Comprehensive code security analysis and architecture diagram assessment',
    siteName: 'ShadowScan'
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ShadowScan - AI-Powered Security Analysis Platform',
    description:
      'Comprehensive code security analysis and architecture diagram assessment'
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png'
  },
  manifest: '/site.webmanifest'
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="format-detection" content="telephone=no" />
      </head>
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
