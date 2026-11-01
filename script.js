* {
  box-sizing: border-box;
}

:root {
  --bg: #f5f7fb;
  --panel: #ffffff;
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --secondary: #e2e8f0;
  --success: #16a34a;
  --danger: #dc2626;
  --warning: #f59e0b;
  --text: #0f172a;
  --muted: #64748b;
  --border: #e2e8f0;
  --shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: linear-gradient(135deg, #eef4ff 0%, #f8fafc 100%);
  color: var(--text);
}

button,
input {
  font: inherit;
}

button {
  cursor: pointer;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px 48px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
}

.eyebrow {
  margin: 0 0 6px;
  color: var(--primary);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 12px;
}

h1,
h2,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 0;
  font-size: 2rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: var(--shadow);
}

.stat-card .label {
  color: var(--muted);
  font-size: 0.82rem;
  margin-bottom: 8px;
  display: block;
}

.stat-card .value {
  font-size: 1.8rem;
  font-weight: 700;
}

.content {
  display: grid;
  grid-template-columns: minmax(300px, 420px) minmax(0, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--shadow);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  gap: 10px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-weight: 600;
  color: var(--text);
}

label span {
  font-size: 0.9rem;
}

input {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 11px 12px;
  background: #fff;
  color: var(--text);
}

input:focus {
  outline: 2px solid rgba(37, 99, 235, 0.15);
  border-color: var(--primary);
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.primary-button,
.secondary-button,
.small-button,
.danger-button {
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 700;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.primary-button {
  background: var(--primary);
  color: white;
}

.primary-button:hover {
  background: var(--primary-dark);
}

.secondary-button {
  background: var(--secondary);
  color: var(--text);
}

.small-button {
  background: #dbeafe;
  color: var(--primary-dark);
  padding: 8px 10px;
  font-size: 0.8rem;
}

.danger-button {
  background: #fee2e2;
  color: var(--danger);
  padding: 8px 10px;
  font-size: 0.8rem;
}

button:hover {
  transform: translateY(-1px);
}

.hidden {
  display: none !important;
}

.search-wrap {
  width: min(260px, 100%);
}

.search-wrap input {
  width: 100%;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  text-align: left;
  padding: 12px 10px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

th {
  color: var(--muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.badge {
  display: inline-block;
  border-radius: 999px;
  padding: 6px 8px;
  font-size: 0.72rem;
  font-weight: 700;
}

.badge.low {
  background: #fef3c7;
  color: #92400e;
}

.badge.ok {
  background: #dcfce7;
  color: #166534;
}

.row-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.transaction-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.transaction-item {
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
  border-radius: 10px;
  padding: 12px 14px;
  background: #f8fafc;
}

.transaction-item.entry {
  border-left-color: var(--success);
}

.transaction-item.exit {
  border-left-color: var(--danger);
}

.transaction-item strong {
  display: block;
  margin-bottom: 4px;
}

.transaction-item .meta {
  color: var(--muted);
  font-size: 0.82rem;
}

.empty-state {
  text-align: center;
  color: var(--muted);
  padding: 28px 10px;
}

@media (max-width: 840px) {
  .content {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
