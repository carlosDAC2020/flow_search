# **Desarrollo de una herramienta de vigilancia tecnológica para identificar oportunidades de financiamiento de proyectos de investigación**

## **Información del Proyecto**

*   **Autores:**
    *   Carlos Daniel Agamez Palomino
    *   Harold Styven Lagares De Voz
*   **Periodo de Desarrollo:** 11 de septiembre de 2025 – 25 de septiembre de 2025
*   **Versión:** 1.0

## **Objetivo General**
Desarrollar una herramienta automatizada que realice vigilancia tecnológica en la web, identificando convocatorias nacionales e internacionales de financiamiento para proyectos de investigación, y que genere informes explicativos sobre dichas oportunidades.

## **Objetivos Específicos**
*   Diseñar un sistema que explore fuentes oficiales y confiables (portales de agencias de financiación, universidades, organizaciones multilaterales, etc.).
*   Implementar algoritmos de web scraping y/o APIs para recolección automatizada de datos.
*   Clasificar las oportunidades encontradas por áreas de investigación, requisitos, fechas y tipo de financiamiento.
*   Generar reportes periódicos (semanales o mensuales) con resúmenes ejecutivos de las nuevas convocatorias.
*   Permitir búsquedas manuales y suscripciones personalizadas a temas de interés.

## **Entregables**
*   Módulo funcional de recolección de datos desde fuentes web (scraper/API).
*   Base de datos estructurada de convocatorias vigentes e históricas.
*   Interfaz web o de escritorio para consultas y visualización de oportunidades.
*   Generador de informes explicativos en formatos PDF/Word.
*   Sistema de alertas por correo o notificaciones automáticas.
*   Documentación técnica y manual de usuario.
*   Informe final del desarrollo del sistema.


## **Propuesta de Solución**
Para cumplir con el objetivo general, se propone el desarrollo de una plataforma tecnológica avanzada que integra agentes de inteligencia artificial con una arquitectura de microservicios moderna y escalable. Esta solución está diseñada para automatizar por completo el ciclo de vigilancia tecnológica, desde la recolección masiva de datos en la web hasta la generación de informes ejecutivos. El sistema operará de forma asíncrona para garantizar un alto rendimiento y una experiencia de usuario fluida, permitiendo a los investigadores centrarse en sus propuestas y no en la búsqueda manual de financiación.

### **Requerimientos**
Los requerimientos para el optimo funcionamiento del sistema son los siguientes:

#### Funcionales
-   A partir de un proyecto, identificar oportunidades de financiación para dicho proyecto.
-   Realizar un enriquecimiento periódico de las oportunidades encontradas para los proyectos.
-   Realizar reportes periódicos de las investigaciones realizadas y los resultados obtenidos.
-   Generar servicio de notificación sobre los resultados de las investigaciones periódicas.
-   CRUD y autenticación de usuarios.

#### No Funcionales
-   Investigación manual de oportunidades.

#### Sistema
-   Implementación de MicroServicios.
-   Manejo asíncrono de tareas (Investigaciones de proyectos se realizarán en segundo plano).

### **Arquitectura y Flujo de Tecnologías**

La arquitectura se basa en un ecosistema de **MicroServicios orquestados por Docker**, lo que permite que cada componente del sistema opere de forma independiente, sea escalable y fácil de mantener. A continuación, se detalla la tecnología asociada a cada servicio y cómo interactúan entre sí.

#### **Stack Tecnológico por Servicio**

| Componente                | Tecnologías Clave                                       | Responsabilidad                                                                                                     |
| :------------------------ | :------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------ |
| **FrontEnd**              | **Angular, TypeScript**                                 | Proporciona la interfaz de usuario (UI) para la interacción. Gestiona la visualización de datos y las solicitudes del cliente. |
| **API (Backend)**         | **Python, Django**                                      | Expone los endpoints para la autenticación, gestión de usuarios y proyectos (CRUD). Orquesta el inicio de tareas asíncronas. |
| **Base de Datos**         | **PostgreSQL**                                          | Almacena de forma persistente y estructurada todos los datos: usuarios, proyectos, convocatorias y resultados.     |
| **Cola de Tareas**        | **Redis**                                               | Actúa como un *message broker*. Recibe las tareas pesadas de la API y las encola para que los Workers las procesen.    |
| **Worker (Procesamiento)** | **Python, Celery, LangChain**                           | Ejecuta las tareas de larga duración en segundo plano (búsqueda, scraping, análisis de IA). Es el motor de la herramienta. |
| **Orquestación**          | **Docker, Docker-Compose**                              | Gestiona el ciclo de vida de todos los servicios, define las redes, volúmenes y variables de entorno para el despliegue. |


#### **Servicios Externos**

Para realizar la vigilancia tecnológica y el enriquecimiento de datos, el sistema se apoya en un conjunto de APIs y tecnologías externas que son fundamentales para su operación.

#### **Gemini API (de Google)**

*   **Rol en el Sistema**: Es el núcleo de la inteligencia artificial del sistema. Este modelo de lenguaje avanzado de Google se utiliza para procesar el texto no estructurado de las convocatorias encontradas. Sus tareas principales incluyen: generar consultas de búsqueda, clasificar la relevancia de las fuentes, resumir los objetivos de la convocatoria y extraer datos clave como fechas límite, montos de financiamiento y requisitos de elegibilidad.
*   **Costos Asociados**:
    *   **Plan Gratuito**: Incluye un límite de peticiones por minuto (ej. 15 RPM para el modelo `gemini-1.5-flash` el cuál utilizamos para nuestra herramienta) y un límite diario de 50 peticiones.
    *   **Planes de Pago (Pay-as-you-go)**: Una vez superada la capa gratuita (+1M de tokens procesados), se paga por uso basado en el número de tokens procesados, alrededor de **$0.35 USD**.


#### **Brave API / Tavily API**

*   **Rol en el Sistema**: Son los motores de búsqueda que alimentan al sistema. Se utilizan para realizar consultas web automatizadas y descubrir nuevas convocatorias en portales que no ofrecen feeds RSS. Tavily está especialmente optimizado para ser utilizado por agentes de IA, proporcionando resultados de búsqueda concisos y relevantes que facilitan el posterior análisis por parte de Gemini.
*   **Costos Asociados**:
    *   **Plan Gratuito**: Incluyen un número limitado de consultas de búsqueda al mes de 2,000 consultas/mes y 1 petición/segundo.
    *   **Planes de Pago**: Ofrecen planes de suscripción mensual para un mayor volumen de búsquedas (ej. $5 USD/mes para 20M consultas/mes).

#### **Tecnologías RSS**

*   **Rol en el Sistema**: El sistema se suscribe a feeds RSS (Really Simple Syndication) de fuentes confiables y conocidas. Este es un método altamente eficiente y estructurado para recibir notificaciones automáticas sobre nuevas convocatorias directamente de la fuente.
*   **Costos Asociados**:
    *   **Costo Cero**: La tecnología RSS es un estándar web abierto y su uso es **completamente gratuito**. No hay APIs, ni claves, ni límites de peticiones.

#### **LangSmith**

*   **Rol en el Sistema**: Es una plataforma de observabilidad y depuración. Se integra con LangChain para ofrecer una trazabilidad completa de las operaciones del agente. Permite a los desarrolladores monitorear cada paso del proceso (búsquedas, llamadas a Gemini, extracción de datos), facilitando la identificación de errores, la optimización de los *prompts* y la mejora continua de la fiabilidad del sistema.
*   **Costos Asociados**:
    *   **Plan Gratuito (Developer Plan)**: Incluye 5000 trazas/mes (registros de ejecución).
    *   **Planes de Pago**: Existen planes de pago que ofrecen más trazas, mayor retención de datos y funcionalidades colaborativas.


### **Análisis de Costos en Operación Real**

Hemos analizado una ejecución típica de nuestra herramienta utilizando el modelo **Gemini 1.5 Flash**.

#### **1. Costo del Flujo de Descubrimiento**

Una ejecución completa de esta fase es un proceso de múltiples pasos. El consumo de tokens se desglosa de la siguiente manera:

*   **Generación de Queries**: Una única llamada a la API para crear 10 consultas de búsqueda estratégicas (5 ideas x 2 regiones).
    *   *Consumo*: ~1,000 tokens.
*   **Escrutinio de Resultados**: Múltiples llamadas pequeñas para clasificar la relevancia de cada resultado encontrado (~40 resultados en un escenario típico).
    *   *Consumo por resultado*: ~200 tokens.
    *   *Consumo total*: ~8,000 tokens.
*   **Extracción de Oportunidades**: Llamadas más intensivas para leer el contenido de las páginas relevantes (~10 fuentes en un escenario típico) y extraer la información.
    *   *Consumo por extracción*: ~1,350 tokens.
    *   *Consumo total*: ~13,500 tokens.

Esto resulta en un consumo total aproximado para el flujo:

*   **Consumo Total de Tokens**: **~22,500 tokens**
*   **Costo por Ejecución**: **~$0.0027 USD**

#### **2. Costo del Flujo de Enriquecimiento**

El enriquecimiento de una oportunidad individual (que implica buscar la fuente primaria, scrapear la página y analizar su contenido) es el paso más intensivo por unidad. En promedio, consume:

*   **Consumo por Oportunidad**: **~5,000 tokens**
*   **Costo por Oportunidad**: **~$0.0004 USD**

#### **Escenario Típico: Una Vigilancia Completa**

Un escenario común es que el flujo de descubrimiento identifique **40 oportunidades** que luego pasan a ser enriquecidas. El desglose de costos sería:

| Flujo | Consumo Estimado | Costo Estimado |
| :--- | :--- | :--- |
| **Descubrimiento** | 22,500 tokens | $0.0027 USD |
| **Enriquecimiento (40 opps)** | 200,000 tokens (40 x 5,000) | $0.0160 USD |
| **TOTAL POR VIGILANCIA** | **~222,500 tokens** | **~$0.0187 USD** |

Como se puede observar, una vigilancia completa que encuentra y enriquece 40 oportunidades tiene un costo inferior a **dos centavos de dólar**.

---

### **Proyección en la Capa Gratuita**

¿Cuántas vigilancias se pueden realizar antes de incurrir en costos? Para responder a esto, debemos considerar los dos cuellos de botella principales de la capa gratuita: las consultas de búsqueda y los tokens de Gemini.

1.  **Límite de Búsqueda (Brave/Tavily)**: ~2,000 consultas/mes.
2.  **Límite de Tokens (Gemini)**: ~1,000,000 tokens/mes.

Ahora, calculemos cuántas ejecuciones permite cada límite:

*   **Ejecuciones limitadas por Búsqueda**:
    *   `2,000 consultas / 10 consultas por ejecución` = **200 ejecuciones/mes**.
*   **Ejecuciones limitadas por Tokens de Gemini (flujo completo)**:
    *   `1,000,000 tokens / 222,500 tokens por ejecución` = **~4 ejecuciones/mes**.

**Conclusión**: El verdadero cuello de botella en la capa gratuita para el **agente completo** (Descubrimiento + Enriquecimiento) es el **límite de tokens de Gemini**. Sin embargo, esto nos da una gran flexibilidad:

*   **Ejecución del Agente Completo**: Puedes realizar aproximadamente **4 vigilancias completas al mes** (encontrando y enriqueciendo ~160 oportunidades en total) sin costo alguno.
*   **Ejecución del Flujo de Descubrimiento Únicamente**: Si solo necesitas encontrar las oportunidades sin enriquecerlas, el límite lo imponen los tokens de este flujo:
    *   `1,000,000 tokens / 22,500 tokens por descubrimiento` = **~44 ejecuciones de descubrimiento al mes**.
    *   Esto equivale a más de **una ejecución de descubrimiento por día**, lo cual es excelente para un monitoreo constante y gratuito.

---

### **Comparativa de Costos: Gemini vs. OpenAI**

Para poner en perspectiva la elección del modelo, a continuación se compara el costo del "Escenario Típico" si se utilizara un modelo equivalente de OpenAI como **GPT-3.5-Turbo**.

| Flujo | Gemini 1.5 Flash (Costo) | OpenAI GPT-3.5-Turbo (Costo Estimado) |
| :--- | :--- | :--- |
| **Descubrimiento** | **$0.0027** | ~$0.0180 |
| **Enriquecimiento (40 opps)** | **$0.0160** | ~$0.1600 |
| **TOTAL POR VIGILANCIA** | **~$0.0187** | **~$0.1780** |

**Conclusión**: Al utilizar Gemini 1.5 Flash, el costo operativo del agente es aproximadamente **9.5 veces más económico** que si se utilizara GPT-3.5-Turbo para las mismas tareas.



#### **Flujo de Trabajo e Interacción entre Servicios**

El funcionamiento del sistema sigue un flujo lógico y asíncrono para garantizar una experiencia de usuario fluida y un procesamiento eficiente.

1.  **Inicio de la Solicitud**: El usuario interactúa con la interfaz de **Angular**, por ejemplo, registrando un nuevo proyecto de investigación y solicitando la búsqueda de financiamiento.

2.  **Gestión de la API**: El FrontEnd envía una petición a la **API de Django**. El backend valida la solicitud, autentica al usuario y guarda la información del proyecto en la base de datos **PostgreSQL**.

3.  **Encolado de Tareas**: En lugar de ejecutar la búsqueda directamente (lo que bloquearía el sistema), la API crea una tarea específica (ej: "buscar_oportunidades") y la envía a **Redis**. Redis la almacena en una cola y la API responde inmediatamente al usuario, informándole que el proceso ha comenzado.

4.  **Procesamiento en Segundo Plano**: El **Worker de Celery**, que está constantemente escuchando la cola de Redis, detecta la nueva tarea y la toma para su procesamiento.

5.  **Investigación y Enriquecimiento**: El Worker utiliza **LangChain** para orquestar una serie de acciones:
    *   Consulta a APIs de búsqueda como **Brave** o **Tavily** y fuentes **RSS** para recopilar información de la web.
    *   Envía los datos recolectados a la **API de Gemini** para su análisis, resumen, extracción de entidades clave (fechas, requisitos) y clasificación.
    *   **LangSmith** se utiliza para monitorear y depurar las cadenas de llamadas a los modelos de lenguaje, asegurando su fiabilidad.

6.  **Almacenamiento de Resultados**: Una vez procesada la información, el Worker estructura los resultados (oportunidades de financiamiento, resúmenes, etc.) y los guarda en la base de datos **PostgreSQL**, asociándolos con el proyecto y usuario correspondientes.

7.  **Notificación y Visualización**: Al finalizar la tarea, el sistema puede generar una notificación automática (vía email o en la app). El usuario ya puede acceder a su panel en **Angular** para visualizar los resultados, los cuales son servidos por la **API de Django** consultando la información previamente almacenada en la base de datos.


Otra forma de ver el flujo de trabajo es mediente la siguiente ilustración:

![Diagrama de flujo del sistema](/images/flow_search_system.png)


#### **Modelo de Datos**

La persistencia y la estructura de la información se gestionan a través de una base de datos relacional PostgreSQL. El diseño del modelo de datos está pensado para reflejar de manera lógica las interacciones entre los usuarios, los proyectos de investigación, las oportunidades de financiamiento y los resultados generados por el sistema. Esta organización garantiza la integridad de los datos, facilita las consultas complejas y asegura la escalabilidad de la plataforma.

##### **Diagrama Entidad-Relación (ERD)**

![Diagrama de la Base de Datos](/images/ER.jpeg)

##### **Descripción de las Entidades**

A continuación, se detalla el propósito de cada una de las tablas principales del sistema:

*   **User**: Almacena la información esencial para la autenticación y gestión de los usuarios, incluyendo su nombre de usuario y contraseña (almacenada de forma segura mediante hashing).

*   **Project**: Representa el núcleo de la vigilancia tecnológica. Cada registro contiene la información clave de un proyecto de investigación definido por el usuario, como el `Título`, la `Descripción` y las `Palabras clave` (`Keywords`). Estos campos son la entrada principal para los agentes de IA que realizan las búsquedas.

*   **Notes**: Proporciona un espacio flexible para que los usuarios registren anotaciones clave. Cada nota está intrínsecamente ligada a un **`Project`**, sirviendo para documentar acciones, hallazgos importantes o ideas surgidas durante el proceso de investigación. Opcionalmente, una nota puede estar asociada directamente a una **`Opportunity`** específica para añadir contexto o registrar los siguientes pasos sobre una convocatoria particular.

*   **Opportunity**: Es la entidad central donde se almacenan las oportunidades de financiamiento identificadas y procesadas por el sistema. Contiene datos estructurados y extraídos por la IA, como el `Origen` de la convocatoria, `Descripción`, `Financiamiento`, `Requisitos`, `Fecha límite` (`Deadline`) y la `URL` original.

*   **Item_context**: Funciona como un repositorio de las fuentes de información brutas que los agentes de IA han considerado relevantes durante una búsqueda. Cada registro contiene el `Título`, `Descripción`, `URL` y un `Resumen` de una página web o documento analizado, sirviendo como la evidencia que respalda una `Opportunity` encontrada.

*   **Research**: Actúa como un registro histórico de cada ejecución del proceso de búsqueda para un proyecto. Almacena metadatos sobre el proceso, como la `Fecha` y `Hora` de ejecución (`Execute_time`), así como métricas de rendimiento como el `Relevance_ratio` y el `Opportunity_ratio`.

*   **Report**: Guarda una referencia a los informes generados al finalizar un ciclo de investigación. Incluye la `Fecha` de creación y la ruta de acceso (`Path`) al archivo del reporte, permitiendo un acceso rápido a los resultados consolidados.

##### **Relaciones Clave**

Las entidades están interconectadas para mantener la coherencia y el contexto de los datos a lo largo del flujo de trabajo de la aplicación:

*   Un **`User`** puede ser propietario y gestionar múltiples **`Projects`**.
*   Un **`Project`** es el contenedor principal de la actividad de vigilancia y puede tener asociados:
    *   Múltiples ejecuciones de **`Research`** a lo largo del tiempo.
    *   Múltiples **`Opportunities`** que se han identificado como relevantes.
    *   Múltiples **`Notes`**, que sirven como bitácora de hallazgos y acciones relacionadas con el proyecto.
*   Cada **`Research`** genera un único **`Report`** final.
*   Una **`Opportunity`** se deriva de la información contenida en uno o varios **`Item_context`**.
*   La relación de las **`Notes`** es la siguiente:
    *   Son creadas por un **`User`**.
    *   Siempre pertenecen a un **`Project`**.
    *   Opcionalmente, pueden hacer referencia a una **`Opportunity`** para añadirle comentarios específicos.


#### **Estrategia de Seguridad y Autenticación**

La seguridad de los datos y el control de acceso son componentes críticos de la arquitectura del sistema. Dado que la plataforma gestionará información específica de los usuarios (proyectos de investigación, resultados, reportes), se implementará un esquema de seguridad robusto basado en tokens para proteger la API y garantizar que cada usuario solo pueda acceder a sus propios recursos.

La estrategia de seguridad se fundamenta en los siguientes pilares:

![Diagrama de flujo de autenticacion](/images/JWT.jpeg)

##### **1. Autenticación basada en Tokens (JWT)**

Debido a la naturaleza desacoplada de la arquitectura (Frontend Angular y Backend Django), se utilizará el estándar **JSON Web Tokens (JWT)** para gestionar la autenticación y las sesiones de usuario. Este enfoque es ideal para APIs sin estado (*stateless*), ya que el servidor no necesita almacenar información de la sesión.

El flujo de autenticación funcionará de la siguiente manera:

*   **Proceso de Login:**
    1.  El usuario ingresará sus credenciales (email y contraseña) en la interfaz de Angular.
    2.  El Frontend enviará estas credenciales a un endpoint específico y público de la API de Django (ej: `/api/token/`).
    3.  El Backend verificará las credenciales contra la base de datos. Para proteger las contraseñas, estas se almacenarán siempre de forma cifrada mediante un algoritmo de hashing fuerte e irreversible (como Argon2 o PBKDF2), garantizando que nunca se guarden en texto plano.
    4.  Si las credenciales son válidas, la API generará un par de tokens JWT firmados digitalmente:
        *   **Access Token (Token de Acceso):** Un token de corta duración (ej. 15 minutos) que el Frontend incluirá en la cabecera `Authorization` de cada solicitud a rutas protegidas. Su corta vida útil minimiza el riesgo en caso de ser interceptado.
        *   **Refresh Token (Token de Refresco):** Un token de larga duración (ej. 1 día) que se utiliza únicamente para solicitar un nuevo *Access Token* cuando el anterior expire, sin necesidad de que el usuario vuelva a iniciar sesión.
    5.  Estos tokens serán devueltos al Frontend, que se encargará de almacenarlos de forma segura.

##### **2. Autorización y Protección de Rutas**

Una vez que el usuario está autenticado, el sistema garantizará el acceso seguro a los recursos.

*   **Protección de Endpoints:** Todos los endpoints de la API que manejen datos sensibles (CRUD de proyectos, visualización de resultados, etc.) serán privados. Requerirán que cada solicitud incluya un *Access Token* válido en la cabecera `Authorization: Bearer <token>`.
*   **Validación en el Backend:** En cada solicitud a una ruta protegida, la API de Django realizará los siguientes pasos:
    1.  Extraerá el JWT de la cabecera.
    2.  Verificará la firma digital del token para asegurar su autenticidad y que no ha sido modificado.
    3.  Validará que el token no haya expirado.
    4.  Si el token es válido, identificará al usuario asociado a él y le dará acceso al recurso solicitado.
    5.  Si el token es inválido, ha expirado o no está presente, la API rechazará la solicitud con un estado de error `401 Unauthorized`.

##### **3. Aislamiento de Datos de Usuario (Data Scoping)**

La autenticación no es suficiente; la autorización debe garantizar que un usuario autenticado solo pueda ver y gestionar sus propios datos. El backend de Django implementará lógica de permisos a nivel de vista o de consulta para que, por ejemplo, al solicitar `/api/projects/`, el sistema filtre automáticamente los resultados para devolver únicamente los proyectos que pertenecen al usuario identificado por el token. Esto previene que un usuario pueda acceder a la información de otro, incluso si conoce el ID del recurso.

##### **4. Flujo de Registro Seguro**

El proceso de creación de nuevas cuentas también seguirá prácticas de seguridad.
*   Se expondrá un endpoint público (`/api/register/`) para el registro de nuevos usuarios.
*   La lógica del backend validará los datos de entrada (ej. formato de email, complejidad de la contraseña).
*   Como se mencionó anteriormente, la contraseña proporcionada por el usuario será inmediatamente procesada por un algoritmo de **hashing** antes de ser almacenada en la base de datos. Este es el principio de seguridad más importante para la protección de credenciales.

#### **Propuesta Visual**

La interfaz de usuario (UI) y la experiencia de usuario (UX) están diseñadas para ser limpias, intuitivas y funcionales, permitiendo a los investigadores centrarse en la gestión de sus proyectos sin distracciones. Se ha optado por un diseño moderno con un tema oscuro para reducir la fatiga visual y resaltar los elementos importantes de la interfaz.

Es importante señalar que las imágenes presentadas a continuación corresponden a un diseño conceptual inicial y están sujetas a cambios. Si bien la disposición específica de algunos componentes podría variar durante el desarrollo para mejorar el flujo de trabajo, el estilo artístico general, la paleta de colores, la tipografía y la estética moderna se mantendrán como la línea base del producto final.

A continuación, se presenta el flujo visual de la aplicación a través de sus pantallas clave.

##### **1. Autenticación y Acceso**

El acceso a la plataforma comienza con una pantalla de inicio de sesión minimalista. Los nuevos usuarios pueden registrarse a través de un formulario sencillo que solicita únicamente la información necesaria para crear la cuenta.

| Inicio de Sesión                                | Creación de Cuenta                                 |
| :---------------------------------------------- | :------------------------------------------------- |
| ![Login de Usuario](/images/login.png)          | ![Registro de Usuario](/images/register.png)       |

##### **2. Dashboard Principal de Proyectos**

Una vez autenticado, el usuario es recibido por el "Dashboard de Proyectos". Esta es la vista central donde se listan todos los proyectos de vigilancia activos. Cada proyecto se muestra en una tarjeta que resume su estado, el número de oportunidades encontradas y la fecha de la última búsqueda. Desde aquí, el usuario puede gestionar proyectos existentes o iniciar uno nuevo.

![Dashboard de Proyectos](/images/deashboard.png)

##### **3. Creación y Gestión de Proyectos**

Al hacer clic en "+ Nuevo Proyecto", se despliega un modal que guía al usuario para definir el alcance de la vigilancia. Aquí se introduce el `Título`, la `Descripción` y las `Palabras Clave` que los agentes de IA utilizarán como base para la búsqueda.

![Creación de un Nuevo Proyecto](/images/create_proyect.png)

##### **4. Vista Detallada del Proyecto y Oportunidades**

Al seleccionar un proyecto, el usuario accede a su panel de control específico. Esta vista presenta una descripción detallada del proyecto y tres pestañas principales:

*   **Oportunidades:** Muestra las convocatorias de financiamiento encontradas, presentadas en tarjetas claras y concisas.
*   **Historial de Búsquedas:** Registra cada ejecución de la investigación, mostrando su fecha, duración y estado.
*   **Fuentes Analizadas:** Proporciona transparencia sobre las URLs y fuentes que el sistema ha consultado.

![Vista de un Proyecto Específico](/images/details.proyect.png)

##### **5. Proceso de Búsqueda Asíncrona**

Cuando se inicia una nueva búsqueda, la interfaz proporciona retroalimentación visual en tiempo real, informando al usuario que el proceso se está ejecutando en segundo plano. Esto confirma la naturaleza asíncrona del sistema, permitiendo al usuario seguir navegando mientras los workers procesan la solicitud. Una vez completada, la ejecución aparece registrada en el historial.

![Flujo de Búsqueda Activa](/images/flow_activate.png)

##### **6. Detalles de la Oportunidad**

Para explorar una convocatoria en profundidad, el usuario puede hacer clic en "Ver Detalles" en cualquiera de las tarjetas de oportunidad. Esto abre un modal con toda la información estructurada y extraída por la IA, como la `Fecha Límite`, `Tipo de Financiación`, `URL` original, `Descripción` y `Requisitos Principales`, permitiendo una evaluación rápida y eficiente.

![Detalles de una Oportunidad de Financiamiento](/images/details_opportunities.png)


##### **Prototipo Interactivo (Demo)**

Para una experiencia más interactiva, se ha desplegado una maqueta (comúnmente llamada *dummy* o *mockup*) de la interfaz. Puedes navegar y explorar el flujo visual del prototipo, aunque sin funcionalidad de backend, en el siguiente enlace:

**[Explorar la Demo en Vivo](https://carlosdac2020.github.io/FINCOR/)**



## **Metodología y Estrategias de Trabajo**
Para garantizar el cumplimiento de los objetivos y la entrega de una solución robusta y escalable, el proyecto se gestionará bajo un marco de trabajo ágil, combinando fases de desarrollo bien definidas con estrategias técnicas especializadas en la recolección y procesamiento inteligente de datos.

### **Metodología de Desarrollo**
El desarrollo del proyecto se ejecutará siguiendo una metodología iterativa con un enfoque ***Core-First*** (del núcleo hacia afuera). Partiendo del diseño arquitectónico, el modelo de datos y la conceptualización de la interfaz de usuario ya definidos, la estrategia consiste en construir y validar el componente de mayor complejidad técnica en nuestro caso los **agentes AI de investigacion** antes de desarrollar el resto de la infraestructura de soporte.

El proceso de desarrollo se llevará a cabo en las siguientes fases:

#### **Fase I: Prueba de Concepto (PoC) y Consolidación del Núcleo de IA**

El objetivo primordial de esta fase es construir y validar el "cerebro" del sistema para garantizar su viabilidad técnica. El esfuerzo se concentrará en desarrollar un prototipo robusto del agente de investigación.
*   **Ingeniería de Prompts y Flujos con LangChain:** Se diseñarán, implementarán y probarán de forma aislada los flujos de LangChain. Esto implica un ciclo iterativo de:
    *   **Construcción de Cadenas (Chains):** Se crearán las secuencias de llamadas que conectan las entradas del usuario (descripción del proyecto) con las APIs de búsqueda (Tavily/Brave) y el modelo de lenguaje (Gemini).
    *   **Optimización de Prompts:** Se realizará una ingeniería de prompts detallada para instruir a las APIs de LLMs sobre cómo analizar el contenido web, identificar y extraer con precisión las entidades clave (fechas, montos, requisitos, áreas temáticas) y generar resúmenes ejecutivos de alta calidad.
    *   **Validación de Salidas:** Se evaluará rigurosamente la precisión y relevancia de los datos extraídos para asegurar que el agente sea fiable y predecible.
*   **Entregable:** Un conjunto de scripts o módulos de Python funcionalmente probados que encapsulan la lógica de investigación y análisis, listos para ser integrados en un sistema mayor.

#### **Fase II: Implementación de la Infraestructura Asíncrona y Backend Inicial**

Una vez validado el núcleo de IA, se construirá la infraestructura de soporte para ejecutarlo de manera eficiente y escalable.
*   **Orquestación de Servicios:** Se levantará el ecosistema de microservicios utilizando **Docker y Docker-Compose**, definiendo las redes, volúmenes y variables de entorno para una gestión unificada.
*   **Implementación del Pipeline Asíncrono:** Se desarrollará el flujo de procesamiento en segundo plano:
    *   **API (Django):** Actuará como el orquestador central. Recibirá las solicitudes del usuario y las traducirá en tareas específicas.
    *   **Cola de Tareas (Redis):** Funcionará como el sistema nervioso descentralizado, encolando las tareas generadas por la API para garantizar que ninguna solicitud se pierda y que el sistema pueda manejar picos de carga.
    *   **Worker (Celery):** Será el "caballo de batalla" del sistema. Se configurará para escuchar la cola de Redis, tomar las tareas y ejecutar los módulos de LangChain desarrollados en la Fase I.
*   **Entregable:** Un backend esquelético pero completamente funcional, con un **endpoint de inicio de investigación genérico**. Este endpoint nos permitirá al equipo de comenzar las integraciones iniciales del frontend, enviando una solicitud y confirmando que la tarea ha sido encolada exitosamente.

#### **Fase III: Consolidación de la API, Lógica de Negocio y Persistencia**

Esta fase se centrará en dotar a la API de toda la lógica de negocio y las capacidades de gestión de datos.
*   **Implementación del Modelo de Datos:** Se traducirá el Diagrama Entidad-Relación al ORM de Django, creando las tablas en la base de datos **PostgreSQL** para almacenar de forma persistente usuarios, proyectos y las oportunidades de financiación descubiertas.
*   **Desarrollo de Endpoints Completos:** Se construirán todos los endpoints RESTful necesarios para la **gestión del ciclo de vida completo de un proyecto**, incluyendo el CRUD (Crear, Leer, Actualizar, Borrar) para proyectos y la consulta de resultados.
*   **Seguridad y Autenticación:** Se integrará un sistema de autenticación basado en tokens (ej. JWT) para proteger la API, asegurando que los usuarios solo puedan acceder y gestionar sus propios datos.

#### **Fase IV: Desarrollo de la Interfaz de Usuario y Experiencia Final**

Con una API robusta y documentada, se construirá la capa de presentación con la que interactuará el usuario final.
*   **Construcción de la Interfaz Reactiva:** Utilizando **Angular**, se desarrollará una Single-Page Application (SPA) que consuma los servicios de la API.
*   **Implementación de Funcionalidades Clave:** El desarrollo se enfocará en crear una experiencia de usuario intuitiva, implementando:
    *   **Paneles de control (Dashboards):** Para la visualización clara y organizada de las oportunidades de financiación encontradas, con filtros y opciones de ordenamiento.
    *   **Formularios de Gestión:** Para la creación y edición de proyectos de investigación.
    *   **Sistema de Notificaciones:** Se integrarán las alertas visuales en la interfaz para informar al usuario sobre la finalización de una investigación o el hallazgo de nuevas oportunidades.

#### **Fase V: Pruebas Integrales, Despliegue y Documentación**

La fase final se dedicará a garantizar la calidad, estabilidad y mantenibilidad del sistema.
*   **Estrategia de Pruebas:** Se ejecutarán pruebas exhaustivas a distintos niveles: unitarias para la lógica de negocio en Django, de integración para la comunicación entre servicios (API-Worker) y **pruebas End-to-End (E2E)** para validar los flujos de usuario completos desde el frontend hasta la base de datos.
*   **Despliegue a Producción:** Se prepararán los contenedores de Docker para un entorno de producción y se automatizará el proceso de despliegue.
*   **Documentación Final:** Se generará la documentación técnica detallada (ej. colección de Postman/Swagger para la API) y el manual de usuario.


### **Estrategias Técnicas Clave**

Para la ejecución de las fases de desarrollo, se implementarán las siguientes estrategias:

*   **Estrategia de Recolección de Datos Híbrida:** En lugar de depender de una única fuente, se combinarán múltiples técnicas para maximizar la cobertura y la calidad de la información.
    *   **Web Scraping Dirigido:** Se identificarán portales clave que no ofrezcan APIs o RSS y se crearán *scrapers* específicos para ellos. Esta tarea será ejecutada por los *Workers* de Celery.
    *   **Consumo de APIs de Búsqueda:** Se utilizarán las APIs de Tavily y/o Brave para realizar búsquedas amplias en la web, simulando el comportamiento de un investigador pero de forma automatizada. Tavily es especialmente útil por su optimización para agentes de IA.
    *   **Suscripción a Feeds RSS:** Se implementará un lector de RSS para monitorear de forma eficiente y estructurada las publicaciones de agencias de financiación y portales oficiales.

*   **Procesamiento de Información Basado en Agentes de IA:** La inteligencia del sistema residirá en el uso de modelos de lenguaje avanzados (LLM) orquestados con LangChain.
    *   **Agente de Búsqueda y Filtrado:** Este agente se encargará de formular *queries* de búsqueda eficientes a partir de la descripción de un proyecto. Posteriormente, realizará un primer filtrado para descartar resultados irrelevantes.
    *   **Agente de Análisis y Extracción:** Recibirá los datos pre-filtrados y utilizará LLMs para leer, comprender y extraer la información estructurada clave: nombre de la convocatoria, entidad financiadora, fechas de apertura y cierre, áreas de investigación, requisitos y montos.

*   **Arquitectura Asíncrona y Orientada a Eventos:** El núcleo del sistema se basará en el patrón productor-consumidor. La API de Django actuará como productora, enviando tareas a la cola de Redis. Los *Workers* de Celery (consumidores) tomarán estas tareas y las ejecutarán en segundo plano. Este enfoque es fundamental para:
    *   **No Bloquear al Usuario:** El usuario recibe una respuesta inmediata de la API, mientras que el procesamiento pesado ocurre de forma asíncrona.
    *   **Escalabilidad y Resiliencia:** Es posible añadir más *Workers* para aumentar la capacidad de procesamiento sin alterar el resto del sistema. Si un *Worker* falla, la tarea puede ser reintentada sin afectar la experiencia del usuario.