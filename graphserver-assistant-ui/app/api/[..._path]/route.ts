import { NextRequest, NextResponse } from "next/server";
import CryptoJS from 'crypto-js';

export const runtime = "edge";

function getCorsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "*",
  };
}

function createHeaders(appId: string, appSecret:string, host: string) {
  // 1. 生成 RFC1123 格式的时间戳
  const date = new Date().toUTCString();

  // 2. 拼接签名字符串
  const signatureOrigin = `host: ${host}\ndate: ${date}\n`;

  // 3. HMAC-SHA256 加密
  const hmac = CryptoJS.HmacSHA256(signatureOrigin, appSecret);
  const signatureBase64 = CryptoJS.enc.Base64.stringify(hmac);

  // 4. 构造 Authorization 字段
  const authorization = `hmac api_key=${appId}, algorithm=hmac-sha256, headers=host date request-line, signature=${signatureBase64}`;

  // 5. 返回 headers
  return {
    "X-JZ-AUTHORIZATION": authorization,
    "X-JZ-DATE": date,
    "X-JZ-HOST": host,
    "X-JZ-APPID": appId
  };
}

async function handleRequest(req: NextRequest, method: string) {
  try {
    const path = req.nextUrl.pathname.replace(/^\/?api\//, "");
    const url = new URL(req.url);
    const searchParams = new URLSearchParams(url.search);
    searchParams.delete("_path");
    searchParams.delete("nxtP_path");
    const queryString = searchParams.toString()
      ? `?${searchParams.toString()}`
      : "";

    const options: RequestInit = {
      method,
      headers: {
        "x-api-key": process.env["LANGCHAIN_API_KEY"] || "",
        "Content-Type": "application/json",
        // "authorization": "hmac api_key=74858E5E666E48448CD8, algorithm=hmac-sha256, headers=host date request-line, signature=UP10uUM9Gnj8Ywr6ETyUaRFcTf9XKdF+LNjUo0MfPBg=",
        // "date": "Wed, 09 Jul 2025 08:29:00 GMT",
        // "host": "172.16.251.149",
        // "appId": "74858E5E666E48448CD8"
      },
    };

    const appid = process.env["APPID"] || "";
    const appSecret = process.env["APPSECRET"] || "";
    const host = process.env["LANGGRAPH_API_HOST"] || "";
    const pz_header = createHeaders(appid, appSecret, host);

    if (["POST", "PUT", "PATCH"].includes(method)) {
      options.body = await req.text();
    }

    console.log({ url, path, queryString, options });

    const res = await fetch(
      `${process.env["LANGGRAPH_API_URL"]}/${path}${queryString}`,
      options
    );

    return new NextResponse(res.body, {
      status: res.status,
      statusText: res.statusText,
      headers: {
        ...res.headers,
        // ...getCorsHeaders(),
        ...pz_header
      },
    });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: e.status ?? 500 });
  }
}

export const GET = (req: NextRequest) => handleRequest(req, "GET");
export const POST = (req: NextRequest) => handleRequest(req, "POST");
export const PUT = (req: NextRequest) => handleRequest(req, "PUT");
export const PATCH = (req: NextRequest) => handleRequest(req, "PATCH");
export const DELETE = (req: NextRequest) => handleRequest(req, "DELETE");

// Add a new OPTIONS handler
export const OPTIONS = () => {
  return new NextResponse(null, {
    status: 204,
    headers: {
      ...getCorsHeaders(),
    },
  });
};
