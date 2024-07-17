import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';

export default defineConfig({
	plugins: [
	  sveltekit()
	],
	server: {
	  https: {
		key: fs.readFileSync('cert.key'),
		cert: fs.readFileSync('cert.crt'),
	  },
	  proxy: {},
	  port: 3000, // or any port you prefer
	}
  });
  