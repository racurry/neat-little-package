// Default ESLint flat config for mr-sparkle plugin
// Modern ESLint 9+ configuration format
//
// This config provides a balanced starting point for JavaScript/TypeScript projects:
// - Uses recommended rules from @eslint/js
// - Supports TypeScript via typescript-eslint
// - Disables formatting rules to avoid conflicts with Prettier
// - Configures sensible defaults for code quality
//
// Install required packages:
//   npm install --save-dev eslint @eslint/js typescript-eslint eslint-config-prettier

import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import tseslint from "typescript-eslint";

export default [
	// Apply to all JavaScript and TypeScript files
	{
		files: ["**/*.{js,mjs,cjs,jsx,ts,tsx}"],
	},

	// Ignore common directories
	{
		ignores: [
			"dist/**",
			"build/**",
			"coverage/**",
			"node_modules/**",
			"**/*.min.js",
		],
	},

	// ESLint recommended rules for JavaScript
	js.configs.recommended,

	// TypeScript-eslint recommended rules
	...tseslint.configs.recommended,

	// Disable ESLint formatting rules that conflict with Prettier
	prettier,

	// Custom rules - code quality only, no formatting
	{
		rules: {
			// Variables
			"no-unused-vars": "off", // Disabled in favor of TypeScript version
			"@typescript-eslint/no-unused-vars": [
				"warn",
				{
					argsIgnorePattern: "^_",
					varsIgnorePattern: "^_",
					caughtErrorsIgnorePattern: "^_",
				},
			],

			// Best practices
			"no-console": "warn", // Warn on console statements (use proper logging)
			eqeqeq: ["error", "always"], // Require === and !==
			"no-eval": "error", // Disallow eval()
			"no-implied-eval": "error", // Disallow implied eval()
			"prefer-const": "warn", // Prefer const over let when possible
			"no-var": "error", // Disallow var (use const/let)

			// TypeScript-specific
			"@typescript-eslint/no-explicit-any": "warn", // Warn on explicit any
			"@typescript-eslint/explicit-function-return-type": "off", // Allow inferred return types
			"@typescript-eslint/explicit-module-boundary-types": "off", // Allow inferred boundary types
		},
	},

	// Test-specific overrides
	{
		files: ["**/*.test.{js,ts,jsx,tsx}", "**/*.spec.{js,ts,jsx,tsx}"],
		rules: {
			"no-console": "off", // Allow console in tests
			"@typescript-eslint/no-explicit-any": "off", // Allow any in tests
		},
	},
];
