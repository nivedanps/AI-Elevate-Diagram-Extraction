
import { experience } from "@/lib/data";
import { motion } from "framer-motion";
import { Briefcase } from "lucide-react";

export default function Experience() {
  return (
    <div className="container mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="max-w-4xl mx-auto"
      >
        <h1 className="text-4xl md:text-6xl font-display font-bold mb-16 text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-500">
          EXPERIENCE_LOG
        </h1>

        <div className="relative border-l border-white/10 ml-4 md:ml-12 space-y-12">
          {experience.map((job, index) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="relative pl-8 md:pl-12 group"
            >
              {/* Timeline Dot */}
              <div className="absolute -left-[5px] top-0 w-[9px] h-[9px] bg-background border border-primary group-hover:bg-primary group-hover:shadow-[0_0_10px_var(--color-primary)] transition-all duration-300" />

              <div className="relative glass-panel p-6 md:p-8 hover:bg-white/5 transition-colors duration-300 group-hover:border-primary/30">
                <div className="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-2">
                  <h3 className="font-display text-2xl text-white group-hover:text-primary transition-colors">
                    {job.role}
                  </h3>
                  <span className="font-mono text-sm text-cyan-400 bg-cyan-950/30 px-3 py-1 border border-cyan-500/20">
                    {job.period}
                  </span>
                </div>
                
                <h4 className="text-lg text-muted-foreground font-medium mb-4 flex items-center gap-2">
                  <Briefcase size={16} /> {job.company}
                </h4>
                
                <p className="text-muted-foreground leading-relaxed">
                  {job.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
