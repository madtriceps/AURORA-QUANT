export function HeroSection() {
  return (
    <section className="relative overflow-hidden border-b border-border">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--color-primary)_0%,_transparent_50%)] opacity-5" />
      <div className="relative mx-auto max-w-6xl px-6 py-24 text-center md:py-32">
        <div className="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-secondary px-4 py-1.5">
          <span className="h-2 w-2 rounded-full bg-success" />
          <span className="text-xs font-medium text-secondary-foreground">
            v4.0 -- ATR Risk-Managed Momentum
          </span>
        </div>
        <h1 className="mx-auto max-w-3xl text-balance text-4xl font-bold tracking-tight text-foreground md:text-5xl lg:text-6xl">
          Quantitative Trading
          <br />
          <span className="text-primary">Built Right</span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-muted-foreground">
          Event-driven backtester with ATR-based position sizing, trailing stops,
          and fixed-fractional risk management. Every trade risks a precise
          percentage of equity -- not a random chunk of your account.
        </p>
        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="#metrics"
            className="inline-flex items-center rounded-md bg-primary px-6 py-3 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
          >
            View Performance
          </a>
          <a
            href="https://github.com/madtriceps/AURORA-QUANT"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center rounded-md border border-border px-6 py-3 text-sm font-medium text-foreground transition-colors hover:border-primary"
          >
            Source Code
          </a>
        </div>
      </div>
    </section>
  )
}
