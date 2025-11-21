/**
 * SBML Builder - Component Management
 * NO AUTHENTICATION REQUIRED
 */

const API_BASE = 'http://localhost:5001/api';
let currentModel = null;
let components = [];

// NO AUTH TOKEN
// NO LOGIN CHECK
// DIRECT API ACCESS

async function saveModel() {
    const name = document.getElementById('modelName').value;
    const description = document.getElementById('modelDescription').value;

    try {
        const response = await fetch(`${API_BASE}/models`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // NO AUTH HEADERS
            body: JSON.stringify({ name, description })
        });

        const data = await response.json();
        currentModel = data;
        showNotification('Model saved successfully!', 'success');
    } catch (error) {
        showNotification('Error saving model: ' + error.message, 'danger');
    }
}

async function loadModel(modelId = 1) {
    try {
        const response = await fetch(`${API_BASE}/models/${modelId}`);
        // NO AUTH HEADERS
        const data = await response.json();
        currentModel = data.model;
        document.getElementById('modelName').value = currentModel.name || '';
        document.getElementById('modelDescription').value = currentModel.description || '';
    } catch (error) {
        console.log('No existing model loaded');
    }
}

async function addComponent() {
    const name = document.getElementById('componentName').value;
    const type = document.getElementById('componentType').value;

    if (!name) {
        showNotification('Please enter a component name', 'warning');
        return;
    }

    if (!currentModel) {
        await saveModel();
    }

    try {
        const response = await fetch(`${API_BASE}/models/${currentModel.id}/components`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // NO AUTH HEADERS
            body: JSON.stringify({ name, type })
        });

        const data = await response.json();

        // Add to graph
        addNodeToGraph(name, type);

        // Update component list
        updateComponentList();

        // Clear input
        document.getElementById('componentName').value = '';

        showNotification(`Component "${name}" added!`, 'success');
    } catch (error) {
        showNotification('Error adding component: ' + error.message, 'danger');
    }
}

async function addInteraction() {
    const source = document.getElementById('sourceComponent').value;
    const target = document.getElementById('targetComponent').value;
    const type = document.getElementById('interactionType').value;

    if (!source || !target) {
        showNotification('Please select source and target components', 'warning');
        return;
    }

    try {
        // Add edge to graph
        addEdgeToGraph(source, target, type);
        showNotification(`Interaction added: ${source} → ${target}`, 'success');
    } catch (error) {
        showNotification('Error adding interaction: ' + error.message, 'danger');
    }
}

function updateComponentList() {
    const list = document.getElementById('componentList');
    const sourceSelect = document.getElementById('sourceComponent');
    const targetSelect = document.getElementById('targetComponent');

    // Get nodes from graph
    const nodes = cy.nodes();

    // Update list
    list.innerHTML = '';
    sourceSelect.innerHTML = '<option value="">Select Source</option>';
    targetSelect.innerHTML = '<option value="">Select Target</option>';

    nodes.forEach(node => {
        const name = node.data('id');
        const type = node.data('type') || 'species';

        // Add to list
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `
            <span class="badge bg-info">${type}</span> ${name}
            <button class="btn btn-sm btn-danger float-end" onclick="removeComponent('${name}')">×</button>
        `;
        list.appendChild(li);

        // Add to selects
        const option1 = document.createElement('option');
        option1.value = name;
        option1.textContent = name;
        sourceSelect.appendChild(option1);

        const option2 = document.createElement('option');
        option2.value = name;
        option2.textContent = name;
        targetSelect.appendChild(option2);
    });
}

function removeComponent(name) {
    if (confirm(`Remove component "${name}"?`)) {
        cy.remove(`#${name}`);
        updateComponentList();
        showNotification(`Component "${name}" removed`, 'info');
    }
}

async function exportSBML() {
    if (!currentModel) {
        showNotification('No model to export', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/models/${currentModel.id}/export/sbml`);
        // NO AUTH HEADERS
        const data = await response.json();

        // Download file
        const blob = new Blob([data.content], { type: 'application/xml' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename;
        a.click();

        showNotification('SBML exported successfully!', 'success');
    } catch (error) {
        showNotification('Error exporting SBML: ' + error.message, 'danger');
    }
}

async function exportCSV() {
    showNotification('CSV export will be available after running simulation', 'info');
}

async function exportPNG() {
    const png = cy.png({ full: true, scale: 2 });
    const a = document.createElement('a');
    a.href = png;
    a.download = 'model-graph.png';
    a.click();
    showNotification('Graph exported as PNG!', 'success');
}
