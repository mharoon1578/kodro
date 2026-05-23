/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Kodro Documentation',
  tagline: 'One-command Spec-Driven Development Engine',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://mharoon1578.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/kodro/',

  // GitHub pages deployment config.
  organizationName: 'mharoon1578',
  projectName: 'kodro',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/mharoon1578/kodro/tree/main/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/mharoon1578/kodro/tree/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/kodro-social-card.jpg',
      navbar: {
        title: 'Kodro',
        logo: {
          alt: 'Kodro Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/mharoon1578/kodro',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/getting-started',
              },
              {
                label: 'Pipeline',
                to: '/docs/pipeline',
              },
              {
                label: 'Configuration',
                to: '/docs/configuration',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/kodro',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/kodro',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/kodroframework',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/mharoon1578/kodro',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Kodro Project. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer/themes/github'),
        darkTheme: require('prism-react-renderer/themes/dracula'),
      },
    }),
};

module.exports = config;
