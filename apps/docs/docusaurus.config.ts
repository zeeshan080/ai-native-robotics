import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI-Native Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive textbook for learning robotics with AI-native approaches',
  favicon: 'img/favicon.ico',

  // GitHub Pages deployment configuration
  url: 'https://zeeshan080.github.io',
  baseUrl: '/ai-native-robotics/',

  organizationName: 'zeeshan080',
  projectName: 'ai-native-robotics',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/zeeshan080/ai-native-robotics/tree/development/apps/docs/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'AI-Native Robotics',
      logo: {
        alt: 'AI-Native Robotics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'mainSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          to: '/profile',
          label: 'Profile',
          position: 'right',
        },
        {
          href: 'https://github.com/zeeshan080/ai-native-robotics',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'custom-navbarAuthButton',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Textbook',
              to: '/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/zeeshan080/ai-native-robotics',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI-Native Robotics. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'json'],
    },
    // Local search configuration
    algolia: undefined, // Disable Algolia
  } satisfies Preset.ThemeConfig,

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        indexDocs: true,
        indexBlog: false,
        docsRouteBasePath: '/',
      },
    ],
  ],

  customFields: {
    // ChatKit backend API URL (can be overridden via env var)
    chatkitApiUrl: process.env.CHATKIT_API_URL || 'http://localhost:8000',
  },
};

export default config;
