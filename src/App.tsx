import { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSticky, setIsSticky] = useState(false);
  const [activeSection, setActiveSection] = useState("home");
  const [typedText, setTypedText] = useState("");
  const typingRef = useRef({ wordIndex: 0, charIndex: 0, isDeleting: false });

  const roles = [
    "Co-Founder & CTO",
    "Full Stack Developer",
    "Software Engineer",
    "Django & React Specialist",
    "Tech Entrepreneur",
  ];

  const typeEffect = useCallback(() => {
    const { wordIndex, charIndex, isDeleting } = typingRef.current;
    const currentWord = roles[wordIndex];

    if (isDeleting) {
      setTypedText(currentWord.substring(0, charIndex - 1));
      typingRef.current.charIndex--;
    } else {
      setTypedText(currentWord.substring(0, charIndex + 1));
      typingRef.current.charIndex++;
    }

    let timeout = isDeleting ? 50 : 100;

    if (!isDeleting && typingRef.current.charIndex === currentWord.length) {
      timeout = 2000;
      typingRef.current.isDeleting = true;
    } else if (isDeleting && typingRef.current.charIndex === 0) {
      typingRef.current.isDeleting = false;
      typingRef.current.wordIndex = (wordIndex + 1) % roles.length;
      timeout = 500;
    }

    const timer = setTimeout(typeEffect, timeout);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    const cleanup = typeEffect();
    return cleanup;
  }, [typeEffect]);

  useEffect(() => {
    const handleScroll = () => {
      setIsSticky(window.scrollY > 100);

      const sections = ["home", "about", "experience", "skills", "projects", "contact"];
      for (const section of [...sections].reverse()) {
        const el = document.getElementById(section);
        if (el && window.scrollY >= el.offsetTop - 150) {
          setActiveSection(section);
          break;
        }
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
          }
        });
      },
      { threshold: 0.1 }
    );

    document.querySelectorAll(".section-animate").forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
    setIsMenuOpen(false);
  };

  const navLinks = [
    { id: "home", label: "Inicio" },
    { id: "about", label: "Sobre Mí" },
    { id: "experience", label: "Experiencia" },
    { id: "skills", label: "Habilidades" },
    { id: "projects", label: "Proyectos" },
    { id: "contact", label: "Contacto" },
  ];

  return (
    <>
      {/* ===== HEADER ===== */}
      <header className={`header ${isSticky ? "sticky" : ""}`}>
        <span className="logo" onClick={() => scrollToSection("home")}>
          Alejandra<span>.</span>
        </span>

        <nav className={`navbar ${isMenuOpen ? "active" : ""}`}>
          {navLinks.map((link) => (
            <a
              key={link.id}
              className={activeSection === link.id ? "active" : ""}
              onClick={() => scrollToSection(link.id)}
            >
              {link.label}
            </a>
          ))}
        </nav>

        <i
          className={`bx ${isMenuOpen ? "bx-x" : "bx-menu"}`}
          id="menu-icon"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        />
      </header>

      {/* ===== HOME SECTION ===== */}
      <section className="home" id="home">
        <div className="home-content">
          <h3>Hola, soy</h3>
          <h1>Alejandra Lopez</h1>
          <h3 className="typing-text">
            Y soy <span>{typedText}</span>
          </h3>
          <p>
            Co-Fundadora & CTO en Kamello | Ingeniera de Software Full Stack con
            experiencia en Python, Django, React y arquitectura de sistemas escalables.
            Apasionada por la innovaci&oacute;n tecnol&oacute;gica y el liderazgo de equipos
            de desarrollo. Transformo ideas en productos digitales de alto impacto.
          </p>

          <div className="social-media">
            <a href="https://github.com/Alejandra-Lopez17" target="_blank" rel="noopener noreferrer">
              <i className="bx bxl-github" />
            </a>
            <a href="https://www.linkedin.com/in/alejandra-lopez1707/" target="_blank" rel="noopener noreferrer">
              <i className="bx bxl-linkedin" />
            </a>
            <a href="mailto:alejandralopez170723@gmail.com">
              <i className="bx bxl-gmail" />
            </a>
            <a href="tel:+573118252321">
              <i className="bx bxs-phone" />
            </a>
          </div>

          <a href="/Alejandra_Lopez_CV.pdf" className="btn" download>
            Descargar CV
          </a>
        </div>

        <div className="home-img">
          <img src="/images/profile.png" alt="Alejandra Lopez - Co-Founder & Software Engineer" />
        </div>
      </section>

      {/* ===== ABOUT SECTION ===== */}
      <section className="about section-animate" id="about">
        <div className="about-img">
          <img src="/images/profile.png" alt="Alejandra Lopez" />
        </div>

        <div className="about-content">
          <h2>Sobre <span>M&iacute;</span></h2>
          <p>
            Soy <strong>Yovana Alejandra Hinestroza Lopez</strong>, Ingeniera de Software
            y Co-Fundadora & CTO de <strong>Kamello</strong>, una startup tecnol&oacute;gica
            enfocada en soluciones digitales innovadoras. Con experiencia liderando equipos
            de desarrollo y dise&ntilde;ando arquitecturas de software escalables.
          </p>
          <p>
            Mi trayectoria incluye desarrollo Full Stack con <strong>Python, Django, React,
            JavaScript, Docker</strong> y gesti&oacute;n de CRM/ERP como <strong>Salesforce
            y SAP</strong>. He logrado mejorar la eficiencia de sistemas en un 20% y liderar
            proyectos end-to-end desde la concepci&oacute;n hasta el despliegue.
          </p>
          <p>
            Actualmente cursando mi <strong>Bachelor en Ingenier&iacute;a de Software</strong> en
            Jala University y constantemente expandiendo mis competencias t&eacute;cnicas
            y de liderazgo para construir productos que generen impacto real.
          </p>
          <a href="#contact" className="btn" onClick={(e) => { e.preventDefault(); scrollToSection("contact"); }}>
            Cont&aacute;ctame
          </a>
        </div>
      </section>

      {/* ===== EXPERIENCE SECTION ===== */}
      <section className="experience section-animate" id="experience">
        <h2 className="heading">Experiencia & <span>Educaci&oacute;n</span></h2>

        <div className="experience-row">
          {/* Experience Column */}
          <div className="experience-column">
            <h3 className="title">Experiencia Profesional</h3>
            <div className="experience-box">
              <div className="experience-content">
                <div className="content">
                  <div className="year">
                    <i className="bx bxs-calendar" /> 03/2026 - Presente
                  </div>
                  <h3>Co-Founder & CTO - Kamello</h3>
                  <p>
                    Liderando la visi&oacute;n tecnol&oacute;gica y el equipo de desarrollo de una
                    startup innovadora. Dise&ntilde;o de arquitectura de software,
                    toma de decisiones estrat&eacute;gicas y desarrollo full-stack de
                    productos digitales escalables. Remoto, Colombia.
                  </p>
                </div>
              </div>

              <div className="experience-content">
                <div className="content">
                  <div className="year">
                    <i className="bx bxs-calendar" /> 04/2022 - 12/2022
                  </div>
                  <h3>Full Stack Developer - UCOLTIS</h3>
                  <p>
                    Desarrollo de funcionalidades full-stack utilizando Python, Django
                    y React. Mejora de la eficiencia del sistema en un 20% mediante
                    optimizaci&oacute;n de c&oacute;digo y arquitectura. Implementaci&oacute;n de APIs
                    REST y gesti&oacute;n de bases de datos SQL.
                  </p>
                </div>
              </div>

              <div className="experience-content">
                <div className="content">
                  <div className="year">
                    <i className="bx bxs-calendar" /> 04/2022 - 12/2022
                  </div>
                  <h3>Web Developer - Universidad Tecnol&oacute;gica de Pereira</h3>
                  <p>
                    Desarrollo web y optimizaci&oacute;n de plataformas digitales
                    universitarias. Implementaci&oacute;n de soluciones frontend y
                    backend, mejorando la experiencia de usuario y el
                    rendimiento de los sistemas acad&eacute;micos.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Education Column */}
          <div className="experience-column">
            <h3 className="title">Educaci&oacute;n</h3>
            <div className="experience-box">
              <div className="experience-content">
                <div className="content">
                  <div className="year">
                    <i className="bx bxs-calendar" /> 2024 - Presente
                  </div>
                  <h3>Bachelor en Ingenier&iacute;a de Software</h3>
                  <p>
                    Jala University - Formaci&oacute;n integral en ingenier&iacute;a de software,
                    algoritmos, arquitectura de sistemas, metodolog&iacute;as &aacute;giles
                    y desarrollo de software empresarial.
                  </p>
                </div>
              </div>

              <div className="experience-content">
                <div className="content">
                  <div className="year">
                    <i className="bx bxs-calendar" /> 2022
                  </div>
                  <h3>Diplomado en Desarrollo de Software</h3>
                  <p>
                    Universidad Tecnol&oacute;gica de Pereira - Especializaci&oacute;n en
                    desarrollo de software, programaci&oacute;n web, bases de datos
                    y buenas pr&aacute;cticas de ingenier&iacute;a.
                  </p>
                </div>
              </div>

              <div className="experience-content">
                <div className="content">
                  <div className="year">
                    <i className="bx bxs-calendar" /> 2022 - 2023
                  </div>
                  <h3>Certificaciones Adicionales</h3>
                  <p>
                    Salesforce CRM Administration, SAP ERP, Docker Fundamentals,
                    Git & GitHub Professional, APIs REST Development.
                    Formaci&oacute;n continua en tecnolog&iacute;as emergentes.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== SKILLS SECTION ===== */}
      <section className="skills section-animate" id="skills">
        <h2 className="heading">Mis <span>Habilidades</span></h2>

        <div className="skills-row">
          <div className="skills-column">
            <h3><i className="bx bx-code-alt" /> Backend & Lenguajes</h3>
            {[
              { name: "Python", level: 90 },
              { name: "Django", level: 88 },
              { name: "SQL / Bases de Datos", level: 85 },
              { name: "APIs REST", level: 87 },
              { name: "Docker", level: 75 },
            ].map((skill) => (
              <div className="skills-box" key={skill.name}>
                <div className="skills-content">
                  <h3>{skill.name}</h3>
                  <span>{skill.level}%</span>
                </div>
                <div className="skill-bar">
                  <span className="skill-per" style={{ width: `${skill.level}%` }} />
                </div>
              </div>
            ))}
          </div>

          <div className="skills-column">
            <h3><i className="bx bx-palette" /> Frontend & Herramientas</h3>
            {[
              { name: "React", level: 85 },
              { name: "JavaScript", level: 88 },
              { name: "HTML5 & CSS3", level: 92 },
              { name: "Git & GitHub", level: 90 },
              { name: "Salesforce / SAP", level: 78 },
            ].map((skill) => (
              <div className="skills-box" key={skill.name}>
                <div className="skills-content">
                  <h3>{skill.name}</h3>
                  <span>{skill.level}%</span>
                </div>
                <div className="skill-bar">
                  <span className="skill-per" style={{ width: `${skill.level}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== PROJECTS SECTION ===== */}
      <section className="projects section-animate" id="projects">
        <h2 className="heading">Mis <span>Proyectos</span></h2>

        <div className="projects-container">
          {[
            {
              title: "Kamello Platform",
              description: "Plataforma tecnol&oacute;gica de la startup Kamello. Arquitectura full-stack con Django, React y PostgreSQL.",
              tags: ["Django", "React", "PostgreSQL"],
              github: "https://github.com/Alejandra-Lopez17",
              image: "https://placehold.co/600x400/112e42/00abf0/png?text=Kamello+Platform",
            },
            {
              title: "Capstone Project",
              description: "Proyecto integral de ingenier&iacute;a de software demostrando arquitectura, desarrollo y despliegue end-to-end.",
              tags: ["Full Stack", "Architecture", "DevOps"],
              github: "https://github.com/Alejandra-Lopez17/capstone-project",
              image: "https://placehold.co/600x400/112e42/00abf0/png?text=Capstone+Project",
            },
            {
              title: "Sistema Web UCOLTIS",
              description: "Sistema web empresarial que mejor&oacute; la eficiencia operativa en un 20%. Python, Django y SQL.",
              tags: ["Python", "Django", "SQL"],
              github: "https://github.com/Alejandra-Lopez17/Proyecto",
              image: "https://placehold.co/600x400/112e42/00abf0/png?text=UCOLTIS+System",
            },
            {
              title: "Portfolio Profesional",
              description: "Este portafolio web responsivo construido con React, TypeScript y dise&ntilde;o moderno.",
              tags: ["React", "TypeScript", "CSS"],
              github: "https://github.com/Alejandra-Lopez17",
              image: "https://placehold.co/600x400/112e42/00abf0/png?text=Portfolio+Web",
            },
            {
              title: "API REST Services",
              description: "Microservicios y APIs RESTful construidos con Django REST Framework y documentaci&oacute;n OpenAPI.",
              tags: ["Django REST", "API", "Docker"],
              github: "https://github.com/Alejandra-Lopez17",
              image: "https://placehold.co/600x400/112e42/00abf0/png?text=REST+APIs",
            },
            {
              title: "CRM Integration",
              description: "Integraci&oacute;n de Salesforce CRM y SAP ERP para automatizaci&oacute;n de procesos empresariales.",
              tags: ["Salesforce", "SAP", "Integration"],
              github: "https://github.com/Alejandra-Lopez17",
              image: "https://placehold.co/600x400/112e42/00abf0/png?text=CRM+Integration",
            },
          ].map((project, index) => (
            <div className="project-box" key={index}>
              <img src={project.image} alt={project.title} />
              <div className="project-layer">
                <h4>{project.title}</h4>
                <p>{project.description}</p>
                <div className="project-tags">
                  {project.tags.map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
                <a href={project.github} target="_blank" rel="noopener noreferrer">
                  <i className="bx bx-link-external" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ===== CONTACT SECTION ===== */}
      <section className="contact section-animate" id="contact">
        <h2 className="heading">Cont&aacute;ctame<span>!</span></h2>

        <div className="contact-info">
          <a href="mailto:alejandralopez170723@gmail.com" className="contact-card">
            <i className="bx bxs-envelope" />
            <h3>Email</h3>
            <p>alejandralopez170723@gmail.com</p>
          </a>

          <a href="https://github.com/Alejandra-Lopez17" target="_blank" rel="noopener noreferrer" className="contact-card">
            <i className="bx bxl-github" />
            <h3>GitHub</h3>
            <p>Alejandra-Lopez17</p>
          </a>

          <a href="https://www.linkedin.com/in/alejandra-lopez1707/" target="_blank" rel="noopener noreferrer" className="contact-card">
            <i className="bx bxl-linkedin" />
            <h3>LinkedIn</h3>
            <p>alejandra-lopez1707</p>
          </a>

          <a href="tel:+573118252321" className="contact-card">
            <i className="bx bxs-phone" />
            <h3>Tel&eacute;fono</h3>
            <p>+57 311 825 2321</p>
          </a>
        </div>

        <form className="contact-form" action="https://formspree.io/f/placeholder" method="POST">
          <div className="input-box">
            <input type="text" name="name" placeholder="Nombre Completo" required />
            <input type="email" name="email" placeholder="Tu Email" required />
          </div>
          <input type="text" name="phone" placeholder="Tu Tel&eacute;fono" style={{ width: "100%", padding: "1.5rem", fontSize: "1.6rem", color: "var(--text-color)", background: "var(--bg-color)", borderRadius: "0.8rem", margin: "0.7rem 0", border: "0.1rem solid var(--main-color)", fontFamily: "'Poppins', sans-serif" }} />
          <textarea name="message" cols={30} rows={10} placeholder="Tu Mensaje" required />
          <input type="submit" value="Enviar Mensaje" className="btn" />
        </form>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="footer">
        <div className="footer-text">
          <p>&copy; {new Date().getFullYear()} Alejandra Lopez | Co-Founder & Software Engineer. Todos los derechos reservados.</p>
        </div>

        <div className="footer-iconTop">
          <a onClick={() => scrollToSection("home")} style={{ cursor: "pointer" }}>
            <i className="bx bx-up-arrow-alt" />
          </a>
        </div>
      </footer>
    </>
  );
}

export default App;
