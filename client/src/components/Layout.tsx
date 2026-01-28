
import { Navigation } from "./Navigation";
import { motion, AnimatePresence } from "framer-motion";
import { useLocation } from "wouter";
import { Github, Linkedin, Twitter, Mail } from "lucide-react";

export function Layout({ children }: { children: React.ReactNode }) {
  const [location] = useLocation();

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden bg-background text-foreground">
      <Navigation />
      
      <main className="flex-grow pt-16 relative z-10">
        <AnimatePresence mode="wait">
          <motion.div
            key={location}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
            className="min-h-[calc(100vh-64px)]"
          >
            {children}
          </motion.div>
        </AnimatePresence>
      </main>

      <footer className="border-t border-white/5 bg-black/40 backdrop-blur-sm py-8 relative z-10">
        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-muted-foreground font-body">
            © 2026 DEV.OS. Crafted with neon & code.
          </div>
          <div className="flex gap-6">
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors"><Github size={20} /></a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors"><Linkedin size={20} /></a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors"><Twitter size={20} /></a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors"><Mail size={20} /></a>
          </div>
        </div>
      </footer>
    </div>
  );
}
