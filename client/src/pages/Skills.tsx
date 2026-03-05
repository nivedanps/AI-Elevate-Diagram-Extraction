
import { skills } from "@/lib/data";
import { motion } from "framer-motion";

export default function Skills() {
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
              Abilities
            </h2>
            <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter uppercase">
              Stack & <br /> Skills
            </h1>
          </div>
          <p className="max-w-xs text-xs text-muted-foreground uppercase tracking-widest leading-loose">
            Core competencies developed through academic excellence and practical exploration.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {skills.map((category, index) => (
            <motion.div
              key={category.category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="p-8 border border-border bg-muted/20 hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center gap-4 mb-8">
                <category.icon className="w-5 h-5 text-foreground/40" />
                <h3 className="text-xs font-display font-bold uppercase tracking-widest">{category.category}</h3>
              </div>

              <div className="flex flex-col gap-4">
                {category.items.map((skill) => (
                  <div key={skill} className="flex items-center justify-between group">
                    <span className="text-xs uppercase font-bold tracking-widest text-muted-foreground group-hover:text-foreground transition-colors">
                      {skill}
                    </span>
                    <div className="w-1.5 h-1.5 rounded-full bg-primary" />
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
