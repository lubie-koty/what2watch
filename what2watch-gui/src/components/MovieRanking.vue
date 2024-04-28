<script setup lang="ts">
import { Ref, ref } from 'vue'
import { routes } from '../routes'

const api_key = import.meta.env.VITE_API_KEY

const messages: Ref<string[]> = ref([])
const message: Ref<string> = ref('')
const webSocket: Ref<WebSocket | undefined> = ref()

async function requestRanking() {
    const response = await fetch(routes.simpleRanking, {
        headers: {
            'X-API-KEY': api_key
        }
    })
    
}
</script>

<template>
    
</template>