// api/query.js
import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

const OPENAI_KEY = process.env.OPENAI_API_KEY;
const HF_KEY = process.env.HF_TOKEN;
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-4o-mini';

async function queryOpenAI(messages, max_tokens=300){
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ model: OPENAI_MODEL, messages, max_tokens })
  });
  const js = await res.json();
  const choice = js.choices?.[0]?.message?.content ?? js.choices?.[0]?.text ?? '';
  return choice || JSON.stringify(js);
}

async function queryHF(messages, max_tokens=300){
  const res = await fetch('https://router.huggingface.co/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${HF_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ model: process.env.HF_MODEL, messages, max_tokens })
  });
  const js = await res.json();
  const choice = js.choices?.[0]?.message?.content ?? js.choices?.[0]?.text ?? '';
  return choice || JSON.stringify(js);
}

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return res.status(405).json({error:'POST only'});
    const { prompt, context = [], max_tokens = 400 } = await req.json();

    // build messages
    const messages = [{role:'system', content:'You are Niblit, a helpful assistant.'}];
    for (const it of context.slice(-10)) {
      messages.push({ role: it.role || 'user', content: it.text || '' });
    }
    messages.push({role:'user', content: prompt});

    // Prefer OpenAI, fallback HF
    if (OPENAI_KEY) {
      const out = await queryOpenAI(messages, max_tokens);
      return res.json({ response: out });
    } else if (HF_KEY) {
      const out = await queryHF(messages, max_tokens);
      return res.json({ response: out });
    } else {
      // fallback echo + local heuristics
      return res.json({ response: `(No LLM configured) Echo: ${prompt.slice(0,300)}` });
    }

  } catch (err) {
    console.error('query error', err);
    res.status(500).json({ error: String(err) });
  }
}
