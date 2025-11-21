/**
 * SBML Builder - Simulation Integration
 * NO AUTHENTICATION REQUIRED
 */

let simChart = null;
let socket = null;
let currentSimulation = null;

function initSimulation() {
    // Initialize Chart.js for results
    const ctx = document.getElementById('simChart').getContext('2d');
    simChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time Steps'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Concentration'
                    }
                }
            }
        }
    });

    // Initialize Socket.IO for real-time updates
    // NO AUTHENTICATION
    socket = io('http://localhost:5001', {
        transports: ['websocket', 'polling']
    });

    socket.on('connect', () => {
        console.log('✅ Connected to simulation server');
    });

    socket.on('simulation_update', (data) => {
        updateSimulationChart(data);
    });

    socket.on('simulation_complete', (data) => {
        handleSimulationComplete(data);
    });

    socket.on('simulation_error', (error) => {
        showNotification('Simulation error: ' + error.message, 'danger');
    });
}

async function runSimulation() {
    if (!currentModel) {
        showNotification('Please save a model first', 'warning');
        return;
    }

    const steps = parseInt(document.getElementById('simSteps').value);
    const method = document.getElementById('simMethod').value;

    // Get model data from graph
    const modelData = {
        components: [],
        interactions: []
    };

    cy.nodes().forEach(node => {
        modelData.components.push({
            id: node.data('id'),
            type: node.data('type')
        });
    });

    cy.edges().forEach(edge => {
        modelData.interactions.push({
            source: edge.data('source'),
            target: edge.data('target'),
            type: edge.data('type')
        });
    });

    try {
        showNotification('Starting simulation...', 'info');

        const response = await fetch(`${API_BASE}/models/${currentModel.id}/simulate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // NO AUTH HEADERS
            body: JSON.stringify({
                steps: steps,
                method: method,
                model_data: modelData
            })
        });

        const data = await response.json();
        currentSimulation = data.simulation_id;

        showNotification(`Simulation started (ID: ${currentSimulation})`, 'success');

        // Clear previous chart data
        simChart.data.labels = [];
        simChart.data.datasets = [];
        simChart.update();

    } catch (error) {
        showNotification('Error starting simulation: ' + error.message, 'danger');
    }
}

async function stopSimulation() {
    if (!currentSimulation) {
        showNotification('No simulation running', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/simulations/${currentSimulation}/stop`, {
            method: 'POST'
            // NO AUTH HEADERS
        });

        const data = await response.json();
        showNotification('Simulation stopped', 'info');
        currentSimulation = null;

    } catch (error) {
        showNotification('Error stopping simulation: ' + error.message, 'danger');
    }
}

function updateSimulationChart(data) {
    // data format: { time: number, values: { component_id: concentration } }

    // Update labels
    if (!simChart.data.labels.includes(data.time)) {
        simChart.data.labels.push(data.time);
    }

    // Update datasets for each component
    Object.keys(data.values).forEach(componentId => {
        let dataset = simChart.data.datasets.find(d => d.label === componentId);

        if (!dataset) {
            // Create new dataset
            const color = getRandomColor();
            dataset = {
                label: componentId,
                data: [],
                borderColor: color,
                backgroundColor: color + '20',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            };
            simChart.data.datasets.push(dataset);
        }

        dataset.data.push(data.values[componentId]);
    });

    simChart.update('none'); // Update without animation for performance
}

function handleSimulationComplete(data) {
    showNotification('Simulation complete!', 'success');
    currentSimulation = null;

    // Final chart update
    if (data.results) {
        displayFinalResults(data.results);
    }
}

function displayFinalResults(results) {
    // results format: { time_points: [], component_values: { component_id: [values] } }

    simChart.data.labels = results.time_points;
    simChart.data.datasets = [];

    Object.keys(results.component_values).forEach(componentId => {
        const color = getRandomColor();
        simChart.data.datasets.push({
            label: componentId,
            data: results.component_values[componentId],
            borderColor: color,
            backgroundColor: color + '20',
            borderWidth: 2,
            pointRadius: 2,
            tension: 0.4
        });
    });

    simChart.update();
}

function getRandomColor() {
    const colors = [
        '#0d6efd', '#198754', '#dc3545', '#0dcaf0', '#ffc107',
        '#6c757d', '#d63384', '#6610f2', '#fd7e14', '#20c997'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

async function getSimulationStatus() {
    if (!currentSimulation) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/simulations/${currentSimulation}/status`);
        // NO AUTH HEADERS
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error getting simulation status:', error);
    }
}

async function downloadSimulationResults() {
    if (!currentSimulation) {
        showNotification('No simulation results available', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/simulations/${currentSimulation}/export/csv`);
        // NO AUTH HEADERS
        const data = await response.json();

        // Download CSV
        const blob = new Blob([data.csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `simulation_${currentSimulation}.csv`;
        a.click();

        showNotification('Simulation results downloaded!', 'success');
    } catch (error) {
        showNotification('Error downloading results: ' + error.message, 'danger');
    }
}

// Initialize simulation when page loads
document.addEventListener('DOMContentLoaded', function() {
    initSimulation();
});
