
<script setup>
import { defineProps, ref } from 'vue';
const props = defineProps({
    manage: {
        type: Boolean,
        default: false
    },
    name: {
        type: String,
        required: true
    },
    place: {
        type: String,
        required: true
    },
    city: {
        type: String,
        required: true
    },
    theater_id: {
        type: Number,
        required: true
    },
    capacity: {
        type: Number,
        required: true
    }
})

const venue_name = ref(null);
const venue_place = ref(null);
const venue_city = ref(null);
const venue_capacity = ref(null);
const token = JSON.parse(sessionStorage.getItem("token"));
const editVenue = async () => {
    const response = await fetch('http://localhost:5000/theater', {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            name: venue_name.value.value,
            place: venue_place.value.value,
            city: venue_city.value.value,
            capacity: venue_capacity.value.value,
            theater_id: props.theater_id
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
console.log(props.theater_id)
const deleteVenue = async () => {
    const response = await fetch('http://localhost:5000/theater', {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            theater_id: props.theater_id
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
    <div class="modal fade" :id="'edit_venue' + theater_id" tabindex="-1" aria-labelledby="edit_venue_label"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="edit_venue_label">Edit Venue</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="venue_name">Name</span>
                        <input ref="venue_name" type="text" :value="name" class="form-control"
                            aria-label="Sizing example input" aria-describedby="venue_name">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="venue_place">Place</span>
                        <input ref="venue_place" type="text" :value="place" class="form-control"
                            aria-label="Sizing example input" aria-describedby="venue_place">
                    </div>

                    <div class="input-group mb-3">
                        <span class="input-group-text" id="venue_city">City</span>
                        <input ref="venue_city" type="text" :value="city" class="form-control"
                            aria-label="Sizing example input" aria-describedby="venue_city">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="venue_capacity">Capacity</span>
                        <input ref="venue_capacity" type="number" :value="capacity" class="form-control"
                            aria-label="Sizing example input" aria-describedby="venue_capacity">
                    </div>



                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" @click="editVenue" data-bs-dismiss="modal" class="btn btn-success">Save
                        changes</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" :id="'delete_venue_' + theater_id" tabindex="-1" aria-labelledby="delete_venue_label"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="delete_venue_label">Delete Venue</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to delete {{ name }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button @click="deleteVenue" type="button" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
    </div>


    <div :id="theater_id" class="card my-2">
        <h5 class="card-header text-light  bg-dark d-flex justify-content-between align-items-center ">
            <div class="d-flex flex-column  gap-1">
                <span>{{ name }}</span>
                <small style="font-size: .75rem;" class="lead">{{ place }}, {{ city }}</small>

            </div>
            <div v-if="manage" class="dropdown">
                <button class="btn btn-secondary text-dark dropdown-toggle" type="button" id="dropdownMenuButton1"
                    data-bs-toggle="dropdown" aria-expanded="false">
                    Manage
                </button>
                <ul class="dropdown-menu dropdown-menu-end bg-secondary p-2" aria-labelledby="dropdownMenuButton1">
                    <li><button class="dropdown-item mb-2 rounded" data-bs-toggle="modal"
                            :data-bs-target="'#edit_venue' + theater_id">Edit</button></li>
                    <li><button class="dropdown-item rounded" data-bs-toggle="modal"
                            :data-bs-target="'#delete_venue_' + theater_id">Delete</button></li>
                </ul>
            </div>
        </h5>
        <div class="card-body p-4 row gap-3">
            <slot name="show"></slot>
            <slot name="newshow"></slot>

        </div>
    </div>
    <slot name="newvenue"></slot>
</template>

