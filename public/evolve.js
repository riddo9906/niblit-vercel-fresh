// public/evolve.js
let autoTimer = null;

const autoIntervalInput = document.getElementById('autoInterval');
const startAutoBtn = document.getElementById('startAuto');
const stopAutoBtn = document.getElementById('stopAuto');

async function doAutoLearn(){
  // simple strategy: use Google "site:en.wikipedia.org self evolving AI" as example
  const query = localStorage.getItem('niblit_auto_query') || 'site:en.wikipedia.org artificial intelligence';
  try {
    // Use DuckDuckGo HTML search or a simple SERP provider that permits scraping.
    // For simplicity, attempt the Wikipedia landing page for "Artificial intelligence"
    const url = 'https://en.wikipedia.org/wiki/Artificial_intelligence';
    const r = await fetch('/api/learn', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ url }) });
    const js = await r.json();
    if (js.ok){
      // store locally (frontend)
      const learned = JSON.parse(localStorage.getItem('niblit_learned') || '[]');
      learned.unshift({ url: js.entry.url, title: js.entry.title, ts: js.entry.ts });
      localStorage.setItem('niblit_learned', JSON.stringify(learned));
      document.getElementById('learnCount').textContent = learned.length;
      document.getElementById('lastLearn').textContent = js.entry.ts;
    }
    console.log('auto learn', js);
  } catch(e){
    console.warn('auto learn failed', e);
  }
}

startAutoBtn.addEventListener('click', ()=> {
  const s = Number(autoIntervalInput.value || 0);
  if (!s || s < 5) return alert('Set interval (seconds). Minimum 5s recommended for testing.');
  if (autoTimer) clearInterval(autoTimer);
  autoTimer = setInterval(doAutoLearn, s*1000);
  doAutoLearn();
});

stopAutoBtn.addEventListener('click', ()=> {
  if (autoTimer) clearInterval(autoTimer);
  autoTimer = null;
});

window.addEventListener('beforeunload', ()=> {
  if (autoTimer) clearInterval(autoTimer);
});
