# -*- coding: utf-8 -*-
"""Generador del sitio Homo Psicologicus — páginas independientes por sección.
Uso:  python build.py   (regenera todos los .html en la carpeta del sitio)
"""
import os

SITE = os.path.dirname(os.path.abspath(__file__))
ASSET_VER = "handhold2"  # bump en cada cambio de estilos/js para romper caché

NAV = [
    ("index.html", "Inicio", ""),
    ("aportes.html", "Aportes", "aportes"),
    ("brujula.html", "Brújula Joven", "brujula"),
    ("escritos.html", "Escritos", "escritos"),
    ("innovacion.html", "Innovación", "innovacion"),
    ("video.html", "Video", "video"),
    ("sobre-mi.html", "Sobre mí", "sobre-mi"),
]

SOCIALS = [
    ("https://universidadnacionalhermiliovaldizan.academia.edu/CarlosDCamachoT", "academia.edu"),
    ("https://www.linkedin.com/in/carloscamachot", "LinkedIn"),
]


THEME_INLINE = """<script>
    (function () {
      var t;
      try { t = localStorage.getItem("hp-theme"); } catch (e) {}
      if (t === "dark" || t === "light") {
        document.documentElement.setAttribute("data-theme", t);
      }
    })();
  </script>"""


def head(title, desc, current, preload_hero=False):
    nav_links = "\n        ".join(
        f'<a href="{href}" {"aria-current=\"page\" " if key == current else ""}>'
        f'{label}</a>' for href, label, key in NAV
    )
    preload = ""
    if preload_hero:
        preload = """
  <link rel="preload" as="image" href="assets/img/hero-marble.webp?v={v}">
  <link rel="preload" as="image" href="assets/img/carlos-portrait.webp?v={v}">""".format(v=ASSET_VER)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ASSET_VER}">
  {THEME_INLINE}
  <script src="app.js?v={ASSET_VER}" defer></script>{preload}
</head>
<body class="grain">

  <a class="skip-link" href="#main">Saltar al contenido</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html">Homo <em>Psicologicus</em></a>
      <nav class="site-nav" aria-label="Principal">
        {nav_links}
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" type="button" aria-label="Cambiar tema claro u oscuro" aria-pressed="false">
          <svg class="theme-icon theme-icon--sun" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg class="theme-icon theme-icon--moon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <a class="btn btn-primary btn-sm" href="https://www.linkedin.com/in/carloscamachot" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </header>

  <main id="main">
"""


def footer():
    social_links = " · ".join(f'<a href="{url}" target="_blank" rel="noopener">{label}</a>' for url, label in SOCIALS)
    return f"""
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <p>Homo Psicologicus — Todos los derechos reservados.</p>
      <p class="footer-meta">{social_links} · <span class="footer-year"></span></p>
    </div>
  </footer>

</body>
</html>"""


def write_page(name, title, desc, current, body, preload_hero=False):
    path = os.path.join(SITE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(head(title, desc, current, preload_hero=preload_hero) + body + footer())
    print("  OK:", name)


def page_header(index, title, intro):
    return f"""    <section class="page-header">
      <div class="container">
        <p class="hero-eyebrow reveal" style="--i:0"><span class="section-index" aria-hidden="true">{index}</span>{title}</p>
        <h1 class="reveal" style="--i:1">{title}</h1>
        <p class="reveal" style="--i:2">{intro}</p>
      </div>
    </section>
"""


def build_index():
    cards = ""
    sections = [
        ("aportes.html", "01", "Aportes", "Cuatro líneas de trabajo para la comunidad: academia, ciencia, mundo laboral y mentoría."),
        ("brujula.html", "02", "Brújula Joven", "Cosas que nadie te enseña: guías prácticas, checklists y FAQ para estudiantes y jóvenes psicólogos."),
        ("escritos.html", "03", "Escritos", "Reflexiones, artículos y notas de psicología, organizados por categoría."),
        ("innovacion.html", "04", "Cogito, Ergo Innovo", "Las oportunidades de la psicología en la innovación: tecnología, investigación y emprendimiento."),
        ("video.html", "05", "En video", "El canal de Homo Psicologicus en video: conversaciones, guías y análisis."),
        ("sobre-mi.html", "06", "Sobre mí", "El proyecto y la persona detrás: Psic. Carlos Camacho."),
    ]
    for href, num, title, desc in sections:
        cards += f"""
          <article class="pillar">
            <span class="pillar-num" aria-hidden="true">{num}</span>
            <h3 class="pillar-title"><a href="{href}">{title}</a></h3>
            <p class="pillar-text">{desc}</p>
          </article>"""
    body = f"""
    <section id="top" class="hero">
      <div class="hero-media" aria-hidden="true">
        <img class="hero-img hero-img--a" src="assets/img/hero-marble.webp?v={ASSET_VER}" alt="" width="1920" height="1072" fetchpriority="high">
        <img class="hero-img hero-img--b" src="assets/img/carlos-portrait.webp?v={ASSET_VER}" alt="" width="1100" height="1971" loading="lazy">
        <div class="hero-scrim"></div>
      </div>
      <div class="container">
        <p class="hero-eyebrow reveal" style="--i:0">Un proyecto de psicología para la comunidad</p>
        <h1 class="hero-title reveal" style="--i:1">
          Homo <em>Psicologicus</em>
        </h1>
        <div class="hero-rule reveal" style="--i:2" aria-hidden="true"></div>
        <p class="hero-sub reveal" style="--i:3">
          Pensar la psicología como ciencia, oficio y compromiso humano.
          Un espacio para aportar a la comunidad académica, científica,
          laboral y de mentoría.
        </p>
        <div class="hero-actions reveal" style="--i:4">
          <a class="btn btn-primary" href="#secciones">Explorar las secciones</a>
          <a class="btn btn-ghost" href="https://universidadnacionalhermiliovaldizan.academia.edu/CarlosDCamachoT" target="_blank" rel="noopener">Perfil académico</a>
        </div>
      </div>
    </section>

    <section id="secciones" class="section">
      <div class="container">
        <div class="section-head">
          <span class="section-index" aria-hidden="true">01</span>
          <h2 class="section-title">Secciones</h2>
        </div>
        <p class="section-intro">
          Cada sección vive en su propia página. Entra en la que más te interese.
        </p>
        <div class="pillars">
          {cards}
        </div>
      </div>
    </section>
"""
    write_page("index.html", "Homo Psicologicus — Psicología para la comunidad",
               "Homo Psicologicus. Un proyecto de psicología orientado al aporte a la comunidad académica, científica, laboral y de mentoría.",
               "", body, preload_hero=True)


def build_aportes():
    body = page_header("01", "Aportes",
                       "Cuatro líneas desde las que trabajar por la comunidad. Cada una convierte el conocimiento psicológico en algo útil para otros.")
    body += """
    <section class="section" style="padding-top:0">
      <div class="container">
        <div class="pillars">
          <article class="pillar">
            <span class="pillar-num" aria-hidden="true">01</span>
            <h3 class="pillar-title">Academia</h3>
            <p class="pillar-text">Investigación, publicación y divulgación científica. Acercar el conocimiento a quien lo necesita. Todo el material académico vive en academia.edu.</p>
            <p style="margin-top:var(--space-s)"><a class="btn btn-outline btn-sm" href="https://universidadnacionalhermiliovaldizan.academia.edu/CarlosDCamachoT" target="_blank" rel="noopener">Ver perfil académico</a></p>
          </article>
          <article class="pillar">
            <span class="pillar-num" aria-hidden="true">02</span>
            <h3 class="pillar-title">Ciencia</h3>
            <p class="pillar-text">Rigor, evidencia y método. Pensar la psicología como disciplina basada en datos, con honestidad intelectual.</p>
          </article>
          <article class="pillar">
            <span class="pillar-num" aria-hidden="true">03</span>
            <h3 class="pillar-title">Mundo laboral</h3>
            <p class="pillar-text">Inserción profesional, derechos laborales y desarrollo de carrera de las y los psicólogos.</p>
          </article>
          <article class="pillar">
            <span class="pillar-num" aria-hidden="true">04</span>
            <h3 class="pillar-title">Mentoría</h3>
            <p class="pillar-text">Acompañamiento a estudiantes y jóvenes profesionales en su camino de formación.</p>
          </article>
        </div>

        <h2 style="font-size:var(--step-3);margin:var(--space-3xl) 0 var(--space-m)">¿Por dónde empezar?</h2>
        <ol class="steps">
          <li class="step step--current">
            <div>
              <h3>Explora Brújula Joven</h3>
              <p>Si eres estudiante o joven psicólogo, ahí están las guías prácticas que nadie te enseña.</p>
            </div>
          </li>
          <li class="step">
            <div>
              <h3>Lee los escritos</h3>
              <p>Artículos y reflexiones organizados por categoría, con enlace directo a la lectura.</p>
            </div>
          </li>
          <li class="step">
            <div>
              <h3>Conoce Cogito, Ergo Innovo</h3>
              <p>Las oportunidades de la psicología en la innovación: tecnología, investigación y emprendimiento.</p>
            </div>
          </li>
          <li class="step">
            <div>
              <h3>Escríbeme</h3>
              <p>Para proponer una guía, un tema o simplemente conversar.</p>
            </div>
          </li>
        </ol>

        <div class="callout callout--tip" style="margin-top:var(--space-xl)">
          <span class="callout__label">💡 Para recordar</span>
          <p>Todo el contenido de Homo Psicologicus es gratuito y pensado para la comunidad.</p>
        </div>
      </div>
    </section>
"""
    write_page("aportes.html", "Aportes — Homo Psicologicus",
               "Los cuatro pilares de Homo Psicologicus: academia, ciencia, mundo laboral y mentoría.", "aportes", body)


def build_brujula():
    body = page_header("02", "🧭 Brújula Joven",
                       "Cosas que nadie te enseña: cómo leer un paper, cómo armar un CV académico, cómo pedir mentoría, cómo navegar un posgrado, cuáles son tus derechos laborales. Guías prácticas, checklists y respuestas a preguntas frecuentes.")
    body += """
    <section class="section" style="padding-top:0">
      <div class="container">
        <div class="callout callout--data">
          <span class="callout__label">📊 Dato clave</span>
          <p>La mayoría de los contenidos de formación que un psicólogo necesita en sus primeros años no aparecen en el plan de estudios. Esta sección cubre exactamente eso.</p>
        </div>

        <h2 style="font-size:var(--step-3);margin-bottom:var(--space-m)">Guías disponibles</h2>
        <ul class="guide-list">
          <li>Cómo leer un paper sin rendirte a la mitad</li>
          <li>Cómo armar un CV académico que te abra puertas</li>
          <li>Cómo pedir mentoría (y que te respondan)</li>
          <li>Cómo navegar un posgrado sin perder el rumbo</li>
          <li>Derechos laborales del psicólogo: lo básico</li>
        </ul>

        <h2 style="font-size:var(--step-3);margin-bottom:var(--space-m)">Checklist: antes de pedir mentoría</h2>
        <ol class="steps">
          <li class="step">
            <div><h3>Define tu objetivo</h3><p>Una frase clara de lo que quieres aprender o resolver.</p></div>
          </li>
          <li class="step">
            <div><h3>Investiga a la persona</h3><p>Lee su producción y conoce su línea de trabajo.</p></div>
          </li>
          <li class="step">
            <div><h3>Escribe un mensaje breve</h3><p>Presentación, objetivo y una pregunta concreta. Máximo 5 líneas.</p></div>
          </li>
          <li class="step">
            <div><h3>Agradece siempre</h3><p>Aunque no responda, una respuesta cortés deja puerta abierta.</p></div>
          </li>
        </ol>

        <h2 style="font-size:var(--step-3);margin:var(--space-xl) 0 var(--space-m)">Preguntas frecuentes</h2>
        <details class="faq" open>
          <summary>¿Qué es Brújula Joven?</summary>
          <div class="faq-body">
            <p>Un espacio de guías prácticas para estudiantes y jóvenes psicólogos. Cada guía responde una pregunta real con pasos concretos, checklists y recursos.</p>
          </div>
        </details>
        <details class="faq">
          <summary>¿Puedo proponer un tema para una guía?</summary>
          <div class="faq-body">
            <p>Sí. Escríbeme por correo o por LinkedIn con tu duda y la sumamos a la lista de próximas guías.</p>
          </div>
        </details>
        <details class="faq">
          <summary>¿Las guías son gratuitas?</summary>
          <div class="faq-body">
            <p>Todo el contenido de Brújula Joven es y será gratuito, pensado para la comunidad.</p>
          </div>
        </details>
      </div>
    </section>
"""
    write_page("brujula.html", "Brújula Joven — Homo Psicologicus",
               "Guías prácticas, checklists y FAQ para estudiantes y jóvenes psicólogos: leer papers, CV académico, mentoría, posgrado y derechos laborales.",
               "brujula", body)


def build_escritos():
    body = page_header("03", "Escritos",
                       "Reflexiones, artículos y notas de psicología. Cada texto con su categoría y su enlace de lectura. Rellena o elimina las tarjetas que quieras.")
    body += """
    <section class="section" style="padding-top:0">
      <div class="container">
        <div class="writing-grid">
          <article class="writing-card">
            <p>
              <span class="chip chip--ia">IA & Competencias</span>
              <span class="chip chip--psicologia">Psicología</span>
            </p>
            <h3 class="writing-title"><a href="#">[Título de tu escrito]</a></h3>
            <p class="writing-excerpt">[Resumen de una o dos líneas sobre el contenido de este texto.]</p>
            <a class="writing-link" href="#">Leer más →</a>
          </article>
          <article class="writing-card">
            <p>
              <span class="chip chip--filosofia">Filosofía</span>
            </p>
            <h3 class="writing-title"><a href="#">[Título de tu escrito]</a></h3>
            <p class="writing-excerpt">[Resumen de una o dos líneas sobre el contenido de este texto.]</p>
            <a class="writing-link" href="#">Leer más →</a>
          </article>
          <article class="writing-card">
            <p>
              <span class="chip chip--psicologia">Psicología</span>
              <span class="chip chip--marcador">Reflexión</span>
            </p>
            <h3 class="writing-title"><a href="#">[Título de tu escrito]</a></h3>
            <p class="writing-excerpt">[Resumen de una o dos líneas sobre el contenido de este texto.]</p>
            <a class="writing-link" href="#">Leer más →</a>
          </article>
        </div>

        <h2 style="font-size:var(--step-2);margin:var(--space-2xl) 0 var(--space-m)">Leyenda de categorías</h2>
        <p>
          <span class="chip chip--ia">IA & Competencias</span>
          <span class="chip chip--filosofia">Filosofía</span>
          <span class="chip chip--psicologia">Psicología</span>
          <span class="chip chip--marcador">Reflexión</span>
        </p>
        <p style="color:var(--ink-2);margin-top:var(--space-xs);font-size:var(--step--1)">
          Terracota = IA / innovación · Verde = filosofía · Marrón = psicología y estructura.
        </p>
      </div>
    </section>
"""
    write_page("escritos.html", "Escritos — Homo Psicologicus",
               "Artículos y reflexiones de psicología organizados por categoría.", "escritos", body)


def build_innovacion():
    body = page_header("04", "Cogito, Ergo Innovo",
                       "Pienso, luego innovo. Un espacio para explorar las oportunidades de la psicología en la innovación: tecnología, investigación aplicada, emprendimiento y nuevos campos de trabajo.")
    body += """
    <section class="section section-ink">
      <div class="container">
        <blockquote class="pull-quote">
          La psicología no solo explica el mundo: también puede transformarlo.
        </blockquote>
        <div class="innov-grid">
          <article class="innov-item">
            <h3 class="innov-title">Psicología y tecnología</h3>
            <p>UX, bienestar digital, inteligencia artificial y salud mental: campos donde el psicólogo ya es protagonista.</p>
          </article>
          <article class="innov-item">
            <h3 class="innov-title">Investigación aplicada</h3>
            <p>De la evidencia a la solución: proyectos que responden problemas reales de personas y organizaciones.</p>
          </article>
          <article class="innov-item">
            <h3 class="innov-title">Emprendimiento</h3>
            <p>Crear servicios, productos y espacios nuevos desde la disciplina. La innovación también es un oficio.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 style="font-size:var(--step-3);margin-bottom:var(--space-m)">Cómo lleva un psicólogo la innovación</h2>
        <ol class="steps">
          <li class="step step--current">
            <div><h3>Entiende a las personas</h3><p>Esa es la materia prima: comportamiento, motivación, contexto.</p></div>
          </li>
          <li class="step">
            <div><h3>Encuentra el problema real</h3><p>No la solución bonita: la necesidad que de verdad existe.</p></div>
          </li>
          <li class="step">
            <div><h3>Diseña con evidencia</h3><p>Método, datos y validación en cada paso del proceso.</p></div>
          </li>
          <li class="step">
            <div><h3>Mide el impacto</h3><p>El rigor psicológico aporta exactamente ahí: saber si algo funciona y por qué.</p></div>
          </li>
        </ol>

        <div class="callout callout--data" style="margin-top:var(--space-xl)">
          <span class="callout__label">📊 Dato clave</span>
          <p>El término <span class="tooltip" tabindex="0" data-tip="La aplicación de conocimientos psicológicos al diseño de productos, servicios y procesos.">UX</span> y el diseño centrado en las personas tienen su raíz directa en la psicología aplicada.</p>
        </div>
      </div>
    </section>
"""
    write_page("innovacion.html", "Cogito, Ergo Innovo — Homo Psicologicus",
               "Las oportunidades de la psicología en la innovación: tecnología, investigación aplicada y emprendimiento.", "innovacion", body)


def build_video():
    body = page_header("05", "En video",
                       "El canal de YouTube de Homo Psicologicus está en preparación. Pronto, conversaciones, guías y análisis en formato video.")
    body += """
    <section class="section" style="padding-top:0">
      <div class="container">
        <!-- Sustituye el enlace por la URL real de tu canal cuando exista -->
        <div class="video-actions" style="margin-bottom:var(--space-l)">
          <a class="btn btn-primary" href="https://www.youtube.com/" target="_blank" rel="noopener">Ver el canal</a>
        </div>
        <div class="empty-state">
          <h3>Contenido en preparación</h3>
          <p>Cuando el canal esté activo, aquí se listarán los videos, episodios y series.</p>
          <a href="index.html">Volver al inicio</a>
        </div>
      </div>
    </section>
"""
    write_page("video.html", "En video — Homo Psicologicus",
               "El canal de video de Homo Psicologicus: conversaciones, guías y análisis.", "video", body)


def build_sobre_mi():
    body = page_header("06", "Sobre mí",
                       "El proyecto y la persona detrás. Este espacio no gira alrededor de la figura, sino del aporte a la comunidad — pero aquí te cuento quién lo impulsa.")
    body += """
    <section class="section section-tint" style="padding-top:0">
      <div class="container">
        <div class="about-grid">
          <figure class="about-photo">
            <img src="assets/img/carlos-portrait.webp?v=handhold2" alt="Psic. Carlos Camacho, de brazos cruzados" width="1100" height="1971" loading="lazy">
          </figure>
          <div class="about-text">
            <p>
              Soy el <strong>Psic. Carlos Camacho</strong>. Homo Psicologicus busca
              poner la psicología al servicio de la comunidad: con rigor
              científico, calidez humana y compromiso con la formación
              de nuevas generaciones.
            </p>
            <p class="about-bio-placeholder">
              [Amplía aquí tu presentación: trayectoria, formación y lo que
              te mueve a trabajar por la comunidad.]
            </p>
          </div>
          <aside class="about-links">
            <a class="btn btn-outline btn-block" href="https://universidadnacionalhermiliovaldizan.academia.edu/CarlosDCamachoT" target="_blank" rel="noopener">academia.edu</a>
            <a class="btn btn-outline btn-block" href="https://www.linkedin.com/in/carloscamachot" target="_blank" rel="noopener">LinkedIn</a>
          </aside>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 style="font-size:var(--step-3);margin-bottom:var(--space-m)">Contacto</h2>
        <p class="section-intro">
          ¿Quieres escribirme, proponer una guía o conversar sobre psicología
          e innovación? Escríbeme por correo o por LinkedIn.
        </p>
        <details class="faq" open>
          <summary>¿Cómo contacto contigo?</summary>
          <div class="faq-body">
            <p>Por <a href="https://www.linkedin.com/in/carloscamachot" target="_blank" rel="noopener">LinkedIn</a> o por correo a <a href="mailto:[tu-correo@ejemplo.com]">[tu-correo@ejemplo.com]</a>. Respondo a todos los mensajes.</p>
          </div>
        </details>
        <details class="faq">
          <summary>¿Aceptas propuestas de temas?</summary>
          <div class="faq-body">
            <p>Con gusto. Cuéntame tu idea y la evaluamos para Brújula Joven, Escritos o Cogito Ergo Innovo.</p>
          </div>
        </details>
        <div class="contact-actions" style="margin-top:var(--space-l)">
          <a class="btn btn-primary" href="https://www.linkedin.com/in/carloscamachot" target="_blank" rel="noopener">Escribir por LinkedIn</a>
          <a class="btn btn-ghost" href="mailto:[tu-correo@ejemplo.com]">Enviar un correo</a>
        </div>
      </div>
    </section>
"""
    write_page("sobre-mi.html", "Sobre mí — Homo Psicologicus",
               "Conoce al Psic. Carlos Camacho y el proyecto Homo Psicologicus.", "sobre-mi", body)


if __name__ == "__main__":
    print("Generando sitio Homo Psicologicus...")
    build_index()
    build_aportes()
    build_brujula()
    build_escritos()
    build_innovacion()
    build_video()
    build_sobre_mi()
    print("Listo.")