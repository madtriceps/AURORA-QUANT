const changes = [
  {
    version: "v4.0",
    title: "ATR Risk-Managed Momentum",
    current: true,
    items: [
      "Replaced fixed position_pct (20-40%) with ATR-based position sizing formula",
      "Added trailing stop-loss that ratchets up as price makes new highs",
      "Aggressiveness now controls 6 parameters: risk%, ATR multiple, max position, trailing stop, RSI cap, kill switch",
      "Fixed max drawdown tracking to compute true peak-to-trough across entire equity curve",
      "Fixed dashboard double-execution bug (strategy.on_bar() + manual open/close)",
      "Upgraded RiskEngine with pre-trade checks, exposure limits, and kill switch with reason logging",
    ],
  },
  {
    version: "v3.0",
    title: "Simple Momentum",
    items: [
      "EMA crossover strategy (20/50 MA)",
      "RSI confirmation filters",
      "Fixed 2x ATR stop loss",
      "Profit Factor ~1.9x confirmed",
    ],
  },
  {
    version: "v2.0",
    title: "Event-Driven Architecture",
    items: [
      "Migrated from loop-based to event-driven backtesting",
      "Added PaperLedger with trade lifecycle management",
      "Streamlit dashboard for backtest visualization",
      "Multi-asset support (BTC, ETH, BNB, ADA, XRP)",
    ],
  },
]

export function ChangelogSection() {
  return (
    <section id="changelog" className="py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mb-12">
          <h2 className="text-2xl font-bold tracking-tight text-foreground md:text-3xl">
            Changelog
          </h2>
        </div>
        <div className="space-y-8">
          {changes.map((release) => (
            <div key={release.version} className="relative">
              <div className="flex items-center gap-3">
                <span
                  className={`font-mono text-sm font-bold ${
                    release.current ? "text-primary" : "text-muted-foreground"
                  }`}
                >
                  {release.version}
                </span>
                <span className="text-sm font-medium text-foreground">
                  {release.title}
                </span>
                {release.current && (
                  <span className="rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
                    Current
                  </span>
                )}
              </div>
              <ul className="mt-3 space-y-2 pl-14">
                {release.items.map((item, i) => (
                  <li
                    key={i}
                    className="text-sm leading-relaxed text-muted-foreground"
                  >
                    <span className="mr-2 text-border" aria-hidden="true">
                      {"--"}
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
