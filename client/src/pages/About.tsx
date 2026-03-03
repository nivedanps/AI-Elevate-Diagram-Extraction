
import { motion } from "framer-motion";
import { User, Target, Zap } from "lucide-react";

export default function About() {
  return (
    <div className="container mx-auto px-4 py-32">
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="max-w-6xl mx-auto"
      >
        <div className="grid md:grid-cols-2 gap-20">
          <div className="space-y-12">
            <div>
              <h2 className="text-sm font-display tracking-[0.3em] font-bold text-foreground/40 mb-4 uppercase">
                Biography
              </h2>
              <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter uppercase mb-8">
                Who Is <br /> Nivedan?
              </h1>
            </div>

            <div className="space-y-6 text-sm text-muted-foreground uppercase tracking-widest leading-loose font-medium">
              <p>
                I am a passionate coding enthusiast pursuing my Bachelor of Engineering in Computer Science at Maharaja Institute of Technology, Mysuru.
              </p>
              <p>
                Currently in my pre-final year, I am dedicated to mastering software development and exploring the frontiers of technology with a focus on AI and modern web architectures.
              </p>
              <p>
                Beyond academia, I am an active participant in hackathons and workshops, constantly refining my technical and soft skills through collaboration and continuous learning.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-8 content-end">
            {[
              { icon: User, label: "Profile", value: "Aspiring Software Engineer" },
              { icon: Target, label: "Status", value: "Pre-final BE CSE student" },
              { icon: Zap, label: "Interests", value: "Cricket, Music, AI Tech" },
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-6 p-6 border border-border group hover:bg-muted/50 transition-colors">
                <div className="p-3 bg-muted text-muted-foreground group-hover:text-foreground transition-colors">
                  <item.icon size={20} />
                </div>
                <div>
                  <div className="text-[10px] font-display tracking-widest text-muted-foreground mb-1 uppercase font-bold">
                    {item.label}
                  </div>
                  <div className="text-xs uppercase font-bold tracking-widest">
                    {item.value}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
