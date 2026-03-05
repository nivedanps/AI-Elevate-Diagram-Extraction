
import { projects } from "@/lib/data";
import { motion } from "framer-motion";
import { ArrowUpRight, Github } from "lucide-react";

export default function Projects() {
  return (
    <div className="container mx-auto px-4 py-20 md:py-32">
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="max-w-6xl mx-auto"
      >
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-8">
          <div>
            <h2 className="text-sm font-display tracking-[0.3em] font-bold text-foreground/40 mb-4 uppercase">
              Selected Works
            </h2>
            <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter uppercase">
              Featured <br /> Projects
            </h1>
          </div>
          <p className="max-w-xs text-xs text-muted-foreground uppercase tracking-widest leading-loose">
            A collection of digital experiences built with precision and modern technology.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          {projects.map((project, index) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group cursor-pointer"
            >
              <div className="relative aspect-[16/10] overflow-hidden bg-muted mb-6">
                <img
                  src={project.image}
                  alt={project.title}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-background/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="p-4 bg-background rounded-full">
                    <ArrowUpRight size={24} />
                  </div>
                </div>
              </div>

              <div className="flex justify-between items-start gap-4">
                <div>
                  <h3 className="font-display text-xl mb-2 group-hover:text-primary transition-colors uppercase font-bold tracking-tight">
                    {project.title}
                  </h3>
                  <div className="flex flex-wrap gap-x-4 gap-y-2">
                    {project.tags.map(tag => (
                      <span key={tag} className="text-[10px] font-display font-bold uppercase tracking-widest text-muted-foreground">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                {project.link.includes("github") && (
                  <a href={project.link} target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-muted rounded-full transition-colors">
                    <Github size={18} />
                  </a>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
