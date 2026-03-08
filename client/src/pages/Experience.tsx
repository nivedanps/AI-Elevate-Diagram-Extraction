
import { achievements } from "@/lib/data";
import { motion } from "framer-motion";
import { Award, ShieldCheck, Cpu, Code2, Cloud, ArrowUpRight } from "lucide-react";

const getIcon = (issuer: string) => {
  if (issuer.includes("AWS")) return <Cloud size={18} />;
  if (issuer.includes("IBM")) return <Cpu size={18} />;
  if (issuer.includes("Java")) return <Code2 size={18} />;
  if (issuer.includes("Security")) return <ShieldCheck size={18} />;
  return <Award size={18} />;
};

export default function Experience() {
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
              Certifications
            </h2>
            <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter uppercase">
              Achievements <br /> & Logs
            </h1>
          </div>
          <p className="max-w-xs text-xs text-muted-foreground uppercase tracking-widest leading-loose">
            A record of specialized certifications and technical accomplishments.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {achievements.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="p-8 border border-border bg-muted/20 hover:bg-muted/50 transition-colors group relative"
            >
              <div className="flex items-start justify-between mb-8">
                <div className="p-3 bg-background text-foreground/40 group-hover:text-primary transition-colors">
                  {getIcon(item.issuer || item.title)}
                </div>
                <div className="text-[10px] font-display font-bold uppercase tracking-widest text-primary px-3 py-1 border border-primary/20">
                  {item.issuer}
                </div>
              </div>

              <div>
                <h3 className="text-xl font-display font-black tracking-tight uppercase mb-4 group-hover:text-primary transition-colors">
                  {item.title}
                </h3>
                <p className="text-xs text-muted-foreground uppercase tracking-[0.15em] leading-relaxed">
                  {item.description}
                </p>
              </div>

              <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity">
                <ArrowUpRight size={16} className="text-primary" />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
