// src/hooks/useCookieCapture.ts
import { useMutation } from '@tanstack/react-query'
import { apiFetch, API_BASE } from '@/lib/api'

export function useCookieCapture() {
    return useMutation({
        mutationFn: async (args: { profile_id: number; login_url: string; max_wait_ms?: number; headless?: boolean }) =>
            apiFetch(`${API_BASE}/automation/cookies/capture`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(args),
            }),
    })
}

export function useCookieRefresh() {
    return useMutation({
        mutationFn: async (args: { profile_id: number; headless?: boolean }) =>
            apiFetch('/automation/cookies/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(args),
            }),
    })
}
