export function useLanguage() {
    return {
        language: localStorage.getItem("--language") || "en",
        setLanguage: (lang: string) => {
            localStorage.setItem("--language", lang);
        }
    }
}