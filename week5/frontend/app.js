// =============================================================================
// API Helper
// =============================================================================
async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// =============================================================================
// Tab Navigation
// =============================================================================
function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  const tabContents = document.querySelectorAll('.tab-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.dataset.tab;

      // Update active tab
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      // Show corresponding content
      tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === tabName) {
          content.classList.add('active');
        }
      });

      // Load data for the tab
      loadTabData(tabName);
    });
  });
}

async function loadTabData(tabName) {
  switch (tabName) {
    case 'dashboard':
      await loadDashboard();
      break;
    case 'agents':
      await loadAgents();
      break;
    case 'timeline':
      await loadTimeline();
      break;
    case 'workflows':
      await loadWorkflows();
      break;
    case 'patterns':
      await loadPatterns();
      break;
  }
}

// =============================================================================
// Dashboard
// =============================================================================
async function loadDashboard() {
  try {
    const metrics = await fetchJSON('/api/metrics');
    document.getElementById('total-executions').textContent = metrics.total_executions;
    document.getElementById('success-rate').textContent = metrics.success_rate + '%';
    document.getElementById('avg-duration').textContent = metrics.average_duration_ms + 'ms';

    // Count active agents
    const agents = await fetchJSON('/api/agents');
    document.getElementById('active-agents').textContent = agents.length;

    // Agent metrics breakdown
    const agentMetricsDiv = document.getElementById('agent-metrics');
    agentMetricsDiv.innerHTML = '';
    for (const [agent, data] of Object.entries(metrics.executions_by_agent)) {
      const div = document.createElement('div');
      div.className = 'agent-metric-item';
      div.innerHTML = `
        <strong>${agent}</strong>
        <span>Total: ${data.total} | Success: ${data.success_rate}% | Avg: ${data.average_duration_ms}ms</span>
      `;
      agentMetricsDiv.appendChild(div);
    }
  } catch (error) {
    console.error('Failed to load dashboard:', error);
  }
}

// =============================================================================
// Agents
// =============================================================================
async function loadAgents() {
  try {
    const capabilityFilter = document.getElementById('agent-capability-filter').value;
    const patternFilter = document.getElementById('agent-pattern-filter').value;

    let url = '/api/agents';
    const params = new URLSearchParams();
    if (capabilityFilter) params.append('capability', capabilityFilter);
    if (patternFilter) params.append('pattern', patternFilter);
    if (params.toString()) url += '?' + params.toString();

    const agents = await fetchJSON(url);
    const agentsList = document.getElementById('agents-list');
    agentsList.innerHTML = '';

    agents.forEach(agent => {
      const card = document.createElement('div');
      card.className = 'agent-card';
      card.innerHTML = `
        <h3>${agent.name}</h3>
        <p>${agent.description || 'No description'}</p>
        <div class="agent-meta">
          <strong>Capabilities:</strong>
          <ul>${agent.capabilities.map(c => `<li>${c}</li>`).join('')}</ul>
        </div>
        <div class="agent-meta">
          <strong>Patterns:</strong>
          <span>${agent.coordination_patterns.map(p => `<span class="badge">${p}</span>`).join(' ')}</span>
        </div>
      `;
      card.addEventListener('click', () => showAgentDetail(agent));
      agentsList.appendChild(card);
    });

    // Populate timeline agent filter
    const timelineAgentFilter = document.getElementById('timeline-agent-filter');
    const currentValue = timelineAgentFilter.value;
    timelineAgentFilter.innerHTML = '<option value="">All Agents</option>';
    agents.forEach(agent => {
      const option = document.createElement('option');
      option.value = agent.name;
      option.textContent = agent.name;
      timelineAgentFilter.appendChild(option);
    });
    timelineAgentFilter.value = currentValue;
  } catch (error) {
    console.error('Failed to load agents:', error);
  }
}

function showAgentDetail(agent) {
  const modal = document.getElementById('agent-detail-modal');
  document.getElementById('modal-agent-name').textContent = agent.name;
  document.getElementById('modal-agent-details').innerHTML = `
    <p><strong>Description:</strong> ${agent.description || 'No description'}</p>
    <p><strong>Capabilities:</strong> ${agent.capabilities.join(', ') || 'None'}</p>
    <p><strong>Tools:</strong> ${agent.tools.join(', ') || 'None'}</p>
    <p><strong>Coordination Patterns:</strong> ${agent.coordination_patterns.join(', ') || 'None'}</p>
  `;
  modal.style.display = 'block';
}

// =============================================================================
// Timeline
// =============================================================================
async function loadTimeline() {
  try {
    const agentFilter = document.getElementById('timeline-agent-filter').value;
    const statusFilter = document.getElementById('timeline-status-filter').value;

    let url = '/api/executions/timeline';
    const params = new URLSearchParams();
    if (agentFilter) params.append('agent_name', agentFilter);
    if (statusFilter) params.append('status', statusFilter);
    if (params.toString()) url += '?' + params.toString();

    const timeline = await fetchJSON(url);
    const timelineView = document.getElementById('timeline-view');
    timelineView.innerHTML = '';

    if (timeline.length === 0) {
      timelineView.innerHTML = '<p class="empty-state">No executions found</p>';
      return;
    }

    function renderTree(nodes, depth = 0) {
      nodes.forEach(node => {
        const item = document.createElement('div');
        item.className = `timeline-item status-${node.status}`;
        item.style.marginLeft = `${depth * 20}px`;
        item.innerHTML = `
          <div class="timeline-header">
            <span class="agent-name">${node.agent_name}</span>
            <span class="timestamp">${new Date(node.timestamp).toLocaleString()}</span>
            <span class="status-badge status-${node.status}">${node.status}</span>
            <span class="duration">${node.duration_ms || 0}ms</span>
          </div>
        `;
        timelineView.appendChild(item);

        if (node.children && node.children.length > 0) {
          renderTree(node.children, depth + 1);
        }
      });
    }

    renderTree(timeline);
  } catch (error) {
    console.error('Failed to load timeline:', error);
  }
}

// =============================================================================
// Workflows
// =============================================================================
async function loadWorkflows() {
  try {
    const workflows = await fetchJSON('/api/workflows');
    const workflowsList = document.getElementById('workflows-list');
    workflowsList.innerHTML = '';

    if (workflows.length === 0) {
      workflowsList.innerHTML = '<p class="empty-state">No workflow templates found</p>';
      return;
    }

    workflows.forEach(workflow => {
      const card = document.createElement('div');
      card.className = 'workflow-card';
      card.innerHTML = `
        <h3>${workflow.name}</h3>
        <p>${workflow.description || 'No description'}</p>
        <p><strong>Pattern:</strong> <span class="badge">${workflow.coordination_pattern || 'none'}</span></p>
        <details>
          <summary>Steps (${workflow.steps.length})</summary>
          <pre>${JSON.stringify(workflow.steps, null, 2)}</pre>
        </details>
      `;
      workflowsList.appendChild(card);
    });
  } catch (error) {
    console.error('Failed to load workflows:', error);
  }
}

// =============================================================================
// Patterns
// =============================================================================
async function loadPatterns() {
  try {
    const patterns = await fetchJSON('/api/patterns');
    const patternsList = document.getElementById('patterns-list');
    patternsList.innerHTML = '';

    if (patterns.length === 0) {
      patternsList.innerHTML = '<p class="empty-state">No coordination patterns found</p>';
      return;
    }

    patterns.forEach(pattern => {
      const card = document.createElement('div');
      card.className = 'pattern-card';
      card.innerHTML = `
        <h3>${pattern.name}</h3>
        <p>${pattern.description || 'No description'}</p>
        ${pattern.when_to_use ? `<p><strong>When to use:</strong> ${pattern.when_to_use}</p>` : ''}
      `;
      patternsList.appendChild(card);
    });
  } catch (error) {
    console.error('Failed to load patterns:', error);
  }
}

// =============================================================================
// Notes (Demo App)
// =============================================================================
async function loadNotes() {
  try {
    const list = document.getElementById('notes');
    list.innerHTML = '';
    const notes = await fetchJSON('/notes/');
    for (const n of notes) {
      const li = document.createElement('li');
      li.textContent = `${n.title}: ${n.content}`;
      list.appendChild(li);
    }
  } catch (error) {
    console.error('Failed to load notes:', error);
  }
}

async function loadActions() {
  try {
    const list = document.getElementById('actions');
    list.innerHTML = '';
    const items = await fetchJSON('/action-items/');
    for (const a of items) {
      const li = document.createElement('li');
      li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
      if (!a.completed) {
        const btn = document.createElement('button');
        btn.textContent = 'Complete';
        btn.onclick = async () => {
          await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
          loadActions();
        };
        li.appendChild(btn);
      }
      list.appendChild(li);
    }
  } catch (error) {
    console.error('Failed to load actions:', error);
  }
}

// =============================================================================
// Event Listeners & Initialization
// =============================================================================
window.addEventListener('DOMContentLoaded', () => {
  // Initialize tabs
  initTabs();

  // Initialize filters
  document.getElementById('agent-capability-filter').addEventListener('change', loadAgents);
  document.getElementById('agent-pattern-filter').addEventListener('change', loadAgents);
  document.getElementById('timeline-agent-filter').addEventListener('change', loadTimeline);
  document.getElementById('timeline-status-filter').addEventListener('change', loadTimeline);

  // Modal close
  document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('agent-detail-modal').style.display = 'none';
  });

  window.addEventListener('click', (e) => {
    const modal = document.getElementById('agent-detail-modal');
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });

  // Notes form
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  // Actions form
  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  // Load initial data
  loadDashboard();
  loadNotes();
  loadActions();
});
