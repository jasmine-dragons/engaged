import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const inter = Geist({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Teacher Teacher",
  description: "Made with 🌲 for TreeHacks 2025 🥰",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
