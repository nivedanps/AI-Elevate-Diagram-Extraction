
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Send, Mail, MapPin, Phone } from "lucide-react";
import { useForm } from "react-hook-form";
import { useToast } from "@/hooks/use-toast";

export default function Contact() {
  const { register, handleSubmit, reset } = useForm();
  const { toast } = useToast();

  const onSubmit = (data: any) => {
    console.log(data);
    toast({
      title: "Transmission Received",
      description: "Expect a response via the provided frequency soon.",
    });
    reset();
  };

  return (
    <div className="container mx-auto px-4 py-20 md:py-32">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-6xl mx-auto"
      >
        <div className="grid md:grid-cols-2 gap-20">
          <div>
            <h2 className="text-sm font-display tracking-[0.3em] font-bold text-foreground/40 mb-4 uppercase">
              Contact
            </h2>
            <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter uppercase mb-8">
              Get In <br /> Touch
            </h1>
            <p className="max-w-xs text-xs text-muted-foreground uppercase tracking-widest leading-loose mb-12">
              Available for collaborations, inquiries, and innovative discussions.
            </p>

            <div className="space-y-6">
              {[
                { icon: Mail, label: "Transmission", value: "nivedanps@outlook.com" },
                { icon: MapPin, label: "Coordinates", value: "Mysore, Karnataka" },
                { icon: Phone, label: "Direct Line", value: "+91 6363294833" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-6 group">
                  <div className="p-3 border border-border text-muted-foreground group-hover:text-primary transition-colors">
                    <item.icon size={18} />
                  </div>
                  <div>
                    <div className="text-[10px] font-display font-bold uppercase tracking-widest text-muted-foreground">
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

          <div className="border border-border p-8 md:p-12 bg-muted/20">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
              <div className="space-y-2">
                <div className="text-[10px] font-display font-bold uppercase tracking-widest text-muted-foreground">
                  Your Identity
                </div>
                <Input
                  {...register("name", { required: true })}
                  placeholder="NAME_REQUIRED"
                  className="bg-transparent border-0 border-b border-border rounded-none px-0 focus-visible:ring-0 focus-visible:border-primary transition-colors uppercase tracking-widest text-xs font-bold"
                />
              </div>

              <div className="space-y-2">
                <div className="text-[10px] font-display font-bold uppercase tracking-widest text-muted-foreground">
                  Your Frequency
                </div>
                <Input
                  {...register("email", { required: true })}
                  type="email"
                  placeholder="EMAIL_ENTRY"
                  className="bg-transparent border-0 border-b border-border rounded-none px-0 focus-visible:ring-0 focus-visible:border-primary transition-colors uppercase tracking-widest text-xs font-bold"
                />
              </div>

              <div className="space-y-2">
                <div className="text-[10px] font-display font-bold uppercase tracking-widest text-muted-foreground">
                  Transmission Details
                </div>
                <Textarea
                  {...register("message", { required: true })}
                  placeholder="WRITE_MESSAGE_HERE..."
                  className="bg-transparent border-0 border-b border-border rounded-none px-0 focus-visible:ring-0 focus-visible:border-primary transition-colors min-h-[120px] resize-none uppercase tracking-widest text-xs font-bold leading-loose"
                />
              </div>

              <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-display font-black uppercase tracking-[0.2em] h-14 rounded-none transition-all">
                Send Transmission <Send className="ml-3 w-4 h-4" />
              </Button>
            </form>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
