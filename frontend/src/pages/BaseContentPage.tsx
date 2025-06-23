import {useMenu} from "../hooks/menu.ts";
import {Outlet} from "react-router-dom";
import {useEffect} from "react";
import {CoinsIcon} from "lucide-react";
import SidebarAsMenu from "../components/widgets/menu/SidebarAsMenu.tsx";

export default function BaseContentPage() {
    const {setMainMenu} = useMenu();
    useEffect(() => {
        setMainMenu({
            title: "Navigate",
            items: [
                // {
                //     "title": "Navigation",
                //     "children": [
                //         {
                //             "title": "Promo page",
                //             "action": "!/",
                //             "icon": <NewspaperIcon/>
                //         },
                //         {
                //             "title": "View something",
                //             "action": "!/something/1",
                //         }
                //     ]
                // }
                {
                    title: "Expenses",
                    action: "/transactions",
                    icon: <CoinsIcon/>
                }
            ]
        });
    }, [])
    return <SidebarAsMenu><Outlet/></SidebarAsMenu>;
}
