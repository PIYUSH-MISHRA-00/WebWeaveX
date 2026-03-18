// @ts-check

const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'WebWeaveX',
  tagline: 'Universal Web Intelligence Engine',
  url: 'https://piyush-mishra-00.github.io',
  baseUrl: '/WebWeaveX/',
  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn'
    }
  },
  organizationName: 'PIYUSH-MISHRA-00',
  projectName: 'WebWeaveX',
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '../docs',
          routeBasePath: '/docs',
          sidebarPath: require.resolve('./sidebars.js')
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css')
        }
      })
    ]
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'WebWeaveX',
        items: [
          { to: '/docs/getting-started', label: 'Docs', position: 'left' },
          {
            href: 'https://github.com/PIYUSH-MISHRA-00/WebWeaveX',
            label: 'GitHub',
            position: 'right'
          }
        ]
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              { label: 'Getting Started', to: '/docs/getting-started' },
              { label: 'Architecture', to: '/docs/architecture' }
            ]
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discussions',
                href: 'https://github.com/PIYUSH-MISHRA-00/WebWeaveX/discussions'
              },
              {
                label: 'Issues',
                href: 'https://github.com/PIYUSH-MISHRA-00/WebWeaveX/issues'
              }
            ]
          }
        ],
        copyright: `Copyright ${new Date().getFullYear()} WebWeaveX`
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme
      }
    })
};

module.exports = config;
