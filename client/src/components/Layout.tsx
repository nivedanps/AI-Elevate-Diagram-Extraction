
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

      <footer className="py-20 relative z-10 opactiy-50">
        <div className="container mx-auto px-4 text-center">
          <div className="text-xs tracking-widest uppercase text-muted-foreground">
            © 2026 NIVEDAN P S — BUILT WITH CODE
          </div>
        </div>
      </footer>
    </div>
  );
}
