"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchOverviewStats } from "../features/stats/stats.api";

type Stats = {
  apis_registered: number;
  audits_performed: number;
};

export default function HomePage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOverviewStats()
      .then((data) => setStats(data))
      .finally(() => setLoading(false));
  }, []);

  const isBackendDown = !stats && !loading;
  const safeStats = stats || { apis_registered: 0, audits_performed: 0 };

  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      <main className="container">
        <div className="hud-bar">
          <span>Home</span>
          <div className="icons auth-links">
            <Link href="/login">[Login]</Link>
            <Link href="/signup">[Signup]</Link>
          </div>
        </div>

        <h1>asyncGuard</h1>

        <div className="stats">
          <div className="stat-box">
            <span
              className="stat-number"
              style={{ color: isBackendDown ? "#ff4d4d" : undefined }}
            >
              {loading
                ? "LOADING..."
                : isBackendDown
                ? "SERVER UNREACHABLE"
                : safeStats.apis_registered}
            </span>
            <span className="stat-label">APIs Registered</span>
          </div>

          <div className="stat-box">
            <span
              className="stat-number"
              style={{ color: isBackendDown ? "#ff4d4d" : undefined }}
            >
              {loading
                ? "LOADING..."
                : isBackendDown
                ? "SERVER UNREACHABLE"
                : safeStats.audits_performed}
            </span>
            <span className="stat-label">Audits Performed</span>
          </div>
        </div>
      </main>
    </>
  );
}
