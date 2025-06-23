import {cn} from "../lib/utils"
import {Button} from "./ui/button"
import {Card, CardContent} from "./ui/card"
import {Input} from "./ui/input"
import {Label} from "./ui/label"
import {useState} from "react";
import {ChevronsUpDown, Loader2} from "lucide-react";
import {strings} from "../i18n.ts";
import {NavLink} from "react-router-dom";
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger
} from "./animate-ui/radix/collapsible.tsx";


export default function LoginForm(
    {
        className = "",
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-expect-error
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        onLogin = (username: string, password: string) => {
        },
        isLoading = false,
        isRegister = false,
        builtins = [],
        ...props
    }: {
        className?: string;
        onLogin?: (username: string, password: string) => void,
        isLoading?: boolean,
        isRegister?: boolean,
        builtins?: Array<{username: string, password: string, title: string}>
    }
) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  return (
      <div className={cn("flex flex-col gap-6", className)} {...props}>
        <Card className="overflow-hidden p-0">
          <CardContent>
            <form className="p-6 md:p-8" onSubmit={(e) => {
              e.preventDefault();
              onLogin(username, password);
            }}>
              <div className="flex flex-col gap-6">
                <div className="flex flex-col items-center text-center">
                  <h1 className="text-2xl font-bold">{strings.welcome}</h1>
                  <p className="text-muted-foreground text-balance">
                    {isRegister? strings.registerSubtitle : strings.logInSubtitle}
                  </p>
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="username">{strings.usernameLabel}</Label>
                  <Input
                      id="username"
                      type="text"
                      placeholder={strings.usernameLabel}
                      value={username}
                      onChange={(e) =>
                          setUsername(e.target.value)}
                      required
                  />
                </div>
                <div className="grid gap-3">
                  <div className="flex items-center">
                    <Label htmlFor="password">{strings.passwordLabel}</Label>
                    {/*{!isRegister && <a*/}
                    {/*    href="#"*/}
                    {/*    className="ml-auto text-sm underline-offset-2 hover:underline"*/}
                    {/*>*/}
                    {/*    {strings.forgotYourPassword}*/}
                    {/*</a>}*/}
                  </div>
                  <Input id="password" type="password" required value={password}
                         onChange={(e) =>
                             setPassword(e.target.value)}/>
                </div>
                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading && <Loader2 className="mr-2 h-5 w-5 animate-spin"/>}
                  {isRegister? strings.registerAction : strings.logInAction}
                </Button>
                  {
                      isRegister
                          ? <NavLink to="/auth/login">{strings.orLoginAction}</NavLink>
                          : <NavLink to="/auth/register">{strings.orRegisterAction}</NavLink>
                  }
                  {
                      builtins.length > 0 && !isRegister && <Collapsible>
                              <div className="flex items-center justify-between space-x-4">
                                  <h4 className="text-sm">{strings.loginWithPrebuilt}</h4>
                                  <CollapsibleTrigger asChild>
                                      <Button variant="outline" size="sm" className="w-9 p-0">
                                          <ChevronsUpDown className="h-4 w-4" />
                                          <span className="sr-only">Toggle</span>
                                      </Button>
                                  </CollapsibleTrigger>
                              </div>
                          <CollapsibleContent className="space-y-2 pt-4">{
                              builtins.map((item, index) =>
                                <div key={index}>
                                    <Button
                                        onClick={() => onLogin(item.username, item.password)}
                                        variant="outline"
                                        className="w-full py-2"
                                    >{item.title}</Button>
                                </div>
                              )
                          }</CollapsibleContent>
                      </Collapsible>
                  }
              </div>
            </form>
          </CardContent>
        </Card>
        {/*<div*/}
        {/*    className="text-muted-foreground *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">*/}
        {/*  By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}*/}
        {/*  and <a href="#">Privacy Policy</a>.*/}
        {/*</div>*/}
      </div>
  )
}
