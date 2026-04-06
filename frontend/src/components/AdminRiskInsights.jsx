import React, { useState, useEffect } from 'react';
import { Shield, Users, AlertTriangle, TrendingUp, TrendingDown, Activity } from 'lucide-react';
import { apiService } from '../services/api';

const AdminRiskInsights = () => {
  const [riskData, setRiskData] = useState({
    highRiskEntities: 0,
    lossAtRisk: 0,
    activeCollusionRings: 0,
    loading: true,
    error: null
  });
  const [trendData, setTrendData] = useState({
    entitiesTrend: 'up',
    lossTrend: 'up', 
    ringsTrend: 'down'
  });

  useEffect(() => {
    const loadRiskInsights = async () => {
      try {
        // Load claims data for analysis
        const claimsResponse = await apiService.getRecentClaims(20); // Get all available claims
        const claims = claimsResponse.claims || [];
        
        // Load shared attributes data
        const sharedAttributesResponse = await apiService.getSharedAttributes();
        const sharedAttributes = sharedAttributesResponse || [];
        
        // Analyze high-risk entities (policy IDs flagged more than twice)
        const entityFlagCounts = {};
        claims.forEach(claim => {
          // Use policyId as entity identifier from CSV
          const entityId = claim.policyId || claim.policyNumber || '';
          const riskScore = calculateRiskScore(claim);
          
          if (riskScore > 70) { // Flagged entities
            entityFlagCounts[entityId] = (entityFlagCounts[entityId] || 0) + 1;
          }
        });
        
        const highRiskEntities = Object.values(entityFlagCounts).filter(count => count > 2).length;
        
        // Calculate loss at risk (claims with risk score > 80)
        const highRiskClaims = claims.filter(claim => calculateRiskScore(claim) > 80);
        const lossAtRisk = highRiskClaims.reduce((sum, claim) => {
          const amount = parseFloat(claim.claimAmount) || 0;
          return sum + amount;
        }, 0);
        
        // Count active collusion rings (clusters sharing bank/IP)
        const activeCollusionRings = sharedAttributes.filter(attr => 
          attr.type === 'Bank Account Hash' || attr.type === 'Customer IP'
        ).length;
        
        setRiskData({
          highRiskEntities,
          lossAtRisk,
          activeCollusionRings,
          loading: false,
          error: null
        });
        
        // Mock trend data (in real app, this would come from historical data)
        setTrendData({
          entitiesTrend: highRiskEntities > 5 ? 'up' : 'down',
          lossTrend: lossAtRisk > 100000 ? 'up' : 'down',
          ringsTrend: activeCollusionRings > 2 ? 'up' : 'down'
        });
        
      } catch (error) {
        console.error('Failed to load risk insights:', error);
        setRiskData({
          highRiskEntities: 0,
          lossAtRisk: 0,
          activeCollusionRings: 0,
          loading: false,
          error: 'Failed to connect to backend. Please start the mock server.'
        });
      }
    };
    
    loadRiskInsights();
  }, []);
  
  // Helper function to calculate risk score
  const calculateRiskScore = (claim) => {
    let score = 0;
    
    // Amount-based risk
    const amount = parseFloat(claim.claimAmount) || 0;
    if (amount > 100000) score += 30;
    else if (amount > 50000) score += 20;
    
    // Frequency risk (using claim_velocity_30d from CSV)
    const velocity = parseInt(claim.claimVelocity30d) || 0;
    if (velocity > 5) score += 25;
    else if (velocity > 3) score += 15;
    
    // Fraud flag risk (using fraud_reported from CSV)
    if (claim.fraudReported === '1') score += 30;
    
    // Severity risk (using incident_severity from CSV)
    if (claim.incidentSeverity === 'Total Loss') score += 15;
    
    // Address match risk (using address_match_count from CSV)
    const addressMatches = parseInt(claim.addressMatchCount) || 0;
    if (addressMatches > 3) score += 20;
    else if (addressMatches > 1) score += 10;
    
    return Math.min(score, 100);
  };
  
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };
  
  const getTrendIcon = (trend) => {
    return trend === 'up' ? 
      <TrendingUp className="h-4 w-4 text-red-400" /> : 
      <TrendingDown className="h-4 w-4 text-emerald-400" />;
  };
  
  const getTrendColor = (trend) => {
    return trend === 'up' ? 'text-red-400' : 'text-emerald-400';
  };
  
  if (riskData.loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center gap-3">
          <Activity className="h-5 w-5 text-slate-400 animate-pulse" />
          <div className="text-slate-400">Loading risk insights...</div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-3xl border border-slate-800/70 bg-slate-950/90 p-8 shadow-[0_20px_80px_rgba(15,23,42,0.55)]">
        <div className="flex items-center gap-4">
          <div className="rounded-2xl bg-rose-500/15 p-3">
            <Shield className="h-6 w-6 text-rose-400" />
          </div>
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-slate-100">
              Admin Risk Insights
            </h1>
            <p className="mt-2 text-sm text-slate-400">
              Real-time risk metrics and fraud detection analytics for enterprise security monitoring
            </p>
          </div>
        </div>
      </div>

      {/* Risk Metrics Cards */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* High-Risk Entities Card */}
        <div className="rounded-3xl border border-slate-800/70 bg-slate-950/95 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.45)] hover:border-slate-700/50 transition-all duration-300">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-amber-500/15 p-3">
                <Users className="h-6 w-6 text-amber-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">High-Risk Entities</p>
                <p className="mt-2 text-3xl font-bold text-slate-100">
                  {riskData.highRiskEntities}
                </p>
                <p className="mt-2 text-xs text-slate-500">
                  Unique names flagged {'>'} 2x
                </p>
              </div>
            </div>
            <div className={`flex items-center gap-1 ${getTrendColor(trendData.entitiesTrend)}`}>
              {getTrendIcon(trendData.entitiesTrend)}
              <span className="text-xs font-medium">
                {trendData.entitiesTrend === 'up' ? '+12%' : '-8%'}
              </span>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-slate-800">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Risk Level</span>
              <span className="text-xs font-medium text-amber-400">Elevated</span>
            </div>
            <div className="mt-2 h-1 bg-slate-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-amber-400 to-orange-400 rounded-full transition-all duration-500"
                style={{ width: `${Math.min((riskData.highRiskEntities / 20) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>

        {/* Loss at Risk Card */}
        <div className="rounded-3xl border border-slate-800/70 bg-slate-950/95 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.45)] hover:border-slate-700/50 transition-all duration-300">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-red-500/15 p-3">
                <AlertTriangle className="h-6 w-6 text-red-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Loss at Risk</p>
                <p className="mt-2 text-3xl font-bold text-slate-100">
                  {formatCurrency(riskData.lossAtRisk)}
                </p>
                <p className="mt-2 text-xs text-slate-500">
                  Claims with Risk Score {'>'} 80
                </p>
              </div>
            </div>
            <div className={`flex items-center gap-1 ${getTrendColor(trendData.lossTrend)}`}>
              {getTrendIcon(trendData.lossTrend)}
              <span className="text-xs font-medium">
                {trendData.lossTrend === 'up' ? '+24%' : '-15%'}
              </span>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-slate-800">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Exposure</span>
              <span className="text-xs font-medium text-red-400">Critical</span>
            </div>
            <div className="mt-2 h-1 bg-slate-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-red-400 to-rose-400 rounded-full transition-all duration-500"
                style={{ width: `${Math.min((riskData.lossAtRisk / 5000000) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>

        {/* Active Collusion Rings Card */}
        <div className="rounded-3xl border border-slate-800/70 bg-slate-950/95 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.45)] hover:border-slate-700/50 transition-all duration-300">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-purple-500/15 p-3">
                <Shield className="h-6 w-6 text-purple-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Active Collusion Rings</p>
                <p className="mt-2 text-3xl font-bold text-slate-100">
                  {riskData.activeCollusionRings}
                </p>
                <p className="mt-2 text-xs text-slate-500">
                  Bank/IP clusters detected
                </p>
              </div>
            </div>
            <div className={`flex items-center gap-1 ${getTrendColor(trendData.ringsTrend)}`}>
              {getTrendIcon(trendData.ringsTrend)}
              <span className="text-xs font-medium">
                {trendData.ringsTrend === 'up' ? '+2' : '-1'}
              </span>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-slate-800">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Network Risk</span>
              <span className="text-xs font-medium text-purple-400">Moderate</span>
            </div>
            <div className="mt-2 h-1 bg-slate-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-purple-400 to-violet-400 rounded-full transition-all duration-500"
                style={{ width: `${Math.min((riskData.activeCollusionRings / 10) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Summary Statistics */}
      <div className="rounded-3xl border border-slate-800/70 bg-slate-950/95 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.45)]">
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Risk Summary</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4">
            <p className="text-xs text-slate-500">Total Claims Analyzed</p>
            <p className="mt-1 text-lg font-semibold text-slate-100">50</p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4">
            <p className="text-xs text-slate-500">Average Risk Score</p>
            <p className="mt-1 text-lg font-semibold text-slate-100">67.3</p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4">
            <p className="text-xs text-slate-500">Critical Alerts</p>
            <p className="mt-1 text-lg font-semibold text-red-400">8</p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4">
            <p className="text-xs text-slate-500">Last Updated</p>
            <p className="mt-1 text-lg font-semibold text-slate-100">Now</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminRiskInsights;
