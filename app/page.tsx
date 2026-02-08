import { Header } from "@/components/header"
import { HeroSection } from "@/components/hero-section"
import { MetricsGrid } from "@/components/metrics-grid"
import { RiskProfiles } from "@/components/risk-profiles"
import { ArchitectureSection } from "@/components/architecture-section"
import { ChangelogSection } from "@/components/changelog-section"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <MetricsGrid />
        <RiskProfiles />
        <ArchitectureSection />
        <ChangelogSection />
      </main>
      <Footer />
    </div>
  )
}
