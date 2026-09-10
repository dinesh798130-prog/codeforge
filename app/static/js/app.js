/**
 * CodeForge Client Application
 * Handles file drop/paste, autonomous triage, execution reporting, and polyglot grid.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-input');
  const codeEditor = document.getElementById('code-editor');
  const editorFilename = document.getElementById('editor-filename');
  const manualLangSelect = document.getElementById('manual-lang-select');
  const detectedLangBadge = document.getElementById('detected-lang-badge');
  const clearBtn = document.getElementById('clear-btn');
  const processBtn = document.getElementById('process-btn');
  const loadingState = document.getElementById('loading-state');
  const presetsContainer = document.getElementById('presets-container');

  // Zone elements
  const zoneDiagnosis = document.getElementById('zone-diagnosis');
  const diagnosisList = document.getElementById('diagnosis-list');
  const countBlocks = document.getElementById('count-blocks');
  const countRisks = document.getElementById('count-risks');
  const countStyle = document.getElementById('count-style');
  const dsaTime = document.getElementById('dsa-time');
  const dsaSpace = document.getElementById('dsa-space');
  const dsaEdge = document.getElementById('dsa-edge');

  const zoneFixed = document.getElementById('zone-fixed');
  const fixedLangLabel = document.getElementById('fixed-lang-label');
  const fixedToolchain = document.getElementById('fixed-toolchain');
  const fixedStatus = document.getElementById('fixed-status');
  const fixedExitCode = document.getElementById('fixed-exit-code');
  const fixedRuntime = document.getElementById('fixed-runtime');
  const fixedCodeBlock = document.getElementById('fixed-code-block');
  const diffCodeBlock = document.getElementById('diff-code-block');
  const fixedTerminalOutput = document.getElementById('fixed-terminal-output');
  const copyFixedBtn = document.getElementById('copy-fixed-btn');
  const rerunFixedBtn = document.getElementById('rerun-fixed-btn');

  const zonePolyglot = document.getElementById('zone-polyglot');
  const parityMatrixStrip = document.getElementById('parity-matrix-strip');
  const polyglotTabs = document.getElementById('polyglot-tabs');
  const polyCmd = document.getElementById('poly-cmd');
  const polyCaveat = document.getElementById('poly-caveat');
  const polyCodeBlock = document.getElementById('poly-code-block');
  const polyTerminalOutput = document.getElementById('poly-terminal-output');
  const polyStatusBadge = document.getElementById('poly-status-badge');
  const copyPolyBtn = document.getElementById('copy-poly-btn');

  let currentFixedCode = '';
  let currentLanguage = 'python';
  let polyglotCache = {};

  // 1. Initialize Presets
  loadPresets();

  // 2. Drag and Drop handlers
  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('drag-over');
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
    if (e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });

  function handleFile(file) {
    editorFilename.textContent = file.name;
    const reader = new FileReader();
    reader.onload = (e) => {
      codeEditor.value = e.target.result;
      detectLanguageFromBackend(file.name, codeEditor.value);
    };
    reader.readAsText(file);
  }

  // Auto-detect on typing debounce
  let typeTimer;
  codeEditor.addEventListener('input', () => {
    clearTimeout(typeTimer);
    typeTimer = setTimeout(() => {
      detectLanguageFromBackend(editorFilename.textContent, codeEditor.value);
    }, 400);
  });

  async function detectLanguageFromBackend(filename, code) {
    if (!code.trim()) return;
    try {
      const res = await fetch('/api/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename, code }),
      });
      const data = await res.json();
      detectedLangBadge.textContent = `Detected: ${data.language.toUpperCase()} (${Math.round(data.confidence * 100)}%)`;
      if (manualLangSelect.value === 'auto') {
        currentLanguage = data.language;
      }
    } catch (err) {
      console.error('Detection failed', err);
    }
  }

  manualLangSelect.addEventListener('change', () => {
    if (manualLangSelect.value !== 'auto') {
      currentLanguage = manualLangSelect.value;
      detectedLangBadge.textContent = `Selected: ${currentLanguage.toUpperCase()}`;
    } else {
      detectLanguageFromBackend(editorFilename.textContent, codeEditor.value);
    }
  });

  clearBtn.addEventListener('click', () => {
    codeEditor.value = '';
    editorFilename.textContent = 'input_code.py';
    hideResults();
  });

  // 3. Process Code Execution
  processBtn.addEventListener('click', async () => {
    const code = codeEditor.value.trim();
    if (!code) {
      alert('Please enter or drop a code file first.');
      return;
    }

    loadingState.classList.remove('hidden');
    hideResults();

    try {
      const res = await fetch('/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: editorFilename.textContent,
          code: code,
          language: manualLangSelect.value === 'auto' ? null : manualLangSelect.value,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Processing failed.');
      }

      const data = await res.json();
      renderAllZones(data);
    } catch (err) {
      alert(`Error during CodeForge execution: ${err.message}`);
    } finally {
      loadingState.classList.add('hidden');
    }
  });

  function hideResults() {
    zoneDiagnosis.classList.add('hidden');
    zoneFixed.classList.add('hidden');
    zonePolyglot.classList.add('hidden');
  }

  // 4. Render All Zones
  function renderAllZones(data) {
    currentLanguage = data.detected_language;
    currentFixedCode = data.fixed_code;
    polyglotCache = data.polyglot_grid;

    // ZONE 1: Diagnosis
    renderDiagnosis(data.diagnoses, data.dsa_summary);
    zoneDiagnosis.classList.remove('hidden');

    // ZONE 2: Fixed Original
    renderFixedOriginal(data);
    zoneFixed.classList.remove('hidden');

    // ZONE 3: Polyglot Grid
    renderPolyglotGrid(data.polyglot_grid);
    zonePolyglot.classList.remove('hidden');

    // Smooth scroll down to diagnosis
    zoneDiagnosis.scrollIntoView({ behavior: 'smooth' });
  }

  function renderDiagnosis(diagnoses, dsa) {
    diagnosisList.innerHTML = '';
    let blocks = 0;
    let risks = 0;
    let styles = 0;

    if (!diagnoses || diagnoses.length === 0) {
      diagnosisList.innerHTML = `
        <div class="diagnosis-item" style="border-left-color: var(--success)">
          <div class="diag-header-line">
            <span class="status-pill status-success">Passed</span>
            <span class="diag-title">No syntax or logical violations detected.</span>
          </div>
        </div>
      `;
    } else {
      diagnoses.forEach((d) => {
        if (d.severity === 'blocks_compilation') blocks++;
        else if (d.severity === 'logic_risk') risks++;
        else styles++;

        const item = document.createElement('div');
        item.className = `diagnosis-item severity-${d.severity}`;
        item.innerHTML = `
          <div class="diag-header-line">
            <span class="diag-line-tag">Line ${d.line}</span>
            <span class="diag-rule-chip">${d.rule_id}</span>
            <span class="diag-title">${escapeHtml(d.fault_type)}</span>
          </div>
          <div class="diag-explanation">${escapeHtml(d.explanation)}</div>
          ${d.code_snippet ? `<pre class="diag-snippet"><code>${escapeHtml(d.code_snippet)}</code></pre>` : ''}
        `;
        diagnosisList.appendChild(item);
      });
    }

    countBlocks.textContent = `${blocks} Blocks Compilation`;
    countRisks.textContent = `${risks} Logic Risks`;
    countStyle.textContent = `${styles} Style Only`;

    // DSA Summary
    if (dsa) {
      dsaTime.textContent = dsa.time_complexity;
      dsaSpace.textContent = dsa.space_complexity;
      dsaEdge.textContent = dsa.edge_cases_tested;
    }
  }

  function renderFixedOriginal(data) {
    fixedLangLabel.textContent = data.detected_language.toUpperCase();
    fixedToolchain.textContent = data.execution.toolchain || 'Default Sandbox';
    fixedExitCode.textContent = data.execution.exit_code;
    fixedRuntime.textContent = `${data.execution.runtime_ms} ms`;

    if (data.execution.exit_code === 0) {
      fixedStatus.textContent = 'Executed Successfully';
      fixedStatus.className = 'status-pill status-success';
    } else {
      fixedStatus.textContent = 'Execution Failed';
      fixedStatus.className = 'status-pill status-error';
    }

    // Code view
    fixedCodeBlock.textContent = data.fixed_code;

    // Diff view
    renderDiff(data.diff);

    // Terminal view
    const output = (data.execution.stdout || '') + (data.execution.stderr ? `\n[STDERR]\n${data.execution.stderr}` : '');
    fixedTerminalOutput.textContent = output.trim() || '[Process finished with no terminal output]';
  }

  function renderDiff(diffText) {
    diffCodeBlock.innerHTML = '';
    if (!diffText) {
      diffCodeBlock.textContent = 'No structural differences detected.';
      return;
    }

    const lines = diffText.split('\n');
    lines.forEach((line) => {
      const span = document.createElement('span');
      if (line.startsWith('+') && !line.startsWith('+++')) {
        span.className = 'diff-line-added';
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        span.className = 'diff-line-deleted';
      }
      span.textContent = line + '\n';
      diffCodeBlock.appendChild(span);
    });
  }

  function renderPolyglotGrid(grid) {
    polyglotTabs.innerHTML = '';
    parityMatrixStrip.innerHTML = '';

    const languages = Object.keys(grid);
    if (languages.length === 0) return;

    languages.forEach((langKey, index) => {
      const item = grid[langKey];

      // Parity pill
      const pill = document.createElement('span');
      const isVerified = item.parity_status === 'verified';
      pill.className = `parity-pill ${isVerified ? 'verified' : 'caveat'}`;
      pill.innerHTML = `${isVerified ? '✅' : '⚠️'} ${item.label}`;
      parityMatrixStrip.appendChild(pill);

      // Tab button
      const tabBtn = document.createElement('button');
      tabBtn.className = `poly-tab-btn ${index === 0 ? 'active' : ''}`;
      tabBtn.textContent = `${item.label} (${item.badge})`;
      tabBtn.addEventListener('click', () => {
        document.querySelectorAll('.poly-tab-btn').forEach((b) => b.classList.remove('active'));
        tabBtn.classList.add('active');
        showPolyglotCard(item);
      });
      polyglotTabs.appendChild(tabBtn);
    });

    // Show first tab by default
    showPolyglotCard(grid[languages[0]]);
  }

  function showPolyglotCard(item) {
    polyCmd.textContent = item.run_cmd;
    polyCaveat.textContent = item.parity_note;
    polyCodeBlock.textContent = item.code;

    const exec = item.execution;
    const output = (exec.stdout || '') + (exec.stderr ? `\n[STDERR]\n${exec.stderr}` : '');
    polyTerminalOutput.textContent = output.trim() || '[No stdout captured]';

    polyStatusBadge.textContent = exec.status === 'success' ? 'Live Execution Verified' : 'Static Sandbox Parity';
    polyStatusBadge.style.color = exec.status === 'success' ? 'var(--success)' : 'var(--warning)';

    copyPolyBtn.onclick = () => {
      navigator.clipboard.writeText(item.code);
      copyPolyBtn.textContent = 'Copied!';
      setTimeout(() => (copyPolyBtn.textContent = 'Copy'), 1500);
    };
  }

  // 5. Tabs Switching in Zone 2
  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach((c) => c.classList.remove('active'));
      btn.classList.add('active');
      const tabId = btn.dataset.tab;
      document.getElementById(tabId).classList.add('active');
    });
  });

  // 6. Action buttons
  copyFixedBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(currentFixedCode);
    copyFixedBtn.textContent = '✓ Copied!';
    setTimeout(() => (copyFixedBtn.textContent = '📋 Copy Code'), 1500);
  });

  rerunFixedBtn.addEventListener('click', async () => {
    rerunFixedBtn.textContent = 'Running...';
    try {
      const res = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          language: currentLanguage,
          code: currentFixedCode,
        }),
      });
      const data = await res.json();
      fixedTerminalOutput.textContent = (data.stdout || '') + (data.stderr ? `\n${data.stderr}` : '');
      fixedRuntime.textContent = `${data.runtime_ms} ms`;
      fixedExitCode.textContent = data.exit_code;
    } catch (err) {
      alert(`Re-run failed: ${err.message}`);
    } finally {
      rerunFixedBtn.textContent = '▶ Re-run Sandbox';
    }
  });

  // 7. Load Presets
  async function loadPresets() {
    try {
      const res = await fetch('/api/presets');
      const presets = await res.json();
      presetsContainer.innerHTML = '';
      presets.forEach((p) => {
        const btn = document.createElement('button');
        btn.className = 'preset-btn';
        btn.textContent = p.title;
        btn.title = p.description;
        btn.addEventListener('click', () => {
          codeEditor.value = p.code;
          editorFilename.textContent = p.filename;
          currentLanguage = p.language;
          detectedLangBadge.textContent = `Preset: ${p.language.toUpperCase()}`;
          manualLangSelect.value = p.language;
          hideResults();
        });
        presetsContainer.appendChild(btn);
      });
    } catch (err) {
      console.warn('Presets could not be fetched', err);
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});
