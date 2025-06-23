import {cn} from "../lib/utils"
import {Button} from "./ui/button"
import {Card, CardContent} from "./ui/card"
import {Input} from "./ui/input"
import {Label} from "./ui/label"
import * as LoginBg from "../assets/react.svg";
import {useState} from "react";
import {Loader2} from "lucide-react";
import {strings} from "../i18n.ts";
import {NavLink} from "react-router-dom";


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
      ...props
    }
) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  return (
      <div className={cn("flex flex-col gap-6", className)} {...props}>
        <Card className="overflow-hidden p-0">
          <CardContent className="grid p-0 md:grid-cols-2">
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
                    {!isRegister && <a
                        href="#"
                        className="ml-auto text-sm underline-offset-2 hover:underline"
                    >
                        {strings.forgotYourPassword}
                    </a>}
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
              </div>
            </form>
            <div className="bg-muted relative hidden md:block">
              <img
                  src={LoginBg.default}
                  alt="Image"
                  className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
              />
            </div>
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
