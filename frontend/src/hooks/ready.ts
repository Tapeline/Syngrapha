import {create} from "zustand/react";

type ReadinessStore = {
    hasLoaded: boolean;
    setReady: (what: string) => void;
    setLoaded: () => void;
    reset: () => void;
    ready: object
    handlers: object,
    notifyWhenReady: (handler: () => void, what: string | null) => void;
}

export const useReadinessStore = create<ReadinessStore>(
    (set) => ({
        hasLoaded: false,
        ready: {},
        setReady: (what: string) => set((state) => {
            if (state.handlers[what])
                for (const handler of state.handlers[what])
                    handler();
            state.ready[what] = true;
            return {ready: state.ready};
        }),
        setLoaded: () => set((state) => {
            if (state.handlers[null])
                for (const handler of state.handlers[null])
                    handler();
            return { hasLoaded: true }
        }),
        reset: () => set({ hasLoaded: false, ready: {} }),
        handlers: {},
        notifyWhenReady: (handler: () => void, what: string | null = null) =>
            set((state) => {
                if (!state.handlers[what]) state.handlers[what] = [];
                state.handlers[what].push(handler);
                return {handlers: state.handlers};
            }),
    })
)
