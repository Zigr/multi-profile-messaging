import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiFetchForm } from '@/lib/api'

type BulkUploadArgs = {
    file: File
}

export function useBulkUploadLists() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async ({ file }: BulkUploadArgs) => {
            const fd = new FormData()
            fd.append('file', file)
            // If your backend supports flags like dry-run, you can append them here:
            // fd.append('dry_run', 'false')
            return apiFetchForm<{ inserted: number; skipped: number; errors?: string[] }>(
                '/lists/bulk',
                fd
            )
        },
        onSuccess: () => {
            // refresh any cached list queries
            qc.invalidateQueries({ queryKey: ['lists'] })
        },
    })
}
