from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "你叫小土豆，你说话比较二次元。"},
    {"role": "user", "content": "你是谁"}
  ]
)
print(completion.choices[0].message.content)

