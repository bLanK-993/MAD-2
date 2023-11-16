

<template>
    <AdminNav />
    <div style="padding: 3rem;">
        <h1 class="text-dark">Admin Dashboard</h1>
        <div class="card my-2">
            <h5 class="card-header d-flex justify-content-between align-items-center ">
                <span>Add a new venue</span>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newvenue">Add</button>
            </h5>
        </div>
        <div class="card my-2">
            <h5 class="card-header d-flex justify-content-between align-items-center ">
                <span>Add a new event</span>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newevent">Add</button>
            </h5>
        </div>
        <div class="card my-2">
            <h5 class="card-header d-flex justify-content-between align-items-center ">
                <span>Add a new show</span>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newshow">Add</button>
            </h5>
        </div>
        <div v-if="toastModal"
            style="position: fixed;z-index: 10; bottom: 1rem;right: 1rem;width: max-content;border:4px solid black; padding: 1rem;background-color: #ddd;border-radius: 10px;">
            <div @click="toastModal = !toastModal" style="position: absolute;top: 2px;right: 4px;cursor: pointer;">X</div>
            <Toast :err=toast></Toast>
        </div>

        <Venue :manage="true" v-for="theater in theaters" :theater_id="theater.id" :capacity="theater.capacity"
            :city="theater.city" :place="theater.place" :name="theater.name">
            <template v-slot:show>
                <Shows :manage="true" v-for="event in theater.events" :theater_id="theater.id" :price="event.price"
                    :event_id="event.id" :name="event.name" :shows="event.shows" :labels="event.labels"
                    :ratings="event.ratings">

                </Shows>
            </template>

        </Venue>
        <div class="modal fade" id="newshow" tabindex="-1" aria-labelledby="newshow" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="newshow">Add a new show</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body d-flex flex-column  gap-2 ">
                        <select v-model="theater_id" class="form-select" aria-label="Default select example">
                            <option :value="null" selected>Select Theater</option>
                            <option v-for="theater in theaters" :value="theater.id">{{ theater.name }}</option>
                        </select>
                        <select v-model="event_id" class="form-select" aria-label="Default select example">
                            <option selected>Select Event</option>
                            <option v-for="event in event_list" :value="event.id">{{ event.name }}</option>
                        </select>
                        <div class="input-group mb-3">
                            <span class="input-group-text">Date </span>
                            <input ref="date" id="cost" type="datetime-local"
                                class="form-control bg-dark text-light bg-dark text-light" aria-label="Sizing example input"
                                aria-describedby="cost">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">Start Time </span>
                            <input ref="start_time" id="cost" type="datetime-local"
                                class="form-control bg-dark text-light bg-dark text-light" aria-label="Sizing example input"
                                aria-describedby="cost">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">End Time </span>
                            <input ref="end_time" id="cost" type="datetime-local"
                                class="form-control bg-dark text-light bg-dark text-light" aria-label="Sizing example input"
                                aria-describedby="cost">
                        </div>

                        <div class="input-group mb-3">
                            <span class="input-group-text" id="seats">Available Seats</span>
                            <input ref="seats" type="text" class="form-control bg-dark text-light"
                                aria-label="Sizing example input" aria-describedby="seats">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" data-bs-dismiss="modal" @click="createShow" class="btn btn-primary">Save
                            changes</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="newevent" tabindex="-1" aria-labelledby="newevent" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="newevent">Add a new event</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body d-flex flex-column  gap-2 ">
                        <select v-model="theater_id" class="form-select" aria-label="Default select example">
                            <option selected>Select Theater</option>
                            <option v-for="theater in theaters" :value="theater.id">{{ theater.name }}</option>
                        </select>
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="event_name">Name</span>
                            <input ref="event_name" type="text" class="form-control" aria-label="Sizing example input"
                                aria-describedby="event_name">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="event_name">Ratings</span>
                            <input
                                @input="(el) => { if (el.target.value > 5) { el.target.value = 5 } if (el.target.value < 0) { el.target.value = 0 } }"
                                ref="event_ratings" min="1" max="5" step="0.01" type="number" class="form-control"
                                aria-label="Sizing example input" aria-describedby="event_name">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="event_name">Price</span>
                            <input ref="event_price" type="number" class="form-control" aria-label="Sizing example input"
                                aria-describedby="event_name">
                        </div>

                        <div class="input-group mb-3">
                            <span class="input-group-text" id="event_name">Labels</span>
                            <input ref="event_labels" type="text" class="form-control" aria-label="Sizing example input"
                                aria-describedby="event_name">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" @click="createEvent" data-bs-dismiss="modal" class="btn btn-primary">Save
                            changes</button>
                    </div>
                </div>
            </div>
        </div>





        <div class="modal fade" id="newvenue" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="newvenuelabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content bg-dark text-light">
                    <div class="modal-header">
                        <h5 class="modal-title" id="newvenuelabel">Create a new venue</h5>
                        <button type="button" class="btn-close btn-close-white " data-bs-dismiss="modal"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="venue_name">Name</span>
                            <input ref="theater_name" type="text" class="form-control bg-dark text-light"
                                aria-label="Sizing example input" aria-describedby="venue_name">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="venue_place">Place </span>
                            <input ref="theater_place" type="text"
                                class="form-control bg-dark text-light bg-dark text-light" aria-label="Sizing example input"
                                aria-describedby="venue_place">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="venue_location">Location </span>
                            <input ref="theater_city" type="text" class="form-control bg-dark text-light"
                                aria-label="Sizing example input" aria-describedby="venue_location">
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text" id="venue_cap">Capacity </span>
                            <input ref="theater_capacity" type="number" class="form-control bg-dark text-light"
                                aria-label="Sizing example input" aria-describedby="venue_cap">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" @click="createTheater" data-bs-dismiss="modal"
                            class="btn btn-primary">Save</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
//@ts-ignore
import AdminNav from '../components/AdminNav.vue';
import Toast from '../components/Toast.vue';
import Venue from '../components/Venues.vue';
//@ts-ignore
import Shows from '../components/Shows.vue';
import { ref, watch } from 'vue'
export default {
    name: "Admin",
    components: {
        AdminNav,
        Toast,
        Venue,
        Shows
    },
    setup() {
        const theater_name = ref();
        const theater_place = ref();
        const theater_city = ref();
        const theater_capacity = ref();
        const theater_id = ref();
        const event_id = ref();
        const event_name = ref()
        const event_ratings = ref()
        const event_price = ref()
        const event_labels = ref()
        const toast = ref();
        const theaters = ref([]);
        const events = ref([]);
        const event_list = ref([])
        const toastModal = ref(false);
        const date = ref();
        const start_time = ref();
        const end_time = ref();
        const seats = ref();
        const token = JSON.parse(sessionStorage.getItem("token"));
        const createTheater = async () => {
            const response = await fetch('http://localhost:5000/theater', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    name: theater_name.value.value,
                    place: theater_place.value.value,
                    city: theater_city.value.value,
                    capacity: theater_capacity.value.value
                })

            })

            const data = await response.json();
            if (response.status === 200) {
                console.log(data);
                toastModal.value = true;
                toast.value = data.message;
                window.location.reload();
            }
            else {
                toastModal.value = true;
                toast.value = data.err;
                console.log("Something went wrong");
            }
        }

        const createEvent = async () => {
            console.log("theater_id", theater_id);
            const response = await fetch('http://localhost:5000/event', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    name: event_name.value.value,
                    ratings: event_ratings.value.value,
                    price: event_price.value.value,
                    labels: event_labels.value.value,
                    theater_id: theater_id.value
                })
            })
            const data = await response.json();
            if (response.status === 200) {
                console.log(data);
                toastModal.value = true;
                events.value = ""
                events.value = data.message;
                toast.value = data.message;
                theater_id.value = null;
            }
            else {
                toastModal.value = true;
                toast.value = data.err;
                console.log("Something went wrong");
            }
        }

        const createShow = async () => {
            const response = await fetch('http://localhost:5000/show', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    date: new Date(date.value.value).getTime(),
                    start_time: new Date(start_time.value.value).getTime(),
                    end_time: new Date(end_time.value.value).getTime(),
                    event_id: event_id.value,
                    theater_id: theater_id.value,
                    available_seats: seats.value.value
                })
            })
            const data = await response.json();
            if (response.status === 200) {
                console.log(data);
                toastModal.value = true;
                toast.value = data.message;
                window.location.reload();
            }
            else {
                toastModal.value = true;
                toast.value = data.err;
                console.log("Something went wrong");
            }
        }
        const print = () => {
            const body = {
                date: new Date(date.value.value).getTime(),
                start_time: new Date(start_time.value.value).getTime(),
                end_time: new Date(end_time.value.value).getTime(),
                seats: seats.value.value,
                event_id: event_id.value,
                theater_id: theater_id.value,
                available_seats: seats.value.value
            }
            console.log(body);
        }
        const getTheater = async () => {
            const response = await fetch('http://localhost:5000/admin/theater', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            const data = await response.json();
            if (response.status === 200) {
                console.log(data);
                theaters.value = data;
            }
            else {
                toastModal.value = true;
                toast.value = data.err;
                console.log("Something went wrong");
                console.log(data.err);
            }
        }
        getTheater()
        const getList = (id) => {
            for (let i = 0; i < theaters.value.length; i++) {
                if (theaters.value[i].id == id) {
                    event_list.value = theaters.value[i].events
                    return
                }
            }
        }
        watch(events, (newVal, oldVal) => {
            console.log(newVal);
            getTheater()
        })
        watch(theater_id, (newVal, oldVal) => {
            console.log("newVal");
            getList(newVal)
        })
        return {
            theater_name,
            theater_place,
            theater_city,
            theater_capacity,
            toast,
            toastModal,
            createTheater,
            getTheater,
            theaters,
            events,
            event_name,
            event_ratings,
            event_price,
            event_labels,
            createEvent,
            theater_id,
            event_id,
            event_list,
            date,
            start_time,
            end_time,
            seats,
            createShow,
            print
        }
    }

}

</script>