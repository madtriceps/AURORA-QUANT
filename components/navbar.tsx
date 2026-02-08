"use client"

import { useState } from "react"

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-md">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <a href="#" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <span className="text-sm font-bold text-primary-foreground">A</span>
          </div>
          <span className="text-lg font-semibold tracking-tight text-foreground">
            AURORA
          </span>
        </a>

        <div className="hidden items-center gap-8 md:flex">
          <a href="#features" className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            Features
          </a>
          <a href="#how-it-works" className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            How It Works
          </a>
          <a href="#faq" className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            FAQ
          </a>
        </div>

        <a
          href="#waitlist"
          className="hidden rounded-lg bg-primary px-5 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90 md:inline-flex"
        >
          Join Waitlist
        </a>

        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-border md:hidden"
          aria-label="Toggle menu"
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" className="text-foreground">
            {mobileOpen ? (
              <path d="M4 4L14 14M14 4L4 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            ) : (
              <>
                <path d="M2 4.5H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                <path d="M2 9H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                <path d="M2 13.5H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </>
            )}
          </svg>
        </button>
      </nav>

      {mobileOpen && (
        <div className="border-t border-border bg-background px-6 py-4 md:hidden">
          <div className="flex flex-col gap-4">
            <a href="#features" onClick={() => setMobileOpen(false)} className="text-sm text-muted-foreground">Features</a>
            <a href="#how-it-works" onClick={() => setMobileOpen(false)} className="text-sm text-muted-foreground">How It Works</a>
            <a href="#faq" onClick={() => setMobileOpen(false)} className="text-sm text-muted-foreground">FAQ</a>
            <a
              href="#waitlist"
              onClick={() => setMobileOpen(false)}
              className="rounded-lg bg-primary px-5 py-2 text-center text-sm font-medium text-primary-foreground"
            >
              Join Waitlist
            </a>
          </div>
        </div>
      )}
    </header>
  )
}
