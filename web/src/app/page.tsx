export default function Home() {
  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-5xl flex-col px-6 sm:px-10">
      <header className="flex items-center justify-between border-b border-grey-200 py-5">
        <span className="font-mono text-sm font-medium tracking-[0.2em] text-ink">
          RECURVE
        </span>
        <span className="font-mono text-xs tracking-wider text-grey-500">
          v0 · scaffold
        </span>
      </header>

      <section className="flex flex-1 flex-col justify-center py-16">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-grey-500">
          Recurring-revenue analytics
        </p>
        <h1 className="mt-6 max-w-3xl font-serif text-5xl leading-[0.98] tracking-tight text-ink sm:text-7xl">
          Know your recurring revenue cold.
        </h1>
        <p className="mt-7 max-w-xl text-lg leading-relaxed text-grey-600">
          Connect Stripe and get the metrics leadership actually runs on — MRR,
          the movement waterfall, cohort retention, NRR — and the accounts about
          to churn. Every number traces back to the rows.
        </p>

        {/* numeral specimen — the type system, not product data */}
        <div className="mt-14 border-t border-grey-200 pt-6">
          <dl className="grid grid-cols-1 gap-x-12 gap-y-6 sm:grid-cols-3">
            <div>
              <dt className="text-xs uppercase tracking-wider text-grey-500">
                MRR
              </dt>
              <dd className="mt-1 font-mono text-3xl tabular-nums text-ink">
                $128,400
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-wider text-grey-500">
                Net new
              </dt>
              <dd className="mt-1 font-mono text-3xl tabular-nums text-signal-ink">
                +$4,210
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-wider text-grey-500">
                Logo churn
              </dt>
              <dd className="mt-1 font-mono text-3xl tabular-nums text-amber-ink">
                −2.1%
              </dd>
            </div>
          </dl>
          <p className="mt-5 max-w-md text-sm text-grey-500">
            Numerals are monospaced so columns align like a ledger. Figures here
            are a type specimen, not live data.
          </p>
        </div>
      </section>

      <footer className="border-t border-grey-200 py-6 text-sm text-grey-500">
        Built by Hassan Raza. Data platform in progress.
      </footer>
    </main>
  );
}
