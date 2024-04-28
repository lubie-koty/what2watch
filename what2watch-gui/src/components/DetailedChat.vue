<script setup lang="ts">
import { Ref, onMounted, ref } from 'vue'
import { routes } from '../routes'

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
    webSocket.value = new WebSocket(routes.detailedChat)
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