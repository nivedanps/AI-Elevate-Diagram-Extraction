
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Send } from "lucide-react";
import { useForm } from "react-hook-form";
import { useToast } from "@/hooks/use-toast";

export default function Contact() {
  const { register, handleSubmit, reset } = useForm();
  const { toast } = useToast();

  const onSubmit = (data: any) => {
    // Mock submission
    console.log(data);
    toast({
      title: "Transmission Sent",
      description: "We have received your message. Stand by for response.",
    });
    reset();
  };

  return (
    <div className="container mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="max-w-3xl mx-auto"
      >
        <h1 className="text-4xl md:text-6xl font-display font-bold mb-16 text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-500">
          INITIATE_CONTACT
        </h1>

        <div className="glass-panel p-8 md:p-12 relative overflow-hidden">
          {/* Decorative grid */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none" />

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 relative z-10">
            <div className="grid md:grid-cols-2 gap-8">
              <div className="space-y-2">
                <label className="font-display text-sm uppercase tracking-wider text-cyan-400">Identity</label>
                <Input 
                  {...register("name", { required: true })}
                  placeholder="ENTER NAME" 
                  className="bg-black/40 border-white/10 rounded-none h-12 focus:border-primary focus:ring-primary/20 font-mono"
                />
              </div>
              <div className="space-y-2">
                <label className="font-display text-sm uppercase tracking-wider text-cyan-400">Frequency</label>
                <Input 
                  {...register("email", { required: true })}
                  type="email" 
                  placeholder="ENTER EMAIL" 
                  className="bg-black/40 border-white/10 rounded-none h-12 focus:border-primary focus:ring-primary/20 font-mono"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="font-display text-sm uppercase tracking-wider text-cyan-400">Transmission</label>
              <Textarea 
                {...register("message", { required: true })}
                placeholder="TYPE MESSAGE..." 
                className="bg-black/40 border-white/10 rounded-none min-h-[200px] focus:border-primary focus:ring-primary/20 font-mono resize-none"
              />
            </div>

            <Button type="submit" size="lg" className="w-full bg-primary hover:bg-primary/90 text-white font-display uppercase tracking-widest h-14 rounded-none shadow-[0_0_20px_rgba(217,70,239,0.4)] hover:shadow-[0_0_40px_rgba(217,70,239,0.6)] transition-all">
              Send Message <Send className="ml-2 w-5 h-5" />
            </Button>
          </form>
        </div>
      </motion.div>
    </div>
  );
}
