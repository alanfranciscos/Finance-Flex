import type { Metadata } from 'next';
import '@styles/global.css';

export const metadata: Metadata = {
  title: 'Finance Flex',
  description: 'Fiancne Flex is a personal finance app.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
