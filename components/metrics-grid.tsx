const metrics = [
  {
    label: "Position Sizing",
    before: "20-40% of account per trade",
    after: "ATR-based: 0.5-2% risk per trade",
    improved: true,
  },
  {
    label: "Max Drawdown",
    before: "69-89%",
    after: "Target <15% (with kill switch)",
    improved: true,
  },
  {
    label: "Stop Loss",
    before: "Fixed 2x ATR (no trailing)",
    after: "Initial + trailing ATR stop",
    improved: true,
  },
  {
    label: "Profit Factor",
    before: "~1.9x",
    after: "~1.9x (logic preserved)",
    improved: false,
  },
  {
    label: "Risk Engine",
    before: "Not integrated with strategy",
    after: "Pre-trade checks + kill switch",
    improved: true,
  },
  {
    label: "Aggressiveness Modes",
    before: "Only changes position size",
    after: "Changes risk, stops, entries, caps",
    improved: true,
  },
]

export function MetricsGrid() {
  return (
    <section id="metrics" className="border-b border-border py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mb-12">
          <h2 className="text-2xl font-bold tracking-tight text-foreground md:text-3xl">
            Performance Review Fixes
          </h2>
          <p className="mt-3 max-w-2xl text-muted-foreground">
            Side-by-side comparison of what changed in v4.0 based on the
            backtest review. The core signal logic (Profit Factor ~1.9x) was
            sound -- the risk management was broken.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {metrics.map((m) => (
            <div
              key={m.label}
              className="rounded-lg border border-border bg-card p-6"
            >
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">
                  {m.label}
                </h3>
                {m.improved && (
                  <span className="rounded-full bg-success/10 px-2.5 py-0.5 text-xs font-medium text-success">
                    Fixed
                  </span>
                )}
                {!m.improved && (
                  <span className="rounded-full bg-secondary px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
                    Kept
                  </span>
                )}
              </div>
              <div className="space-y-3">
                <div>
                  <p className="mb-1 text-xs uppercase tracking-wider text-muted-foreground">
                    Before
                  </p>
                  <p className="font-mono text-sm text-danger">{m.before}</p>
                </div>
                <div>
                  <p className="mb-1 text-xs uppercase tracking-wider text-muted-foreground">
                    After
                  </p>
                  <p className="font-mono text-sm text-success">{m.after}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
