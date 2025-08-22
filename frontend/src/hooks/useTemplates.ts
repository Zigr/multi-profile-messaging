import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiFetch, type Template } from '@/lib/api'

const KEY = ['templates']

export function useTemplates() {
    return useQuery({
        queryKey: KEY,
        queryFn: () => apiFetch<Template[]>('/templates'),
    })
}

export function useCreateOrUpdateTemplate() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (t: Template) => {
            const method = t.id ? 'PUT' : 'POST'
            const url = t.id ? `/templates/${t.id}` : '/templates'
            return apiFetch<Template>(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(t),
            })
        },
        onSuccess: () => qc.invalidateQueries({ queryKey: KEY }),
    })
}

export function useDeleteTemplate() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (id: number) =>
            apiFetch<void>(`/templates/${id}`, { method: 'DELETE' }),
        onSuccess: () => qc.invalidateQueries({ queryKey: KEY }),
    })
}

