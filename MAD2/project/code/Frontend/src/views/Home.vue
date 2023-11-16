<script >

import NavBar from '../components/Nav.vue'
import Toast from '../components/Toast.vue'
import Venue from '../components/Venues.vue'
import Shows from '../components/Shows.vue'
import { ref, watch, computed } from 'vue'
export default {
    name: "Home",
    components: {
        NavBar,
        Toast,
        Venue,
        Shows
    },
    setup() {
        const errModal = ref(false);
        const err = ref('');
        const theaters = ref([]);
        const cities = ref(null);
        const labels = ref(null);
        const seats = ref()
        const selectedCity = ref(null);
        const searchTheater = ref(null);
        const selectedLabel = ref(null);
        const searchEvent = ref(null);
        const token = JSON.parse(sessionStorage.getItem("token"));
        const getTheater = async () => {
            console.log("fetching");
            const response = await fetch('http://localhost:5000/get/theater', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token} `
                }
            })
            const data = await response.json();
            if (response.status === 200) {
                theaters.value = data;
                console.log(theaters);
            }
            else {
                errModal.value = true;
                err.value = data.err;
                console.log("Something went wrong");
            }
        }
        const getCity = async () => {
            const response = await fetch("http://localhost:5000/city")
            const data = await response.json();
            if (response.status === 200) {
                cities.value = data;
                console.log(cities);
            }
            else {
                errModal.value = true;
                err.value = data.err;
                console.log("Something went wrong");
            }
        }



        const filteredTheaters = computed(() => {
            if (selectedLabel.value) {
                return theaters.value.filter(theater => {
                    return theater.events.some(event => {
                        return event.labels.some(label => {
                            return label.name.toLowerCase().includes(selectedLabel.value.toLowerCase())
                        })
                    })
                })
            } else {
                return searchTheater.value ?
                    filteredTheaters.value.length > 0 ? filteredTheaters.value.filter((theater) => {
                        console.log(searchTheater.value);
                        if (selectedCity.value) {
                            for (let event of theater.events) {
                                if ((event.name.toLowerCase().includes(searchTheater.value.toLowerCase()) && theater.city === selectedCity.value) || (theater.name.toLowerCase().includes(searchTheater.value.toLowerCase()) && theater.city === selectedCity.value))
                                    return true
                            }
                        }
                        return [...theater.events, theater].some((event) => {
                            return event.name.toLowerCase().includes(searchTheater.value.toLowerCase()) || theater.name.toLowerCase().includes(searchTheater.value.toLowerCase())
                        })
                    }) : theaters.value.filter((theater) => {
                        console.log(searchTheater.value);
                        if (selectedCity.value) {
                            for (let event of theater.events) {
                                if ((event.name.toLowerCase().includes(searchTheater.value.toLowerCase()) && theater.city === selectedCity.value) || (theater.name.toLowerCase().includes(searchTheater.value.toLowerCase()) && theater.city === selectedCity.value))
                                    return true
                            }
                        }
                        return [...theater.events, theater].some((event) => {
                            return event.name.toLowerCase().includes(searchTheater.value.toLowerCase()) || theater.name.toLowerCase().includes(searchTheater.value.toLowerCase())
                        })
                    })
                    : selectedCity.value ? theaters.value.filter((theater) => {
                        return theater.city === selectedCity.value
                    }) : theaters.value
            }
        })

        const getLabel = async () => {
            const response = await fetch("http://localhost:5000/label")
            const data = await response.json();
            if (response.status === 200) {
                labels.value = data.message;
                console.log(labels);
            }
            else {
                errModal.value = true;
                err.value = data.err;
                console.log("Something went wrong");
            }
        }

        getTheater()
        getCity()
        getLabel()
        return {
            err,
            theaters,
            errModal,
            searchTheater,
            filteredTheaters,
            cities,
            selectedCity,
            searchEvent,
            labels,
            selectedLabel
        }
    }
}

</script>
<template>
    <NavBar />
    <div v-if="errModal" @click="errModal = !errModal"
        style="position: fixed;bottom: 1rem;right: 1rem;width: max-content;border:2px solid red; padding: 1rem;background-color: #ddd;border-radius: 10px;">
        <div style="position: absolute;top: 2px;right: 4px;cursor: pointer;">X</div>
        <Toast :err=err></Toast>
    </div>
    <div class="d-sm-flex gap-2 justify-center items-center m-3">
        <div class="input-group m-2">
            <input v-model="searchTheater" @input="el => console.log(el.target.value)" type="text" class="form-control"
                placeholder="Search event/theater" aria-label="Search event/theater">
        </div>
        <div>
            <select v-model="selectedCity" style="min-width: 200px;" class="form-select m-2"
                aria-label="Default select example">
                <option :value="null" selected>Location</option>
                <option v-for="city in cities" :value="city.name">{{ city.name }}</option>
            </select>
        </div>
        <div>
            <select v-model="selectedLabel" style="min-width: 200px;" class="form-select m-2" aria-label="Select Labels">
                <option :value="null" selected>Labels</option>
                <option v-for="label in labels" :value="label.name">{{ label.name }}</option>
            </select>
        </div>
    </div>

    <div v-for="theater in filteredTheaters" class="m-3">
        <Venue :theater_id="theater.id" :name="theater.name" :city="theater.city" :place="theater.place"
            :capacity="theater.capacity">
            <template v-slot:show>
                <Shows v-for="event in theater.events" :theater_id="theater.id" :event_id="event.id" :price="event.price"
                    :name="event.name" :shows="event.shows" :labels="event.labels" :ratings="event.ratings" />
            </template>
        </Venue>
    </div>
</template>
