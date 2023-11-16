
<template>
    <NavBar />
    <div class="m-3 d-flex flex-wrap justify-content-between ">
        <h1 class="display-6">Admin Summary</h1>
        <button @click="exportData" class="btn btn-outline-dark">Download Data</button>
    </div>
    <div v-if="toastModal"
        style="position: fixed;z-index: 10; bottom: 1rem;right: 1rem;width: max-content;border:4px solid black; padding: 1rem;background-color: #ddd;border-radius: 10px;">
        <div @click="toastModal = !toastModal" style="position: absolute;top: 2px;right: 4px;cursor: pointer;">X</div>
        <Toast :err=toast></Toast>
    </div>
    <div>
        <select v-model="theater_id" style="width: max-content;" class="form-select m-3"
            aria-label="Default select example">
            <option :value="null" selected>Select Theater</option>
            <option v-for="theater in theaters" :value="theater.id">{{ theater.name }}</option>
        </select>
    </div>
    <div class="overflow-scroll">
        <table ref="table" class="table table-light text-bg-light table-striped">
            <thead>
                <tr>
                    <th scope="col">S.no</th>
                    <th scope="col">Event</th>
                    <th scope="col">Shows Running</th>
                    <th scope="col">Tickets Sold</th>
                    <th scope="col">Ticket Price</th>
                    <th scope="col">Revenue</th>
                    <th scope="col">Capacity</th>
                </tr>
            </thead>
            <tbody v-if="theaters.length > 0 && theater_id">
                <template v-for="theater in theaters" :key="theater.id" v-if="theaters.length > 0">
                    <tr v-if="theater.id == theater_id" :key="event.id" v-for="(event, index) in theater.events">
                        <td class="p-4">{{ index + 1 }}</td>
                        <td class="p-4">{{ event.name }}</td>
                        <td class="p-4">{{ event.shows.length }}</td>
                        <td class="p-4">{{ getCount(event.shows) }}</td>
                        <td class="p-4">₹{{ event.price }}</td>
                        <td class="p-4">₹{{ getCount(event.shows) * event.price }}</td>
                        <td class="p-4">{{ theater.capacity }}</td>
                    </tr>
                </template>
            </tbody>
            <tbody v-else-if="theaters.length > 0 && !theater_id">
                <tr>
                    <td colspan="7" class="text-center">No theaters selected</td>
                </tr>
            </tbody>
            <tbody v-else>
                <tr>
                    <td colspan="7" class="text-center">No theaters found</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import NavBar from "../components/AdminNav.vue"
import Toast from "../components/Toast.vue"
import { ref } from "vue";
export default {
    name: "AdminSummary",
    components: {
        NavBar,
        Toast
    },
    setup() {
        const theaters = ref([]);
        const token = JSON.parse(sessionStorage.getItem("token"));
        const toast = ref("");
        const toastModal = ref(false)
        const theater_id = ref(null)
        const table = ref(null)
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
        const exportData = async () => {
            let id = theater_id.value
            const response = await fetch("http://localhost:5000/export/" + id, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            const data = await response.json();
            if (response.status === 200) {
                console.log(data);
            }
            else {
                toastModal.value = true;
                toast.value = data.err;
                console.log("Something went wrong");
                console.log(data.err);
            }
        }
        const getCount = (shows) => {
            let count = 0;
            for (let show of shows) {
                count += show.tickets.length;
            }
            return count;
        }
        getTheater()

        // class csvExportFromTable {
        //     constructor(table, header = true) {
        //         this.table = table;
        //         this.rows = Array.from(table.querySelectorAll("tr"));
        //         if (!header && this.rows[0].querySelectorAll("th").length) {
        //             this.rows.shift();
        //         }
        //     }

        //     exportCsvFromTable() {
        //         const lines = [];
        //         const ncols = this._longest();
        //         for (const row of this.rows) {
        //             let line = "";
        //             for (let i = 0; i < ncols; i++) {
        //                 if (row.children[i] !== undefined) {
        //                     line += csvExportFromTable.safeData(row.children[i]);
        //                 }
        //                 line += i !== ncols - 1 ? "," : "";
        //             }
        //             lines.push(line);
        //         }
        //         //console.log(lines);
        //         return lines.join("\n");
        //     }
        //     _longest() {
        //         return this.rows.reduce((length, row) => (row.childElementCount > length ? row.childElementCount : length), 0);
        //     }
        //     static safeData(td) {
        //         let data = td.textContent;
        //         //Replace all double quote to two double quotes
        //         data = data.replace(/"/g, `""`);
        //         //Replace , and \n to double quotes
        //         data = /[",\n"]/.test(data) ? `"${data}"` : data;
        //         return data;
        //     }
        // }
        // const CSVDownload = () => {
        //     if (theaters.value.length === 0) {
        //         toastModal.value = true;
        //         toast.value = "No data to download";
        //         return;
        //     }
        //     const tableData = new csvExportFromTable(table.value);
        //     const csvData = tableData.exportCsvFromTable();
        //     const csvBlob = new Blob([csvData], { type: "text/csv" });
        //     const url = URL.createObjectURL(csvBlob);
        //     const a = document.createElement("a");
        //     a.href = url;
        //     a.download = "file.csv";
        //     a.click();
        //     setTimeout(() => {
        //         URL.revokeObjectURL(url);
        //     }, 500);
        // }
        return {
            theaters,
            getCount,
            toast,
            toastModal,
            table,
            theater_id,
            exportData
        }
    }
}
</script>