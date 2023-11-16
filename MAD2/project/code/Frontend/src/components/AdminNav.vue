


<template>
    <nav class="navbar navbar-dark navbar-expand-lg bg-dark">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/admin">Dashboard</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse " id="navbarTogglerDemo03">
                <ul class="nav">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/summary">Summary</router-link>
                    </li>
                </ul>
            </div>
            <div class="collapse navbar-collapse justify-content-end" id="navbarTogglerDemo03">
                <ul class="nav">
                    <li class="nav-item">
                        <button @click="logout" class="nav-link">Logout</button>
                    </li>
                </ul>
            </div>

        </div>
    </nav>
</template>

<script>
export default {
    name: "AdminNav",
    setup() {
        const logout = () => {
            sessionStorage.removeItem("token");
            window.location.href = "/";
        }
        return {
            logout
        }
    }
}
</script>