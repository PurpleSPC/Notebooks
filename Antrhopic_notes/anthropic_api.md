# Claude with the Anthropic API

## Anthopic Overview

### Model
#### **Claude Opus**
- most capable model
    - complex requirements
    - high level of intel
    - work for a long time
    - manages multi step process
- supports reasoning
- moderate latency
- higher cost

#### **Claude Sonnet**
- balanced intel speed cost
- most use cases
- fast text gen
- precise edits to complex code
- doesnt break functionality
#### **Haiku**
- optimized for speed and cost
- fastest model
- doesn't support reasoning
- quick code completes
- real time interacts

### How to choose
- need to choose based on needs: Intelligence vs Speed vs Cost (Good Fast Cheap pick 2)
- can use any or all 3 models in the same app
  - use haiku for user facing
  - sonnet for main logic
  - opus for deeper reasoning

## Accessing Claude via the API
### **5 steps from prompt to response**
1. Request to server
- requests should not be made directly from client code
- api key must remain secret
- client requests are processed through a server the developer implements
2. Request to anthropic api
- requests go through an SDK or plain HTTP request
- Includes API key, Model, Messages, Max Tokens
3. model processing
- tokenization - breaks up sentences and words to tokens
- embedding - a vector representation of each token
- contextualization - adjusts embeddings based on its neighbors
- generation - final embeddings to an output layer that predicts probabilities of the next word
  - stops when max tokens is reached
  - stops when EOS (natural end) of a response
4. response to server
- response passed back through SDK and developer server
  - contains
    - message
    - usage
    - stop reason
5. response to client
- response passed back to the client

### Basic API requests

### Multi Turn Conversations
- the API does not store any messages
- to have a conversation:
  - manually maintain a list of messages in the conversation
  - provide that list with each new propmpt

## Prompt evaluations 

## Prompt engineering

## Tool Use

## Retrieval Augmented Generation

## Features of Claude

## Model Context Protocol

## Anthropic apps 

### Claude Code

### Computer use

## Agents and workflows