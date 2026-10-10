// @ts-check
/**
 * Build-time script: generates /search-index.json from content collections.
 * Parses markdown frontmatter directly (no Astro runtime needed).
 * Run after `astro build`: `node scripts/generate-search-index.mjs`
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));

/** Parse YAML-ish frontmatter (title, description, slug, tags, draft, city) */
function parseFrontmatter(filePath) {
  const raw = readFileSync(filePath, 'utf8');
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return {};
  const fm = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (!kv) continue;
    const key = kv[1];
    let val = kv[2].trim();
    if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
    if (val.startsWith("'") && val.endsWith("'")) val = val.slice(1, -1);
    if (val === 'true') val = true;
    if (val === 'false') val = false;
    if (key === 'tags') {
      val = val
        .replace(/^\[|\]$/g, '')
        .split(',')
        .map((s) => s.trim().replace(/^["']|["']$/g, ''))
        .filter(Boolean);
    }
    fm[key] = val;
  }
  return fm;
}

function collect(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith('.md'))
    .map((f) => {
      // Astro 5 derives slug from filename — do NOT rely on frontmatter slug.
      const slug = f.replace(/\.md$/, '');
      return { file: join(dir, f), slug, fm: parseFrontmatter(join(dir, f)) };
    });
}

const cities = collect(join(root, 'src/content/cities'));
const articles = collect(join(root, 'src/content/articles'));

const index = [
  ...cities.map((c) => ({
    title: `${c.fm.nameEn || c.fm.title} Travel Guide`,
    description: c.fm.description || '',
    url: `/cities/${c.slug}/`,
    tags: Array.isArray(c.fm.tags) ? c.fm.tags : [],
  })),
  ...articles
    .filter((a) => !a.fm.draft)
    .map((a) => ({
      title: a.fm.title || '',
      description: a.fm.description || '',
      url: `/guides/${a.slug}/`,
      tags: Array.isArray(a.fm.tags) ? a.fm.tags : [],
    })),
];

const outDir = join(root, 'dist');
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'search-index.json'), JSON.stringify(index));
console.log(`[search-index] generated ${index.length} entries → dist/search-index.json`);
