import backoff  # for exponential backoff
import groq
from retrying import retry
import logging

client = groq.Client()

@backoff.on_exception(
        backoff.expo, 
        (groq.RateLimitError, groq.APIConnectionError),
        max_time = 30,
        on_backoff=lambda details: logging.warning(
            f"Retrying due to {details['exception']} (attempt {details['tries']})"
    ))
def chat_completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)


class GroqModel:
    def __init__(self, model_name, stop_words, max_new_tokens) -> None:
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.stop_words = stop_words
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def chat_generate(self, input_string, temperature = 0.0):
        response = chat_completions_with_backoff(
                model = self.model_name,
                messages=[
                        {"role": "system", "content": "You are a helpful assistant. Make sure you carefully and fully understand the details of user's requirements before you start solving the problem."},
                        {"role": "user", "content": input_string}
                    ],
                temperature = temperature,
                top_p = 1,
                stop = self.stop_words
        )
        generated_text = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        return generated_text, finish_reason

    def generate(self, input_string, temperature = 0.0):
        print("model_name: ", self.model_name)
        if self.model_name in ['deepseek-r1-distill-llama-70b', 'gpt-3.5-turbo']:
            return self.chat_generate(input_string, temperature)
        else:
            raise Exception("Model name not recognized")