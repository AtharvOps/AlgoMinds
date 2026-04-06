const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Helper function to read claims CSV
function readClaimsCSV() {
  const csvPath = path.join(__dirname, 'backend', 'database', 'claims.csv');
  
  if (!fs.existsSync(csvPath)) {
    return [];
  }
  
  const content = fs.readFileSync(csvPath, 'utf-8');
  const lines = content.split('\n').filter(line => line.trim());
  
  if (lines.length < 2) return [];
  
  const headers = lines[0].split(',').map(h => h.trim());
  const claims = [];
  
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    if (values.length === headers.length) {
      const claim = {
        internalId: values[headers.indexOf('claim_id')] || '',
        policyNumber: values[headers.indexOf('policy_id')] || '',
        vehicleRegNo: values[headers.indexOf('vehicle_reg_no')] || '',
        claimAmount: values[headers.indexOf('claim_amount')] || '0',
        incidentType: values[headers.indexOf('incident_type')] || '',
        collisionType: values[headers.indexOf('collision_type')] || '',
        incidentSeverity: values[headers.indexOf('incident_severity')] || '',
        authoritiesContacted: values[headers.indexOf('authorities_contacted')] || '',
        incidentState: values[headers.indexOf('incident_state')] || '',
        propertyDamage: values[headers.indexOf('property_damage')] || '',
        witnesses: values[headers.indexOf('witnesses')] || '0',
        policeReportAvailable: values[headers.indexOf('police_report_available')] || '',
        autoMake: values[headers.indexOf('auto_make')] || '',
        customerIp: values[headers.indexOf('customer_ip')] || '',
        bankAccountHash: values[headers.indexOf('bank_account_hash')] || '',
        garageName: values[headers.indexOf('garage_name')] || '',
        claimVelocity30d: values[headers.indexOf('claim_velocity_30d')] || '0',
        addressMatchCount: values[headers.indexOf('address_match_count')] || '0',
        fraudReported: values[headers.indexOf('fraud_reported')] || '0',
        incidentDate: values[headers.indexOf('incident_date')] || new Date().toISOString().split('T')[0],
        submissionDate: values[headers.indexOf('submission_date')] || new Date().toISOString().split('T')[0],
        // Add derived fields for frontend compatibility
        ingestionStatus: values[headers.indexOf('fraud_reported')] === '1' ? 'Fraud Detected' : 'Pending',
        claimDate: new Date().toISOString().split('T')[0], // Current date for demo
        previousClaims: values[headers.indexOf('claim_velocity_30d')] || '0',
        policyValidity: '12', // Default value
        damageConsistency: values[headers.indexOf('fraud_reported')] === '1' ? '0' : '1',
        userPhone: '9876543210', // Mock phone number
        garageId: 'GAR001', // Mock garage ID
        garageCity: values[headers.indexOf('incident_state')] || 'Unknown',
        isFraud: values[headers.indexOf('fraud_reported')] || '0',
      };
      claims.push(claim);
    }
  }
  
  return claims.reverse(); // Most recent first
}

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'API running 🚀' });
});

app.get('/claims/recent', (req, res) => {
  const limit = parseInt(req.query.limit) || 10;
  const claims = readClaimsCSV();
  const recentClaims = claims.slice(0, limit);
  
  res.json({
    claims: recentClaims,
    count: recentClaims.length
  });
});

app.get('/link-analysis/shared-attributes', (req, res) => {
  // Read real claims data for analysis
  const claims = readClaimsCSV();
  
  // Analyze shared attributes from real data
  const sharedAttributes = [];
  
  // Bank Account Hash analysis
  const bankHashGroups = {};
  claims.forEach(claim => {
    if (claim.bankAccountHash) {
      if (!bankHashGroups[claim.bankAccountHash]) {
        bankHashGroups[claim.bankAccountHash] = [];
      }
      bankHashGroups[claim.bankAccountHash].push(claim.internalId);
    }
  });
  
  Object.keys(bankHashGroups).forEach(hash => {
    if (bankHashGroups[hash].length > 1) {
      sharedAttributes.push({
        id: `bank-${hash}`,
        type: 'Bank Account Hash',
        icon: 'Building2',
        value: hash,
        claimIds: bankHashGroups[hash],
        riskScore: bankHashGroups[hash].length >= 4 ? 91 : bankHashGroups[hash].length >= 3 ? 85 : 75,
        description: `${bankHashGroups[hash].length} claims share identical bank account hash`
      });
    }
  });
  
  // Customer IP analysis
  const ipGroups = {};
  claims.forEach(claim => {
    if (claim.customerIp) {
      if (!ipGroups[claim.customerIp]) {
        ipGroups[claim.customerIp] = [];
      }
      ipGroups[claim.customerIp].push(claim.internalId);
    }
  });
  
  Object.keys(ipGroups).forEach(ip => {
    if (ipGroups[ip].length > 1) {
      sharedAttributes.push({
        id: `ip-${ip}`,
        type: 'Customer IP',
        icon: 'MapPin',
        value: ip,
        claimIds: ipGroups[ip],
        riskScore: ipGroups[ip].length >= 3 ? 85 : 72,
        description: `${ipGroups[ip].length} claims submitted from same IP address`
      });
    }
  });
  
  // Garage Name analysis
  const garageGroups = {};
  claims.forEach(claim => {
    if (claim.garageName) {
      if (!garageGroups[claim.garageName]) {
        garageGroups[claim.garageName] = [];
      }
      garageGroups[claim.garageName].push(claim.internalId);
    }
  });
  
  Object.keys(garageGroups).forEach(garage => {
    if (garageGroups[garage].length > 2) {
      sharedAttributes.push({
        id: `garage-${garage}`,
        type: 'Garage Name',
        icon: 'Users',
        value: garage,
        claimIds: garageGroups[garage],
        riskScore: garageGroups[garage].length >= 5 ? 91 : garageGroups[garage].length >= 4 ? 85 : 78,
        description: `${garageGroups[garage].length} claims involve same repair garage`
      });
    }
  });
  
  // Sort by risk score (highest first)
  sharedAttributes.sort((a, b) => b.riskScore - a.riskScore);
  
  res.json(sharedAttributes);
});

app.post('/link-analysis/escalate/:clusterId', (req, res) => {
  const { clusterId } = req.params;
  // In real app, this would escalate the cluster to investigation team
  res.json({ 
    success: true, 
    message: `Cluster ${clusterId} escalated to investigation team`,
    timestamp: new Date().toISOString()
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.listen(PORT, '127.0.0.1', () => {
  console.log(`🚀 Mock backend server running on http://127.0.0.1:${PORT}`);
  console.log(`📊 Claims endpoint available at http://127.0.0.1:${PORT}/claims/recent`);
  console.log(`❤️  Health check at http://127.0.0.1:${PORT}/health`);
});
