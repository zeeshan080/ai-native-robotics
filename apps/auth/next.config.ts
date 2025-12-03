import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@repo/auth-config", "@repo/auth-database"],
};

export default nextConfig;
