
import { projects } from "@/lib/data";
import { motion } from "framer-motion";
import { ExternalLink, Github } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Projects() {
  return (
    <div className="container mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="max-w-6xl mx-auto"
      >
        <h1 className="text-4xl md:text-6xl font-display font-bold mb-16 text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-500">
          PROJECT_ARCHIVE
        </h1>

        <div className="grid md:grid-cols-2 gap-8">
          {projects.map((project, index) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="glass-panel group overflow-hidden"
            >
              <div className="relative aspect-video overflow-hidden">
                <div className="absolute inset-0 bg-primary/20 opacity-0 group-hover:opacity-100 transition-opacity z-10 mix-blend-overlay" />
                <img 
                  src={project.image} 
                  alt={project.title}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0"
                />
              </div>

              <div className="p-8 border-t border-white/5 relative bg-background/80 backdrop-blur-sm">
                <h3 className="font-display text-2xl mb-3 text-white group-hover:text-primary transition-colors">
                  {project.title}
                </h3>
                <p className="text-muted-foreground mb-6 line-clamp-2">
                  {project.description}
                </p>

                <div className="flex flex-wrap gap-2 mb-8">
                  {project.tags.map(tag => (
                    <span key={tag} className="text-xs font-mono px-2 py-1 border border-white/10 text-cyan-400 bg-cyan-950/20">
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex gap-4">
                  <Button size="sm" className="bg-white/5 hover:bg-white/10 text-white border border-white/10 rounded-none w-full">
                    <Github className="mr-2 w-4 h-4" /> Code
                  </Button>
                  <Button size="sm" className="bg-primary/80 hover:bg-primary text-white rounded-none w-full shadow-[0_0_15px_rgba(217,70,239,0.3)]">
                    <ExternalLink className="mr-2 w-4 h-4" /> Live Demo
                  </Button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
