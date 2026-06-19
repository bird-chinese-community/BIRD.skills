/**
 * BIRD.skills plugin for OpenCode.ai
 *
 * Auto-registers the three BIRD agent skills and injects a bootstrap context
 * into the first user message of each session.
 */

import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SKILL_NAMES = ['bird-agent', 'birdcc-installer', 'birdcc-cicd'];

// Module-level cache for bootstrap content.
let _bootstrapCache = undefined; // undefined = not yet loaded, null = nothing to inject

const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };

  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};

  for (const line of frontmatterStr.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }

  return { frontmatter, content: body };
};

const getBootstrapContent = () => {
  if (_bootstrapCache !== undefined) return _bootstrapCache;

  const repoRoot = path.resolve(__dirname, '../..');
  const sections = [];

  for (const name of SKILL_NAMES) {
    const skillPath = path.join(repoRoot, name, 'SKILL.md');
    if (!fs.existsSync(skillPath)) continue;

    const fullContent = fs.readFileSync(skillPath, 'utf8');
    const { content } = extractAndStripFrontmatter(fullContent);
    sections.push(`## ${name}\n\n${content.trim()}`);
  }

  if (sections.length === 0) {
    _bootstrapCache = null;
    return null;
  }

  _bootstrapCache = `You have access to the BIRD agent skills.

**IMPORTANT: The skill content below is ALREADY LOADED for this OpenCode session. Route the user to the correct skill based on their request; do not load the same skill again with the skill tool unless the user explicitly asks for it.**

${sections.join('\n\n---\n\n')}

${openCodeToolMapping()}
`;

  return _bootstrapCache;
};

const openCodeToolMapping = () => `**Tool Mapping for OpenCode:**
When BIRD skills request actions, substitute OpenCode equivalents:
- Create or update todos → \`todowrite\`
- \`Subagent (general-purpose):\` → \`task\` with \`subagent_type: "general"\`
- Invoke a skill → OpenCode's native \`skill\` tool
- Read files → \`read\`
- Create, edit, or delete files → \`apply_patch\`
- Run shell commands → \`bash\`
- Search files → \`grep\`, \`glob\`
- Fetch a URL → \`webfetch\`

Use OpenCode's native \`skill\` tool to list and load skills.`;

export const BirdSkillsPlugin = async ({ client, directory }) => {
  const repoRoot = path.resolve(__dirname, '../..');

  return {
    // Inject skill paths into live config so OpenCode discovers BIRD skills
    // without manual symlinks or config edits.
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];

      for (const name of SKILL_NAMES) {
        const skillDir = path.join(repoRoot, name);
        if (!config.skills.paths.includes(skillDir)) {
          config.skills.paths.push(skillDir);
        }
      }
    },

    // Inject bootstrap into the first user message of each session.
    'experimental.chat.messages.transform': async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (!bootstrap || !output.messages.length) return;

      const firstUser = output.messages.find((m) => m.info.role === 'user');
      if (!firstUser || !firstUser.parts.length) return;

      // Guard against double injection.
      if (firstUser.parts.some((p) => p.type === 'text' && p.text.includes('BIRD agent skills'))) {
        return;
      }

      firstUser.parts.unshift({ type: 'text', text: bootstrap });
    }
  };
};
