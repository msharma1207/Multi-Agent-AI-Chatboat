import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'CortexAI — Multi-model AI workspace',
  description: 'Chat, create and collaborate with leading AI models in one workspace.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
