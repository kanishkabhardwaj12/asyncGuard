import Link from "next/link";
import { fetchOverviewStats } from "../features/stats/stats.api";

export default async function HomePage() {
    const stats = await fetchOverviewStats();
  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      <main className="container">
        {/* Top HUD */}
        <div className="hud-bar">
          <span>Home</span>
          <div className="icons auth-links">
            <Link href="/login">[Login]</Link>
            <Link href="/signup">[Signup]</Link>
          </div>
        </div>

        {/* Title */}
        <h1>asyncGuard</h1>

        {/* Stats Section */}
        <div className="stats">
          <div className="stat-box">
            <span className="stat-number">{stats.apis_registered}</span>
            <span className="stat-label">APIs Registered</span>
          </div>

          <div className="stat-box">
            <span className="stat-number">{stats.audits_performed}</span>
            <span className="stat-label">Audits Performed</span>
          </div>
        </div>
      </main>
    </>
  );
}
