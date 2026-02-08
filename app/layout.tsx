import type { Metadata, Viewport } from "next"
import { Inter, JetBrains_Mono } from "next/font/google"
import "./globals.css"

const _inter = Inter({ subsets: ["latin"] })
const _jetbrainsMono = JetBrains_Mono({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AURORA - Automated Crypto Trading",
  description:
    "Institutional-grade automated trading for the crypto markets. Risk-managed. Hands-free. Join the waitlist.",
}

export const viewport: Viewport = {
  themeColor: "#050507",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="font-sans">{children}</body>
    </html>
  )
}
