import { useMemo, useState } from 'react'
import {
    Box,
    Button,
    Separator,
    Field,
    HStack,
    Input,
    Table,
    Text,
    Textarea,
    VStack,
} from '@chakra-ui/react'
import { useTemplates, useCreateOrUpdateTemplate, useDeleteTemplate } from '@/hooks/useTemplates'
import type { Template } from '@/lib/api'
import { toaster } from "../components/ui/toaster"

const emptyTemplate = (): Template => ({
    name: '',
    subject: '',
    body: '',
})

export default function TemplatesPage() {
    const { data: templates = [], isLoading, isError, error } = useTemplates()
    const createOrUpdate = useCreateOrUpdateTemplate()
    const removeTemplate = useDeleteTemplate()

    const [editing, setEditing] = useState<Template | null>(null)
    const [loading, setLoading] = useState(false)

    // optional: log fetch error once
    useMemo(() => {
        if (isError && error) console.error(error)
    }, [isError, error])

    function onSave(t: Template) {
        setLoading(true)
        createOrUpdate.mutate(t, {
            onSuccess: () => {
                setEditing(null)
                toaster.create({ title: 'Template saved', type: 'success' })
            },
            onError: (e: any) =>
                toaster.create({ title: 'Save failed', description: String(e), type: 'error' }),
            onSettled: () => setLoading(false),
        })
    }

    function onDelete(id: number) {
        setLoading(true)
        removeTemplate.mutate(id, {
            onSuccess: () => toaster.create({ title: 'Template deleted', type: 'success' }),
            onError: (e: any) =>
                toaster.create({ title: 'Delete failed', description: String(e), type: 'error' }),
            onSettled: () => setLoading(false),
        })
    }

    return (
        <Box p={4}>
            <HStack justify="space-between" marginBottom={4}>
                <Text as="h2" fontSize="lg" fontWeight="semibold">
                    Templates
                </Text>
                <Button onClick={() => setEditing(emptyTemplate())}>New Template</Button>
            </HStack>

            <Table.Root>
                <Table.Header>
                    <Table.Row>
                        <Table.ColumnHeader width="30%">Name</Table.ColumnHeader>
                        <Table.ColumnHeader width="30%">Subject</Table.ColumnHeader>
                        <Table.ColumnHeader>Actions</Table.ColumnHeader>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {isLoading ? (
                        <Table.Row><Table.ColumnHeader colSpan={3}>Loading…</Table.ColumnHeader></Table.Row>
                    ) : templates.length === 0 ? (
                        <Table.Row><Table.ColumnHeader colSpan={3}>No templates yet</Table.ColumnHeader></Table.Row>
                    ) : (
                        templates.map((t) => (
                            <Table.Row key={t.id}>
                                <Table.ColumnHeader>{t.name}</Table.ColumnHeader>
                                <Table.ColumnHeader>{t.subject}</Table.ColumnHeader>
                                <Table.ColumnHeader>
                                    <HStack gap={2}>
                                        <Button size="sm" onClick={() => setEditing(t)}>Edit</Button>
                                        {t.id ? (
                                            <Button size="sm" onClick={() => onDelete(t.id!)} disabled={loading}>
                                                Delete
                                            </Button>
                                        ) : null}
                                    </HStack>
                                </Table.ColumnHeader>
                            </Table.Row>
                        ))
                    )}
                </Table.Body>
            </Table.Root>

            {editing && (
                <>
                    <Separator marginY={6} />
                    <Box borderWidth="1px" borderRadius="md" padding={4}>
                        <Text as="h3" fontWeight="semibold" marginBottom={3}>
                            {editing.id ? 'Edit Template' : 'Create Template'}
                        </Text>
                        <VStack align="stretch" gap={4}>
                            <HStack gap={4}>
                                <Field.Root>
                                    <Field.Label>Name</Field.Label>
                                    <Input
                                        value={editing.name}
                                        onChange={(e) => setEditing({ ...editing!, name: e.target.value })}
                                        placeholder="welcome"
                                    />
                                </Field.Root>
                                <Field.Root>
                                    <Field.Label>Subject (optional)</Field.Label>
                                    <Input
                                        value={editing.subject ?? ''}
                                        onChange={(e) => setEditing({ ...editing!, subject: e.target.value })}
                                        placeholder="Hello {Name}"
                                    />
                                </Field.Root>
                            </HStack>
                            <Field.Root>
                                <Field.Label>Body</Field.Label>
                                <Textarea
                                    value={editing.body}
                                    onChange={(e) => setEditing({ ...editing!, body: e.target.value })}
                                    placeholder="Hi {Name}, welcome to {City}!"
                                    rows={8}
                                />
                            </Field.Root>
                            <HStack gap={3} justify="flex-end">
                                <Button onClick={() => setEditing(null)} disabled={loading}>Cancel</Button>
                                <Button onClick={() => onSave(editing!)} disabled={loading}>
                                    {editing.id ? 'Save Changes' : 'Create Template'}
                                </Button>
                            </HStack>
                        </VStack>
                    </Box>
                </>
            )}
        </Box>
    )
}

