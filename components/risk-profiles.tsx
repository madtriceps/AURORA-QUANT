const profiles = [
  {
    name: "Conservative",
    description: "Lowest risk per trade, widest stops, strictest entry filters",
    params: [
      { label: "Risk per Trade", value: "0.5%" },
      { label: "ATR Stop Multiple", value: "2.5x" },
      { label: "Max Position", value: "10% of equity" },
      { label: "Trailing Stop", value: "2.0x ATR" },
      { label: "RSI Entry Cap", value: "<60" },
      { label: "Kill Switch", value: "10% drawdown" },
    ],
  },
  {
    name: "Moderate",
    description: "Balanced risk and reward, default configuration",
    highlight: true,
    params: [
      { label: "Risk per Trade", value: "1.0%" },
      { label: "ATR Stop Multiple", value: "2.0x" },
      { label: "Max Position", value: "15% of equity" },
      { label: "Trailing Stop", value: "1.75x ATR" },
      { label: "RSI Entry Cap", value: "<70" },
      { label: "Kill Switch", value: "15% drawdown" },
    ],
  },
  {
    name: "Aggressive",
    description: "Higher risk tolerance, tighter stops, more permissive entries",
    params: [
      { label: "Risk per Trade", value: "2.0%" },
      { label: "ATR Stop Multiple", value: "1.5x" },
      { label: "Max Position", value: "20% of equity" },
      { label: "Trailing Stop", value: "1.5x ATR" },
      { label: "RSI Entry Cap", value: "<75" },
      { label: "Kill Switch", value: "25% drawdown" },
    ],
  },
]

export function RiskProfiles() {
  return (
    <section id="risk" className="border-b border-border py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mb-12">
          <h2 className="text-2xl font-bold tracking-tight text-foreground md:text-3xl">
            Risk Profiles
          </h2>
          <p className="mt-3 max-w-2xl text-muted-foreground">
            Each profile now changes six independent parameters -- not just
            position size. Conservative mode takes fewer trades with smaller
            positions; aggressive mode is more permissive but has a wider kill
            switch.
          </p>
        </div>
        <div className="grid gap-6 lg:grid-cols-3">
          {profiles.map((profile) => (
            <div
              key={profile.name}
              className={`rounded-lg border p-6 ${
                profile.highlight
                  ? "border-primary bg-primary/5"
                  : "border-border bg-card"
              }`}
            >
              <div className="mb-6">
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-semibold text-foreground">
                    {profile.name}
                  </h3>
                  {profile.highlight && (
                    <span className="rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
                      Default
                    </span>
                  )}
                </div>
                <p className="mt-2 text-sm text-muted-foreground">
                  {profile.description}
                </p>
              </div>
              <div className="space-y-3">
                {profile.params.map((param) => (
                  <div
                    key={param.label}
                    className="flex items-center justify-between"
                  >
                    <span className="text-sm text-muted-foreground">
                      {param.label}
                    </span>
                    <span className="font-mono text-sm text-foreground">
                      {param.value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-lg border border-border bg-card p-6">
          <h3 className="mb-3 text-sm font-semibold text-foreground">
            Position Sizing Formula
          </h3>
          <div className="rounded-md bg-muted p-4">
            <code className="font-mono text-sm leading-relaxed text-secondary-foreground">
              <span className="text-primary">stop_distance</span> = ATR *
              atr_stop_multiple
              <br />
              <span className="text-primary">position_size</span> = (equity *
              risk_pct) / stop_distance
              <br />
              <span className="text-primary">max_cap</span> = equity *
              max_exposure_pct / price
              <br />
              <span className="text-muted-foreground">
                {"// size = min(position_size, max_cap, affordable)"}
              </span>
            </code>
          </div>
        </div>
      </div>
    </section>
  )
}
