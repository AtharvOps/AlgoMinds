import React, { useMemo, useState } from 'react'
import ErrorBoundary from './components/ErrorBoundary'
import ClaimInvestigationDetail from './components/ClaimInvestigationDetail'
import FraudIntelligenceOverview from './components/FraudIntelligenceOverview'
import InternalDataIngestionDashboard from './components/InternalDataIngestionDashboard'
import LinkAnalysisView from './components/LinkAnalysisView'
import NetworkLinkAnalysis from './components/NetworkLinkAnalysis'
import SidebarNavigation from './components/SidebarNavigation'

const App = () => {
  const sections = useMemo(
    () => [
      { key: 'inbound', label: 'Inbound Claims', component: <InternalDataIngestionDashboard /> },
      { key: 'fraud', label: 'Fraud Analytics', component: <FraudIntelligenceOverview /> },
      { key: 'network', label: 'Network Analysis', component: <LinkAnalysisView /> },
      { key: 'links', label: 'Link Analysis', component: <NetworkLinkAnalysis /> },
      { key: 'security', label: 'Security Logs', component: <ClaimInvestigationDetail /> },
    ],
    []
  )

  const [activeSection, setActiveSection] = useState('inbound')
  const currentSection = sections.find((item) => item.key === activeSection) || sections[0]

  return (
    <ErrorBoundary>
      <SidebarNavigation
        sections={sections}
        activeSection={activeSection}
        onSelectSection={setActiveSection}
      >
        <div className="space-y-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm uppercase tracking-[0.22em] text-slate-500">Enterprise workspace</p>
            <h2 className="mt-3 text-2xl font-semibold text-slate-950">{currentSection.label}</h2>
            {currentSection.component}
          </div>
        </div>
      </SidebarNavigation>
    </ErrorBoundary>
  )
}

export default App