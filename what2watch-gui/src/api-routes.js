const apiUri = import.meta.env.VITE_API_URI;

export const routes = {
  plotChat: `${apiUri}/chat/plot`,
  detailedChat: `${apiUri}/chat/detailed`,
  simpleRanking: `${apiUri}/ranking/simple`,
};
