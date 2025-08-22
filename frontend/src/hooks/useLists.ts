import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {API_BASE, apiFetch, type ListEntry, type ListType } from '@/lib/api'

export function useLists(params?: { profileId?: number; type?: ListType }) {
    const { profileId, type } = params || {}
    const key = ['lists', { profileId: profileId ?? null, type: type ?? null }] as const
    const qs = new URLSearchParams()
    if (profileId != null) qs.set('profile_id', String(profileId))
    if (type) qs.set('type', type)
    const url = `${API_BASE}/lists${qs.toString() ? `?${qs.toString()}` : ''}`
    return useQuery({
        queryKey: key,
        queryFn: () => apiFetch<ListEntry[]>(url),
    })
}

export function useCreateListEntry() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (entry: ListEntry) =>
            apiFetch<ListEntry>(`${API_BASE}/lists`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(entry),
            }),
        onSuccess: (_data, variables) => {
            // Invalidate generic list and filtered variants
            qc.invalidateQueries({ queryKey: [`${API_BASE}/lists`] })
            qc.invalidateQueries({
                queryKey: ['lists', { profileId: variables.profile_id ?? null, type: variables.type ?? null }],
            })
        },
    })
}

export function useDeleteListEntry() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (id: number) => apiFetch<void>(`${API_BASE}/lists/${id}`, { method: 'DELETE' }),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: [`${API_BASE}lists`] })
        },
    })
}
