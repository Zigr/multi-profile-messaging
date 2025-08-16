// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { CustomProvider } from "./components/ui/provider"
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { routeTree } from '@/routeTree.gen'   // <-- MUST match generatedRouteTree


const router = createRouter({ routeTree })


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CustomProvider>
      <RouterProvider router={router} />
    </CustomProvider>
  </React.StrictMode>
)

