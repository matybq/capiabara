import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "CapIAbara",
        short_name: "CapIAbara",
        theme_color: "#E8593C",
        background_color: "#FBF6EE",
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
