import { useMemo, useState } from 'react'
import {
    Box,
    Button,
    Separator,
    HStack,
    Input,
    Field,
    Table,
    Text,
    VStack,
    NativeSelect,
} from '@chakra-ui/react'
import { useProfiles } from '@/hooks/useProfiles'
import { useLists, useCreateListEntry, useDeleteListEntry } from '@/hooks/useLists'
import { useBulkUploadLists } from '@/hooks/useListsBulk'
import type { ListEntry, ListType } from '@/lib/api'
import { toaster } from "../components/ui/toaster"

type NewEntry = {
    profile_id: number | ''
    type: ListType
    value: string
}

const emptyEntry = (): NewEntry => ({
    profile_id: '',
    type: 'whitelist',
    value: '',
})

function downloadCsvTemplate() {
    const lines = [
        'profile_id,type,value',                // headers
        '1,whitelist,alice@example.com',       // sample row 1
        '2,blacklist,spam_user_42',            // sample row 2
    ]
    const csv = lines.join('\n')
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'lists_template.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
}

export default function ListsPage() {
    const { data: profiles = [] } = useProfiles()

    // Filters
    const [filterProfileId, setFilterProfileId] = useState<number | ''>('')
    const [filterType, setFilterType] = useState<ListType | ''>('')

    const { data: entries = [], isLoading } = useLists({
        profileId: filterProfileId === '' ? undefined : Number(filterProfileId),
        type: filterType === '' ? undefined : filterType,
    })

    // Create/delete
    const createEntry = useCreateListEntry()
    const deleteEntry = useDeleteListEntry()
    const bulkUpload = useBulkUploadLists()
    const [editing, setEditing] = useState<NewEntry | null>(null)
    const [submitting, setSubmitting] = useState(false)
    const [csvFile, setCsvFile] = useState<File | null>(null)

    const profileOptions = useMemo(
        () => profiles.map((p) => ({ id: p.id!, name: p.name })),
        [profiles]
    )

    function onCreate(e: NewEntry) {
        if (e.profile_id === '' || !e.value.trim()) {
            toaster.create({ title: 'Profile and value are required', type: 'warning' })
            return
        }
        setSubmitting(true)
        createEntry.mutate(
            { profile_id: Number(e.profile_id), type: e.type, value: e.value.trim() } as ListEntry,
            {
                onSuccess: () => {
                    setEditing(null)
                    toaster.create({ title: 'Entry added', type: 'success' })
                },
                onError: (err: any) =>
                    toaster.create({ title: 'Create failed', description: String(err), type: 'error' }),
                onSettled: () => setSubmitting(false),
            }
        )
    }

    function onDelete(id: number) {
        deleteEntry.mutate(id, {
            onSuccess: () => toaster.create({ title: 'Entry deleted', type: 'success' }),
            onError: (err: any) =>
                toaster.create({ title: 'Delete failed', description: String(err), type: 'error' }),
        })
    }

    return (
        <Box p={4}>
            <HStack justify="space-between" marginBottom={4}>
                <Text as="h2" fontSize="lg" fontWeight="semibold">
                    Lists (Whitelist / Blacklist)
                </Text>
                <HStack gap={3}>
                    <Button onClick={() => setEditing(emptyEntry())}>Add Entry</Button>
                </HStack>
            </HStack>
            {/* Bulk CSV uploader */}
            <Box borderWidth="1px" borderRadius="md" padding={4} marginBottom={4}>
                <Text as="h3" fontWeight="semibold" marginBottom={2}>
                    Bulk Upload (CSV)
                </Text>
                <Text fontSize="sm" color="gray.500" marginBottom={3}>
                    Expected headers: <code>profile_id,type,value</code> — example rows:
                    <br />
                    <code>1,whitelist,alice@example.com</code> &nbsp; | &nbsp; <code>2,blacklist,spam_user_42</code>
                </Text>
                <HStack gap={4} align="center">
                    <Input
                        type="file"
                        accept=".csv,text/csv"
                        onChange={(e) => setCsvFile(e.target.files?.[0] ?? null)}
                    />
                    <Button
                        onClick={() => {
                            if (!csvFile) {
                                toaster.create({ title: 'Please choose a CSV file', type: 'warning' })
                                return
                            }
                            bulkUpload.mutate(
                                { file: csvFile },
                                {
                                    onSuccess: (res) => {
                                        toaster.create({
                                            title: 'Upload complete',
                                            description: `Inserted: ${res.inserted}, Skipped: ${res.skipped}`,
                                            type: 'success',
                                        })
                                        setCsvFile(null)
                                    },
                                    onError: (err: any) =>
                                        toaster.create({
                                            title: 'Upload failed',
                                            description: String(err),
                                            type: 'error',
                                        }),
                                }
                            )
                        }}
                        disabled={bulkUpload.isPending}
                    >
                        {bulkUpload.isPending ? 'Uploading…' : 'Upload CSV'}
                    </Button>
                    <Button variant="outline" onClick={downloadCsvTemplate}>
                        Download CSV template
                    </Button>
                </HStack>
            </Box>

            <HStack gap={4} marginBottom={4}>
                <Field.Root maxW="300px">
                    <Field.Label>Filter by Profile</Field.Label>
                    <NativeSelect.Root size="sm" width="240px">
                        <NativeSelect.Field
                            value={filterProfileId}
                            onChange={(e) => setFilterProfileId(e.target.value === '' ? '' : Number(e.target.value))}
                        >
                            <option value="">All</option>
                            {profileOptions.map((p) => (
                                <option key={p.id} value={p.id}>{p.name}</option>
                            ))}
                        </NativeSelect.Field>
                    </NativeSelect.Root>
                </Field.Root>
                <Field.Root maxW="220px">
                    <Field.Label>Filter by Type</Field.Label>
                    <NativeSelect.Root size="sm" width="240px">
                        <NativeSelect.Field
                            value={filterType}
                            onChange={(e) => setFilterType(e.target.value as ListType | '')}
                        >
                            <option value="">All</option>
                            <option value="whitelist">whitelist</option>
                            <option value="blacklist">blacklist</option>
                        </NativeSelect.Field>
                    </NativeSelect.Root>
                </Field.Root>
            </HStack>

            <Table.Root>
                <Table.Header>
                    <Table.Row>
                        <Table.ColumnHeader width="30%">Profile</Table.ColumnHeader>
                        <Table.ColumnHeader width="20%">Type</Table.ColumnHeader>
                        <Table.ColumnHeader>Value</Table.ColumnHeader>
                        <Table.ColumnHeader>Actions</Table.ColumnHeader>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {isLoading ? (
                        <Table.Row><Table.ColumnHeader colSpan={4}>Loading…</Table.ColumnHeader></Table.Row>
                    ) : entries.length === 0 ? (
                        <Table.Row><Table.ColumnHeader colSpan={4}>No entries</Table.ColumnHeader></Table.Row>
                    ) : (
                        entries.map((e) => (
                            <Table.Row key={e.id}>
                                <Table.ColumnHeader>{profiles.find((p) => p.id === e.profile_id)?.name ?? e.profile_id}</Table.ColumnHeader>
                                <Table.ColumnHeader>{e.type}</Table.ColumnHeader>
                                <Table.ColumnHeader>{e.value}</Table.ColumnHeader>
                                <Table.ColumnHeader>
                                    <Button size="sm" onClick={() => onDelete(e.id!)}>Delete</Button>
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
                            Add Entry
                        </Text>
                        <VStack align="stretch" gap={4}>
                            <HStack gap={4}>
                                <Field.Root>
                                    <Field.Label>Profile</Field.Label>
                                    <NativeSelect.Root size="sm" width="240px">
                                        <NativeSelect.Field
                                            value={editing.profile_id}
                                            onChange={(e) =>
                                                setEditing({ ...editing, profile_id: e.target.value === '' ? '' : Number(e.target.value) })
                                            }
                                        >
                                            <option value="">Select profile…</option>
                                            {profileOptions.map((p) => (
                                                <option key={p.id} value={p.id}>{p.name}</option>
                                            ))}
                                        </NativeSelect.Field>
                                    </NativeSelect.Root>
                                </Field.Root>
                                <Field.Root maxW="220px">
                                    <Field.Label>Type</Field.Label>
                                    <NativeSelect.Root size="sm" width="240px">
                                        <NativeSelect.Field
                                            value={editing.type}
                                            onChange={(e) => setEditing({ ...editing, type: e.target.value as ListType })}
                                        >
                                            <option value="whitelist">whitelist</option>
                                            <option value="blacklist">blacklist</option>
                                        </NativeSelect.Field>
                                    </NativeSelect.Root>
                                </Field.Root>
                            </HStack>
                            <Field.Root>
                                <Field.Label>Value</Field.Label>
                                <Input
                                    value={editing.value}
                                    onChange={(e) => setEditing({ ...editing, value: e.target.value })}
                                    placeholder="email@example.com or user id"
                                />
                            </Field.Root>
                            <HStack gap={3} justify="flex-end">
                                <Button onClick={() => setEditing(null)} disabled={submitting}>Cancel</Button>
                                <Button onClick={() => onCreate(editing)} disabled={submitting}>
                                    Add
                                </Button>
                            </HStack>
                        </VStack>
                    </Box>
                </>
            )}
        </Box>
    )
}
