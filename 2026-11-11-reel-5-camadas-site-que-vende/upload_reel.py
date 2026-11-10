import base64, json, os, sys, urllib.request

env_path = "C:/Users/guilh/AppData/Local/hermes/.env"
api_key = None
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("COMPOSIO_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            break

OWNER = "guimotoyama"
REPO = "GLMstore-Social-CORDIS"
FOLDER = "2026-11-11-reel-5-camadas-site-que-vende"
SRC = "C:/Users/guilh/AppData/Local/hermes/cache/scratch/reel-final"
MCP_URL = "https://connect.composio.dev/mcp"

# files to publish (name -> source path)
ITEMS = [
    ("reel-5-camadas-site-que-vende.mp4", f"{SRC}/reel-5-camadas-site-que-vende.mp4"),
    ("capa-reel.png",                     f"{SRC}/capa-reel.png"),
    ("legenda-e-roteiro.md",              f"{SRC}/legenda.md"),
    ("reel-fonte.html",                   f"{SRC}/reel-fonte.html"),
    ("record_site.js",                   f"{SRC}/record_site.js"),
    ("upload_reel.py",                   f"{SRC}/upload_reel.py"),
]

def mcp_tool_call(tool_name, arguments):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": tool_name, "arguments": arguments}}
    req = urllib.request.Request(MCP_URL, data=json.dumps(payload).encode("utf-8"), headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-consumer-api-key": api_key
    })
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read().decode("utf-8")
    for line in raw.split("\n"):
        if line.startswith("data: "):
            try:
                parsed = json.loads(line[6:])
                if parsed.get("result", {}).get("content"):
                    for item in parsed["result"]["content"]:
                        if item.get("type") == "text":
                            inner = json.loads(item["text"])
                            if inner.get("successful"):
                                data = inner.get("data", {})
                                if isinstance(data, dict) and "results" in data:
                                    try:
                                        return data["results"][0]["response"]["data_preview"]["data"]
                                    except (KeyError, IndexError, TypeError):
                                        pass
                                if isinstance(data, dict) and "data" in data:
                                    return data["data"]
                                return data
                            return inner
                return parsed
            except (json.JSONDecodeError, KeyError):
                continue
    return None

def proxy(endpoint, method, body=None):
    args = {"toolkit_slug": "github", "endpoint": endpoint, "method": method}
    if body:
        args["body"] = body
    return mcp_tool_call("COMPOSIO_PROXY_EXECUTE", args)

# 1. current ref
ref = proxy(f"/repos/{OWNER}/{REPO}/git/ref/heads/main", "GET")
sha_main = ref["object"]["sha"]
print("sha_main:", sha_main)

# 2. base tree
commit = proxy(f"/repos/{OWNER}/{REPO}/git/commits/{sha_main}", "GET")
base_tree = commit["tree"]["sha"]
print("base_tree:", base_tree)

# 3. blobs
blob_shas = {}
for name, path in ITEMS:
    with open(path, "rb") as f:
        content = f.read()
    b64 = base64.b64encode(content).decode("ascii")
    print(f"  blob {name} ({len(content)//1024} KB)...", end=" ", flush=True)
    sha = None
    for attempt in range(4):
        try:
            r = proxy(f"/repos/{OWNER}/{REPO}/git/blobs", "POST", {"content": b64, "encoding": "base64"})
            sha = r.get("sha") if isinstance(r, dict) else None
        except Exception as ex:
            print(f"[retry {attempt+1}: {type(ex).__name__}]", end=" ", flush=True)
            import time as _t; _t.sleep(3 * (attempt + 1))
        if sha:
            break
    if not sha:
        print("FAILED"); print(json.dumps(r, indent=2)[:400]); sys.exit(1)
    blob_shas[name] = sha
    print(sha[:8])

# 4. tree
tree_entries = [{"path": f"{FOLDER}/{n}", "mode": "100644", "type": "blob", "sha": blob_shas[n]} for n, _ in ITEMS]
tree = proxy(f"/repos/{OWNER}/{REPO}/git/trees", "POST", {"base_tree": base_tree, "tree": tree_entries})
tree_sha = tree["sha"]
print("tree_sha:", tree_sha)

# 5. commit
msg = ("Reel: 5 camadas de um site que vende\n\n"
       "Video 9:16 (1080x1920), 31s, 25fps, H.264. Direcao F. Site gravado real "
       "(LP-Advogados) com scroll continuo via Playwright recordVideo. Camadas "
       "sincronizadas com as secoes reais do site: hero, Justitia, arvore, "
       "estrelas, formulario.\n\n"
       "Feito por CORDIS para Agencia GLM Store.")
c = proxy(f"/repos/{OWNER}/{REPO}/git/commits", "POST", {"message": msg, "tree": tree_sha, "parents": [sha_main]})
commit_sha = c["sha"]
print("commit_sha:", commit_sha)

# 6. ref
proxy(f"/repos/{OWNER}/{REPO}/git/refs/heads/main", "PATCH", {"sha": commit_sha, "force": False})
print("ref updated")

with open("C:/Users/guilh/AppData/Local/hermes/cache/scratch/reel_upload.json", "w") as f:
    json.dump({"folder": FOLDER, "commit": commit_sha, "blobs": blob_shas}, f, indent=2)
print("DONE")
