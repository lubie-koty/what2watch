<script setup lang="ts">
import { Ref, onMounted, ref, watch } from "vue";
import { routes } from "../api-routes";
import { Recommendation } from "../schemas/recommendations";

const props = defineProps<{
  numberOfMovies: Number;
}>();

const apiKey = import.meta.env.VITE_API_KEY;
const apiCallInProgress: Ref<boolean> = ref(false);

const recommendations: Ref<Recommendation[] | undefined> = ref();

async function requestRanking() {
  apiCallInProgress.value = true;
  try {
    const response = await fetch(
      `${routes.simpleRanking}?number_of_movies=${props.numberOfMovies}`,
      {
        headers: {
          "X-API-KEY": apiKey,
        },
      }
    );
    recommendations.value = (await response.json()).recommendations;
  } catch (error) {
    alert(error);
  } finally {
    apiCallInProgress.value = false;
  }
}

onMounted(async () => {
  await requestRanking();
});

watch(
  () => props.numberOfMovies,
  async () => {
    await requestRanking();
  }
);
</script>

<template>
  <div class="ranking-card">
    <div class="header">Top {{ $props.numberOfMovies }} movies:</div>
    <hr />
    <div v-if="apiCallInProgress">
      <div class="loader"></div>
    </div>
    <ul v-else>
      <li v-for="(recommendation, idx) in recommendations">
        <div class="number">{{ idx + 1 }}</div>
        <div class="title">
          {{ recommendation.title }}
        </div>
        <div class="average-vote">{{ recommendation.vote_average }}</div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.ranking-card {
  display: flex;
  flex-direction: column;

  height: 100%;
  max-height: 53vh;
  padding: 1rem;
  transition: 0.3s;

  border: 0.75px solid;
  border-radius: 8px;
  border-color: #1a1a1a;
  background-color: #1a1a1a;
}

.ranking-card .header {
  font-weight: bold;
}

.ranking-card hr {
  width: 100%;
  color: #f9f9f9;
}

.ranking-card ul {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow-y: auto;
  list-style-type: none;
}

.ranking-card li {
  display: flex;
  flex-wrap: wrap;
}

.ranking-card li .number {
  flex: 5%;
  text-align: left;
}

.ranking-card li .title {
  flex: 60%;
  text-align: right;
  padding-right: 0.5em;
  border-right: 1px solid #f9f9f9;
}

.ranking-card li .average-vote {
  flex: 1%;
  text-align: right;
  padding-right: 0.5em;
}

@media (prefers-color-scheme: light) {
  .ranking-card {
    border-color: #f9f9f9;
    background-color: #f9f9f9;
  }

  .ranking-card hr {
    color: #1a1a1a;
  }
  .ranking-card li .title {
    border-right: 1px solid #1a1a1a;
  }
}
</style>
