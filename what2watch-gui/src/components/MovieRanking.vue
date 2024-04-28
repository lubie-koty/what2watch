<script setup lang="ts">
import { Ref, onMounted, ref } from 'vue'
import { routes } from '../routes'
import { Recommendation } from '../schemas/recommendations' 

const apiKey = import.meta.env.VITE_API_KEY

const recommendations: Ref<Recommendation[] | undefined> = ref()

async function requestRanking() {
    const response = await fetch(
        `${routes.simpleRanking}?number_of_movies=4`,
        {
            headers: {
                'X-API-KEY': apiKey
            }
        }
    )
    const data = await response.json()
    recommendations.value = data.recommendations
}

onMounted(async () => {
    await requestRanking()
})
</script>

<template>
<div v-for="(recommendation, index) in recommendations">
    {{index}} - {{ recommendation.title }}
</div>
</template>

<style scoped>

</style>
