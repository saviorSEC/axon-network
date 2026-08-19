#!/usr/bin/env python3
"""Build AXON internal-network galaxy (flock-globe style, 3d-force-graph)."""
import json, pathlib

GAL = json.load(open("/root/.openclaw/workspace/AXON/galaxy/data.json"))
S = {s["id"]: dict(s) for s in GAL["services"]}

# ---------- zones (planets) ----------
zones = [
 {"id":"z-core","name":"CORE // EVIDENCE.COM","color":"#00e5ff",
  "note":"Azure Boydton VA (52.227.0.0/16) — istio-envoy mesh. Portal SPA, API gateway, upload plane, admin."},
 {"id":"z-identity","name":"IDENTITY // OIDC SSO","color":"#7c5cff",
  "note":"Self-hosted OAuth2/OIDC at id.evidence.com + auth/sso/login gateways. Device flow enabled."},
 {"id":"z-commander","name":"COMMANDER // TENANT FLEET","color":"#4ade80",
  "note":"80+ live *.commander.evidence.com hosts — German states (bayern/brandenburg/bw), region codes (aprbue/man/pfo), body-cam clusters bdc242-260+, aw1/aw2."},
 {"id":"z-devops","name":"DEVOPS // INTERNAL TOOLS","color":"#ff3d81",
  "note":"jenkins/jira/vault/grafana/k8s/consul — all SSO-gated behind evidence.com wildcard."},
 {"id":"z-corp","name":"CORPORATE // AXON.COM","color":"#ffb020",
  "note":"Marketing (Vercel/Cloudflare), help (CloudFront), Salesforce (my.axon.com), staging, GlobalProtect VPN, IoT enterprise API, public static S3."},
 {"id":"z-dedrone","name":"DEDRONE // C2 · API · DEV","color":"#ff9de2",
  "note":"Counter-drone (acquired). C2 console, OIDC auth, Tomcat APIs, internal GitLab exposed, Quarkus dev API, Icinga, dev S3, city-dev tenant cluster."},
 {"id":"z-acquired","name":"ACQUIRED // FUSUS · CARBYNE","color":"#ffd166",
  "note":"Fusus RTCC (EUR Dublin + DE Frankfurt clusters, Zoho-hosted portals), Carbyne 911 (independent WordPress on Cloudflare)."},
 {"id":"z-ecosystem","name":"ECOSYSTEM // DATA PARTNERS","color":"#60a5fa",
  "note":"Flock (ALPR feed), 3Si (GPS/DTD), RapidSOS (911 EDX). Cross-company data-sharing."},
 {"id":"z-thirdparty","name":"THIRD-PARTY INFRA","color":"#94a3b8",
  "note":"Salesforce Experience Cloud, Proofpoint MX, Cloudflare CDN, Route53, AWS/Azure hosting."},
]

# ---------- services (satellites) ----------
def svc(sid, zone, name=None, role=None, note=None, dns=None, endpoints=None, keys=None, cert=None):
    s = S.get(sid, {"id": sid, "name": sid})
    return {"id": sid, "name": name or s.get("name", sid), "zone": zone,
            "role": role or s.get("role", ""), "note": note or s.get("note", ""),
            "dns": dns if dns is not None else s.get("dns", []),
            "endpoints": endpoints if endpoints is not None else s.get("endpoints", []),
            "keys": keys if keys is not None else s.get("keys", []),
            "cert": cert or s.get("cert")}

services = [
 # core
 svc("s-evidence-main","z-core", cert="*.evidence.com (wildcard)"),
 svc("s-evidence-api","z-core"),
 svc("s-evidence-upload","z-core"),
 svc("s-evidence-admin","z-core"),
 svc("s-evidence-status","z-core"),
 svc("s-evidence-docs","z-core"),
 svc("s-evidence-dev","z-core"),
 svc("s-evidence-mail","z-core"),
 svc("s-evidence-local","z-core"),
 svc("s-evidence-regions","z-core"),
 # identity
 svc("s-evidence-id","z-identity"),
 svc("s-evidence-auth","z-identity"),
 svc("s-evidence-login","z-identity"),
 # commander tenants
 {"id":"s-commander","name":"commander.evidence.com (80+ hosts)","zone":"z-commander",
  "role":"REGIONAL TENANT FLEET","note":"istio-envoy 'Sign In - Axon' on 80+ live hosts. Regional/tenant-per-host deployment of Axon Commander.",
  "dns":[],"endpoints":["/"],"keys":[],"cert":"*.commander.evidence.com"},
 {"id":"s-commander-de","name":"bayern · brandenburg · bw · bc.bayern","zone":"z-commander",
  "role":"GERMAN STATE TENANTS","note":"German state deployments — Bavaria, Brandenburg, Baden-Württemberg.",
  "dns":[],"endpoints":[],"keys":[]},
 {"id":"s-commander-bdc","name":"bdc242 … bdc260+","zone":"z-commander",
  "role":"BODY-CAM CLUSTERS","note":"Body-camera data center clusters — sequential hostnames suggest per-agency/region provisioning.",
  "dns":[],"endpoints":[],"keys":[]},
 {"id":"s-commander-regions","name":"aprbue01 · aprman01 · aprpfo01 · aw1 · aw2 · pm-pp","zone":"z-commander",
  "role":"REGION-CODE TENANTS","note":"Region/zone code hosts (bue/man/pfo = ?), aw1/aw2 (Asia-Pacific?), commander-pm-pp (project management?).",
  "dns":[],"endpoints":[],"keys":[]},
 # devops
 svc("s-jenkins","z-devops"),
 svc("s-devops-tools","z-devops"),
 svc("s-devops-secrets","z-devops"),
 svc("s-devops-mesh","z-devops"),
 svc("s-devops-data","z-devops"),
 svc("s-devops-other","z-devops"),
 # corporate
 svc("s-www","z-corp"),
 svc("s-help","z-corp"),
 svc("s-community","z-corp"),
 svc("s-my","z-corp"),
 svc("s-stage","z-corp"),
 svc("s-vpn","z-corp", cert="SAN: www.vpn.axon.com"),
 svc("s-academy","z-corp"),
 svc("s-iot","z-corp"),
 svc("s-s3-static","z-corp"),
 # dedrone
 svc("s-dedrone","z-dedrone"),
 svc("s-dedrone-c2","z-dedrone"),
 svc("s-dedrone-api","z-dedrone"),
 svc("s-dedrone-gitlab","z-dedrone"),
 svc("s-dedrone-quarkus","z-dedrone"),
 svc("s-dedrone-icinga","z-dedrone"),
 svc("s-dedrone-s3","z-dedrone"),
 svc("s-dedrone-soc","z-dedrone"),
 svc("s-dedrone-adsb","z-dedrone"),
 # acquired
 svc("s-fusus","z-acquired"),
 svc("s-fusus-eur","z-acquired"),
 svc("s-fusus-de","z-acquired"),
 svc("s-fusus-assist","z-acquired"),
 svc("s-carbyne","z-acquired"),
 # ecosystem
 svc("s-flock","z-ecosystem"),
 svc("s-3si","z-ecosystem"),
 svc("s-rapidsos","z-ecosystem", keys=["REDACTED — sandbox token in private notes"]),
 # third-party
 svc("s-salesforce","z-thirdparty"),
 svc("s-proofpoint","z-thirdparty"),
 svc("s-cloudflare","z-thirdparty"),
 svc("s-azure","z-thirdparty"),
 svc("s-aws","z-thirdparty"),
]

# ---------- ip pools ----------
ipPools = [
 {"id":"i-azure-va","name":"Azure US East // Boydton VA 52.227.0.0/16","zone":"z-core",
  "role":"evidence.com core + commander fleet + upload plane", "ips":["52.227.251.93","52.227.251.71","52.227.173.38","52.227.180.79","52.227.251.98","52.227.251.121"]},
 {"id":"i-aws-eu-central-1","name":"AWS eu-central-1 // Frankfurt","zone":"z-dedrone",
  "role":"Dedrone APIs + Fusus DE", "ips":["52.59.102.12","35.158.156.140"]},
 {"id":"i-aws-eu-west-1","name":"AWS eu-west-1 // Dublin","zone":"z-acquired",
  "role":"Fusus EUR cluster", "ips":["108.129.17.7"]},
 {"id":"i-aws-us-west-2","name":"AWS us-west-2 // Boardman + Seattle","zone":"z-corp",
  "role":"stage.axon.com, c2.dedrone.com, RapidSOS sandbox", "ips":["54.148.215.143","75.2.90.23","40.38.188.121"]},
 {"id":"i-aws-us-east-2","name":"AWS us-east-2 // Columbus","zone":"z-corp",
  "role":"my.axon.com (Salesforce Experience Cloud)", "ips":["3.146.43.227"]},
 {"id":"i-aws-us-east-1","name":"AWS us-east-1 // Reston","zone":"z-corp",
  "role":"IoT enterprise API", "ips":["64.40.137.234"]},
 {"id":"i-ironmountain","name":"Iron Mountain // Scottsdale AS12025","zone":"z-corp",
  "role":"vpn.axon.com — Palo Alto GlobalProtect", "ips":["74.206.96.236"]},
 {"id":"i-zoho","name":"Zoho // Seattle AS2639","zone":"z-acquired",
  "role":"Fusus assist/cliq/connect portals", "ips":["136.143.189.127"]},
 {"id":"i-qts","name":"QTS // San Jose AS17018","zone":"z-ecosystem",
  "role":"3Si DTD portal", "ips":["65.74.157.197"]},
]

# ---------- links ----------
links = [[s["id"], s["zone"]] for s in services]
links += [[p["id"], p["zone"]] for p in ipPools]
links += [
 # data streams / cross-connections
 ["s-evidence-main","s-evidence-id"],
 ["s-evidence-login","s-evidence-id"],
 ["s-evidence-upload","s-evidence-api"],
 ["s-evidence-main","s-evidence-api"],
 ["s-evidence-main","s-commander"],
 ["s-commander","s-commander-de"],
 ["s-commander","s-commander-bdc"],
 ["s-commander","s-commander-regions"],
 ["s-evidence-main","s-evidence-local"],
 ["s-evidence-main","s-evidence-regions"],
 ["s-community","s-my"],
 ["s-my","s-salesforce"],
 ["s-evidence-main","s-www"],
 ["s-fusus","s-evidence-main"],
 ["s-flock","s-evidence-main"],
 ["s-rapidsos","s-evidence-main"],
 ["s-3si","s-flock"],
 ["s-dedrone-c2","s-dedrone-api"],
 ["s-fusus-eur","s-fusus-de"],
 ["s-academy","s-dedrone"],
 ["s-dedrone","s-evidence-main"],
]
links = [list(l) for l in {tuple(l) for l in links}]

AXON_INT = {"zones": zones, "services": services, "ipPools": ipPools, "links": links}
print("zones:", len(zones), "| services:", len(services), "| pools:", len(ipPools), "| links:", len(links))
json.dump(AXON_INT, open("/tmp/axon-network/data.json","w"), indent=1, ensure_ascii=False)
pathlib.Path("/tmp/axon-network/axon_network.js").write_text(
    "// AXON INTERNAL NETWORK — subdomain/endpoint topology (public DNS + CT + client bundle data)\n"
    "// Passive OSINT — TLP:AMBER (sanitized for public render). Updated 2026-08-19.\n"
    "const AXON_INT = " + json.dumps(AXON_INT, ensure_ascii=False) + ";\n", encoding="utf-8")
print("data written")
