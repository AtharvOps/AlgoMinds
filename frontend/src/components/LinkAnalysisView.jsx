import React, { useState, useEffect } from 'react';
import { Network, AlertTriangle, Users, MapPin, Building2 } from 'lucide-react';
import { apiService } from '../services/api';
import ErrorBoundary from './ErrorBoundary';

const LinkAnalysisView = () => {
  const [sharedAttributes, setSharedAttributes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [escalatedClusters, setEscalatedClusters] = useState(new Set());

  // Calculate network risk score
  const calculateNetworkScore = () => {
    if (sharedAttributes.length === 0) return 0;
    
    let score = 0;
    sharedAttributes.forEach(attr => {
      if (attr.riskScore >= 90) score += 30;
      else if (attr.riskScore >= 80) score += 20;
      else if (attr.riskScore >= 70) score += 10;
      
      // Additional risk factors
      if (attr.claimIds && attr.claimIds.length > 5) score += 15;
      if (attr.type === 'Bank Account Hash') score += 10;
      if (attr.type === 'Customer IP') score += 5;
    });
    
    return Math.min(score, 100);
  };

  const getRiskLevel = (score) => {
    if (score >= 80) return { level: 'CRITICAL', color: 'text-red-500', bg: 'bg-red-500/10' };
    if (score >= 60) return { level: 'HIGH', color: 'text-orange-500', bg: 'bg-orange-500/10' };
    if (score >= 40) return { level: 'MEDIUM', color: 'text-yellow-500', bg: 'bg-yellow-500/10' };
    return { level: 'LOW', color: 'text-green-500', bg: 'bg-green-500/10' };
  };

  const networkScore = calculateNetworkScore();
  const riskLevel = getRiskLevel(networkScore);

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        const data = await apiService.getSharedAttributes();
        setSharedAttributes(data);
      } catch (error) {
        console.error('Failed to load shared attributes:', error);
        // Set empty array to show no data instead of dummy data
        setSharedAttributes([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const handleEscalate = async (clusterId) => {
    try {
      await apiService.escalateCluster(clusterId);
      setEscalatedClusters(prev => new Set(prev).add(clusterId));
    } catch (error) {
      console.error('Failed to escalate cluster:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-400">Analyzing claim connections...</div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="space-y-6">
        {/* Header */}
        <div className="rounded-3xl border border-slate-800/70 bg-slate-950/90 p-8 shadow-[0_20px_80px_rgba(15,23,42,0.55)]">
          <div className="flex items-center gap-4">
            <div className="rounded-2xl bg-sky-500/15 p-3">
              <Network className="h-6 w-6 text-sky-400" />
            </div>
            <div>
              <h1 className="text-3xl font-semibold tracking-tight text-slate-100">
                Network Link Analysis
              </h1>
              <p className="mt-2 text-sm text-slate-400">
                Detect and analyze shared attribute clusters across multiple claims for potential collusion patterns.
              </p>
            </div>
          </div>
        </div>

        {/* Netflix-style Network Score Card */}
        <div className="rounded-3xl border border-slate-800/70 bg-slate-950/90 p-8 shadow-[0_20px_80px_rgba(15,23,42,0.55)]">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-slate-100">Network Risk Score</h2>
              <p className="mt-1 text-sm text-slate-400">
                AI-powered fraud network analysis based on shared attribute patterns
              </p>
            </div>
            <div className={`rounded-2xl px-6 py-4 ${riskLevel.bg}`}>
              <div className={`text-4xl font-bold ${riskLevel.color}`}>
                {networkScore}
              </div>
              <div className={`text-sm font-semibold ${riskLevel.color}`}>
                {riskLevel.level}
              </div>
            </div>
          </div>
          
          {/* Risk Indicators */}
          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-slate-800/50 bg-slate-900/50 p-4">
              <div className="text-sm text-slate-400">Active Clusters</div>
              <div className="mt-2 text-2xl font-semibold text-slate-100">
                {sharedAttributes.length}
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800/50 bg-slate-900/50 p-4">
              <div className="text-sm text-slate-400">High Risk Clusters</div>
              <div className="mt-2 text-2xl font-semibold text-red-400">
                {sharedAttributes.filter(attr => attr.riskScore >= 80).length}
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800/50 bg-slate-900/50 p-4">
              <div className="text-sm text-slate-400">Escalated</div>
              <div className="mt-2 text-2xl font-semibold text-amber-400">
                {escalatedClusters.size}
              </div>
            </div>
          </div>
        </div>

        {/* Shared Attributes Cards - Single Row Scrolling */}
        <div className="overflow-x-auto pb-4">
          <div className="flex gap-6 min-w-max">
            {sharedAttributes.map((attribute) => {
              const IconComponent = attribute.icon;
              const isEscalated = escalatedClusters.has(attribute.id);
              
              return (
                <div
                  key={attribute.id}
                  className={`flex-shrink-0 rounded-3xl border bg-slate-950/95 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.45)] transition-all duration-300 ${
                    isEscalated 
                      ? 'border-amber-500/50 bg-amber-500/5' 
                      : 'border-slate-800/70 hover:border-slate-700/50'
                  }`}
                  style={{ minWidth: '320px', maxWidth: '320px' }}
                >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`rounded-2xl p-2 ${
                      attribute.type === 'Bank Account Hash' ? 'bg-blue-500/15' :
                      attribute.type === 'Customer IP' ? 'bg-green-500/15' :
                      'bg-purple-500/15'
                    }`}>
                      <IconComponent className={`h-5 w-5 ${
                        attribute.type === 'Bank Account Hash' ? 'text-blue-400' :
                        attribute.type === 'Customer IP' ? 'text-green-400' :
                        'text-purple-400'
                      }`} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-100">{attribute.type}</h3>
                      <p className="text-sm text-slate-400">{attribute.description}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-2xl font-bold ${
                      attribute.riskScore >= 90 ? 'text-red-400' :
                      attribute.riskScore >= 80 ? 'text-amber-400' :
                      'text-emerald-400'
                    }`}>
                      {attribute.riskScore}
                    </div>
                    <p className="text-xs text-slate-500">Risk Score</p>
                  </div>
                </div>

                <div className="mt-4 space-y-3">
                  <div>
                    <p className="text-xs font-medium text-slate-500 uppercase tracking-[0.12em]">Shared Value</p>
                    <p className="mt-1 font-mono text-sm text-slate-300">{attribute.value}</p>
                  </div>
                  
                  <div>
                    <p className="text-xs font-medium text-slate-500 uppercase tracking-[0.12em]">Connected Claims</p>
                    <div className="mt-2 flex flex-wrap gap-1">
                      {attribute.claimIds.map(claimId => (
                        <span
                          key={claimId}
                          className="rounded-full bg-slate-800 px-2 py-1 text-xs font-medium text-slate-300"
                        >
                          {claimId}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => handleEscalate(attribute.id)}
                    disabled={isEscalated}
                    className={`inline-flex items-center justify-center rounded-2xl px-4 py-2 text-sm font-semibold transition-all duration-200 ${
                      isEscalated
                        ? 'bg-amber-500 text-white cursor-not-allowed'
                        : 'bg-rose-500 text-white shadow-lg shadow-rose-500/20 hover:bg-rose-400 focus:outline-none focus:ring-2 focus:ring-rose-300'
                    }`}
                  >
                    {isEscalated ? (
                      <>
                        <AlertTriangle className="mr-2 h-4 w-4" />
                        Escalated
                      </>
                    ) : (
                      'Escalate Cluster'
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      </div>
    </ErrorBoundary>
  );
};

export default LinkAnalysisView;
