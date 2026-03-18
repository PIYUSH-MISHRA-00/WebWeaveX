import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/WebWeaveX/docs',
    component: ComponentCreator('/WebWeaveX/docs', 'a2a'),
    routes: [
      {
        path: '/WebWeaveX/docs',
        component: ComponentCreator('/WebWeaveX/docs', 'b84'),
        routes: [
          {
            path: '/WebWeaveX/docs',
            component: ComponentCreator('/WebWeaveX/docs', 'cb8'),
            routes: [
              {
                path: '/WebWeaveX/docs/architecture',
                component: ComponentCreator('/WebWeaveX/docs/architecture', '09f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/WebWeaveX/docs/cli',
                component: ComponentCreator('/WebWeaveX/docs/cli', 'dc0'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/WebWeaveX/docs/crawler-engine',
                component: ComponentCreator('/WebWeaveX/docs/crawler-engine', '20f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/WebWeaveX/docs/getting-started',
                component: ComponentCreator('/WebWeaveX/docs/getting-started', '4fa'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/WebWeaveX/docs/plugins',
                component: ComponentCreator('/WebWeaveX/docs/plugins', '312'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/WebWeaveX/docs/sdk',
                component: ComponentCreator('/WebWeaveX/docs/sdk', 'bdd'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/WebWeaveX/',
    component: ComponentCreator('/WebWeaveX/', '60d'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
