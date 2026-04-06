import React from 'react'

const suspectedRings = [
  { name: 'Claims Pool A', members: 8, status: 'Under review' },
  { name: 'Bank Routing Cluster', members: 5, status: 'Action needed' },
  { name: 'Address Match Group', members: 12, status: 'Monitoring' },
]

const NetworkLinkAnalysis = () => {
  return (
    <section className="grid gap-6 lg:grid-cols-[320px_minmax(0,1fr)]">
      <aside className="rounded-3xl border border-slate-800/80 bg-slate-950/95 p-6 shadow-[0_20px_60px_rgba(15,23,42,0.35)]">
        <p className="text-sm uppercase tracking-[0.28em] text-slate-400">Suspected Fraud Rings</p>
        <h2 className="mt-4 text-2xl font-semibold text-slate-100">Priority clusters</h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          Groups with overlapping IPs, addresses, and banking details flagged for network review.
        </p>

        <div className="mt-6 space-y-4">
          {suspectedRings.map((ring) => (
            <div key={ring.name} className="rounded-3xl border border-slate-800/80 bg-slate-900 p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-slate-100">{ring.name}</p>
                  <p className="mt-1 text-xs text-slate-500">{ring.members} linked claims</p>
                </div>
                <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-300">
                  {ring.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </aside>

      <div className="rounded-3xl border border-slate-800/80 bg-slate-950/95 p-6 shadow-[0_20px_60px_rgba(15,23,42,0.35)]">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Network Link Analysis</p>
            <h3 className="mt-2 text-2xl font-semibold text-slate-100">Collusion visualization</h3>
          </div>
          <div className="rounded-2xl bg-slate-900 px-4 py-2 text-sm text-slate-300">
            Data source: company database
          </div>
        </div>

        <p className="mt-4 text-sm leading-6 text-slate-400">
          Analyzing shared attributes (IP, Address, Bank Acc) to identify collusion networks within the company database.
        </p>

        <div className="mt-8 rounded-[32px] border border-slate-800/70 bg-slate-900 p-8">
          <div className="flex h-[320px] items-center justify-center rounded-3xl bg-slate-950/80">
            <svg viewBox="0 0 320 240" className="h-full w-full max-w-[28rem] max-h-[23rem]" role="img" aria-label="Network graph placeholder">
              <defs>
                <linearGradient id="nodeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#38bdf8" />
                  <stop offset="100%" stopColor="#22c55e" />
                </linearGradient>
              </defs>
              <g stroke="#475569" strokeWidth="2" fill="none">
                <line x1="60" y1="48" x2="160" y2="72" />
                <line x1="160" y1="72" x2="240" y2="40" />
                <line x1="60" y1="48" x2="100" y2="156" />
                <line x1="100" y1="156" x2="220" y2="180" />
                <line x1="220" y1="180" x2="280" y2="120" />
                <line x1="240" y1="40" x2="280" y2="120" />
              </g>
              <circle cx="60" cy="48" r="14" fill="url(#nodeGradient)" opacity="0.95" />
              <circle cx="160" cy="72" r="18" fill="url(#nodeGradient)" opacity="0.95" />
              <circle cx="240" cy="40" r="12" fill="url(#nodeGradient)" opacity="0.95" />
              <circle cx="100" cy="156" r="16" fill="url(#nodeGradient)" opacity="0.95" />
              <circle cx="220" cy="180" r="20" fill="url(#nodeGradient)" opacity="0.95" />
              <circle cx="280" cy="120" r="14" fill="url(#nodeGradient)" opacity="0.95" />
              <text x="40" y="35" fill="#cbd5e1" fontSize="10" fontWeight="600">IP Match</text>
              <text x="146" y="55" fill="#cbd5e1" fontSize="10" fontWeight="600">Address</text>
              <text x="225" y="28" fill="#cbd5e1" fontSize="10" fontWeight="600">Bank</text>
              <text x="215" y="168" fill="#cbd5e1" fontSize="10" fontWeight="600">Suspicious</text>
            </svg>
          </div>
          <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="text-sm text-slate-400">
              Placeholder for a node visualization or network graph component integration.
            </div>
            <button
              type="button"
              className="inline-flex items-center justify-center rounded-2xl bg-sky-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:bg-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-300"
            >
              Explore network details
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}

export default NetworkLinkAnalysis
