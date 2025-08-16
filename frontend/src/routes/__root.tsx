import { Outlet } from '@tanstack/react-router'
import { createRootRoute } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import { HStack } from '@chakra-ui/react'
import NavLink from '@/components/NavLink'

export const Route = createRootRoute({
    component: () => (
        <>
            <HStack as="nav" gap={4} marginBottom={4}>
                <NavLink to="/">Home</NavLink>
                <NavLink to="/settings">Settings</NavLink>
                <NavLink to="/settings/profiles">Profiles</NavLink>
                <NavLink to="/templates">Templates</NavLink>
                <NavLink to="/lists">Lists</NavLink>
                <NavLink to="/logs">Logs</NavLink>
            </HStack>
            <Outlet />
            <TanStackRouterDevtools position="bottom-right" />
        </>
    ),
})
