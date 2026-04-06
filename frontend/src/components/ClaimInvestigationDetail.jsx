import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'

const ClaimInvestigationDetail = () => {
  const [claimData, setClaimData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadClaimData = async () => {
      try {
        const response = await apiService.getRecentClaims(1);
        const claims = response.claims || [];
        
        if (claims.length > 0) {
          const claim = claims[0];
          setClaimData({
            claimId: claim.internalId,
            policyNumber: claim.policyId || claim.policyNumber,
            claimantName: claim.policyId, // Use policy ID as identifier
            incidentDate: claim.incidentDate || new Date().toISOString().split('T')[0],
            claimType: claim.incidentType || 'Unknown',
            submissionDate: claim.submissionDate || new Date().toISOString().split('T')[0],
            amountClaimed: `$${parseFloat(claim.claimAmount || 0).toLocaleString()}`,
            status: claim.fraudReported === '1' ? 'Flagged for review' : 'Under review',
            source: 'Enterprise SQL ingestion'
          });
        }
        
        setLoading(false);
      } catch (err) {
        setError('Failed to connect to backend. Please start the mock server.');
        setLoading(false);
      }
    };

    loadClaimData();
  }, []);

  const reasoningPoints = claimData ? [
    claimData.amountClaimed && parseFloat(claimData.amountClaimed.replace(/[$,]/g, '')) > 100000 ? 'High claim amount detected' : null,
    claimData.status === 'Flagged for review' ? 'Fraud flag detected in system' : null,
    claimData.claimType === 'Total Loss' ? 'Total loss incident with high severity' : null
  ].filter(Boolean) : [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-400">Loading claim investigation data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-400">{error}</div>
      </div>
    );
  }

  if (!claimData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-400">No claim data available</div>
      </div>
    );
  }
  return (
    <section className="space-y-8 rounded-3xl border border-slate-800/80 bg-slate-950/95 p-8 shadow-[0_24px_80px_rgba(15,23,42,0.55)]">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.32em] text-slate-400">Claim Investigation Detail</p>
          <h1 className="mt-2 text-3xl font-semibold text-slate-100">Review claim flagged by fraud intelligence</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
            View the claim metadata and the ML model reasoning behind the fraud flag. Choose the investigator action after review.
          </p>
        </div>
        <div className="rounded-3xl bg-slate-900 px-5 py-4 text-sm text-slate-300">
          <p className="text-slate-400">Claim status</p>
          <p className="mt-2 text-lg font-semibold text-slate-100">{claimData.status}</p>
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-[1fr_420px]">
        <div className="rounded-3xl border border-slate-800/80 bg-slate-900 p-6">
          <div className="grid gap-4 sm:grid-cols-2">
            {Object.entries(claimData).map(([key, value]) => (
              <div key={key} className="rounded-3xl border border-slate-800/80 bg-slate-950/80 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{key.replace(/([A-Z])/g, ' $1').replace(/^./, (c) => c.toUpperCase())}</p>
                <p className="mt-3 text-base font-semibold text-slate-100">{value}</p>
              </div>
            ))}
          </div>
        </div>

        <aside className="rounded-3xl border border-slate-800/80 bg-slate-900 p-6">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.22em] text-slate-400">Model Reasoning</p>
              <h2 className="mt-2 text-xl font-semibold text-slate-100">Why this claim was flagged</h2>
            </div>
            <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-300">
              ML score: high
            </span>
          </div>

          <ul className="mt-6 space-y-3">
            {reasoningPoints.map((point) => (
              <li key={point} className="rounded-3xl border border-slate-800/80 bg-slate-950/90 p-4 text-slate-200">
                <p className="text-sm leading-6">{point}</p>
              </li>
            ))}
          </ul>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <button
              type="button"
              className="inline-flex min-w-[170px] items-center justify-center rounded-2xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-500/20 transition hover:bg-emerald-400"
            >
              Mark as Legitimate
            </button>
            <button
              type="button"
              className="inline-flex min-w-[170px] items-center justify-center rounded-2xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:border-slate-600 hover:bg-slate-700"
            >
              Escalate to Fraud Unit
            </button>
          </div>
        </aside>
      </div>
    </section>
  )
}

export default ClaimInvestigationDetail
