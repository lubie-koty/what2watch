<script setup lang="ts">
import { Ref, onMounted, ref } from "vue";
import { routes } from "../api-routes";
import { ChatMessage, ChatResponse } from "../schemas/recommendations";

const props = defineProps<{
  plotChatSelected: boolean;
}>();

const apiKey = import.meta.env.VITE_API_KEY;
const apiCallInProgress: Ref<boolean> = ref(false);

const messages: Ref<ChatMessage[]> = ref([]);
const userInput: Ref<string> = ref("");

function handleApiMessage(response: ChatResponse) {
  if (response.is_successful) {
    messages.value.push({
      isUserMessage: false,
      message: `Movie recommendations for "${
        userInput.value
      }":\n${response.data!.join("\n")}`,
    });
  } else {
    messages.value.push({
      isUserMessage: false,
      message: response.error_message!,
    });
  }
  userInput.value = '';
}

function getChatRequestPromise(route: string) {
  return fetch(
    `${route}?movie_title=${userInput.value}`,
    {
      headers: {
        "X-API-KEY": apiKey,
      },
    }
  );
}

async function requestRecommendations() {
  messages.value.push({
    isUserMessage: true,
    message: userInput.value
  })

  let chatPromise: Promise<Response>;
  if (props.plotChatSelected) {
    chatPromise = getChatRequestPromise(routes.plotChat);
  } else {
    chatPromise = getChatRequestPromise(routes.detailedChat);
  }

  apiCallInProgress.value = true;
  try {
    const response = await chatPromise;
    handleApiMessage((await response.json()) as ChatResponse);
  } catch (error) {
    alert(error);
  } finally {
    apiCallInProgress.value = false;
  }
}

onMounted(() => {
  messages.value.push({
    isUserMessage: false,
    message: 'Hello, how can I help you today?'
  })
})
</script>

<template>
  <div class="chat-card">
    <div class="chat-box">
      <div
        v-for="message in messages"
        class="message"
        :class="{darker: message.isUserMessage}"
      >
        {{ message.message }}
      </div>
    </div>
    <form class="input-box" @submit.prevent="requestRecommendations">
      <div class="input">
        <div class="loader" v-if="apiCallInProgress"></div>
        <input
          v-else
          v-model="userInput"
        >
        </input>
      </div>
      <button
        type="submit"
        :disabled="apiCallInProgress"
      >
        <span class="material-symbols-outlined">
          send
        </span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.chat-card {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: 90% 10%;
  grid-template-areas:
    "chat"
    "input";

  height: 100%;
  max-height: 53vh;
  padding: 1rem;
  transition: 0.3s;

  border: 0.75px solid;
  border-radius: 8px;
  border-color: #1a1a1a;
  background-color: #1a1a1a;
}

.chat-box {
  grid-area: chat;

  display: flex;
  flex-direction: column;
  gap: 0.5em;
  overflow-y: auto;
}

.input-box {
  grid-area: input;

  display: flex;
  flex: 1;
}

.input-box .input {
  flex: 1 0 90%;
  align-self: center;
}

.input-box .input input {
  font-family: inherit;
  font-size: inherit;
  width: 98%;
  vertical-align: bottom;
  resize: none;
  outline: none;
  border: none;
  border-bottom: 1px solid #dedede;
  background-color: inherit;
}

.input-box button {
  border: none;
}

.message {
  margin-right: 1em;
  width: min-content;
  border: none;
  background-color: #535353;
  border-radius: 5px;
  padding: 10px;
  color: rgba(255, 255, 255, 0.9);
  white-space: pre;
}

.message.darker {
  align-self: end;
  text-align: right;
  background-color: #313131;
  color: rgba(255, 255, 255, 0.5);
}

@media (prefers-color-scheme: light) {
  .chat-card {
    border-color: #f9f9f9;
    background-color: #f9f9f9;
  }

  .chat-card hr {
    color: #1a1a1a;
  }
}
</style>
