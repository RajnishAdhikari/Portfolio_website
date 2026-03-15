import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: 1,
            staleTime: 5 * 60 * 1000, // 5 minutes
        },
    },
});

// Helper to invalidate specific queries
export const invalidateQueries = (queryKeys) => {
    if (Array.isArray(queryKeys)) {
        queryKeys.forEach(key => queryClient.invalidateQueries({ queryKey: [key] }));
    } else {
        queryClient.invalidateQueries({ queryKey: [queryKeys] });
    }
};
