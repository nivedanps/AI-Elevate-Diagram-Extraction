
import { HeroScene } from "@/components/3d/HeroScene";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowDown, Github, Linkedin, Instagram, Mail, Twitter, Globe } from "lucide-react";

import About from "./About";
import Education from "./Education";
import Experience from "./Experience";
import Skills from "./Skills";
import Projects from "./Projects";
import Contact from "./Contact";

const socialLinks = [
  { icon: Github, href: "https://github.com/nivedanps" },
  { icon: Linkedin, href: "https://linkedin.com/in/nivedanps" },
  { icon: Mail, href: "mailto:nivedanps@outlook.com" },
];

export default function Home() {
  return (
    <div className="relative bg-background min-h-screen">
      <HeroScene />

      {/* Sidebar - Socials */}
      <div className="fixed left-8 bottom-32 hidden lg:flex flex-col gap-6 z-40">
        <div className="text-[10px] font-display tracking-[0.3em] font-bold text-foreground/40 vertical-text mb-4">
          /// CONNECT
        </div>
        {socialLinks.map((social, i) => (
          <motion.a
            key={i}
            href={social.href}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 1 + i * 0.1 }}
            className="text-foreground/40 hover:text-foreground transition-colors"
          >
            <social.icon size={18} />
          </motion.a>
        ))}
      </div>

      {/* Status Indicators */}
      <div className="fixed left-8 top-32 hidden lg:block z-40 space-y-2">
        <div className="text-[10px] font-display tracking-widest text-foreground/40">
          /// SYSTEM_READY
        </div>
        <div className="text-[10px] font-display tracking-widest text-foreground/40">
          LOC: MYSORE, KARNATAKA, INDIA
        </div>
      </div>

      {/* Version Indicator */}
      <div className="fixed right-8 bottom-32 hidden lg:block z-40 text-right">
        <div className="text-[10px] font-display tracking-widest text-foreground/40">
          XX_INIT_SEQ
        </div>
        <div className="text-[10px] font-display tracking-widest text-foreground/40">
          VER. 2.0.4
        </div>
      </div>

      {/* HERO SECTION */}
      <section id="home" className="relative h-screen flex items-center justify-center pt-20">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] max-w-[400px] max-h-[400px] bg-primary/30 rounded-full blur-[80px] -z-10 animate-pulse pointer-events-none" />
        <div className="container relative z-10 px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "circOut" }}
            className="space-y-6"
          >
            <div className="inline-block px-4 py-1.5 border border-foreground/10 rounded-full text-[10px] font-display tracking-[0.2em] font-bold uppercase mb-4">
              SOFTWARE ENGINEERING STUDENT
            </div>

            <h1 className="text-6xl md:text-[10rem] font-display font-black tracking-tighter leading-[0.85] uppercase mb-8">
              HI! I&apos;M <br />
              <span className="text-stroke-outline">NIVEDAN</span>
            </h1>

            <p className="max-w-xl mx-auto text-sm md:text-base text-muted-foreground uppercase tracking-[0.2em] font-medium leading-relaxed mb-12">
              Building new blocks of boxes through New AI tools & coding enthusiast. <br />
              Based in Mysore, Karnataka, India.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <a
                href="#projects"
                onClick={(e) => {
                  e.preventDefault();
                  document.getElementById("projects")?.scrollIntoView({ behavior: "smooth" });
                }}
                className="group flex items-center gap-3 text-xs font-display tracking-widest font-bold uppercase transition-all hover:bg-primary hover:text-primary-foreground border border-foreground/10 px-8 py-4 rounded-full"
              >
                View My Work <ArrowDown size={14} className="group-hover:translate-y-1 transition-transform" />
              </a>
              <a
                href="/resume.pdf"
                target="_blank"
                className="group flex items-center gap-3 text-xs font-display tracking-widest font-bold uppercase transition-all bg-foreground text-background hover:bg-foreground/90 px-8 py-4 rounded-full"
              >
                Download CV
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      <div className="space-y-0 relative z-20 text-foreground">
        <section id="about" className="border-t border-border bg-background">
          <About />
        </section>

        <section id="education" className="border-t border-border bg-muted/30">
          <Education />
        </section>

        <section id="achievements" className="border-t border-border bg-background">
          <Experience />
        </section>

        <section id="skills" className="border-t border-border bg-muted/30">
          <Skills />
        </section>

        <section id="projects" className="border-t border-border bg-background">
          <Projects />
        </section>

        <section id="contact" className="border-t border-border bg-muted/30">
          <Contact />
        </section>
      </div>
    </div>
  );
}
