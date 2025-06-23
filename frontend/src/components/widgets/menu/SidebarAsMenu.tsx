import {
    SidebarInset,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarProvider,
    SidebarTrigger,
    SidebarMenu,
    SidebarMenuSub,
    SidebarMenuSubItem,
    SidebarMenuSubButton,
    SidebarHeader,
    SidebarContent, SidebarGroup, SidebarGroupLabel, SidebarGroupContent, SidebarFooter, Sidebar,
} from "../../animate-ui/radix/sidebar.tsx";
import {Separator} from "../../ui/separator.tsx";
import {
    Breadcrumb,
    BreadcrumbItem, BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbSeparator
} from "../../ui/breadcrumb.tsx";
import {useAuthStore} from "../../../hooks/auth.ts";
import {type MenuItem, type PagePathPart, useMenu} from "../../../hooks/menu.ts";
import {NavLink} from "react-router-dom";
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger
} from "../../animate-ui/radix/collapsible.tsx";
import {ChevronRight} from "lucide-react";
import SideNavUser from "./SideNavUser.tsx";
import ThemeSwitch from "../ThemeSwitch.tsx";
import {Fragment, type MouseEventHandler, type ReactNode} from "react";
import LanguageSwitch from "../LanguageSwitch.tsx";


const DISPLAY_THEME_SWITCH = true;


function _Link(
    {icon, title, action}: {
        icon?: ReactNode,
        title: string,
        action: string | MouseEventHandler<HTMLSpanElement> | undefined
    }
) {
    if (typeof action === "string") {
        if (action.startsWith("!"))
            return <span
                onClick={() => {
                    window.location.href = action.substring(1);
                }}
            >
                {icon}<span>{title}</span>
            </span>
        return <NavLink to={action}>{icon}<span>{title}</span></NavLink>
    }
    return <span onClick={action}>
        {icon}<span>{title}</span>
    </span>
}


function SidebarElement({element}: { element: MenuItem }) {
    const {children, icon, title, action} = element;
    if (children) {
        return <Collapsible
            key={title}
            asChild
            defaultOpen={true}
            className="group/collapsible"
        >
            <SidebarMenuItem>
                <CollapsibleTrigger asChild>
                    <SidebarMenuButton tooltip={title}>
                        {icon}
                        <span>{title}</span>
                        <ChevronRight className="ml-auto transition-transform duration-300
                            group-data-[state=open]/collapsible:rotate-90" />
                    </SidebarMenuButton>
                </CollapsibleTrigger>
                <CollapsibleContent>
                    <SidebarMenuSub>
                        {children.map((item, index) => (
                            <SidebarMenuSubItem key={index}>
                                <SidebarMenuSubButton asChild isActive={
                                    typeof item.action === 'string' &&
                                    window.location.href.startsWith(item.action)
                                }>
                                    {/*<_Link action={item.action}*/}
                                    {/*       title={item.title}*/}
                                    {/*       icon={item.icon}/>*/}
                                    {_Link({
                                        action: item.action,
                                        title: item.title,
                                        icon: item.icon
                                    })}
                                </SidebarMenuSubButton>
                            </SidebarMenuSubItem>
                        ))}
                    </SidebarMenuSub>
                </CollapsibleContent>
            </SidebarMenuItem>
        </Collapsible>
    }
    return <SidebarMenuItem><SidebarMenuButton asChild isActive={
        typeof action === 'string' && window.location.href.startsWith(action)
    }>
        {_Link({
            action: action,
            title: title,
            icon: icon
        })}
    </SidebarMenuButton></SidebarMenuItem>
}


function SidebarData() {
    const {userData, isLoggedIn} = useAuthStore();
    const {pageMenu, mainMenu} = useMenu();
    console.log(pageMenu, mainMenu)
    return (
        <Sidebar>
            <SidebarHeader className="flex-row justify-center">
                {/* <img src="https://elschool.ru/Content/images/elschool-white.svg"
                      className="w-[128px]"/> */
                    // TODO
                }
                <span>Syngrapha</span>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>{mainMenu.title}</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>{
                            mainMenu.items.map((item, index) =>
                                <SidebarElement element={item} key={index}/>)
                        }</SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
                { pageMenu &&
                    <SidebarGroup>
                        <SidebarGroupLabel>{pageMenu.title}</SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu>{
                                pageMenu.items.map((item, index) =>
                                    <SidebarElement element={item} key={index}/>)
                            }</SidebarMenu>
                        </SidebarGroupContent>
                    </SidebarGroup>
                }
            </SidebarContent>
            <SidebarFooter>
                {
                    DISPLAY_THEME_SWITCH && <SidebarMenu>
                        <SidebarMenuItem className="flex">
                            <ThemeSwitch/>
                            <LanguageSwitch/>
                        </SidebarMenuItem>
                    </SidebarMenu>
                }
                {
                    isLoggedIn
                        ? <SideNavUser user={{
                            username: `${userData?.username}`,
                            email: userData?.email,
                            avatar: userData?.photo,
                        }}/>
                        : <SidebarMenu>
                            <SidebarElement element={{
                                title: "Log in",
                                action: "/auth/login"
                            }}/>
                        </SidebarMenu>
                }
            </SidebarFooter>
        </Sidebar>
    )
}

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
export default function SidebarAsMenu({children}) {
    const {pageTitle} = useMenu();
    return <SidebarProvider>
        <SidebarData/>
        <SidebarInset>
            <header  className="flex h-16 shrink-0 items-center
                gap-2 transition-[width,height] ease-linear
                group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
                <div className="flex items-center gap-2 px-4">
                    <SidebarTrigger className="-ml-1" />
                    <Separator orientation="vertical" className="mr-2 h-4" />
                    {typeof pageTitle === 'string'
                        ? <span>{pageTitle}</span>
                        : <Breadcrumb><BreadcrumbList>{
                            pageTitle.map((part: PagePathPart, index: number) => {
                                return (
                                    <Fragment key={index}>
                                        <BreadcrumbSeparator/>
                                        <BreadcrumbItem>
                                        {part.href?.startsWith("!")
                                            ? <BreadcrumbLink href={part.href.substring(1)}>
                                                {part.title}
                                            </BreadcrumbLink>
                                            : <BreadcrumbLink asChild>
                                                <NavLink to={part.href || "#"}>
                                                    {part.title}
                                                </NavLink>
                                            </BreadcrumbLink>}
                                        </BreadcrumbItem>
                                    </Fragment>
                                )
                            })
                        }</BreadcrumbList></Breadcrumb>}
                </div>
            </header>
            <div className="flex flex-1 flex-col gap-4 p-5 lg:px-10 pt-0">
                {children}
            </div>
        </SidebarInset>
    </SidebarProvider>
}