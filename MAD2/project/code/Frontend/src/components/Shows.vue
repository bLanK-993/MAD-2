<script setup>
import { ref, computed } from "vue"
const props = defineProps({
    manage: {
        type: Boolean,
        default: false
    },
    name: {
        type: String,
        required: true
    },
    labels: {
        type: Array,
        required: true
    },
    ratings: {
        type: Number,
        required: true
    },
    shows: {
        type: Array,
        required: true
    },
    event_id: {
        type: Number,
        required: true
    },
    price: {
        type: Number,
        required: true
    },
    theater_id: {
        type: Number,
        required: true
    }

})
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

const eligible_shows = computed(() => {
    return props.shows.filter(show => {
        if (show.available_seats > 0 && new Date(show.date) > new Date()) {
            return show
        }
    })
})

const housefull = computed(() => {
    return props.shows.filter(show => {
        console.log(show);
        if (show.available_seats == 0) {
            return true
        }
    })
})

const selected_show = ref(null);
const cost = ref(0);
const event_name = ref(null);
const seats = ref(null);
const token = JSON.parse(sessionStorage.getItem("token"));

const bookTicket = async () => {
    const response = await fetch("http://localhost:5000/ticket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token} `
        },
        body: JSON.stringify({
            event_id: props.event_id,
            show_id: selected_show.value,
            seats: seats.value,
            theater_id: props.theater_id
        })
    })
    const data = await response.json();
    if (response.status === 200) {
        alert(data.message)
        console.log(data);
    }
    else {
        alert(data.err)
        console.log("Something went wrong");
    }
}


const print = () => {
    console.log(props.event_id)
    console.log(props.theater_id)
    console.log(seats.value)
    console.log(selected_show.value)
    console.log(cost.value)
    console.log(token)
}

const editEvent = async () => {
    const response = await fetch('http://localhost:5000/event', {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            event_id: props.event_id,
            name: event_name.value.value
        })

    })
    const data = await response.json();
    if (response.status === 200) {
        window.location.reload();
        console.log(data);
    }
    else {
        console.log("Something went wrong");
    }
}

const deleteEvent = async () => {
    const response = await fetch('http://localhost:5000/event', {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            event_id: props.event_id
        })
    })
    const data = await response.json();
    if (response.status === 200) {
        window.location.reload();
        console.log(data);
    }
    else {
        console.log("Something went wrong");
    }

}


</script>



<template>
    <div class="modal fade" :id="'edit_event' + event_id" tabindex="-1" aria-labelledby="edit_event_label"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="edit_event_label">Edit event</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="event_name">Name</span>
                        <input ref="event_name" type="text" :value="name" class="form-control"
                            aria-label="Sizing example input" aria-describedby="event_name">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" @click="editEvent" class="btn btn-success">Save changes</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" :id="'delete_event' + event_id" tabindex="-1" aria-labelledby="delete_event_label"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="delete_event_label">Delete event</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to delete {{ name }} ?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" @click="deleteEvent" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
    </div>

    <div class="card text-light bg-dark" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title d-flex justify-content-between ">
                <div class="d-flex flex-column gap-1">
                    <p class=" mb-0">{{ name }}</p>
                    <div class="d-flex gap-2 ">
                        <small v-for="label in labels" style="font-size: .75rem;font-weight: bold;"
                            class="card-subtitle mb-2 lead p-1 px-2 bg-primary text-dark">{{ label.name }}</small>
                    </div>

                    <small style="font-size: 1rem;" class="lead">{{ ratings }} ⭐</small>
                </div>

                <div v-if="manage" class="dropdown">
                    <button class="btn badge bg-secondary dropdown-toggle text-dark " type="button" id="dropdownMenuButton1"
                        data-bs-toggle="dropdown" aria-expanded="false">
                        &nbsp;
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end bg-secondary p-2" aria-labelledby="dropdownMenuButton1">
                        <li><button class="dropdown-item mb-2 rounded" data-bs-toggle="modal"
                                :data-bs-target="'#edit_event' + event_id">Edit</button></li>
                        <li><button class="dropdown-item rounded" data-bs-toggle="modal"
                                :data-bs-target="'#delete_event' + event_id">Delete</button></li>
                    </ul>
                </div>

            </h5>

            <div class="card-text d-flex flex-wrap justify-content-between  gap-3">

                <div style="width: max-content;">
                    <p style="font-size: 1rem;" class="lead m-0">Shows:</p>
                    <ul>
                        <template v-if="eligible_shows.length > 0">
                            <li v-for="show in eligible_shows" style="font-size: 1rem;"
                                class="lead d-flex flex-column  m-0">
                                <span>{{ toDate(show.date) }}</span>
                                <span>{{ dateToTime(show.start_time) +
                                    " - " + dateToTime(show.end_time) }}</span>
                            </li>
                        </template>
                        <template v-else>
                            <li style="font-size: 1rem;" class="lead d-flex flex-column  m-0">
                                <span>No shows available</span>
                            </li>
                        </template>
                    </ul>
                </div>
            </div>
            <div class="w-100 d-flex justify-content-between ">
                <button class="card-link btn btn-success text-bg-success my-2 w-50">₹{{ price }}</button>
                <button class="card-link btn btn-primary my-2 w-50" data-bs-toggle="modal" :disabled="housefull.value"
                    :data-bs-target="'#book_show' + event_id">{{ !housefull.value && eligible_shows.length > 0 ? "Book" :
                        !housefull.value && eligible_shows.length ? "No Shows" : housefull.value ? "Housefull" : "No Shows"
                    }}</button>
            </div>
        </div>
    </div>
    <div class="modal fade" :id="'book_show' + event_id" tabindex="-1" aria-labelledby="book_show_label" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="d-flex flex-column ">
                        <h5 class="modal-title" id="book_show_label">Book Show</h5>
                        <select v-model="selected_show" class="form-select badge px-5 bg-primary rounded-pill"
                            aria-label="Default select example">
                            <option selected>Select a show</option>
                            <template v-if="eligible_shows.length > 0">
                                <option v-for="show in eligible_shows" :id="show.id" :value="show.id">
                                    <div class="d-flex flex-column gap-2"><span>{{ dateToTime(show.start_time) +
                                        " - " + dateToTime(show.end_time) }}</span>
                                        <span>({{ toDate(show.date)
                                        }})</span>
                                    </div>
                                </option>
                            </template>
                            <template v-else>
                                <option disabled>No shows available</option>
                            </template>

                        </select>


                    </div>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body bg-secondary ">
                    <div v-for="show in shows">
                        <div v-if="show.id == selected_show">
                            <div class="input-group mb-3">
                                <span class="input-group-text">Date </span>
                                <input id="date" type="text" class="form-control bg-dark text-light bg-dark text-light"
                                    aria-label="Sizing example input" aria-describedby="cost"
                                    :value="'(' + toDate(show.date) + ') ' + dateToTime(show.start_time) + ' - ' + dateToTime(show.end_time)"
                                    disabled>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text" id="seats">Available Seats</span>
                                <input type="text" :disabled="show.available_seats == 0"
                                    class="form-control bg-dark text-light" aria-label="Sizing example input"
                                    aria-describedby="seats" :value="show.available_seats" disabled>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">Cost/Ticket </span>
                                <input id="cost" type="text" class="form-control bg-dark text-light bg-dark text-light"
                                    aria-label="Sizing example input" aria-describedby="cost" :value="price" disabled>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">Required Seats</span>
                                <input v-model="seats" id="req_seats" ref="req_seats" type="number" min="1"
                                    :max="show.available_seats" :disabled="show.available_seats == 0"
                                    @input="el => { if (el.target.value > show.available_seats) { el.target.value = show.available_seats } if (el.target.value <= 0) { el.target.value = 1 }; cost = el.target.value * price }"
                                    class="form-control bg-dark text-light bg-dark text-light "
                                    aria-label="Sizing example input" aria-describedby="req_seats">
                            </div>
                        </div>
                    </div>
                </div>
                <hr>

                <div class="d-flex flex-column align-items-start p-3">
                    <p class="lead">Estimated Cost</p>
                    <h2 class="display-6 text-dark">₹{{ cost }}</h2>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" data-bs-dismiss="modal" @click="bookTicket" class="btn btn-success">Confirm
                        Bookings</button>
                </div>
            </div>
        </div>
    </div>
</template>