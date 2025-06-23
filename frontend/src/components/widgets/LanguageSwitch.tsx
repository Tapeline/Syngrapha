import {strings} from "../../i18n.ts";
import {useLanguage} from "../../hooks/language.ts";
import Combobox from "./Combobox.tsx";

export default function LanguageSwitch() {
    const {language, setLanguage} = useLanguage();
    return <div className="flex items-center space-x-2 px-2">
        <Combobox
            onChange={(lang) => {
                setLanguage(lang);
                window.location.reload();
            }}
            hint={strings.languageLabel}
            notFound={strings.languageLabel}
            values={[
                {value: "en", label: "English"},
                {value: "ru", label: "Русский"},
            ]}
            initial={language}
        />
    </div>
}
