import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import pkg from './package.json';

export default defineConfig({
	plugins: [sveltekit()],
	define: {
		'import.meta.env.APP_VERSION': JSON.stringify(pkg.version)
	},
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
