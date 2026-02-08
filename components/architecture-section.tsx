const modules = [
  {
    name: "core/ledger.py",
    description:
      "Paper trading ledger with proper peak-to-trough max drawdown tracking, equity history, and trade lifecycle management.",
    tag: "Fixed",
  },
  {
    name: "core/risk.py",
    description:
      "Risk engine with per-trade checks, portfolio exposure limits, leverage guards, and automatic kill switch on drawdown breach.",
    tag: "Upgraded",
  },
  {
    name: "strategies/momentum.py",
    description:
      "EMA crossover strategy with ATR-based position sizing, trailing stops, and aggressiveness-dependent entry filters.",
    tag: "Rewritten",
  },
  {
    name: "core/config.py",
    description:
      "Risk profiles with six parameters each (risk_pct, ATR multiple, max position, drawdown kill switch, trailing stop, RSI cap).",
    tag: "Updated",
  },
  {
    name: "dashboard/app.py",
    description:
      "Streamlit backtest dashboard. Fixed double-execution bug where signals were being acted on twice per bar.",
    tag: "Fixed",
  },
  {
    name: "core/indicators.py",
    description:
      "Technical indicator calculations: EMA, RSI, ATR, MACD, VWAP. Pure numpy, no external TA library dependency.",
    tag: "Stable",
  },
]

const tagColors: Record<string, string> = {
  Fixed: "text-success bg-success/10",
  Upgraded: "text-primary bg-primary/10",
  Rewritten: "text-warning bg-warning/10",
  Updated: "text-primary bg-primary/10",
  Stable: "text-muted-foreground bg-secondary",
}

export function ArchitectureSection() {
  return (
    <section id="architecture" className="border-b border-border py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mb-12">
          <h2 className="text-2xl font-bold tracking-tight text-foreground md:text-3xl">
            Module Architecture
          </h2>
          <p className="mt-3 max-w-2xl text-muted-foreground">
            Event-driven design where the strategy processes bars, manages its
            own state, and executes trades through the ledger. No duplicate
            execution paths.
          </p>
        </div>
        <div className="space-y-3">
          {modules.map((mod) => (
            <div
              key={mod.name}
              className="flex flex-col gap-3 rounded-lg border border-border bg-card p-5 sm:flex-row sm:items-start sm:justify-between"
            >
              <div className="flex-1">
                <div className="flex items-center gap-3">
                  <h3 className="font-mono text-sm font-semibold text-foreground">
                    {mod.name}
                  </h3>
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
                      tagColors[mod.tag] || "text-muted-foreground bg-secondary"
                    }`}
                  >
                    {mod.tag}
                  </span>
                </div>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {mod.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-lg border border-border bg-card p-6">
          <h3 className="mb-4 text-sm font-semibold text-foreground">
            Data Flow
          </h3>
          <div className="flex flex-wrap items-center gap-3 font-mono text-sm">
            <span className="rounded-md bg-secondary px-3 py-1.5 text-secondary-foreground">
              DataLoader
            </span>
            <span className="text-muted-foreground" aria-hidden="true">
              {"\u2192"}
            </span>
            <span className="rounded-md bg-secondary px-3 py-1.5 text-secondary-foreground">
              Candle Bars
            </span>
            <span className="text-muted-foreground" aria-hidden="true">
              {"\u2192"}
            </span>
            <span className="rounded-md bg-primary/10 px-3 py-1.5 text-primary">
              Strategy.on_bar()
            </span>
            <span className="text-muted-foreground" aria-hidden="true">
              {"\u2192"}
            </span>
            <span className="rounded-md bg-secondary px-3 py-1.5 text-secondary-foreground">
              Indicators
            </span>
            <span className="text-muted-foreground" aria-hidden="true">
              {"\u2192"}
            </span>
            <span className="rounded-md bg-primary/10 px-3 py-1.5 text-primary">
              Position Sizing
            </span>
            <span className="text-muted-foreground" aria-hidden="true">
              {"\u2192"}
            </span>
            <span className="rounded-md bg-success/10 px-3 py-1.5 text-success">
              Ledger
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}
