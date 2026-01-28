
import { 
  Code2, 
  Database, 
  Layout, 
  Server, 
  Smartphone, 
  Terminal, 
  Cpu, 
  Globe 
} from "lucide-react";

export const projects = [
  {
    id: 1,
    title: "Neon Nexus",
    description: "A futuristic social platform with real-time 3D environments and voice chat.",
    tags: ["React", "Three.js", "WebRTC", "Socket.io"],
    image: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=800",
    link: "#"
  },
  {
    id: 2,
    title: "Cyber Commerce",
    description: "Next-gen e-commerce dashboard with predictive analytics and dark mode UI.",
    tags: ["Next.js", "TypeScript", "Tailwind", "PostgreSQL"],
    image: "https://images.unsplash.com/photo-1555421689-492a18d9c3ad?auto=format&fit=crop&q=80&w=800",
    link: "#"
  },
  {
    id: 3,
    title: "Synthwave Audio",
    description: "Browser-based DAW (Digital Audio Workstation) for creating electronic music.",
    tags: ["WebAudio API", "Vue", "Canvas", "Firebase"],
    image: "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&q=80&w=800",
    link: "#"
  },
  {
    id: 4,
    title: "HoloStream",
    description: "AR-enabled video streaming service for immersive content consumption.",
    tags: ["AR.js", "React Native", "Node.js", "AWS"],
    image: "https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?auto=format&fit=crop&q=80&w=800",
    link: "#"
  }
];

export const skills = [
  { category: "Frontend", icon: Layout, items: ["React", "TypeScript", "Next.js", "Tailwind CSS", "Three.js", "Framer Motion"] },
  { category: "Backend", icon: Server, items: ["Node.js", "Express", "PostgreSQL", "GraphQL", "Redis", "Python"] },
  { category: "Tools", icon: Terminal, items: ["Git", "Docker", "AWS", "Linux", "Vite", "Figma"] },
  { category: "Mobile", icon: Smartphone, items: ["React Native", "Flutter", "iOS", "Android"] }
];

export const experience = [
  {
    id: 1,
    role: "Senior Frontend Engineer",
    company: "CyberTech Industries",
    period: "2023 - Present",
    description: "Leading the development of immersive 3D web interfaces for enterprise clients. optimized rendering performance by 40%."
  },
  {
    id: 2,
    role: "Full Stack Developer",
    company: "Neon Systems",
    period: "2021 - 2023",
    description: "Built scalable microservices architecture and implemented real-time data visualization dashboards using D3.js and React."
  },
  {
    id: 3,
    role: "UI/UX Developer",
    company: "Pixel Perfect",
    period: "2019 - 2021",
    description: "Collaborated with designers to translate high-fidelity mockups into pixel-perfect interactive web applications."
  }
];

export const education = [
  {
    id: 1,
    degree: "Master of Computer Science",
    school: "Tech University of Tomorrow",
    period: "2017 - 2019",
    description: "Specialized in Human-Computer Interaction and Computer Graphics."
  },
  {
    id: 2,
    degree: "Bachelor of Engineering",
    school: "State Institute of Technology",
    period: "2013 - 2017",
    description: "Major in Software Engineering with a minor in Digital Art."
  }
];
