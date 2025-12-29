export async function fetchOverviewStats() {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/stats/overview`,
      {
        credentials: "include",
      }
    );
  
    if (!res.ok) {
      throw new Error("Failed to fetch stats");
    }
  
    return res.json();
  }
  