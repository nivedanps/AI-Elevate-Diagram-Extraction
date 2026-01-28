
import { motion } from "framer-motion";
import { User, Rocket, Heart } from "lucide-react";

export default function About() {
  return (
    <div className="container mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-4xl mx-auto"
      >
        <h1 className="text-4xl md:text-6xl font-display font-bold mb-12 text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-500">
          ABOUT_ME
        </h1>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6 text-lg text-muted-foreground font-light leading-relaxed">
            <p>
              <strong className="text-white font-medium">I am a digital architect</strong> obsessed with the future of the web. 
              My journey began when I hacked my first game console, and I haven't stopped breaking and building things since.
            </p>
            <p>
              I specialize in creating <span className="text-cyan-400">high-performance applications</span> that don't just work—they feel alive. 
              Using cutting-edge tech like React, Three.js, and WebGL, I turn static pixels into immersive experiences.
            </p>
            <p>
              When I'm not coding, you can find me exploring cyberpunk aesthetics, producing electronic music, or gaming.
            </p>
          </div>

          <div className="relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-primary to-cyan-500 rounded-none blur-xl opacity-30 animate-pulse" />
            <div className="relative bg-black/50 backdrop-blur-md border border-white/10 p-8">
              <div className="space-y-8">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary/10 border border-primary/20 rounded-none">
                    <User className="text-primary w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-display text-xl mb-1">Profile</h3>
                    <p className="text-sm text-muted-foreground">Full Stack Creative Developer based in the Cloud.</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-none">
                    <Rocket className="text-cyan-500 w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-display text-xl mb-1">Mission</h3>
                    <p className="text-sm text-muted-foreground">To push the boundaries of what's possible in a browser.</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="p-3 bg-fuchsia-500/10 border border-fuchsia-500/20 rounded-none">
                    <Heart className="text-fuchsia-500 w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-display text-xl mb-1">Passion</h3>
                    <p className="text-sm text-muted-foreground">Interactive storytelling and 3D web experiences.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
