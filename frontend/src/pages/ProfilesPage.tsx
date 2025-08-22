"use client"

import { useMemo, useState } from 'react'
import {
    Box,
    Button,
    Separator,
    Field,
    HStack,
    Input,
    NativeSelect,
    Switch,
    Table,
    Text,
    VStack,
} from '@chakra-ui/react'

import { toaster } from "../components/ui/toaster"
import { useCreateOrUpdateProfile, useDeleteProfile, useProfiles } from '@/hooks/useProfiles'
import { useCookieCapture, useCookieRefresh } from '@/hooks/useCookieCapture'
type Platform = 'email' | 'telegram'

type Profile = {
    id?: number
    name: string
    platform: Platform
    credentials: Record<string, any>
    proxy?: string | null
}

const emptyEmailProfile = (): Profile => ({
    name: '',
    platform: 'email',
    credentials: {
        // Gmail (SSL) defaults; toggled off when MailCatcher is enabled
        host: 'smtp.gmail.com',
        port: 465,
        user: '',
        password: '',
        useMailcatcher: false,
    },
    proxy: '',
})

export default function ProfilesPage() {

    const [editing, setEditing] = useState<Profile | null>(null)
    const [loading, setLoading] = useState(false)
    // TanStack Query data
    const { data: profiles = [], isLoading, isError, error } = useProfiles()
    const createOrUpdate = useCreateOrUpdateProfile()
    const removeProfile = useDeleteProfile()

    const isEmail = useMemo(() => editing?.platform === 'email', [editing])
    const useMailcatcher = useMemo(
        () => Boolean(editing?.credentials?.useMailcatcher),
        [editing]
    )
    const captureCookies = useCookieCapture()
    const refreshCookies = useCookieRefresh()

    // top-level load errors
    if (isError) {
        // render once; toast optional
        console.error(error)
    }
    // --- CRUD
    async function saveProfile(p: Profile) {
        setLoading(true)
        createOrUpdate.mutate(p, {
            onSuccess: () => {
                setEditing(null)
                toaster.create({ title: 'Saved', type: 'success' })
            },
            onError: (e: any) => {
                toaster.create({ title: 'Save failed', description: String(e), type: 'error' })
            },
            onSettled: () => setLoading(false),
        })
    }

    async function deleteProfile(id: number) {
        setLoading(true)
        removeProfile.mutate(id, {
            onSuccess: () => toaster.create({ title: 'Deleted', type: 'success' }),
            onError: (e: any) =>
                toaster.create({ title: 'Delete failed', description: String(e), type: 'error' }),
            onSettled: () => setLoading(false),
        })
    }

    // --- Render
    return (
        <Box p={4}>
            <HStack justify="space-between" marginBottom={4}>
                <Text as="h2" fontSize="lg" fontWeight="semibold">
                    Profiles
                </Text>
                <HStack gap={3}>
                    <Button onClick={() => setEditing(emptyEmailProfile())}>
                        New Email Profile
                    </Button>
                    <Button
                        onClick={() =>
                            setEditing({
                                name: '',
                                platform: 'telegram',
                                credentials: { token: '' }, // or cookies later
                                proxy: '',
                            })
                        }
                    >
                        New Telegram Profile
                    </Button>
                </HStack>
            </HStack>

            <Table.Root>
                <Table.Header>
                    <Table.Row>
                        <Table.ColumnHeader width="30%">Name</Table.ColumnHeader>
                        <Table.ColumnHeader width="20%">Platform</Table.ColumnHeader>
                        <Table.ColumnHeader>Actions</Table.ColumnHeader>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {isLoading ? (
                        <Table.Row><Table.ColumnHeader colSpan={3}>Loading…</Table.ColumnHeader></Table.Row>
                    ) : profiles.length === 0 ? (
                        <Table.Row><Table.ColumnHeader colSpan={3}>No profiles yet</Table.ColumnHeader></Table.Row>
                    ) : profiles.map((p) => (
                        <Table.Row key={p.id}>
                            <Table.ColumnHeader>{p.name}</Table.ColumnHeader>
                            <Table.ColumnHeader textTransform="capitalize">{p.platform}</Table.ColumnHeader>
                            <Table.ColumnHeader>
                                <HStack gap={2}>
                                    <Button size="sm" onClick={() => setEditing(p)}>
                                        Edit
                                    </Button>
                                    {p.id ? (
                                        <Button size="sm" onClick={() => deleteProfile(p.id!)} disabled={loading}>
                                            Delete
                                        </Button>
                                    ) : null}
                                    {p.platform !== 'email' && p.id ? (
                                        <Button
                                            size="sm"
                                            onClick={() => {
                                                const loginUrl = prompt('Enter login URL:', 'https://web.telegram.org/a/') || ''
                                                if (!loginUrl) return
                                                captureCookies.mutate(
                                                    { profile_id: p.id!, login_url: loginUrl, headless: false, max_wait_ms: 120000 },
                                                    {
                                                        onSuccess: () => toaster.create({ title: 'Cookies captured', type: 'success' }),
                                                        onError: (e: any) => toaster.create({ title: 'Capture failed', description: String(e), type: 'error' }),
                                                    }
                                                )
                                            }}
                                        >
                                            Capture Cookies
                                        </Button>
                                    ) : null}

                                    {p.platform !== 'email' && p.id ? (
                                        <Button
                                            size="sm"
                                            onClick={() =>
                                                refreshCookies.mutate(
                                                    { profile_id: p.id!, headless: true },
                                                    {
                                                        onSuccess: () => toaster.create({ title: 'Cookies refreshed', type: 'success' }),
                                                        onError: (e: any) => toaster.create({ title: 'Refresh failed', description: String(e), type: 'error' }),
                                                    }
                                                )
                                            }
                                        >
                                            Refresh Cookies
                                        </Button>
                                    ) : null}

                                </HStack>
                            </Table.ColumnHeader>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table.Root>

            {editing && (
                <>
                    <Separator marginY={6} />
                    <Box borderWidth="1px" borderRadius="md" padding={4}>
                        <Text as="h3" fontWeight="semibold" marginBottom={3}>
                            {editing.id ? 'Edit Profile' : 'Create Profile'}
                        </Text>

                        <VStack align="stretch" gap={4}>
                            <HStack gap={4}>
                                <Field.Root>
                                    <Field.Label>Name</Field.Label>
                                    <Input
                                        value={editing.name}
                                        onChange={(e) => setEditing({ ...editing, name: e.target.value })}
                                        placeholder="my-email-profile"
                                    />
                                </Field.Root>

                                <Field.Root>
                                    <Field.Label>Platform</Field.Label>
                                    <NativeSelect.Root size="sm" width="240px">
                                        <NativeSelect.Field
                                            value={editing.platform}
                                            onChange={(e) =>
                                                setEditing({
                                                    ...editing,
                                                    platform: e.target.value as Platform,
                                                })
                                            }
                                        >
                                            <option value="email">email</option>
                                            <option value="telegram">telegram</option>
                                        </NativeSelect.Field>
                                    </NativeSelect.Root>
                                </Field.Root>

                                <Field.Root>
                                    <Field.Label>Proxy (HTTP)</Field.Label>
                                    <Input
                                        value={editing.proxy ?? ''}
                                        onChange={(e) => setEditing({ ...editing, proxy: e.target.value })}
                                        placeholder="http://user:pass@host:port"
                                    />
                                </Field.Root>
                            </HStack>

                            {isEmail && (
                                <Box>
                                    <Text fontWeight="semibold" marginBottom={2}>
                                        SMTP Settings
                                    </Text>

                                    <HStack gap={6} marginBottom={3}>
                                        <Field.Root display="flex" alignItems="center">
                                            <Field.Label margin="0">Use MailCatcher</Field.Label>
                                            <Switch.Root
                                                checked={useMailcatcher}
                                                onChange={(e) =>
                                                    setEditing({
                                                        ...editing!,
                                                        credentials: {
                                                            ...editing!.credentials,
                                                            useMailcatcher: (e.target as HTMLInputElement).checked,
                                                            ...((e.target as HTMLInputElement).checked
                                                                ? { host: 'localhost', port: 1025, user: '', password: '' }
                                                                : { host: 'smtp.gmail.com', port: 465 }),
                                                        },
                                                    })
                                                }
                                            >
                                                <Switch.HiddenInput />
                                                <Switch.Control>
                                                </Switch.Control>
                                            </Switch.Root>
                                        </Field.Root>
                                        {useMailcatcher && (
                                            <Text>
                                                MailCatcher UI: <strong>http://localhost:1080</strong>
                                            </Text>
                                        )}
                                    </HStack>

                                    <HStack gap={4}>
                                        <Field.Root>
                                            <Field.Label>SMTP Host</Field.Label>
                                            <Input
                                                value={editing.credentials.host ?? ''}
                                                onChange={(e) =>
                                                    setEditing({
                                                        ...editing!,
                                                        credentials: { ...editing!.credentials, host: e.target.value },
                                                    })
                                                }
                                                disabled={useMailcatcher}
                                            />
                                        </Field.Root>
                                        <Field.Root>
                                            <Field.Label>Port</Field.Label>
                                            <Input
                                                type="number"
                                                value={editing.credentials.port ?? ''}
                                                onChange={(e) =>
                                                    setEditing({
                                                        ...editing!,
                                                        credentials: {
                                                            ...editing!.credentials,
                                                            port: Number(e.target.value || 0),
                                                        },
                                                    })
                                                }
                                                disabled={useMailcatcher}
                                            />
                                        </Field.Root>
                                        <Field.Root>
                                            <Field.Label>Username</Field.Label>
                                            <Input
                                                value={editing.credentials.user ?? ''}
                                                onChange={(e) =>
                                                    setEditing({
                                                        ...editing!,
                                                        credentials: { ...editing!.credentials, user: e.target.value },
                                                    })
                                                }
                                                disabled={useMailcatcher}
                                            />
                                        </Field.Root>
                                        <Field.Root>
                                            <Field.Label>Password (App Password)</Field.Label>
                                            <Input
                                                type="password"
                                                value={editing.credentials.password ?? ''}
                                                onChange={(e) =>
                                                    setEditing({
                                                        ...editing!,
                                                        credentials: { ...editing!.credentials, password: e.target.value },
                                                    })
                                                }
                                                disabled={useMailcatcher}
                                            />
                                        </Field.Root>
                                    </HStack>
                                </Box>
                            )}

                            {!isEmail && (
                                <Box>
                                    <Text fontWeight="semibold" marginBottom={2}>
                                        Telegram Settings
                                    </Text>
                                    <HStack gap={4}>
                                        <Field.Root>
                                            <Field.Label>Bot Token</Field.Label>
                                            <Input
                                                value={editing.credentials.token ?? ''}
                                                onChange={(e) =>
                                                    setEditing({
                                                        ...editing!,
                                                        credentials: { ...editing!.credentials, token: e.target.value },
                                                    })
                                                }
                                                placeholder="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
                                            />
                                        </Field.Root>
                                    </HStack>
                                </Box>
                            )}

                            <HStack gap={3} justify="flex-end">
                                <Button onClick={() => setEditing(null)} disabled={loading}>
                                    Cancel
                                </Button>
                                <Button onClick={() => saveProfile(editing!)} disabled={loading}>
                                    {editing.id ? 'Save Changes' : 'Create Profile'}
                                </Button>
                            </HStack>
                        </VStack>
                    </Box>
                </>
            )}
        </Box>
    )
}
