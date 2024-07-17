import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';

export default defineConfig({
  plugins: [
    // mkcert create-ca 
    //mkcert create-cert 0.0.0.0 localhost 127.0.0.1 ::1 192.168.31.58
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
