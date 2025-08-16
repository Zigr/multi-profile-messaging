import { Outlet } from '@tanstack/react-router'
import { createFileRoute } from '@tanstack/react-router'
import { Box, HStack } from '@chakra-ui/react'
import NavLink from '@/components/NavLink'

export const Route = createFileRoute('/settings')({
  component: () => (
    <Box p={4}>
      <HStack gap={4} marginBottom={4}>
        <NavLink to="/settings">General</NavLink>
        <NavLink to="/settings/profiles">Profiles</NavLink>
      </HStack>
      <Outlet />
    </Box>
  ),
})
