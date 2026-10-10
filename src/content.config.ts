// @ts-check
import { defineCollection, z } from 'astro:content';

// City collection: one entry per destination
const cities = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    // English name used in URLs and headings
    nameEn: z.string(),
    // Chinese name for reference
    nameZh: z.string(),
    province: z.string(),
    description: z.string(),
    // Hero image (WebP preferred)
    heroImage: z.string().optional(),
    // Coordinates for potential map embeds
    lat: z.number().optional(),
    lng: z.number().optional(),
    // Tags for filtering
    tags: z.array(z.string()).default([]),
    // SEO
    seoTitle: z.string().optional(),
    seoDescription: z.string().optional(),
    // Order on homepage
    order: z.number().default(99),
    // Featured flag
    featured: z.boolean().default(false),
  }),
});

// Article collection: guides, tips, city articles
const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // ISO date, e.g. 2026-10-10
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    // Which city this article belongs to (optional for guides)
    city: z.string().optional(),
    // Category: guide | city | tips | visa | payment | transport | sim | safety
    category: z.string().default('guide'),
    // Tags for related articles
    tags: z.array(z.string()).default([]),
    // Author
    author: z.string().default('China Travel Guide Team'),
    // SEO
    seoTitle: z.string().optional(),
    seoDescription: z.string().optional(),
    // FAQ for FAQPage JSON-LD
    faq: z
      .array(
        z.object({
          question: z.string(),
          answer: z.string(),
        })
      )
      .default([]),
    // Featured image
    heroImage: z.string().optional(),
    // Draft flag
    draft: z.boolean().default(false),
  }),
});

export const collections = { cities, articles };
