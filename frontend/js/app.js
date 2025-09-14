document.addEventListener('DOMContentLoaded', () => {
    // Placeholder para los proyectos existentes
    const projects = [
        {
            id: 1,
            title: "Optimización de Cascos Navales con IA",
            description: "Análisis de hidrodinámica computacional para reducir el consumo de combustible.",
            status: "Completado"
        },
        {
            id: 2,
            title: "Mantenimiento Predictivo para Sistemas de Propulsión",
            description: "Uso de sensores y machine learning para predecir fallos en motores y ejes.",
            status: "Completado"
        },
        {
            id: 3,
            title: "Materiales Compuestos para Superestructuras",
            description: "Investigación de nuevos materiales ligeros y resistentes para construcción naval.",
            status: "Completado"
        }
    ];

    const projectGrid = document.getElementById('project-grid');

    if (projectGrid) {
        projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <span class="card-status">${project.status}</span>
            `;
            // Al hacer clic, navega a la vista de detalle (simulación)
            card.addEventListener('click', () => {
                window.location.href = `project.html?id=${project.id}`;
            });
            projectGrid.appendChild(card);
        });
    }
});