# **working with OpenAI API**
## **basic request format:**
```Python
    from openai import OpenAI

    client = OpenAI(api_key="ENTER KEY HERE")
    
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_completion_tokens=100,
  
    # Enter your prompt
    messages=[{"role": "user", "content": "INSERT YOUR PROMPT HERE"}]
)

print(response.choices[0].message.content)
```
## **Text editing**
```Python
prompt = """
upate name to Ragnar, pronouns to lord/master, and job title to Senior Dragon Slayer in the following text:

Joanne is a content developer at datacamp. Her favorite programming language is R, which she uses for statistical analysis.
"""

response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [{'role': 'user', 'content': prompt}]
)

print(response.choices[0].message.content)
```
## **Text Summarization**
```Python
text = """
Customer: Hi, I'm trying to log into my account, but it keeps saying my password is incorrect. I'm sure I'm entering the right one.

Support: I'm sorry to hear that! Have you tried resetting your password?
...
"""

prompt = f"""Summarize the customer support chat in three concise key point: {text}"""
```

## **Calculating cost of using the API**
    - charged by token.
    - tokens are the individual units that the prompt is made of
    - ![alt text](image.png)
```python
# define price per token
input_token_price = 0.15 / 1_000_000   # tokens sold by the million
output_token_price = 0.6 / 1_000_000

# extract token usage
input_tokens = response.usage.prompt_tokens
output_tokens = max_completion_tokens

# calculate cost
cost = (input_tokens * input_token_price + output_tokens * output_token_price)

print(f"estimated cost: ${cost}")
```

## **Text Generation**
#### **Temperature** parameter: 
- a value between 0(deterministic) and 2(random) that controls the 'randomness' and 'ceativity' of the response. 

#### **Marketing Uses**
    - example: creating a tagline for a new electric vehicle
    - 'temperature' and 'max_tokens' can be tweaked to experiment with results.

#### **Product Descriptions**
    - example: "write a compelling descriptions for the 'widget'. Highlight its key features: a,b,c and d. Use a persuasive and engaging tone to appeal to fitness enthusiasts and busy professionals."

```python
# Create a request to the Chat Completions endpoint to create a slogan for a new restaurant
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": "Create a slogan for a new italian restaurant named Stinky's. Highlight our specials: stinky cheese, stinky meat, and stinky bread. use a persuasive and engaging tone to appeal to overweight housewives and alcohoic accountants"}],
  max_completion_tokens = 100
)

print(response.choices[0].message.content)
```

```python
# Create a detailed prompt to generate a product description for SonicPro headphones, including:
# Active noise cancellation (ANC)
# 40-hour battery life
# Foldable design
prompt = """
create a product description for the SonicPro headphones. Highlight the key features: Active noise cancellation (ANC), 40-hour battery life and Foldable design. Use a persuasive tone to appeal to middle aged irish men.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    # Experiment with max_completion_tokens and temperature settings
    max_completion_tokens=100,
    temperature=0.2
)

print(response.choices[0].message.content)
```
## **Shot prompting**
 - refers to adding examples of results to a prompt
```python
prompt = """
Classify the following animals as Land, Sea or Both:
1. Zebra = Land
2. Crocodile = Both
3. Blue Whale =
4. Polar Bear = 
5. Salmon = 
6. Dog = 
"""
```


Practice:
```python
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define a multi-line prompt to classify sentiment
prompt = """create a rating from 1-5(positive to negative) based on these reviews:
1. Unbelievably good! = 1
2. Shoes fell apart on the second use. = 5
3. The shoes look nice, but they aren't very comfortable. =
4. Can't wait to show them off! = """

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": prompt}],
  max_completion_tokens=100
)

print(response.choices[0].message.content)
```


```python
# Add the example to the prompt
prompt = """Classify sentiment as 1-5 (negative to positive):
1. Love these! =5
2. Unbelievably good! =
3. Shoes fell apart on the second use. =
4. The shoes look nice, but they aren't very comfortable. =
5. Can't wait to show them off! =
"""
response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_completion_tokens=100)
print(response.choices[0].message.content)
```

## **Chat Roles**
### **System Role**
    - controls the assistant's behavior
    - gives the model instructions on how the assistant should respond
```python
response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {'role': 'system',
        'content': "You are a python programming tutor who speaks concisely."},
        {'role': 'user',
        'content': 'What is the difference between mutable and immutable objects?'}
    ]
)
```
    - **system message:** guardrails and restrictions on model output
```python
sys_msg = """
You are finance education assistant that helps students study for exams.
If you are asked for specific, real-world financial advice with risk to their finances, respond with:
I'm sorry, I am not allowed to provide financial advice
"""

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {'role': 'system',
        'content': sys_msg},
        {'role': 'user',
        'content': 'Which stocks should I buy?'}
    ]
)

print(response.choices[0].message.content)
```

### **User Role**
    - gives the prompt to the assistant
### **Assistant Role**
    - response to user instruction
    - can also be written by the developer as example responses.
      - user/assistant pairs
### **Which role to use when adding examples and context?**
    - system- important template formatting or specific responses to return (guardrails)
    - Assistant - example converstaions for multi-turn tasks
    - User - context required for the new input, usually single turn

## **Multi-turn conversations**
ChatGPT and other chatbots use the user/assistant content pairs to feed back into the model for a conversation

```python
messages = [{'role':'system', 'content': 'you are a data science tutor who provides short, simple explanations'}]

user_qs = ["Why is python so popular?", "summarize this in one sentence"]

for q in user_qs:
    print('User: ' , q)
    user_dict = {'role': 'user', 'content': q}
    messages.append(user_dict)

    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = messages
    )

    assistant_dict = {'role': 'assistant', 'content': response.choices[0].message.content}
    messages.append(assistant_dict)
    print('Assistant: ', response.choices[0].message.content, "\n")
```