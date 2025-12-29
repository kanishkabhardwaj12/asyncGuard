import "./global.css";

export const metadata = {
  title: "CHECKPOINT 2025",
  description: "Look back at your 2025",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
