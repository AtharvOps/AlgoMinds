import React from 'react'

const SidebarNavigation = ({ sections, activeSection, onSelectSection, children }) => {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)]">
        <aside className="flex flex-col justify-between border-r border-slate-200 bg-slate-950 px-6 py-8 text-slate-100 shadow-xl shadow-slate-950/20">
          <div>
            <div className="mb-10">
              <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Enterprise ERP</p>
              <h1 className="mt-4 text-2xl font-semibold text-white">Navigation</h1>
            </div>

            <nav className="space-y-2">
              {sections.map((item) => (
                <button
                  key={item.key}
                  type="button"
                  onClick={() => onSelectSection(item.key)}
                  className={`block w-full rounded-3xl px-4 py-3 text-left text-sm font-medium transition ${
                    activeSection === item.key
                      ? 'bg-slate-100 text-slate-950'
                      : 'hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </nav>
          </div>

          <footer className="rounded-3xl border border-slate-800/80 bg-slate-900 px-5 py-4 text-sm shadow-inner shadow-slate-950/10">
            <p className="text-slate-500">System Status</p>
            <div className="mt-2 inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-2 text-emerald-300">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
              <span className="font-semibold">Secure</span>
            </div>
          </footer>
        </aside>

        <main className="bg-slate-50 p-8">
          {children}
        </main>
      </div>
    </div>
  )
}

export default SidebarNavigation
