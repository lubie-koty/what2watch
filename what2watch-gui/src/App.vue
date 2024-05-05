<script setup lang="ts">
import { ref, Ref } from "vue";

import MovieChat from "./components/MovieChat.vue";
import MovieRanking from "./components/MovieRanking.vue";

const plotChatSelected: Ref<boolean> = ref(false);
const numberOfMoviesSelected: Ref<number> = ref(10);
</script>

<template>
  <div class="container">
    <div class="ranking-container card">
      <div>
        <select v-model="numberOfMoviesSelected">
          <option disabled value="">Number of movies:</option>
          <option>10</option>
          <option>25</option>
          <option>50</option>
          <option>100</option>
        </select>
      </div>
      <movie-ranking :number-of-movies="numberOfMoviesSelected" />
    </div>
    <div class="chat-container card">
      <div class="button-container">
        <button
          @click="plotChatSelected = true"
          :class="{ active: plotChatSelected }"
        >
          Plot Chat
        </button>
        <button
          @click="plotChatSelected = false"
          :class="{ active: !plotChatSelected }"
        >
          Detailed Chat
        </button>
      </div>
      <div class="chat">
        <movie-chat :plot-chat-selected="plotChatSelected" />
      </div>
    </div>
    <div class="footer-container">
      <footer>What 2 Watch App</footer>
    </div>
  </div>
</template>

<style scoped>
.container {
  min-width: 50vw;
  min-height: 70vh;
  display: grid;
  grid-template-columns: 30% auto;
  grid-template-rows: 90% auto;
  grid-template-areas:
    "ranking chat"
    "footer footer";
  gap: 1rem;
}

.chat-container {
  grid-area: chat;

  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-container .button-container {
  display: flex;
  flex: 0;
  gap: 0.5rem;
}

.button-container button.active {
  border-color: #ffffff;
}

.chat-container .chat {
  flex: 1;
}

.ranking-container {
  grid-area: ranking;

  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-container {
  grid-area: footer;
}

.footer-container footer {
  text-align: center;
  font-size: 0.8rem;
  color: color-mix(in srgb, currentColor 60%, transparent);
}

.card {
  padding: 1rem;
  transition: 0.3s;
  border: 0.75px solid;
  border-radius: 1rem;
  border-color: #5b5b5b;
  box-shadow: 0 4px 8px 0 #5b5b5b;
  background-color: #5b5b5b;
}

@media (prefers-color-scheme: light) {
  .card {
    border-color: #bfbfbf;
    box-shadow: 0 4px 8px 0 #bfbfbf;
    background-color: #bfbfbf;
  }
}
</style>
