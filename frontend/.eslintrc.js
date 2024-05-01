module.exports = {
  parser: '@typescript-eslint/parser',
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true,
  },
  plugins: ['react', 'prettier', '@typescript-eslint', 'unused-imports'],
  extends: [
    'next/core-web-vitals',
    'eslint:recommended',
    'standard',
    'prettier',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:prettier/recommended',
    'plugin:react/jsx-runtime',
  ],
  overrides: [],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  ignorePatterns: ['node_modules/', '_explicacoes/'],
  // Cherry of the cake
  rules: {
    'no-console': 2,
    'react/no-unknown-property': ['error', { ignore: ['jsx', 'global'] }],
    'react/jsx-uses-react': 'off',
    'import/order': [
      'error',
      {
        groups: [
          'index',
          'sibling',
          'parent',
          'internal',
          'external',
          'builtin',
          'object',
          'type',
        ],
        'newlines-between': 'always',
      },
    ],
    'import/newline-after-import': 'error',
    'import/no-duplicates': 'error',
    'unused-imports/no-unused-imports': 'error',
    'unused-imports/no-unused-vars': [
      'error',
      { varsIgnorePattern: '^_', argsIgnorePattern: '^_' },
    ],
  },
};
