export interface Recommendation {
  title: string;
  vote_count: number;
  vote_average: number;
  score: number;
}

export interface ChatResponse {
  is_successful: boolean;
  error_message?: string;
  data?: string[];
}

export interface ChatMessage {
  isUserMessage: boolean;
  message: string;
}
