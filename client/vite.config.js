import { babel } from '@rollup/plugin-babel';
import react from '@vitejs/plugin-react';
import copy from 'rollup-plugin-copy';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({
      babelHelpers: 'runtime',
      exclude: 'node_modules/**',
      extensions: ['.js', '.jsx', '.es6', '.es', '.mjs'],
      presets: [
        [
          '@babel/preset-env',
          {
            targets: {
              browsers: ['> 0.25%', 'not dead', 'IE 11'],
            },
            useBuiltIns: 'entry', // Добавляем полифиллы
            corejs: 3, // Указываем версию core-js
          },
        ],
        '@babel/preset-react',
      ],
      plugins: [
        [
          '@babel/plugin-transform-runtime',
          {
            regenerator: true,
            useESModules: true,
          },
        ],
      ],
    }),
    copy({
      targets: [{ src: 'scripts/start.js', dest: 'dist' }],
      hook: 'writeBundle',
    }),
  ],
  resolve: {
    alias: {
      '@': '/src',
      '@assets': '/src/assets',
      '@app': '/src/app',
      '@routes': '/src/app/Routes',
      '@entities': '/src/entities',
      '@features': '/src/features',
      '@pages': '/src/pages',
      '@shared': '/src/shared',
      '@locale': '/src/locale',
      '@utils': '/src/utils',
      '@widgets': '/src/widgets',
      '@constants': '/src/constants',
      '@context': '/src/context',
      '@hooks': '/src/hooks',
      '@config': '/src/config',
    },
  },
});
