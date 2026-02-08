import { WaitlistForm } from "./waitlist-form"

export function Hero() {
  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center px-6 pt-20">
      {/* Subtle radial glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute top-1/4 left-1/2 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-[0.07]"
        style={{
          background: "radial-gradient(circle, var(--color-primary) 0%, transparent 70%)",
        }}
      />

      <div className="relative z-10 mx-auto flex max-w-3xl flex-col items-center text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-secondary px-4 py-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-primary" />
          <span className="text-xs font-medium tracking-wide text-muted-foreground uppercase">
            Early Access
          </span>
        </div>

        <h1 className="text-balance text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl lg:text-6xl">
          Automated Trading for the Crypto Markets
        </h1>

        <p className="mt-6 max-w-xl text-pretty text-lg leading-relaxed text-muted-foreground">
          Institutional-grade execution with built-in risk management.
          Set your parameters. Let the engine work. Stay in control.
        </p>

        <div id="waitlist" className="mt-10 w-full max-w-md">
          <WaitlistForm />
        </div>

        <p className="mt-4 text-xs text-muted-foreground">
          No spam. We notify you when early access opens.
        </p>
      </div>
    </section>
  )
}
