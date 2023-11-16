<script>
export default {
    name: "Nav",
    setup() {
        const logout = () => {
            sessionStorage.removeItem("token");
            window.location.href = "/login";
        }
        return {
            logout
        }
    }
}
</script>


<template>
  <nav class="navbar navbar-dark navbar-expand-lg bg-dark border-bottom border-primary">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/home">Ticket</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse " id="navbarTogglerDemo03">
                <ul class="nav">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/profile">Profile</router-link>
                    </li>
                </ul>
                <ul class="nav ms-auto">
                    <li class="nav-item">
                        <button @click="logout" class="nav-link" >Logout</button>
                    </li>
                </ul>
            </div>

        </div>
    </nav>
</template>