
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
    title: "Zoo Management System",
    description: "A user-friendly UI/UX design for managing records of animals and zookeepers, including built-in portals for visitors and admins.",
    tags: ["PHP", "UI/UX", "Web Development"],
    image: "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?auto=format&fit=crop&q=80&w=800",
    link: "#"
  },
  {
    id: 2,
    title: "Smart Faculty Feedback Portal",
    description: "A college website that gathers feedback under one portal with secure admin access and separate portals for faculty and admins.",
    tags: ["React", "PHP", "HTML", "Web Design"],
    image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&q=80&w=800",
    link: "https://github.com/nivedanps/project.git"
  }
];

export const skills = [
  { category: "Technical Skills", icon: Code2, items: ["Python", "Java", "HTML", "PHP", "Web Technology"] },
  { category: "Tools & Environment", icon: Terminal, items: ["GitHub", "Jupyter Notebook", "Antigravity", "VSCode"] },
  { category: "Soft Skills", icon: Layout, items: ["Team Collaboration", "Problem Solving"] }
];

export const achievements = [
  {
    id: 1,
    title: "AWS Cloud Practitioner Essentials",
    issuer: "AWS",
    description: "Certified in cloud fundamentals and AWS ecosystem."
  },
  {
    id: 2,
    title: "IBM-AI Fundamentals",
    issuer: "IBM",
    description: "Foundational knowledge in Artificial Intelligence."
  },
  {
    id: 3,
    title: "Java Skills",
    issuer: "Acube",
    description: "Core Java programming and application development."
  },
  {
    id: 4,
    title: "Developing Front-End Apps with React",
    issuer: "Certification",
    description: "Building modern, responsive user interfaces."
  },
  {
    id: 5,
    title: "Cyber Security Technologies",
    issuer: "Certification",
    description: "Knowledge in security protocols and threat mitigation."
  }
];

// Experience constant kept for backward compatibility if needed, but mapped to empty or removed if we rename everywhere
export const experience = [];

export const education = [
  {
    id: 1,
    degree: "Bachelor of Engineering, Computer Science",
    school: "Maharaja Institute of Technology, Mysuru",
    period: "2023 - Present",
    description: "Currently pursuing pre-final year with a CGPA of 8.43. Passionate about AI and coding."
  },
  {
    id: 2,
    degree: "PUC (84.16%)",
    school: "Sadvidya Semi-Residential College, Mysuru",
    period: "2022 - 2023",
    description: "Completed pre-university education with high distinction."
  },
  {
    id: 3,
    degree: "SSLC (91.20%)",
    school: "Bharatiya Vidya Bhavan, Mysuru",
    period: "2021",
    description: "Completed secondary education with excellent academic standing."
  }
];
