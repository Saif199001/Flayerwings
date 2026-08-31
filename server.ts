import express, { Request, Response } from "express";
import cors from "cors";
import path from "path";
import { createServer as createViteServer } from "vite";

interface Tool {
  id: number;
  name: string;
  slug: string;
  description: string;
  is_active: boolean;
}

interface Lead {
  id: number;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  website?: string;
  lead_type?: string;
  source?: string;
  message?: string;
  social_profile_url?: string;
  status: string;
  created_at: string;
}

interface Project {
  id: number;
  title: string;
  slug: string;
  project_type: string;
  status: string;
  short_description: string;
  description: string;
  url: string;
  featured: boolean;
  published: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

// In-Memory Data Stores
const TOOLS: Tool[] = [
  {
    id: 1,
    name: "Social Media Audit",
    slug: "social-media-audit",
    description: "Get a quick assessment of your social media presence and discover opportunities to improve it.",
    is_active: true,
  },
  {
    id: 2,
    name: "AI Caption Generator",
    slug: "caption-generator",
    description: "Generate platform-ready social media captions from a business, topic and tone.",
    is_active: true,
  },
  {
    id: 3,
    name: "Social Media Content Ideas",
    slug: "content-ideas",
    description: "Generate practical content ideas tailored to a business, audience and social platform.",
    is_active: true,
  },
];

const PROJECTS: Project[] = [
  {
    id: 1,
    title: "Flayer Wings SaaS",
    slug: "flayer-wings-saas",
    project_type: "product",
    status: "in_progress",
    short_description: "Social media management, analytics and workflow platform built for modern businesses.",
    description: "We are building our own SaaS platform at Flayer Wings—designed from real-world social media management challenges.",
    url: "https://flayerwings.info/product",
    featured: true,
    published: true,
    sort_order: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

const leads: Lead[] = [];
let leadIdSequence = 1;

// Business Logic Services
function runSocialAudit(business: string, profileUrl: string) {
  const checks = [
    { key: "profile", title: "Profile clarity", score: 7, tip: "Make the bio immediately explain who you help, what you offer and the next action." },
    { key: "content", title: "Content consistency", score: 6, tip: "Use repeatable content pillars and a realistic weekly publishing rhythm." },
    { key: "conversion", title: "Conversion path", score: 5, tip: "Give visitors one obvious next step such as a free audit, WhatsApp or enquiry form." },
    { key: "proof", title: "Trust signals", score: 6, tip: "Show genuine work, testimonials, process or product progress instead of generic claims." },
  ];
  const average = Math.round((checks.reduce((sum, item) => sum + item.score, 0) / checks.length) * 10) / 10;
  return {
    business: (business || "").trim(),
    profile_url: (profileUrl || "").trim(),
    score: average,
    checks,
    next_step: "Start with the lowest-scoring area and improve one conversion path before increasing posting volume.",
  };
}

function generateCaption(topic: string, tone = "professional", platform = "instagram") {
  const toneText = (tone || "").trim() || "professional";
  const platformText = (platform || "").trim().toLowerCase() || "instagram";
  return {
    caption: `${(topic || "").trim()} — ${toneText} content made for ${platformText}. Share the value, invite the conversation, and give your audience one clear next step.`,
    hashtags: ["#FlayerWings", "#SocialMedia", "#DigitalGrowth"],
  };
}

function generateContentIdeas(business: string, audience = "general audience", platform = "instagram") {
  const b = (business || "").trim();
  const aud = (audience || "").trim() || "general audience";
  const plat = (platform || "").trim() || "instagram";
  const ideas = [
    `3 common problems ${aud} face with ${b}`,
    `A behind-the-scenes look at how ${b} delivers its work`,
    `Myth vs fact: what ${aud} should know about ${b}`,
    `A quick tip that helps ${aud} get better results from ${b}`,
    `Customer question of the week about ${b}`,
    `Before vs after: the transformation ${b} can create`,
    `A short founder story: why ${b} exists`,
    `A checklist ${aud} can save and use today`,
    `A product/service feature explained in simple language`,
    `A poll or question designed for ${aud} on ${plat}`,
  ];
  return { ideas };
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(cors());
  app.use(express.json());

  // API Routes
  const router = express.Router();

  // Health
  router.get(["/health", "/health/"], (req: Request, res: Response) => {
    res.json({ status: "ok", service: "flayer-wings-api" });
  });

  // Tools
  router.get(["/tools", "/tools/"], (req: Request, res: Response) => {
    res.json(TOOLS.filter((t) => t.is_active));
  });

  router.get("/tools/:slug", (req: Request, res: Response) => {
    const tool = TOOLS.find((t) => t.slug === req.params.slug && t.is_active);
    if (!tool) {
      return res.status(404).json({ detail: "Tool not found" });
    }
    res.json(tool);
  });

  // Tool Generators
  router.post(["/tools/social-media-audit/generate", "/tools/social-media-audit/generate/"], (req: Request, res: Response) => {
    const { business, profile_url } = req.body || {};
    if (!business || !profile_url) {
      return res.status(400).json({ detail: "Both business name and profile URL are required." });
    }
    const result = runSocialAudit(business, profile_url);
    res.json(result);
  });

  router.post(["/tools/caption-generator/generate", "/tools/caption-generator/generate/"], (req: Request, res: Response) => {
    const { topic, tone, platform } = req.body || {};
    if (!topic) {
      return res.status(400).json({ detail: "Topic is required." });
    }
    const result = generateCaption(topic, tone, platform);
    res.json(result);
  });

  router.post(["/tools/content-ideas/generate", "/tools/content-ideas/generate/"], (req: Request, res: Response) => {
    const { business, audience, platform } = req.body || {};
    if (!business) {
      return res.status(400).json({ detail: "Business name or description is required." });
    }
    const result = generateContentIdeas(business, audience, platform);
    res.json(result);
  });

  // Leads
  router.post(["/leads", "/leads/"], (req: Request, res: Response) => {
    const { name, email, phone, company, website, lead_type, source, message, social_profile_url } = req.body || {};
    if (!name || !email) {
      return res.status(400).json({
        name: !name ? ["This field is required."] : undefined,
        email: !email ? ["This field is required."] : undefined,
      });
    }

    const newLead: Lead = {
      id: leadIdSequence++,
      name: name.trim(),
      email: email.trim(),
      phone: phone?.trim() || "",
      company: company?.trim() || "",
      website: website?.trim() || "",
      lead_type: lead_type || "contact",
      source: source || "",
      message: message?.trim() || "",
      social_profile_url: social_profile_url?.trim() || "",
      status: "new",
      created_at: new Date().toISOString(),
    };

    leads.push(newLead);
    res.status(201).json(newLead);
  });

  router.get(["/leads", "/leads/"], (req: Request, res: Response) => {
    res.json(leads);
  });

  // Projects
  router.get(["/projects", "/projects/"], (req: Request, res: Response) => {
    res.json(PROJECTS.filter((p) => p.published));
  });

  router.get("/projects/:slug", (req: Request, res: Response) => {
    const project = PROJECTS.find((p) => p.slug === req.params.slug && p.published);
    if (!project) {
      return res.status(404).json({ detail: "Project not found" });
    }
    res.json(project);
  });

  // Content
  router.get(["/content", "/content/"], (req: Request, res: Response) => {
    res.json({ results: [] });
  });

  app.use("/api/v1", router);

  // Vite development middleware vs production static files
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true, host: "0.0.0.0", port: PORT },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req: Request, res: Response) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Flayer Wings server running at http://0.0.0.0:${PORT}`);
  });
}

startServer();
