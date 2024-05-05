<script setup lang="ts">
import { Ref, computed, onMounted, ref } from "vue";
import { routes } from "../api-routes";
import { ChatMessage, ChatResponse } from "../schemas/recommendations";

const props = defineProps<{
  plotChatSelected: boolean;
}>();

const apiKey = import.meta.env.VITE_API_KEY;
const apiCallInProgress: Ref<boolean> = ref(false);

const messages: Ref<ChatMessage[]> = ref([]);
const message: Ref<string> = ref("");

const chatTitle = computed(() => {
  return `Current chat: ${props.plotChatSelected ? "Plot" : "Detailed"}`;
});

function handleApiMessage(response: ChatResponse) {
  if (response.is_successful) {
    messages.value.push({
      isUserMessage: false,
      message: `Movie recommendations for ${
        message.value
      }:\n${response.data!.join("\n")}`,
    });
  } else {
    messages.value.push({
      isUserMessage: false,
      message: response.error_message!,
    });
  }
}

async function requestPlotRecommendations() {
  apiCallInProgress.value = true;
  try {
    const response = await fetch(
      `${routes.plotChat}?movie_title=${message.value}`,
      {
        headers: {
          "X-API-KEY": apiKey,
        },
      }
    );
    handleApiMessage((await response.json()) as ChatResponse);
  } catch (error) {
    alert(error);
  } finally {
    apiCallInProgress.value = false;
  }
}

async function requestDetailedRecommendations() {
  apiCallInProgress.value = true;
  try {
    const response = await fetch(
      `${routes.detailedChat}?movie_title=${message.value}`,
      {
        headers: {
          "X-API-KEY": apiKey,
        },
      }
    );
    handleApiMessage((await response.json()) as ChatResponse);
  } catch (error) {
    alert(error);
  } finally {
    apiCallInProgress.value = false;
  }
}

async function requestRecommendations() {
  if (props.plotChatSelected) {
    await requestPlotRecommendations();
  } else {
    await requestDetailedRecommendations();
  }
}
</script>

<template>
  <div class="chat-card">
    <div class="chat-box"></div>
    <div class="input-box">
      <div class="input">
        <textarea></textarea>
      </div>
      <button><span class="material-symbols-outlined"> send </span></button>
    </div>
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

.input-box .input textarea {
  width: 90%;
  height: 100%;
}

.input-box button {
  border-color: #fff;
  border-radius: 50%;
}

.message {
  border: 2px solid #dedede;
  background-color: #f1f1f1;
  border-radius: 5px;
  padding: 10px;
  margin: 10px 0;
}

.darker {
  text-align: right;
  border-color: #ccc;
  background-color: #ddd;
}

.message::after {
  content: "";
  clear: both;
  display: table;
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
