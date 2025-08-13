"use client";

import { ThemeProvider as NextThemesProvider } from "next-themes";

export function ThemeProvider({ children, ...props }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      element="html" // 🔹 Force class on <html>
      {...props}
    >
      {children}
    </NextThemesProvider>
  );
}
