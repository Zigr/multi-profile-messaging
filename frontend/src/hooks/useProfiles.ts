
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiFetch, type Profile, API_BASE } from '@/lib/api'

const KEY = [`${API_BASE}/profiles`]


export function useProfiles() {
    console.log(`API_BASE: ${API_BASE}`)
    return useQuery({
        queryKey: KEY,
        queryFn: () => apiFetch<Profile[]>(`${API_BASE}/profiles`),
    })
}

export function useCreateOrUpdateProfile() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (p: Profile) => {
            const method = p.id ? 'PUT' : 'POST'
            const url = p.id ? `${API_BASE}/profiles/${p.id}` : `${API_BASE}/profiles`
            return apiFetch<Profile>(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(p),
            })
        },
        onSuccess: () => qc.invalidateQueries({ queryKey: KEY }),
    })
}

export function useDeleteProfile() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (id: number) =>
            apiFetch<void>(`${API_BASE}/profiles/${id}`, { method: 'DELETE' }),
        onSuccess: () => qc.invalidateQueries({ queryKey: KEY }),
    })
}
