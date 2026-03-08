
import { education } from "@/lib/data";
import { motion } from "framer-motion";

export default function Education() {
  return (
    <div className="container mx-auto px-4 py-20 md:py-32">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-6xl mx-auto"
      >
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-8">
          <div>
            <h2 className="text-sm font-display tracking-[0.3em] font-bold text-foreground/40 mb-4 uppercase">
              Education
            </h2>
            <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter uppercase">
              Academic <br /> Path
            </h1>
          </div>
          <p className="max-w-xs text-xs text-muted-foreground uppercase tracking-widest leading-loose">
            A foundation built on computer science principles and continuous academic growth.
          </p>
        </div>

        <div className="grid gap-12">
          {education.map((edu, index) => (
            <motion.div
              key={edu.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="group border-b border-border pb-12 last:border-0"
            >
              <div className="grid md:grid-cols-4 gap-8">
                <div className="md:col-span-1">
                  <span className="text-xs font-display font-bold tracking-[0.2em] text-foreground/40 uppercase">
                    {edu.period}
                  </span>
                </div>
                <div className="md:col-span-3">
                  <h3 className="text-2xl font-display font-black tracking-tight uppercase mb-2 group-hover:text-primary transition-colors">
                    {edu.degree}
                  </h3>
                  <h4 className="text-sm font-bold tracking-widest uppercase mb-4 text-foreground/60">
                    {edu.school}
                  </h4>
                  <p className="text-sm text-muted-foreground uppercase tracking-widest leading-relaxed max-w-2xl">
                    {edu.description}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
