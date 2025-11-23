// public/chat.js
const dom = {
  chatBox: document.getElementById('chatBox'),
  prompt: document.getElementById('prompt'),
  sendBtn: document.getElementById('sendBtn'),
  msgCount: document.getElementById('msgCount'),
  kb: document.getElementById('kb'),
  saveKb: document.getElementById('saveKb'),
  clearKb: document.getElementById('clearKb'),
  learnUrl: document.getElementById('learnUrl'),
  learnUrlBtn: document.getElementById('learnUrlBtn'),
  learnCount: document.getElementById('learnCount'),
  lastLearn: document.getElementById('lastLearn'),
  status: document.getElementById('status'),
  uptime: document.getElementById('uptime'),
  bgFile: document.getElementById('bgFile'),
  bgBtn: document.getElementById('bgBtn')
};

let state = {
  messages: JSON.parse(localStorage.getItem('niblit_messages')||'[]'),
  kb: localStorage.getItem('niblit_kb') || '',
  learned: JSON.parse(localStorage.getItem('niblit_learned')||'[]'),
  startTs: Date.now()
};

function renderMessages(){
  dom.chatBox.innerHTML = '';
  state.messages.forEach(m=>{
    const el = document.createElement('div');
    el.className = 'msg ' + (m.role==='user' ? 'user' : 'bot');
    el.textContent = m.text;
    dom.chatBox.appendChild(el);
  });
  dom.chatBox.scrollTop = dom.chatBox.scrollHeight;
  dom.msgCount.textContent = state.messages.length;
}

function setStatus(s){ dom.status.textContent = 'Status: '+s; }

async function sendPrompt(text){
  if (!text) return;
  state.messages.push({ role:'user', text });
  saveState();
  renderMessages();
  setStatus('querying...');
  try {
    const resp = await fetch('/api/query', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ prompt:text, context: state.messages }) });
    const js = await resp.json();
    const reply = js.response || js.error || '(no response)';
    state.messages.push({ role:'assistant', text: reply });
    saveState();
    renderMessages();
    setStatus('idle');
  } catch(e){
    console.error(e);
    state.messages.push({ role:'assistant', text: 'Error: '+e.message });
    saveState(); renderMessages(); setStatus('error');
  }
}

function saveState(){
  localStorage.setItem('niblit_messages', JSON.stringify(state.messages.slice(-200)));
  localStorage.setItem('niblit_kb', dom.kb.value);
  localStorage.setItem('niblit_learned', JSON.stringify(state.learned));
  dom.learnCount.textContent = state.learned.length;
  dom.lastLearn.textContent = (state.learned[0]?.ts || 'never');
}

dom.sendBtn.addEventListener('click', ()=> {
  const t = dom.prompt.value.trim(); dom.prompt.value='';
  sendPrompt(t);
});

dom.prompt.addEventListener('keydown', e=> {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); dom.sendBtn.click(); }
});

dom.saveKb.addEventListener('click', ()=>{
  state.kb = dom.kb.value;
  saveState();
  setStatus('KB saved locally');
});

dom.clearKb.addEventListener('click', ()=>{
  dom.kb.value = ''; state.kb=''; saveState();
  setStatus('KB cleared');
});

dom.learnUrlBtn.addEventListener('click', async ()=>{
  const url = dom.learnUrl.value.trim();
  if (!url) return alert('Enter URL');
  setStatus('learning from url...');
  try {
    const r = await fetch('/api/learn', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ url }) });
    const js = await r.json();
    if (js.ok) {
      state.learned.unshift({ url: js.entry.url, title: js.entry.title, ts: js.entry.ts });
      saveState();
      setStatus('learned OK');
      dom.learnUrl.value = '';
    } else {
      setStatus('learn error');
      console.warn(js);
      alert('Learn failed: '+JSON.stringify(js));
    }
  } catch (e) {
    console.error(e); setStatus('learn error'); alert(e.message);
  }
});

dom.bgBtn.addEventListener('click', ()=> dom.bgFile.click());
dom.bgFile.addEventListener('change', e=>{
  const f = e.target.files?.[0];
  if (!f) return;
  const r = new FileReader();
  r.onload = ()=> {
    document.body.style.backgroundImage = `url(${r.result})`;
    localStorage.setItem('niblit_bg', r.result);
  };
  r.readAsDataURL(f);
});

function init(){
  if (localStorage.getItem('niblit_bg')) document.body.style.backgroundImage = `url(${localStorage.getItem('niblit_bg')})`;
  dom.kb.value = state.kb || '';
  renderMessages();
  saveState();
  setInterval(()=> {
    const s = Math.floor((Date.now()-state.startTs)/1000);
    dom.uptime.textContent = `Uptime: ${s}s`;
  }, 1000);
}

init();
