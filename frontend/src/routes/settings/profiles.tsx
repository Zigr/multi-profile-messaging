import { createFileRoute } from '@tanstack/react-router'
import ProfilesPage from '@/pages/ProfilesPage'

export const Route = createFileRoute('/settings/profiles')({
  component: () => <ProfilesPage />,
})
