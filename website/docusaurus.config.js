// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from "prism-react-renderer";

const siteUrl = "https://doteki.org";
const tagline = "Bring your GitHub profile to life with dynamic content 🎋";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "dōteki",
  tagline: tagline,
  favicon: "img/logo.png",

  // Set the production url of your site here
  url: siteUrl,
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "welpo",
  projectName: "doteki",
  deploymentBranch: "gh-pages",

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        // `hashed` is recommended as long-term-cache of index file is possible.
        hashed: true,
      }),
    ],
  ],

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: "./sidebars.js",
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/welpo/doteki/tree/main/website/",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  headTags: [
    {
      tagName: "meta",
      attributes: { "http-equiv": "X-UA-Compatible", content: "IE=edge" },
    },
    {
      tagName: "meta",
      attributes: {
        "http-equiv": "content-type",
        content: "text/html; charset=utf-8",
      },
    },

    // Open Graph meta tags.
    {
      tagName: "meta",
      attributes: { property: "og:type", content: "website" },
    },
    {
      tagName: "meta",
      attributes: { property: "og:url", content: siteUrl },
    },
    {
      tagName: "meta",
      attributes: { property: "og:title", content: "dōteki" },
    },
    {
      tagName: "meta",
      attributes: {
        property: "og:description",
        content: tagline,
      },
    },
    {
      tagName: "meta",
      attributes: {
        name: "description",
        content: tagline,
      },
    },
    {
      tagName: "meta",
      attributes: { property: "og:image", content: "/img/social-card.jpg" },
    },
    {
      tagName: "meta",
      attributes: { property: "og:image:height", content: "1024" },
    },
    {
      tagName: "meta",
      attributes: { property: "og:image:width", content: "1792" },
    },

    // Twitter card.
    {
      tagName: "meta",
      attributes: { name: "twitter:image", content: "/img/social-card.jpg" },
    },
    {
      tagName: "meta",
      attributes: { name: "twitter:card", content: "summary_large_image" },
    },

    {
      tagName: "meta",
      attributes: {
        name: "viewport",
        content: "width=device-width, initial-scale=1.0",
      },
    },
    {
      tagName: "meta",
      attributes: { content: "light dark", name: "color-scheme" },
    },
    {
      tagName: "meta",
      attributes: {
        media: "(prefers-color-scheme: light)",
        content: "#426a68",
        name: "theme-color",
      },
    },
    {
      tagName: "meta",
      attributes: {
        media: "(prefers-color-scheme: dark)",
        content: "#2B4845",
        name: "theme-color",
      },
    },

    // Icons.
    {
      tagName: "link",
      attributes: { rel: "apple-touch-icon", href: "/img/logo.png" },
    },
    { tagName: "link", attributes: { rel: "icon", href: "/img/logo.png" } },
  ],

  scripts: [
    {
      src: "https://stats.doteki.org/count.js",
      async: true,
      "data-goatcounter": "https://stats.doteki.org/count",
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: "img/social-card.jpg",
      navbar: {
        title: "dōteki",
        logo: {
          alt: "doteki logo: a river passing through a bamboo forest",
          src: "img/logo.png",
        },
        items: [
          {
            type: "docSidebar",
            sidebarId: "tutorialSidebar",
            position: "left",
            label: "Documentation",
          },
          { to: "/docs/category/plugins", label: "Plugins", position: "left" },
          {
            href: "https://github.com/welpo/doteki",
            "aria-label": "GitHub",
            className: "header-github-link",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        copyright: `Copyright © ${new Date().getFullYear()} dōteki`,
      },
      prism: {
        theme: prismThemes.oneLight,
        darkTheme: prismThemes.oceanicNext,
        additionalLanguages: ["toml"],
      },
      colorMode: {
        defaultMode: "light",
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),
};

export default config;
