import Link from 'next/link'
import { Shield, Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">ShadowScan</span>
          </Link>

          <nav className="hidden md:flex gap-6">
            <Link
              href="/analyze"
              className="text-sm font-medium transition-colors hover:text-primary"
            >
              Analyze
            </Link>
            <Link
              href="/reports"
              className="text-sm font-medium transition-colors hover:text-primary"
            >
              Reports
            </Link>
            <Link
              href="/docs"
              className="text-sm font-medium transition-colors hover:text-primary"
            >
              Documentation
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" asChild className="hidden md:inline-flex">
            <Link href="/auth/login">Sign In</Link>
          </Button>
          <Button size="sm" asChild className="hidden md:inline-flex">
            <Link href="/auth/register">Get Started</Link>
          </Button>

          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  )
}
