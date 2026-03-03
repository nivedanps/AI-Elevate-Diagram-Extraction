
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
  { icon: Github, href: "https://github.com" },
  { icon: Linkedin, href: "https://linkedin.com" },
  { icon: Twitter, href: "https://twitter.com" },
  { icon: Globe, href: "#" },
  { icon: Mail, href: "mailto:contact@example.com" },
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
        <div className="container relative z-10 px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "circOut" }}
            className="space-y-6"
          >
            <div className="inline-block px-4 py-1.5 border border-foreground/10 rounded-full text-[10px] font-display tracking-[0.2em] font-bold uppercase mb-4">
              Software Student & AI Enthusiast
            </div>

            <h1 className="text-6xl md:text-[10rem] font-display font-black tracking-tighter leading-[0.85] uppercase mb-8">
              HI! I&apos;M <br />
              <span className="text-stroke-outline">NIVEDAN</span>
            </h1>

            <p className="max-w-xl mx-auto text-sm md:text-base text-muted-foreground uppercase tracking-[0.2em] font-medium leading-relaxed mb-12">
              Building intelligent systems & scalable web applications. <br />
              Based in Mysore, Karnataka, India.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <a href="#projects" className="group flex items-center gap-3 text-xs font-display tracking-widest font-bold uppercase transition-colors hover:text-primary">
                Explore Work <ArrowDown size={14} className="animate-bounce" />
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      <div className="space-y-0">
        <section id="about" className="border-t border-border">
          <About />
        </section>

        <section id="education" className="border-t border-border bg-muted/30">
          <Education />
        </section>

        <section id="achievements" className="border-t border-border">
          <Experience />
        </section>

        <section id="skills" className="border-t border-border bg-muted/30">
          <Skills />
        </section>

        <section id="projects" className="border-t border-border">
          <Projects />
        </section>

        <section id="contact" className="border-t border-border bg-muted/30">
          <Contact />
        </section>
      </div>
    </div>
  );
}
