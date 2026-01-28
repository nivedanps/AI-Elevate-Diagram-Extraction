
import { HeroScene } from "@/components/3d/HeroScene";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, Code, Zap } from "lucide-react";
import { Link } from "wouter";

export default function Home() {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <HeroScene />
      
      <div className="container relative z-10 px-4">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-primary tracking-[0.2em] uppercase font-bold text-sm mb-4 animate-pulse">
              System Online // Ready to Deploy
            </h2>
            <h1 className="text-5xl md:text-8xl font-display font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white via-white to-white/50 mb-6 drop-shadow-[0_0_30px_rgba(255,255,255,0.3)]">
              BUILDING THE <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-fuchsia-500 to-cyan-500 neon-text">
                IMPOSSIBLE
              </span>
            </h1>
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
            className="text-xl md:text-2xl text-muted-foreground font-light max-w-2xl mx-auto leading-relaxed"
          >
            Creative Technologist crafting immersive digital experiences at the intersection of design and code.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center pt-8"
          >
            <Link href="/projects">
              <Button size="lg" className="bg-primary hover:bg-primary/80 text-white font-display uppercase tracking-wider rounded-none border border-primary/50 shadow-[0_0_20px_rgba(217,70,239,0.4)] hover:shadow-[0_0_40px_rgba(217,70,239,0.6)] transition-all h-14 px-8 text-lg">
                View Projects <Code className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="bg-transparent border-cyan-500/50 text-cyan-400 hover:text-cyan-300 hover:bg-cyan-950/30 font-display uppercase tracking-wider rounded-none hover:border-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.1)] hover:shadow-[0_0_20px_rgba(6,182,212,0.3)] transition-all h-14 px-8 text-lg">
                Contact Me <Zap className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          </motion.div>
        </div>
      </div>
      
      {/* Decorative Elements */}
      <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-background to-transparent z-10 pointer-events-none" />
    </div>
  );
}
