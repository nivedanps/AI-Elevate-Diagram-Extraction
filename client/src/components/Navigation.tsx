
import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";
import { Menu, X, Sun, Moon, Github, Linkedin, Instagram, Mail } from "lucide-react";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";

const navItems = [
  { name: "Home", path: "#home" },
  { name: "About", path: "#about" },
  { name: "Education", path: "#education" },
  { name: "Achievements", path: "#achievements" },
  { name: "Skills", path: "#skills" },
  { name: "Works", path: "#projects" },
  { name: "Contact", path: "#contact" },
];

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [activeSection, setActiveSection] = useState("home");

  useEffect(() => {
    setMounted(true);
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);

      const sectionIds = ["home", "about", "education", "achievements", "skills", "projects", "contact"];
      const scrollPos = window.scrollY + 200; // Offset to trigger early

      for (const id of sectionIds) {
        const el = document.getElementById(id);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPos >= top && scrollPos < top + height) {
            setActiveSection((prev) => (prev !== id ? id : prev));
          }
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, path: string) => {
    e.preventDefault();
    setIsOpen(false);
    const element = document.querySelector(path);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  if (!mounted) return null;

  return (
    <header className="fixed top-6 left-0 right-0 z-50 flex justify-center px-4 w-full overflow-hidden">
      <nav
        className={cn(
          "flex items-center gap-2 px-6 py-3 rounded-full border bg-background/60 backdrop-blur-xl transition-all duration-300 shadow-lg",
          scrolled ? "border-border" : "border-transparent bg-transparent shadow-none"
        )}
      >
        <a href="#home" onClick={(e) => handleNavClick(e, "#home")} className="text-xl font-display font-black tracking-tighter mr-4">
          NIVEDAN
        </a>

        {/* Desktop Nav Items */}
        <div className="hidden md:flex items-center gap-6 mr-6">
          {navItems.map((item) => (
            <a
              key={item.path}
              href={item.path}
              onClick={(e) => handleNavClick(e, item.path)}
              className={cn(
                "text-[10px] uppercase tracking-[0.2em] font-bold transition-all duration-300",
                activeSection === item.path.substring(1)
                  ? "text-primary border-b-2 border-primary pb-1"
                  : "text-foreground/40 hover:text-foreground"
              )}
            >
              {item.name}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
            className="p-2 rounded-full hover:bg-muted transition-colors text-foreground/80 hover:text-foreground"
            aria-label="Toggle theme"
          >
            {mounted && (resolvedTheme === "dark" ? <Sun size={18} /> : <Moon size={18} />)}
          </button>

          <button
            className="md:hidden p-2 rounded-full hover:bg-muted transition-colors"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </nav>

      {/* Mobile Nav Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 top-20 flex flex-col items-center justify-center bg-background/95 backdrop-blur-2xl z-40 md:hidden"
          >
            <div className="flex flex-col gap-8 text-center">
              {navItems.map((item) => (
                <a
                  key={item.path}
                  href={item.path}
                  onClick={(e) => handleNavClick(e, item.path)}
                  className={cn(
                    "text-2xl font-display font-bold uppercase tracking-widest transition-colors",
                    activeSection === item.path.substring(1) ? "text-primary" : "hover:text-primary"
                  )}
                >
                  {item.name}
                </a>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
