import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import Link from "next/link";

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
      <body className={inter.className}>
        <div className="blob-wrapper">
          <div className="blob"></div>
        </div>
        <nav className="nav">
          <Link href="/setup">Get Started</Link>
          <Link href="/history">History</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
