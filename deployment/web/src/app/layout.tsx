import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Plastic Waste Monitoring Dashboard",
  description: "Segment floating plastic in aerial photos (PDIS-Net thesis prototype)",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
