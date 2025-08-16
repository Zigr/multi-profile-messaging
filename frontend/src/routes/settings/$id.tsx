import { createFileRoute, useParams } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/$id')({
    component: () => {
        const { id } = useParams({ from: '/settings/$id' })
        return <div>Settings item: {id}</div>
    },
})
