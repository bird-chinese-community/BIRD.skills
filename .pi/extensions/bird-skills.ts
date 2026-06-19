import { readFileSync } from "node:fs";
import { basename, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const EXTREMELY_IMPORTANT_MARKER = "";
const BOOTSTRAP_MARKER = "bird-skills:bootstrap for pi";

const extensionDir = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(extensionDir, "../..");
const skillPaths = [
  resolve(packageRoot, "bird-agent"),
  resolve(packageRoot, "birdcc-installer"),
  resolve(packageRoot, "birdcc-cicd"),
];

interface CachedSkill {
  content: string | null;
  initialized: boolean;
}

const cachedSkills: Record<string, CachedSkill> = {
  "bird-agent": { content: null, initialized: false },
  "birdcc-installer": { content: null, initialized: false },
  "birdcc-cicd": { content: null, initialized: false },
};

export default function birdSkillsPiExtension(pi: ExtensionAPI) {
  let injectBootstrap = true;

  pi.on("resources_discover", async () => ({
    skillPaths,
  }));

  pi.on("session_start", async () => {
    injectBootstrap = true;
  });

  pi.on("session_compact", async () => {
    injectBootstrap = true;
  });

  pi.on("agent_end", async () => {
    injectBootstrap = false;
  });

  pi.on("context", async (event) => {
    if (!injectBootstrap) return;
    if (event.messages.some(messageContainsBootstrap)) return;

    const bootstrap = getBootstrapContent();
    if (!bootstrap) return;

    const bootstrapMessage = {
      role: "user" as const,
      content: [{ type: "text" as const, text: bootstrap }],
      timestamp: Date.now(),
    };

    const insertAt = firstNonCompactionSummaryIndex(event.messages);
    return {
      messages: [
        ...event.messages.slice(0, insertAt),
        bootstrapMessage,
        ...event.messages.slice(insertAt),
      ],
    };
  });
}

function getBootstrapContent(): string | null {
  const skills = skillPaths.map((path) => {
    const name = basename(path);
    const cached = cachedSkills[name];
    if (cached && cached.initialized) {
      return { name, body: cached.content };
    }
    const body = loadSkillBody(path);
    cachedSkills[name] = { content: body, initialized: true };
    return { name, body };
  });

  if (skills.every((skill) => skill.body === null)) {
    return null;
  }

  const sections = skills
    .filter((skill): skill is { name: string; body: string } => skill.body !== null)
    .map((skill) => `## ${skill.name}\n\n${skill.body}`)
    .join("\n\n---\n\n");

  return `${EXTREMELY_IMPORTANT_MARKER}
${BOOTSTRAP_MARKER}

You have access to the BIRD agent skills. The content for each skill is included below and is already loaded for this Pi session. Route the user to the correct skill based on their request.

${sections}

${piToolMapping()}
`;
}

function loadSkillBody(skillPath: string): string | null {
  try {
    const skillContent = readFileSync(resolve(skillPath, "SKILL.md"), "utf8");
    return stripFrontmatter(skillContent);
  } catch {
    return null;
  }
}

function stripFrontmatter(content: string): string {
  const match = content.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
  return (match ? match[1] : content).trim();
}

function piToolMapping(): string {
  return `## Pi tool mapping

Pi's built-in coding tools are lowercase: \`read\`, \`write\`, \`edit\`, \`bash\`, plus optional \`grep\`, \`find\`, and \`ls\`. Use \`bash\` to run the \`uv run scripts/...\` commands referenced in the skills.

If a skill says to invoke another skill, use Pi's native skill system: load the relevant \`SKILL.md\` with \`read\` when it applies, or let the user invoke \`/skill:name\` explicitly.`;
}

function messageContainsBootstrap(message: unknown): boolean {
  const content = (message as { content?: unknown }).content;
  if (typeof content === "string") return content.includes(BOOTSTRAP_MARKER);
  if (!Array.isArray(content)) return false;
  return content.some((part) => {
    return (
      part &&
      typeof part === "object" &&
      (part as { type?: unknown }).type === "text" &&
      typeof (part as { text?: unknown }).text === "string" &&
      (part as { text: string }).text.includes(BOOTSTRAP_MARKER)
    );
  });
}

function firstNonCompactionSummaryIndex(messages: unknown[]): number {
  let index = 0;
  while ((messages[index] as { role?: unknown } | undefined)?.role === "compactionSummary") {
    index += 1;
  }
  return index;
}
