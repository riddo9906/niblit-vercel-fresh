// api/index.js
export default async function handler(req, res) {
  res.setHeader('content-type','application/json');
  res.end(JSON.stringify({
    name: 'Niblit Web API',
    version: '1.0',
    uptime: Date.now()
  }));
}
