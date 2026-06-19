import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "CapIAbara",
        short_name: "CapIAbara",
        theme_color: "#4A2E15",
        background_color: "#FAF6F0",
        display: "standalone",
        icons: [
          { src: "/assets/capi.png", sizes: "192x192", type: "image/png" },
          { src: "/assets/capi.png", sizes: "512x512", type: "image/png" },
        ],
      },
    }),
  ],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
