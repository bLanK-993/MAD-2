
<template>
    <NavBar />
    <h1 class="m-3 display-6 ">Tickets booked</h1>

    <div class="d-flex flex-wrap gap-4 m-3">
        <div v-for="ticket in tickets" class="card text-light bg-dark" style="width: 18rem;">
            <div class="card-body">
                <div class="card-title d-flex justify-content-between ">
                    <div class="d-flex flex-column gap-1">
                        <h2 class="">{{ ticket.event.name }}</h2>
                        <div class="d-flex gap-2 ">
                            <small v-for="label in ticket.event.labels" style="font-size: .75rem;font-weight: bold;"
                                class="card-subtitle mb-2 lead p-1 px-2 bg-primary text-dark">{{ label.name }}</small>
                        </div>

                        <small style="font-size: 1rem;" class="lead">{{ ticket.event.ratings }} ⭐</small>
                        <small style="cursor: pointer;" class="badge bg-primary" data-bs-toggle="modal"
                            :data-bs-target="'#rate' + ticket.event.id">Rate the
                            movie</small>

                        <!-- Modal -->
                        <div class="modal fade" :id="'rate' + ticket.event.id" tabindex="-1" aria-labelledby="rate"
                            aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered ">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title text-dark " id="rate">Provide your ratings</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="input-group mb-3">
                                            <span class="input-group-text" id="rate_event">Ratings</span>
                                            <input v-model="ratings"
                                                @input="(el) => { if (el.target.value > 5) { el.target.value = 5 } if (el.target.value < 0) { el.target.value = 0 } }"
                                                min="1" max="5" step="0.01" type="number" class="form-control"
                                                aria-label="Sizing example input" aria-describedby="rate_event">
                                        </div>
                                        <input :value="ticket.event.id" class=" d-none " type="number">
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary"
                                            data-bs-dismiss="modal">Close</button>
                                        <button @click="changeRatings(ticket.event.id)" type="button"
                                            class="btn btn-primary" data-bs-dismiss="modal">Save
                                            changes</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <div class="card-text d-flex flex-column justify-content-between ">

                    <div style="width: max-content;">
                        <p style="font-size: 1rem; font-weight: bold;" class="lead m-0">Show:</p>
                        <p><span>{{ dateToTime(ticket.show.start_time) +
                            " - " + dateToTime(ticket.show.end_time) }}</span></p>
                    </div>
                    <div style="width: max-content;">
                        <p style="font-size: 1rem; font-weight: bold;" class="lead m-0">Seats:</p>
                        <p><span>{{ ticket.seats }}</span></p>
                    </div>
                    <div style="width: max-content;">
                        <p style="font-size: 1rem; font-weight: bold;" class="lead m-0">Venue:</p>
                        <p class="m-0">{{ ticket.theater.name }},{{ ticket.theater.place }}, {{ ticket.theater.city
                        }}</p>
                    </div>
                </div>
                <div class="w-100 d-flex justify-content-end ">
                    <button class="card-link btn btn-success text-bg-success my-2 w-50">₹{{ ticket.event.price *
                        ticket.seats
                    }}</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>






import NavBar from "../components/Nav.vue"
import { ref } from "vue"
export default {
    name: "Profile",
    components: {
        NavBar
    },
    setup() {
        const tickets = ref([])
        const err = ref(null)
        const token = JSON.parse(sessionStorage.getItem("token"));
        const ratings = ref(null);
        const getTickets = async () => {
            const response = await fetch("http://localhost:5000/ticket", {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            const data = await response.json();
            if (response.status === 200) {
                tickets.value = data;
                console.log(data);
            } else {
                errModal.value = true;
                err.value = data.err;
                console.log("Something went wrong");
            }
        }
        const changeRatings = async (id) => {
            const response = await fetch("http://localhost:5000/event/ratings", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    event_id: id,
                    ratings: ratings.value
                })
            })
            const data = await response.json();
            if (response.status === 200) {
                alert(data.message)
                window.location.reload();
                console.log(data);
            } else {
                console.log("Something went wrong");
            }

        }
        const print = (id) => {
            console.log(ratings.value);
            console.log(id);
        }
        const dateToTime = (time) => {
            const new_time = new Date(time)
            const t = new_time.getTime();
            const timer = new Date(t).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            return `${timer}`;
        }
        const toDate = (date) => {
            const new_date = new Date(date)
            const d = new_date.getTime();
            const dates = new Date(d).toLocaleDateString('en-US');
            return `${dates}`;
        }
        getTickets()
        return {
            tickets,
            err,
            dateToTime,
            toDate,
            ratings,
            changeRatings,
            print
        }
    }
}
</script>