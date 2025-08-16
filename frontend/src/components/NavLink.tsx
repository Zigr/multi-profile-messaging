import styled from '@emotion/styled'
import { Link as RouterLink, type LinkProps as RouterLinkProps } from '@tanstack/react-router'
import type React from 'react'

// A Chakra-friendly, theme-aware nav link built on TanStack Router's Link
export type NavLinkProps = RouterLinkProps & React.ComponentPropsWithoutRef<'a'>

const NavLink = styled(RouterLink)`
  color: var(--chakra-colors-blue-500);
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`

export default NavLink
