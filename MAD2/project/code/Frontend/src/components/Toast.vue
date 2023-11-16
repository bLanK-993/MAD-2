<script setup>
import { defineProps } from 'vue';
defineProps({
    err:{
        type:String,
        default:''
    }
})
</script>


<template>
    <div v-if="err">
        {{err}}
    </div>
</template>