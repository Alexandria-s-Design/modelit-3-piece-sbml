/**
 * SBML Builder - Graph Visualization (Cytoscape.js)
 * NO AUTHENTICATION REQUIRED
 */

let cy = null;

function initGraph() {
    cy = cytoscape({
        container: document.getElementById('cy'),

        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#0d6efd',
                    'label': 'data(id)',
                    'color': '#fff',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '12px',
                    'width': '60px',
                    'height': '60px',
                    'border-width': 2,
                    'border-color': '#0a58ca'
                }
            },
            {
                selector: 'node[type="species"]',
                style: {
                    'background-color': '#0d6efd',
                    'shape': 'ellipse'
                }
            },
            {
                selector: 'node[type="reaction"]',
                style: {
                    'background-color': '#198754',
                    'shape': 'rectangle'
                }
            },
            {
                selector: 'node[type="parameter"]',
                style: {
                    'background-color': '#ffc107',
                    'shape': 'diamond'
                }
            },
            {
                selector: 'node[type="compartment"]',
                style: {
                    'background-color': '#6c757d',
                    'shape': 'roundrectangle'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: 'edge[type="activation"]',
                style: {
                    'line-color': '#198754',
                    'target-arrow-color': '#198754'
                }
            },
            {
                selector: 'edge[type="inhibition"]',
                style: {
                    'line-color': '#dc3545',
                    'target-arrow-color': '#dc3545',
                    'target-arrow-shape': 'tee'
                }
            },
            {
                selector: 'edge[type="catalysis"]',
                style: {
                    'line-color': '#0dcaf0',
                    'target-arrow-color': '#0dcaf0',
                    'line-style': 'dashed'
                }
            }
        ],

        layout: {
            name: 'circle'
        }
    });

    // Make nodes draggable
    cy.nodes().grabify();
}

function addNodeToGraph(id, type = 'species') {
    cy.add({
        group: 'nodes',
        data: { id: id, type: type }
    });

    resetLayout();
}

function addEdgeToGraph(source, target, type = 'activation') {
    cy.add({
        group: 'edges',
        data: {
            id: `${source}-${target}`,
            source: source,
            target: target,
            type: type
        }
    });
}

function resetLayout() {
    cy.layout({
        name: 'circle',
        animate: true,
        animationDuration: 500
    }).run();
}

function fitGraph() {
    cy.fit();
}

function clearGraph() {
    cy.elements().remove();
}
