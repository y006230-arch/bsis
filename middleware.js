const PUBLIC = [
  /^\/dashboard\/?$/,
  /^\/api\/login$/,
  /^\/api\/logout$/,
  /^\/assets\//,
  /^\/favicon\.ico$/,
];

function getClientIp(request) {
  const xf = request.headers.get('x-forwarded-for');
  if (xf) return xf.split(',')[0].trim();
  const real = request.headers.get('x-real-ip');
  if (real) return real.trim();
  return '';
}

function getSecret() {
  return process.env.AUTH_SECRET || '';
}

function b64urlToJson(payload) {
  const pad = payload.length % 4 === 0 ? '' : '='.repeat(4 - (payload.length % 4));
  const b64 = payload.replace(/-/g, '+').replace(/_/g, '/') + pad;
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return JSON.parse(new TextDecoder().decode(bytes));
}

function bufToB64url(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function hmacVerify(payload, sig, secret) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const mac = await crypto.subtle.sign('HMAC', key, enc.encode(payload));
  return bufToB64url(mac) === sig;
}

async function verifySession(request) {
  const secret = getSecret();
  if (!secret) return false;

  const cookie = request.headers.get('cookie') || '';
  const match = cookie.match(/(?:^|;\s*)bsis_auth=([^;]+)/);
  if (!match) return false;

  const token = decodeURIComponent(match[1]);
  const dot = token.indexOf('.');
  if (dot < 0) return false;

  const payload = token.slice(0, dot);
  const sig = token.slice(dot + 1);

  try {
    if (!(await hmacVerify(payload, sig, secret))) return false;
    const data = b64urlToJson(payload);
    if (!data.exp || Date.now() > data.exp) return false;
    const ip = getClientIp(request);
    if (data.ip && ip && data.ip !== ip) return false;
    return true;
  } catch {
    return false;
  }
}

export default async function middleware(request) {
  const path = new URL(request.url).pathname;

  if (PUBLIC.some((re) => re.test(path))) {
    return;
  }

  if (await verifySession(request)) {
    return;
  }

  if (path.startsWith('/api/')) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return Response.redirect(new URL('/dashboard', request.url));
}

export const config = {
  matcher: ['/((?!_next/static|_next/image).*)'],
};
