"use client"
import {
    BadgeCheck,
    ChevronsUpDown,
    LogOut,
} from "lucide-react"
import {
    Avatar,
    AvatarFallback,
    AvatarImage,
} from "../../ui/avatar"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "../../ui/dropdown-menu"
import {
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar,
} from "../../animate-ui/radix/sidebar"
import {UserIcon} from "lucide-react";
import {strings} from "../../../i18n.ts";
import {useAuthStore} from "../../../hooks/auth.ts";
import {useNavigate} from "react-router-dom";

export default function SideNavUser(
    {
        user
    }: {
        user: {
            username: string
            email: string
            avatar: string
        }
    }
) {
    const {isMobile, setOpenMobile} = useSidebar();
    const {logout} = useAuthStore();
    const navigate = useNavigate();
    return (
        <SidebarMenu>
            <SidebarMenuItem>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <SidebarMenuButton
                            size="lg"
                            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                        >
                            <Avatar className="h-8 w-8 rounded-lg">
                                <AvatarImage src={user.avatar} alt={user.username}/>
                                <AvatarFallback className="rounded-lg">
                                    <UserIcon/>
                                </AvatarFallback>
                            </Avatar>
                            <div className="grid flex-1 text-left text-sm leading-tight">
                                <span className="truncate font-semibold">{user.username}</span>
                                <span className="truncate text-xs">{user.email}</span>
                            </div>
                            <ChevronsUpDown className="ml-auto size-4"/>
                        </SidebarMenuButton>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent
                        className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                        side={isMobile ? "bottom" : "right"}
                        align="end"
                        sideOffset={4}
                    >
                        <DropdownMenuLabel className="p-0 font-normal">
                            <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                                <Avatar className="h-8 w-8 rounded-lg">
                                    <AvatarImage src={user.avatar} alt={user.username}/>
                                    <AvatarFallback className="rounded-lg">
                                        <UserIcon/>
                                    </AvatarFallback>
                                </Avatar>
                                <div className="grid flex-1 text-left text-sm leading-tight">
                                    <span className="truncate font-semibold">{user.username}</span>
                                    <span className="truncate text-xs">{user.email}</span>
                                </div>
                            </div>
                        </DropdownMenuLabel>
                        <DropdownMenuSeparator/>
                        <DropdownMenuGroup>
                            <DropdownMenuItem onClick={
                                () => {
                                    navigate("/profile");
                                    setOpenMobile(false);
                                }
                            }>
                                <BadgeCheck/>
                                {strings.account}
                            </DropdownMenuItem>
                            {/*<DropdownMenuItem>*/}
                            {/*    <CreditCard/>*/}
                            {/*    Billing*/}
                            {/*</DropdownMenuItem>*/}
                            {/*<DropdownMenuItem>*/}
                            {/*    <Bell/>*/}
                            {/*    Notifications*/}
                            {/*</DropdownMenuItem>*/}
                        </DropdownMenuGroup>
                        <DropdownMenuSeparator/>
                        <DropdownMenuItem onClick={() => {
                            logout();
                            setOpenMobile(false);
                            window.location.href = "/";
                        }}>
                            <LogOut/>
                            {strings.logoutAction}
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </SidebarMenuItem>
        </SidebarMenu>
    )
}