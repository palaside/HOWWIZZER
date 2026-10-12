// src/lib/apiMiddleware.js
export async function submitCommand(payload) {
  const response = await fetch('/api/execute', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Command failed: ${err}`);
  }
  return response.json();
}
