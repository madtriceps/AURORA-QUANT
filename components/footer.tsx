export function Footer() {
  return (
    <footer className="border-t border-border py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 sm:flex-row">
        <div className="flex items-center gap-3">
          <div className="flex h-6 w-6 items-center justify-center rounded bg-primary">
            <span className="text-xs font-bold text-primary-foreground">A</span>
          </div>
          <span className="text-sm text-muted-foreground">
            AURORA QUANT v4.0
          </span>
        </div>
        <p className="text-xs text-muted-foreground">
          Paper trading only. Not financial advice. Past performance does not
          guarantee future results.
        </p>
      </div>
    </footer>
  )
}
