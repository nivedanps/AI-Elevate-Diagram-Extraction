
import { education } from "@/lib/data";
import { motion } from "framer-motion";
import { GraduationCap } from "lucide-react";

export default function Education() {
  return (
    <div className="container mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="max-w-4xl mx-auto"
      >
        <h1 className="text-4xl md:text-6xl font-display font-bold mb-16 text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-500">
          ACADEMIC_DATA
        </h1>

        <div className="grid gap-8">
          {education.map((edu, index) => (
            <motion.div
              key={edu.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="glass-panel p-8 relative overflow-hidden group"
            >
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <GraduationCap size={120} />
              </div>

              <div className="relative z-10">
                <span className="text-primary font-mono text-sm mb-2 block">{edu.period}</span>
                <h3 className="font-display text-2xl md:text-3xl text-white mb-2">{edu.degree}</h3>
                <h4 className="text-xl text-cyan-400 mb-4">{edu.school}</h4>
                <p className="text-muted-foreground max-w-2xl">{edu.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
