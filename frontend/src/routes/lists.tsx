import { createFileRoute } from '@tanstack/react-router'
import ListsPage from '@/pages/ListsPage'

export const Route = createFileRoute('/lists')({
  component: () => <ListsPage />,
})
