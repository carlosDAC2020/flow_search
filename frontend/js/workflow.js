document.addEventListener('DOMContentLoaded', () => {
    // --- DATOS DE DEMOSTRACIÓN ---
    const projectInfo = {
        title: "Análisis de Oportunidades: Detección de Deforestación con IA",
        description: "Sistema de detección de deforestación en áreas rurales con inteligencia artificial para ayudar a los campesinos a tomar medidas de acción y promover la conservación.",
        // MEJORA: Resumen conciso para la tarjeta del historial, evitando redundancia.
        summary: "Investigación sobre la aplicación de IA para el monitoreo y la detección temprana de deforestación en zonas rurales.",
        keywords: ["Inteligencia Artificial", "Medio Ambiente", "Deforestación", "Sostenibilidad"],
        creationDate: "12/09/2025"
    };

    const searchResults = [
        { title: "Climate Change AI Innovation Grants", url: "#", description: "CCAI is pleased to announce its 2025 Innovation Grants program..." },
        { title: "Convocatorias Minciencias - Sostenibilidad", url: "#", description: "El Ministerio de Ciencia abre la convocatoria para proyectos de IA aplicada..." },
        { title: "TechFunding - Deforestation Solutions", url: "#", description: "Seeking proposals for innovative technology using AI to monitor deforestation..." }
    ];

    const identifiedOpportunities = [
        { origin: 'Climate Change AI Grants', description: 'Financiación de hasta $150,000 para proyectos que usen IA para combatir el cambio climático.', financing_type: 'Grant (Subvención)', application_deadline: '2025-12-15' },
        { origin: 'Minciencias - Convocatoria 821', description: 'Apoyo a proyectos de I+D en sostenibilidad ambiental con componentes de inteligencia artificial.', financing_type: 'Financiación Nacional', application_deadline: '2025-11-30' }
    ];
    
    // Almacén para las investigaciones completadas
    const completedResearches = [];

    // --- ELEMENTOS DEL DOM ---
    const dom = {
        projectTitle: document.getElementById('project-title'),
        projectDescription: document.getElementById('project-description'),
        projectKeywords: document.getElementById('project-keywords'),
        creationDate: document.getElementById('creation-date'),
        workflowContainer: document.getElementById('workflow-container'),
        resultsTabs: document.getElementById('results-tabs'),
        resultsContent: document.getElementById('results-content'),
        researchesGrid: document.getElementById('researches-grid'),
        detailsTabs: document.querySelector('.details-tabs'),
        detailsPanel: document.querySelector('.details-content-panel'),
        tabContexto: document.getElementById('tab-contexto'),
        tabOportunidades: document.getElementById('tab-oportunidades'),
        tabReportes: document.getElementById('tab-reportes'),
    };
    
    // Configuración de los pasos del flujo de trabajo
    const steps = [
        { id: 'queries', name: 'Consultas', duration: 1500, data: [], render: () => `<p>Generando consultas inteligentes basadas en el objetivo del proyecto...</p>` },
        { id: 'search', name: 'Resultados', duration: 2000, data: searchResults, render: renderContextItems },
        { id: 'identification', name: 'Oportunidades', duration: 2500, data: identifiedOpportunities, render: renderOpportunities },
        { id: 'report', name: 'Reporte', duration: 1000, data: { reportUrl: '#' }, render: renderReportLink }
    ];

    // --- FUNCIONES DE RENDERIZADO ---
    function renderContextItems(data) {
        return `<p>${data.length} items de contexto encontrados:</p><ul class="results-list">${data.map(r => `<li><a href="${r.url}" target="_blank">${r.title}</a><p>${r.description}</p></li>`).join('')}</ul>`;
    }
    function renderOpportunities(data) {
        return `<div class="opportunities-list">${data.map(o => `<div class="opportunity-card"><h4>${o.origin}</h4><p>${o.description}</p><div class="opportunity-meta"><span class="financing-type">${o.financing_type}</span> | <span><strong>Fecha Límite:</strong> ${o.application_deadline}</span></div></div>`).join('')}</div>`;
    }
    function renderReportLink(data) {
        return `<div><p>El reporte ejecutivo ha sido generado y está listo para su revisión.</p><br><a href="${data.reportUrl}" class="report-link" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M10.854 7.854a.5.5 0 0 0-.708-.708L7.5 9.793 6.354 8.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/><path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 1.5L13 5H9.5V1.5z"/></svg> Ver Reporte_Deforestacion_IA_2025.pdf</a></div>`;
    }

    // --- LÓGICA DE LA SIMULACIÓN Y LA INTERFAZ ---
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    function loadProjectInfo() {
        dom.projectTitle.textContent = projectInfo.title;
        dom.projectDescription.textContent = projectInfo.description;
        dom.creationDate.textContent = `Creado el: ${projectInfo.creationDate}`;
        dom.projectKeywords.innerHTML = projectInfo.keywords.map(k => `<span class="keyword-tag">${k}</span>`).join('');
    }
    
    function showResultInWorkflow(stepId) {
        dom.resultsTabs.querySelectorAll('.tab-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.step === stepId));
        dom.resultsContent.querySelectorAll('.result-section').forEach(sec => sec.classList.toggle('active', sec.dataset.step === stepId));
    }

    function activateDetailsTab(tabName) {
         dom.detailsTabs.querySelectorAll('.details-tab-btn').forEach(btn => {
             btn.classList.toggle('active', btn.dataset.tab === tabName);
         });
         dom.detailsPanel.querySelectorAll('.details-content').forEach(content => {
             content.classList.toggle('active', content.id === `tab-${tabName}`);
         });
    }

    async function simulateWorkflow() {
        // Limpiar el placeholder inicial del panel de resultados
        dom.resultsContent.innerHTML = '';
        
        for (const step of steps) {
            const stepElement = document.getElementById(`step-${step.id}`);
            const statusElement = stepElement.querySelector('.step-status');
            
            stepElement.classList.add('active');
            statusElement.className = 'step-status active';

            await delay(step.duration);

            // Crear contenido para el panel de resultados del flujo
            if (step.id !== 'queries') { // No crear pestaña para el primer paso
                const resultSection = document.createElement('div');
                resultSection.className = 'result-section';
                resultSection.dataset.step = step.id;
                resultSection.innerHTML = step.render(step.data);
                dom.resultsContent.appendChild(resultSection);

                const tabButton = document.createElement('button');
                tabButton.className = 'tab-btn';
                tabButton.dataset.step = step.id;
                tabButton.textContent = step.name;
                tabButton.addEventListener('click', () => showResultInWorkflow(step.id));
                dom.resultsTabs.appendChild(tabButton);
                showResultInWorkflow(step.id);
            }

            stepElement.classList.remove('active');
            stepElement.classList.add('completed');
            statusElement.className = 'step-status completed';
        }

        await delay(1500); // Pequeña pausa antes de la transición
        
        // MEJORA: Ocultar el panel del flujo de trabajo con una transición
        dom.workflowContainer.classList.add('hidden');
        
        // Guardar los datos finales de la investigación
        const finalData = {
            id: Date.now(),
            title: projectInfo.title, // El título completo se mantiene en los datos
            summary: projectInfo.summary, // El resumen se usa para la tarjeta
            date: projectInfo.creationDate,
            opportunitiesCount: identifiedOpportunities.length,
            contexto: renderContextItems(searchResults),
            oportunidades: renderOpportunities(identifiedOpportunities),
            reportes: renderReportLink({ reportUrl: '#' })
        };
        completedResearches.push(finalData);
        
        // Crear y mostrar la nueva tarjeta en el historial
        createResearchCard(finalData);

        // MEJORA: Seleccionar automáticamente la primera tarjeta creada
        const firstCard = dom.researchesGrid.querySelector('.research-card:not(.placeholder)');
        if (firstCard) {
            firstCard.click();
        }
    }
    
    function createResearchCard(data) {
        const placeholder = dom.researchesGrid.querySelector('.placeholder');
        if(placeholder) placeholder.style.display = 'none'; // Ocultar el placeholder

        const card = document.createElement('div');
        card.className = 'research-card';
        card.dataset.researchId = data.id;
        
        // MEJORA: La tarjeta usa el `summary` para ser más concisa
        card.innerHTML = `
            <div class="card-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            </div>
            <div class="card-content">
                <h4>${data.title}</h4>
                <p>${data.summary}</p> 
                <div class="card-footer">
                    <span class="footer-meta">Finalizado el: ${data.date}</span>
                    <span class="footer-meta opportunities-count">${data.opportunitiesCount} Oportunidades</span>
                </div>
            </div>
        `;
        
        // Añadir la nueva tarjeta al principio de la lista
        dom.researchesGrid.prepend(card);
        
        // Añadir evento para mostrar detalles al hacer clic
        card.addEventListener('click', () => {
            // Quitar el estado activo de otras tarjetas
            document.querySelectorAll('.research-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active'); // Activar la tarjeta actual
            
            const researchData = completedResearches.find(r => r.id == data.id);
            if(researchData) {
                // Rellenar los paneles de detalles
                dom.tabContexto.innerHTML = researchData.contexto;
                dom.tabOportunidades.innerHTML = researchData.oportunidades;
                dom.tabReportes.innerHTML = researchData.reportes;
                // Activar la primera pestaña por defecto al seleccionar una tarjeta
                activateDetailsTab('contexto');
            }
        });
    }

    // --- INICIO DE LA APLICACIÓN ---
    loadProjectInfo();
    simulateWorkflow(); // Inicia la simulación al cargar la página
    
    // Event listener para las pestañas de la sección de detalles
    dom.detailsTabs.addEventListener('click', (e) => {
        if (e.target.matches('.details-tab-btn')) {
            activateDetailsTab(e.target.dataset.tab);
        }
    });
});