// worker.js - روی Cloudflare Workers
export default {
  async fetch(request, env) {
    if (request.method === 'POST') {
      const data = await request.json();
      
      // پردازش پیام‌ها
      if (data.inline_message) {
        const chat_id = data.inline_message.chat_id;
        const text = data.inline_message.text;
        
        // پاسخ به پیام
        await sendMessage(chat_id, `پیام شما: ${text}`);
      }
      
      return new Response(JSON.stringify({status: "ok"}), {
        headers: {'Content-Type': 'application/json'}
      });
    }
    
    return new Response('ربات روبیکا فعال است!');
  }
}

async function sendMessage(chat_id, text) {
  const token = "EGHCC0YBCIFSTJBFFDIQHKNPXHYPPWMTDZQAJXDVEJDEWCSOOQGBCJMASKTHSUEN";
  const url = `https://botapi.rubika.ir/v3/${token}/sendMessage`;
  
  await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({chat_id, text})
  });
}
