import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Profile from "../views/Profile.vue";
import Landing from "../views/Landing.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "root",
      component: Landing,
    },
    {
      path: "/home",
      name: "home",
      component: Home,
    },
    {
      path: "/profile",
      name: "profile",
      component: Profile,
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/Login.vue"),
    },
    {
      path: "/signup",
      name: "signup",
      component: () => import("../views/Signup.vue"),
    },
    {
      path: "/admin-login",
      name: "admin-login",
      component: () => import("../views/AdminLogin.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("../views/Admin.vue"),
    },
    {
      path: "/summary",
      name: "summary",
      component: () => import("../views/Summary.vue"),
    },
  ],
});

router.beforeEach((to, from, next) => {
  const publicPages = ["/login", "/signup", "/admin-login", "/"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = sessionStorage.getItem("token");

  if (authRequired && !loggedIn) {
    return next("/login");
  }

  next();
});

export default router;
