module.exports = {
  root: true,
  env: { browser: true, es2020: true, node: true },
  extends: [
    'eslint:recommended',
    'plugin:prettier/recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.js'],
  parserOptions: {
    requireConfigFile: false,
    ecmaVersion: 2020,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: { version: 'detect' },
    'import/resolver': {
      alias: {
        map: [
          ['@', './src'],
          ['@assets', './src/assets'],
          ['@app', './src/app'],
          ['@api', './src/api'],
          ['@routes', './src/app/Routes'],
          ['@utils', './src/utils'],
          ['@hooks', './src/hooks'],
          ['@config', './src/config'],
          ['@constants', './src/constants'],
          ['@locale', './src/locale'],
        ],
        extensions: ['.js', '.jsx', '.json'],
      },
    },
  },
  plugins: ['react', 'react-refresh', 'import', 'sonarjs'],
  rules: {
    'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    'no-unused-vars': ['warn'],
    'react/prop-types': 'off',
    'react/display-name': 'off',
    'react/no-children-prop': 'off',
    'react-hooks/exhaustive-deps': 'off',
    'sonarjs/no-duplicate-string': 'warn',
    'sonarjs/no-identical-functions': 'warn',
    'import/order': [
      'error',
      {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
        'newlines-between': 'always',
        alphabetize: { order: 'asc', caseInsensitive: true },
      },
    ],
    'import/newline-after-import': ['error', { count: 1 }],
  },
};
