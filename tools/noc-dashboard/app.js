// ── Clock ──────────────────────────────────────────────────────────────────
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) +
    ' | ' + now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
}
setInterval(updateClock, 1000);
updateClock();

// ── State ──────────────────────────────────────────────────────────────────
let ticketCounter = 1000;
let tickets = [];
let activeTicketId = null;

const STATUSES = ['Open', 'Active', 'Escalated', 'Resolved'];

// ── Seed Tickets ───────────────────────────────────────────────────────────
const seedTickets = [
  {
    client: 'Hartwell Medical Group',
    service: 'Fiber Internet',
    issue: 'Client reports complete loss of internet connectivity at their main campus. All staff affected. EMR system unreachable.',
    priority: 'P1',
    status: 'Escalated',
    notes: [
      { ts: '09:14', text: 'Confirmed signal loss at ONT. Dispatched field tech. Escalated to Transport team.' }
    ]
  },
  {
    client: 'Suncoast Law Partners',
    service: 'VoIP / SIP Trunking',
    issue: 'Outbound calls dropping after 90 seconds. Inbound unaffected. Issue began after weekend maintenance window.',
    priority: 'P2',
    status: 'Active',
    notes: [
      { ts: '10:02', text: 'Reviewed SIP logs. SIP timer mismatch suspected. Coordinating with Unified Comms team.' }
    ]
  },
  {
    client: 'Orion Logistics LLC',
    service: 'Managed Network / SD-WAN',
    issue: 'Secondary WAN link showing degraded throughput. Primary path stable. Client monitoring alerts firing.',
    priority: 'P3',
    status: 'Open',
    notes: []
  },
  {
    client: 'Bayside Hotel & Resorts',
    service: 'Managed WiFi',
    issue: 'Guest WiFi portal intermittently failing to authenticate users. Issue reported at Building C only.',
    priority: 'P3',
    status: 'Open',
    notes: []
  },
  {
    client: 'Pinnacle Financial Services',
    service: 'Ethernet / MPLS',
    issue: 'Latency spike reported between branch offices. Round-trip time elevated from 4ms to 38ms.',
    priority: 'P2',
    status: 'Resolved',
    notes: [
      { ts: '08:30', text: 'Identified congested CE router interface. QoS policy reapplied. Latency normalized. Client confirmed resolution.' }
    ]
  }
];

seedTickets.forEach(t => addTicket(t));

// ── Ticket Functions ───────────────────────────────────────────────────────
function addTicket({ client, service, issue, priority, status = 'Open', notes = [] }) {
  const id = 'TKT-' + (++ticketCounter);
  const created = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  tickets.unshift({ id, client, service, issue, priority, status, notes, created });
  renderTickets();
}

function renderTickets() {
  const list = document.getElementById('ticket-list');
  list.innerHTML = '';
  tickets.forEach(t => {
    const card = document.createElement('div');
    card.className = 'ticket-card';
    card.innerHTML = `
      <div class="ticket-top">
        <span class="ticket-id">${t.id}</span>
        <div style="display:flex;gap:.3rem;">
          <span class="badge badge-${t.priority}">${t.priority}</span>
          <span class="status-badge status-${t.status}">${t.status}</span>
        </div>
      </div>
      <div class="ticket-client">${t.client}</div>
      <div class="ticket-service">${t.service} &mdash; <span style="color:#8b949e;font-size:.75rem;">${t.created}</span></div>
      <div class="ticket-preview">${t.issue}</div>
    `;
    card.addEventListener('click', () => openTicketModal(t.id));
    list.appendChild(card);
  });
}

function openTicketModal(id) {
  const t = tickets.find(x => x.id === id);
  if (!t) return;
  activeTicketId = id;

  document.getElementById('modal-header').innerHTML = `
    <span class="badge badge-${t.priority}" style="margin-right:.5rem;">${t.priority}</span>
    ${t.id} — ${t.client}
    <div style="margin-top:.4rem;font-size:.8rem;font-weight:400;color:var(--muted);">${t.service}</div>
  `;

  renderModalBody(t);

  const actions = document.getElementById('modal-actions');
  actions.innerHTML = '';
  if (t.status !== 'Active' && t.status !== 'Resolved')
    actions.appendChild(makeBtn('Mark Active', 'btn-active', () => changeStatus(id, 'Active')));
  if (t.status !== 'Escalated' && t.status !== 'Resolved')
    actions.appendChild(makeBtn('Escalate', 'btn-escalate', () => changeStatus(id, 'Escalated')));
  if (t.status !== 'Resolved')
    actions.appendChild(makeBtn('Resolve', 'btn-resolve', () => changeStatus(id, 'Resolved')));
  actions.appendChild(makeBtn('Add Note', 'btn-note', () => promptNote(id)));

  document.getElementById('modal-overlay').classList.remove('hidden');
}

function renderModalBody(t) {
  const notesHtml = t.notes.map(n =>
    `<div class="note-entry"><span class="note-ts">${n.ts}</span>${n.text}</div>`
  ).join('');

  document.getElementById('modal-body').innerHTML = `
    <p><strong>Status:</strong> <span class="status-badge status-${t.status}">${t.status}</span></p>
    <p style="margin-top:.5rem;"><strong>Issue:</strong><br>${t.issue}</p>
    ${notesHtml ? `<div style="margin-top:.75rem;"><strong>Activity Log:</strong>${notesHtml}</div>` : ''}
  `;
}

function makeBtn(label, cls, fn) {
  const b = document.createElement('button');
  b.textContent = label;
  b.className = cls;
  b.addEventListener('click', fn);
  return b;
}

function changeStatus(id, newStatus) {
  const t = tickets.find(x => x.id === id);
  if (!t) return;
  const ts = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  t.status = newStatus;
  t.notes.push({ ts, text: `Status changed to ${newStatus}.` });
  renderTickets();
  openTicketModal(id);
}

function promptNote(id) {
  const text = window.prompt('Enter note / update:');
  if (!text || !text.trim()) return;
  const t = tickets.find(x => x.id === id);
  if (!t) return;
  const ts = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  t.notes.push({ ts, text: text.trim() });
  renderModalBody(t);
}

document.getElementById('modal-close').addEventListener('click', () => {
  document.getElementById('modal-overlay').classList.add('hidden');
  activeTicketId = null;
  renderTickets();
});

// ── New Ticket Form ────────────────────────────────────────────────────────
document.getElementById('new-ticket-btn').addEventListener('click', () => {
  document.getElementById('ticket-form').classList.remove('hidden');
});
document.getElementById('tf-cancel').addEventListener('click', () => {
  document.getElementById('ticket-form').classList.add('hidden');
  clearForm();
});
document.getElementById('tf-submit').addEventListener('click', () => {
  const client   = document.getElementById('tf-client').value.trim();
  const service  = document.getElementById('tf-service').value.trim();
  const issue    = document.getElementById('tf-issue').value.trim();
  const priority = document.getElementById('tf-priority').value;
  if (!client || !service || !issue) { alert('Please fill in all fields.'); return; }
  addTicket({ client, service, issue, priority });
  document.getElementById('ticket-form').classList.add('hidden');
  clearForm();
});
function clearForm() {
  ['tf-client','tf-service','tf-issue'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('tf-priority').value = 'P3';
}

// ── Network Devices ────────────────────────────────────────────────────────
const devices = [
  { name: 'Core-RTR-ORL-01', type: 'Core Router', status: 'up',   meta: 'Cisco ASR 1002X | BGP Active' },
  { name: 'Core-RTR-ORL-02', type: 'Core Router', status: 'up',   meta: 'Cisco ASR 1002X | BGP Active' },
  { name: 'Dist-SW-ORL-01',  type: 'Distribution Switch', status: 'up',   meta: 'Catalyst 9300 | OSPF Area 0' },
  { name: 'Dist-SW-ORL-02',  type: 'Distribution Switch', status: 'warn', meta: 'Catalyst 9300 | High CPU 87%' },
  { name: 'Fiber-Node-A1',   type: 'Fiber Node',   status: 'up',   meta: 'Rx: -4.2 dBm | Tx: -1.1 dBm' },
  { name: 'Fiber-Node-B3',   type: 'Fiber Node',   status: 'down', meta: 'Signal Loss — Fault Active' },
  { name: 'VoIP-GW-ORL-01',  type: 'VoIP Gateway', status: 'up',   meta: 'SIP Sessions: 142/500' },
  { name: 'SDWAN-HUB-01',    type: 'SD-WAN Hub',   status: 'warn', meta: 'Secondary path degraded' },
  { name: 'WiFi-CTRL-01',    type: 'WiFi Controller', status: 'up', meta: 'APs Online: 84/86' },
  { name: 'MPLS-PE-ORL-01',  type: 'MPLS PE Router', status: 'up', meta: 'L3VPN Peers: 12 | Active' },
];

function renderDevices() {
  const grid = document.getElementById('device-grid');
  grid.innerHTML = '';
  devices.forEach(d => {
    const dotCls = d.status === 'up' ? 'dot-up' : d.status === 'warn' ? 'dot-warn' : 'dot-down';
    const label  = d.status === 'up' ? 'Operational' : d.status === 'warn' ? 'Degraded' : 'Down';
    const card   = document.createElement('div');
    card.className = 'device-card';
    card.innerHTML = `
      <div class="device-name">${d.name}</div>
      <div class="device-type">${d.type}</div>
      <div class="device-status">
        <span class="dot ${dotCls}"></span>
        <span>${label}</span>
      </div>
      <div class="device-meta">${d.meta}</div>
    `;
    grid.appendChild(card);
  });
}

document.getElementById('refresh-btn').addEventListener('click', () => {
  // Simulate minor status flicker to feel live
  devices.forEach(d => {
    if (d.status === 'up' && Math.random() < 0.1) d._flash = true;
  });
  renderDevices();
});

renderDevices();

// ── Client Records ─────────────────────────────────────────────────────────
const clients = [
  {
    name: 'Hartwell Medical Group',
    contact: 'Mark Yuen — IT Director',
    account: 'ENT-004821',
    services: ['Fiber Internet (1Gbps)', 'Managed Security', 'Unified Communications'],
    note: 'HIPAA environment. Maintenance windows require 72hr notice. On-call escalation path documented.'
  },
  {
    name: 'Suncoast Law Partners',
    contact: 'Diane Reyes — Office Manager',
    account: 'ENT-003317',
    services: ['SIP Trunking (50 channels)', 'Business TV', 'Ethernet 500M'],
    note: 'SLA: 4-hour response. Sensitive to call quality issues during business hours (M–F 8am–6pm).'
  },
  {
    name: 'Orion Logistics LLC',
    contact: 'Carlos Webb — Network Admin',
    account: 'ENT-005540',
    services: ['SD-WAN (5 sites)', 'Managed Network', 'Fiber 500M'],
    note: '24/7 operations. Dual WAN configured for failover. Customer manages CE routers independently.'
  },
  {
    name: 'Bayside Hotel & Resorts',
    contact: 'Sandra Kim — IT Manager',
    account: 'ENT-007102',
    services: ['Managed WiFi (86 APs)', 'Fiber 1Gbps', 'Business TV'],
    note: 'High-density WiFi environment. Guest SSID isolated from corporate. Renovations Q3 2026 — may require AP additions.'
  },
  {
    name: 'Pinnacle Financial Services',
    contact: 'James Ortiz — CISO',
    account: 'ENT-002299',
    services: ['MPLS / L3VPN', 'Ethernet 1Gbps', 'Managed Security'],
    note: 'PCI-DSS environment. All changes require change ticket and CISO approval. No remote access without MFA confirmation.'
  }
];

function renderClients() {
  const list = document.getElementById('client-list');
  list.innerHTML = '';
  clients.forEach(c => {
    const card = document.createElement('div');
    card.className = 'client-card';
    card.innerHTML = `
      <div class="client-name">${c.name}</div>
      <div class="client-info">
        <span>${c.contact}</span><br>
        <span>Account: ${c.account}</span><br>
        <span style="font-style:italic;">${c.note}</span>
      </div>
      <div class="client-services">
        ${c.services.map(s => `<span class="svc-tag">${s}</span>`).join('')}
      </div>
    `;
    list.appendChild(card);
  });
}
renderClients();

// ── Runbooks ───────────────────────────────────────────────────────────────
const runbooks = [
  {
    title: 'Fiber / ONT Signal Loss',
    steps: [
      '<strong>Verify scope:</strong> Confirm whether signal loss is at the ONT, the demarcation point, or further upstream.',
      '<strong>Check optical levels:</strong> Rx power should be between -8 dBm and -27 dBm. Values outside this range indicate fiber fault.',
      '<strong>Isolate:</strong> Determine if issue is single-client or affects multiple customers on the same node (node outage vs. drop fault).',
      '<strong>Ping test:</strong> Attempt ICMP ping to customer CPE. If no response, confirm no physical layer on ONT.',
      '<strong>Escalate to Transport:</strong> If fiber fault confirmed, open transport ticket and dispatch field tech. Provide pole/strand location if available.',
      '<strong>Notify client:</strong> Set expectations with ETA and ticket number. Update every 30 minutes for P1.'
    ]
  },
  {
    title: 'VoIP / SIP Call Dropping',
    steps: [
      '<strong>Gather info:</strong> Direction affected (inbound/outbound/both), duration before drop, affected DIDs, sample call IDs.',
      '<strong>Review SIP logs:</strong> Look for BYE messages, 408 Timeout, 487 Request Terminated, or missing re-INVITEs.',
      '<strong>Check timer settings:</strong> SIP session timers (Session-Expires header) must match between client PBX and Spectrum gateway.',
      '<strong>Firewall/NAT review:</strong> Confirm RTP ports (10000–20000 UDP) and SIP port 5060 are not being blocked or NAT\'d incorrectly.',
      '<strong>QoS verification:</strong> Voice traffic should be marked DSCP EF (46). Confirm QoS policy is applied end-to-end.',
      '<strong>Coordinate:</strong> If PBX-side, loop in client\'s UC admin. If trunk-side, escalate to Unified Communications team.'
    ]
  },
  {
    title: 'WAN / Ethernet Link Down',
    steps: [
      '<strong>Confirm layer 1:</strong> Check physical link status on CPE and PE router. Look for CRC errors, input errors, or interface flaps.',
      '<strong>Layer 2 check:</strong> Verify VLAN tagging, encapsulation (dot1q vs. QinQ), and MAC learning on the switch port.',
      '<strong>Layer 3 check:</strong> Confirm routing protocol (OSPF/BGP) adjacency status. Check if default route is being received.',
      '<strong>Traffic test:</strong> Run throughput test from Spectrum test endpoint. Compare against committed information rate (CIR).',
      '<strong>Trace route:</strong> Identify where packets are being dropped. Note any asymmetric routing.',
      '<strong>Escalate:</strong> If issue is in Spectrum network, open NOC ticket with circuit ID and affected interface. Target restoration per SLA.'
    ]
  },
  {
    title: 'Managed WiFi — Authentication Failure',
    steps: [
      '<strong>Scope the issue:</strong> Identify affected SSID (guest vs. corporate), AP locations, and whether issue is intermittent or total failure.',
      '<strong>Check captive portal:</strong> Verify captive portal controller is reachable and certificate is valid (not expired).',
      '<strong>RADIUS check:</strong> If using 802.1X, confirm RADIUS server is up and responding. Check shared secret matches on AP and RADIUS.',
      '<strong>DHCP scope:</strong> Confirm DHCP pool for the SSID is not exhausted. Check lease time and available addresses.',
      '<strong>AP association logs:</strong> Review controller logs for deauth/disassociation reason codes.',
      '<strong>Remediate or escalate:</strong> Apply fix if in scope (portal config, DHCP expansion). Otherwise escalate to Managed WiFi team with controller logs.'
    ]
  },
  {
    title: 'MPLS / VPN Latency Spike',
    steps: [
      '<strong>Baseline comparison:</strong> Confirm normal RTT between affected sites. Anything >10ms above baseline warrants investigation.',
      '<strong>Identify path:</strong> Traceroute between site PEs to identify where delay is introduced. Note any PE-to-P or P-to-PE hops with high latency.',
      '<strong>Interface utilization:</strong> Check ingress/egress bandwidth on affected CE and PE interfaces. Congestion often causes latency.',
      '<strong>QoS policy:</strong> Confirm traffic is being classified and queued correctly. Business-critical apps (voice, ERP) should be in priority queues.',
      '<strong>Check for re-routing:</strong> Confirm MPLS label switched path (LSP) has not shifted to a longer backup path.',
      '<strong>Escalate to MPLS team:</strong> Provide circuit IDs, affected sites, traceroute output, and time of onset.'
    ]
  },
  {
    title: 'Escalation Checklist',
    steps: [
      '<strong>Document before escalating:</strong> Capture all troubleshooting steps taken, test results, and timeline of events.',
      '<strong>Identify circuit/account:</strong> Include Spectrum circuit ID, account number, and affected service.',
      '<strong>Determine escalation path:</strong> Transport → fiber/ONT issues | UC Team → voice/SIP | MPLS Team → routing/VPN | Field Ops → physical dispatch.',
      '<strong>Set client expectations:</strong> Communicate escalation status, new point of contact, and updated ETA before handing off.',
      '<strong>Bridge call if P1:</strong> Initiate 3-way bridge with client, escalation team, and yourself for P1 tickets.',
      '<strong>Own the ticket:</strong> Stay on the ticket even after escalating. You are still the client\'s primary contact.'
    ]
  }
];

function renderRunbooks() {
  const list = document.getElementById('runbook-list');
  list.innerHTML = '';
  runbooks.forEach((rb, i) => {
    const item = document.createElement('div');
    item.className = 'runbook-item';
    item.innerHTML = `<span class="runbook-title">${rb.title}</span><span class="runbook-arrow">&#8250;</span>`;
    item.addEventListener('click', () => openRunbook(i));
    list.appendChild(item);
  });
}

function openRunbook(i) {
  const rb = runbooks[i];
  document.getElementById('rb-title').textContent = rb.title;
  const ol = document.getElementById('rb-steps');
  ol.innerHTML = rb.steps.map(s => `<li>${s}</li>`).join('');
  document.getElementById('runbook-overlay').classList.remove('hidden');
}
document.getElementById('rb-close').addEventListener('click', () => {
  document.getElementById('runbook-overlay').classList.add('hidden');
});

renderRunbooks();
