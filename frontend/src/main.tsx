// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { CustomProvider } from "./components/ui/provider"
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { routeTree } from '@/routeTree.gen'   // <-- MUST match generatedRouteTree
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'


const router = createRouter({
  routeTree,
  defaultPreload: 'intent',
})

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CustomProvider>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </CustomProvider>
  </React.StrictMode>
)

