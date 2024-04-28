const chat_uri = import.meta.env.VITE_CHAT_WS_URI
const api_uri = import.meta.env.VITE_API_URI
const api_key = import.meta.env.VITE_API_KEY

export const routes = {
    plotChat: `${chat_uri}/plot?key=${api_key}`,
    detailedChat: `${chat_uri}/detailed?key=${api_key}`,
    simpleRanking: `${api_uri}/ranking/simple`
}