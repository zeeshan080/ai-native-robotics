# AI-Native Robotics Documentation Site

This is the Docusaurus-based documentation site for the AI-Native Physical AI & Humanoid Robotics Textbook.

## Technology Stack

- **Docusaurus 3.x**: Modern static site generator
- **React 18**: UI framework
- **TypeScript**: Type-safe development
- **Local Search**: @easyops-cn/docusaurus-search-local plugin

## Development

```bash
# From repository root
pnpm dev

# Or from this directory
pnpm start
```

The site will be available at `http://localhost:3000`.

## Build

```bash
# From repository root
pnpm build

# Or from this directory
pnpm build
```

The production build will be in the `build/` directory.

## Project Structure

```
apps/docs/
├── docs/               # Documentation content
│   └── intro.md        # Homepage
├── src/
│   └── css/
│       └── custom.css  # Custom styles
├── static/             # Static assets (images, etc.)
├── docusaurus.config.ts # Docusaurus configuration
├── sidebars.ts         # Sidebar configuration
└── package.json
```

## Configuration

- **Docs-only mode**: The site uses `routeBasePath: '/'` to serve docs at the root
- **No blog**: Blog functionality is disabled
- **Local search**: Uses @easyops-cn/docusaurus-search-local for offline search
- **TypeScript**: Full TypeScript support throughout

## Adding Content

1. Create markdown files in `docs/`
2. Update `sidebars.ts` to include new pages
3. Add frontmatter for metadata:

```markdown
---
sidebar_position: 1
title: My Page Title
---

# My Page

Content here...
```

## Customization

- **Styles**: Edit `src/css/custom.css`
- **Config**: Edit `docusaurus.config.ts`
- **Sidebar**: Edit `sidebars.ts`

## Learn More

- [Docusaurus Documentation](https://docusaurus.io/)
- [Docusaurus TypeScript Support](https://docusaurus.io/docs/typescript-support)
