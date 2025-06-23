import {type MouseEventHandler, type ReactNode} from "react";
import {create} from "zustand/react";

export type MenuItem = {
    title: string;
    action?: string | MouseEventHandler<HTMLDivElement>;
    icon?: ReactNode;
    children?: Array<MenuItem>
}

export type MenuSection = {
    title: string;
    items: MenuItem[];
}
export type PagePathPart = {
    title: string;
    href?: string;
}
export type PageTitle = string | Array<PagePathPart>;

type MenuStore = {
    mainMenu: MenuSection;
    pageMenu: MenuSection | null;
    pageTitle: PageTitle;
    setMainMenu: (newMenu: MenuSection) => void;
    setPageTitle: (newTitle: PageTitle) => void;
    setPageMenu: (newMenu: MenuSection | null) => void;
}

export const useMenu = create<MenuStore>(
    (set) => ({
        mainMenu: {title: "Main", items: []},
        pageMenu: null,
        pageTitle: "",
        setMainMenu: (newMenu: MenuSection) => set({ mainMenu: newMenu }),
        setPageTitle: (newTitle: PageTitle) => set({ pageTitle: newTitle }),
        setPageMenu: (newMenu: MenuSection | null) => set({ pageMenu: newMenu }),
    })
)
