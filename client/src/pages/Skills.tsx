
import { skills } from "@/lib/data";
import { motion } from "framer-motion";

export default function Skills() {
  return (
    <div className="container mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="max-w-6xl mx-auto"
      >
        <h1 className="text-4xl md:text-6xl font-display font-bold mb-16 text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-500">
          SKILL_MATRIX
        </h1>

        <div className="grid md:grid-cols-2 gap-8">
          {skills.map((category, index) => (
            <motion.div
              key={category.category}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="glass-panel p-8"
            >
              <div className="flex items-center gap-4 mb-8">
                <div className="p-3 bg-white/5 border border-white/10">
                  <category.icon className="w-6 h-6 text-cyan-400" />
                </div>
                <h3 className="font-display text-2xl">{category.category}</h3>
              </div>

              <div className="space-y-6">
                {category.items.map((skill, i) => (
                  <div key={skill} className="group">
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-muted-foreground group-hover:text-white transition-colors">{skill}</span>
                      <span className="text-primary/50 group-hover:text-primary transition-colors">
                        {Math.floor(Math.random() * 20 + 80)}%
                      </span>
                    </div>
                    <div className="h-1 bg-white/5 w-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${Math.random() * 40 + 60}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: 0.2 + (i * 0.1) }}
                        className="h-full bg-gradient-to-r from-primary to-cyan-500 shadow-[0_0_10px_var(--color-primary)]"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
