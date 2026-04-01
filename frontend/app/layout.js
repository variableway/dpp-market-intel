import "./globals.css";

export const metadata = {
  title: "DPP Market Intelligence",
  description: "DPP / CBAM dashboard and news application"
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
