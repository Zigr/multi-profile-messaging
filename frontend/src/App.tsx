import React from 'react';
import { ChakraProvider, Box, FormControl, FormLabel, Input, Switch, Button } from '@chakra-ui/react';

function App() {
    return (
        <ChakraProvider>
            <Box p={4} maxW="600px" mx="auto">
                <FormControl display="flex" alignItems="center" mb={4}>
                    <FormLabel htmlFor="useMailCatcher" mb="0">Use local MailCatcher?</FormLabel>
                    <Switch id="useMailCatcher" />
                </FormControl>
                <FormControl mb={4}>
                    <FormLabel>SMTP Host</FormLabel>
                    <Input placeholder="smtp.gmail.com" />
                </FormControl>
                <FormControl mb={4}>
                    <FormLabel>Port</FormLabel>
                    <Input placeholder="465" />
                </FormControl>
                <FormControl mb={4}>
                    <FormLabel>Username</FormLabel>
                    <Input placeholder="your@gmail.com" />
                </FormControl>
                <FormControl mb={4}>
                    <FormLabel>App Password</FormLabel>
                    <Input type="password" />
                </FormControl>
                <Button colorScheme="blue">Save Settings</Button>
            </Box>
        </ChakraProvider>
    );
}

export default App;
