<script setup lang="ts">
import { Ref, onMounted, ref } from 'vue'

const chatURI = import.meta.env.VITE_CHAT_WS_URI
const apiKey = import.meta.env.VITE_API_KEY

const messages: Ref<string[]> = ref([])
const message: Ref<string> = ref('')
const webSocket: Ref<WebSocket | undefined> = ref()

function sendMessage() {
    if (!message.value.trim()) {
        return
    }
    webSocket.value!.send(message.value)
    message.value = ''
}

onMounted(() => {
    webSocket.value = new WebSocket(`${chatURI}?key=${apiKey}`)
    webSocket.value.onmessage = (ev) => {
        messages.value.push(ev.data)
    }
})
</script>

<template>
    <input type="text" v-model="message">
    <button type="button" @click="sendMessage">send</button>
    <br>
    <ul>
        <li v-for="msg in messages">
            {{ msg }}
        </li>
    </ul>
</template>