# Quickstart: Monorepo with Docusaurus Setup

**Feature**: 002-monorepo-docusaurus-setup
**Prerequisites**: Node.js 20+, pnpm 8+

## Phase 1: Initialize Monorepo

### Step 1.1: Install Turborepo

```bash
# From repository root
pnpm add -D turbo@latest
```

### Step 1.2: Create Workspace Directories

```bash
mkdir -p apps packages
```

### Step 1.3: Create pnpm-workspace.yaml

Create `/pnpm-workspace.yaml`:
```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### Step 1.4: Create turbo.json

Create `/turbo.json`:
```json
{
  "$schema": "https://turbo.build/schema.json",
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".docusaurus/**", "build/**"],
      "env": ["NODE_ENV"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"],
      "outputs": []
    },
    "type-check": {
      "dependsOn": ["^type-check"],
      "outputs": []
    },
    "clean": {
      "cache": false
    }
  }
}
```

### Step 1.5: Update Root package.json

Ensure `/package.json` includes:
```json
{
  "name": "ai-native-robotics",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "type-check": "turbo type-check",
    "clean": "turbo clean"
  },
  "devDependencies": {
    "turbo": "^2.6.1"
  },
  "packageManager": "pnpm@10.18.3",
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=8.0.0"
  }
}
```

### Step 1.6: Update .gitignore

Add to `.gitignore`:
```
# Turborepo
.turbo

# Dependencies
node_modules

# Build outputs
dist
build
.docusaurus

# Environment
.env.local
```

### Step 1.7: Verify Phase 1

```bash
pnpm install
turbo run build  # Should complete with no tasks (empty apps/)
```

---

## Phase 2: Add Docusaurus

### Step 2.1: Create Docusaurus App

```bash
npx create-docusaurus@latest apps/docs classic --typescript
```

When prompted:
- TypeScript: Yes (already selected via `--typescript`)
- Package manager: pnpm

### Step 2.2: Update Docusaurus package.json

Edit `/apps/docs/package.json`:
```json
{
  "name": "@ai-native-robotics/docs",
  "version": "1.0.0",
  "private": true,
  ...
}
```

### Step 2.3: Install Search Plugin

```bash
cd apps/docs
pnpm add @easyops-cn/docusaurus-search-local
cd ../..
```

### Step 2.4: Configure Docusaurus

Edit `/apps/docs/docusaurus.config.ts`:
```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI-Native Physical AI & Humanoid Robotics',
  tagline: 'Learn Physical AI, ROS 2, and Humanoid Robotics',
  favicon: 'img/favicon.ico',
  url: 'https://your-domain.com',
  baseUrl: '/',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        language: ["en"],
        indexDocs: true,
        docsRouteBasePath: '/',
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI & Robotics',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'mainSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'xml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```

### Step 2.5: Configure Sidebar

Edit `/apps/docs/sidebars.ts`:
```typescript
import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  mainSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
  ],
};

export default sidebars;
```

### Step 2.6: Create Initial Content

Edit `/apps/docs/docs/intro.md`:
```markdown
---
slug: /
sidebar_position: 1
---

# Welcome to AI-Native Physical AI & Humanoid Robotics

This is the introduction to the textbook.
```

### Step 2.7: Verify Phase 2

```bash
# From root
pnpm install
pnpm dev  # Should start Docusaurus at localhost:3000

# Or from apps/docs
cd apps/docs
pnpm dev
```

---

## Verification Checklist

- [ ] `pnpm install` runs without errors from root
- [ ] `turbo run build` completes successfully
- [ ] `pnpm dev` starts Docusaurus server
- [ ] Site accessible at `http://localhost:3000`
- [ ] Search box appears in navbar
- [ ] Sidebar navigation works
- [ ] Hot-reload works when editing markdown

## Common Issues

### Issue: "Cannot find module 'turbo'"
**Solution**: Run `pnpm install` from root

### Issue: Port 3000 already in use
**Solution**: Docusaurus will prompt to use next available port, or stop the other process

### Issue: Workspace package not found
**Solution**: Ensure `pnpm-workspace.yaml` includes `apps/*`
