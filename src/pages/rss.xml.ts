import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const articles = (await getCollection('articles')).filter((a) => !a.data.draft);
  const sorted = articles.sort(
    (a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime()
  );

  return rss({
    title: 'China Travel Guide',
    description:
      'Practical, up-to-date travel guides for Western visitors to China. Visa, payments, high-speed rail, eSIM, and city guides.',
    site: context.site ?? 'https://china-travel-guide-ne9.pages.dev',
    items: sorted.map((entry) => ({
      title: entry.data.title,
      description: entry.data.description,
      pubDate: entry.data.pubDate,
      link: `/guides/${entry.slug}/`,
      categories: [entry.data.category, ...(entry.data.tags ?? [])],
    })),
    customData: `<language>en-us</language>`,
  });
}
