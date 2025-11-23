// api/learn.js
import fetch from 'node-fetch';
import cheerio from 'cheerio';
import dotenv from 'dotenv';
dotenv.config();

const GITHUB_TOKEN = process.env.GITHUB_TOKEN; // optional for persistence
const GITHUB_REPO = process.env.GITHUB_REPO;   // owner/repo
const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'main';
const GITHUB_PATH = process.env.GITHUB_PATH || 'knowledge/knowledge.json';

function extractText(html){
  const $ = cheerio.load(html);
  // remove scripts/styles
  $('script,style,noscript,iframe').remove();
  // pick article/main or fallback to body
  let text = '';
  if ($('article').length) text = $('article').text();
  else if ($('main').length) text = $('main').text();
  else text = $('body').text();
  // compress whitespace
  return text.replace(/\s+/g, ' ').trim().slice(0, 60_000);
}

async function persistToGitHub(knowledgeObj){
  if (!GITHUB_TOKEN || !GITHUB_REPO) return { ok:false, reason:'no_github_config' };
  const api = 'https://api.github.com';
  // get current file sha if exists
  const path = GITHUB_PATH;
  const getUrl = `${api}/repos/${GITHUB_REPO}/contents/${path}?ref=${GITHUB_BRANCH}`;
  let sha = null;
  try {
    const getRes = await fetch(getUrl, {
      headers:{ Authorization: `Bearer ${GITHUB_TOKEN}`, 'User-Agent':'Niblit' }
    });
    if (getRes.ok){
      const js = await getRes.json();
      sha = js.sha;
    }
  } catch(e){
    // ignore
  }

  const putUrl = `${api}/repos/${GITHUB_REPO}/contents/${path}`;
  const content = Buffer.from(JSON.stringify(knowledgeObj, null, 2)).toString('base64');
  const body = {
    message: 'Niblit: update knowledge',
    content,
    branch: GITHUB_BRANCH
  };
  if (sha) body.sha = sha;

  const pushRes = await fetch(putUrl, {
    method: 'PUT',
    headers:{ Authorization:`Bearer ${GITHUB_TOKEN}`, 'User-Agent':'Niblit', 'Content-Type':'application/json' },
    body: JSON.stringify(body)
  });
  const pushJs = await pushRes.json();
  return pushRes.ok ? { ok:true, result:pushJs } : { ok:false, reason:pushJs };
}

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return res.status(405).json({error:'POST only'});
    const { url, metadata = {} } = await req.json();
    if (!url) return res.status(400).json({ error:'missing url' });

    // fetch page
    const r = await fetch(url, { timeout: 15000, headers:{ 'User-Agent':'Niblit/1.0' }});
    if (!r.ok) return res.status(500).json({ error:'fetch_failed', status:r.status });

    const html = await r.text();
    const text = extractText(html);

    // prepare knowledge object entry
    const entry = {
      url,
      title: (/<title>(.*?)<\/title>/i.exec(html) || [null, null])[1] || metadata.title || url,
      ts: new Date().toISOString(),
      snippet: text.slice(0, 2000),
      full: text
    };

    // attempt persistence
    const pers = await persistToGitHub({ entries: [entry] });

    return res.json({ ok:true, entry, persisted: pers });
  } catch (err) {
    console.error('learn error', err);
    res.status(500).json({ error: String(err) });
  }
}
