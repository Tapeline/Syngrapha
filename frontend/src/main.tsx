import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from './App.tsx'
import PromoPage from "./pages/PromoPage.tsx";
import AuthLayout from "./pages/auth/AuthLayout.tsx";
import AuthLoginPage from "./pages/auth/AuthLoginPage.tsx";
import AuthRegisterPage from "./pages/auth/AuthRegisterPage.tsx";
import NotFoundPage from "./pages/NotFoundPage.tsx";
import BaseContentPage from "./pages/BaseContentPage.tsx";
import ViewSomethingPage from "./pages/ViewSomethingPage.tsx";
import ViewAccountPage from "./pages/ViewAccountPage.tsx";
import './index.css'
import RequireAuth from "./pages/RequireAuth.tsx";
import ListFilterCreateTransactionsPage from "./pages/ListFilterCreateTransactionsPage.tsx";
import ViewTransactionPage from "./pages/ViewTransactionPage.tsx";
import ViewProductPage from "./pages/ViewProductPage.tsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<App />}>
                  <Route path="/welcome" element={<PromoPage/>}/>

                  <Route path="/auth" element={<AuthLayout/>}>
                      <Route path="login" element={<AuthLoginPage/>} />
                      <Route path="register" element={<AuthRegisterPage/>} />
                  </Route>

                  <Route element={<BaseContentPage/>}>
                      <Route path="/transactions" element={
                          <RequireAuth><ListFilterCreateTransactionsPage/></RequireAuth>
                      }/>
                      <Route path="/transactions/:transId" element={
                          <RequireAuth><ViewTransactionPage/></RequireAuth>
                      }/>
                      <Route path="/transactions/:transId/:prodId" element={
                          <RequireAuth><ViewProductPage/></RequireAuth>
                      }/>
                      <Route path="/profile" element={
                          <RequireAuth><ViewAccountPage/></RequireAuth>
                      }/>
                  </Route>
              </Route>
              <Route path="*" element={<NotFoundPage/>}/>
          </Routes>
      </BrowserRouter>
  </StrictMode>,
)
