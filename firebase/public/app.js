/* speechalerts hosted feed: reads Firestore (status/current, events, alerts) and renders a
   terminal-style scrollback. Every time is shown in the viewer's zone (override: ?tz=Area/City). */
(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  const browserTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
  let TZ = browserTz;
  if (params.get("tz")) {
    try { new Intl.DateTimeFormat("en", { timeZone: params.get("tz") }); TZ = params.get("tz"); } catch (_) { /* keep browser zone */ }
  }

  // ---------- formatting ----------
  const fmtCache = {};
  function fmt(opts, tz) {
    const key = tz + JSON.stringify(opts);
    return (fmtCache[key] ||= new Intl.DateTimeFormat(undefined, { timeZone: tz, ...opts }));
  }
  const toDate = (v) => (v && typeof v.toDate === "function") ? v.toDate() : (typeof v === "number" ? new Date(v * 1000) : (v ? new Date(v) : null));
  const clock = (d, tz = TZ) => fmt({ hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }, tz).format(d);
  const hm = (d, tz = TZ) => fmt({ hour: "2-digit", minute: "2-digit", hour12: false }, tz).format(d);
  const dayLabel = (d, tz = TZ) => fmt({ weekday: "short", month: "short", day: "2-digit" }, tz).format(d);
  const zoneAbbr = (d, tz) => {
    const parts = fmt({ timeZoneName: "short", hour: "numeric" }, tz).formatToParts(d);
    return (parts.find((p) => p.type === "timeZoneName") || {}).value || tz;
  };
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pad = (s, n) => { s = String(s); return s.length >= n ? s : s + " ".repeat(n - s.length); };
  const mmss = (sec) => { sec = Math.max(0, Math.round(sec || 0)); const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60; return (h ? h + ":" : "") + String(m).padStart(h ? 2 : 1, "0") + ":" + String(s).padStart(2, "0"); };
  function relative(ms) {
    const abs = Math.abs(ms), past = ms < 0;
    const m = Math.round(abs / 60000);
    let s;
    if (abs < 45000) s = "now";
    else if (m < 60) s = m + "m";
    else if (m < 60 * 36) s = Math.floor(m / 60) + "h " + String(m % 60).padStart(2, "0") + "m";
    else s = Math.round(m / 1440) + "d";
    if (s === "now") return s;
    return past ? s + " ago" : "in " + s;
  }
  const ago = (d) => d ? relative(d.getTime() - Date.now()) : "never";

  // ---------- state ----------
  const S = { status: null, events: [], alerts: [], streams: [], segments: [], tailN: 25, stream: null, streamUserPick: false, follow: true, connected: false, error: null, segError: null };
  let unsubSegments = null, subscribedStream = null;

  // ---------- firestore ----------
  let db;
  try {
    db = firebase.firestore();
  } catch (e) {
    S.error = "Firebase config missing: " + e.message;
    render();
    return;
  }

  db.collection("status").doc("current").onSnapshot((snap) => {
    S.status = snap.exists ? snap.data() : null;
    S.connected = true;
    render();
  }, onErr);

  db.collection("events").orderBy("starts_at").onSnapshot((snap) => {
    S.events = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    render();
  }, onErr);

  db.collection("alerts").orderBy("created_at", "desc").limit(400).onSnapshot((snap) => {
    S.alerts = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    render();
  }, onErr);

  db.collection("streams").orderBy("started_at", "desc").limit(12).onSnapshot((snap) => {
    S.streams = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    render();
  }, onErr);

  function subscribeTranscript(key) {
    if (key === subscribedStream) return;
    if (unsubSegments) { unsubSegments(); unsubSegments = null; }
    subscribedStream = key;
    S.segments = []; S.segError = null; S.follow = true;
    if (!key || key.startsWith("replay:")) { renderTranscript(); return; }
    unsubSegments = db.collection("streams").doc(key).collection("segments").orderBy("t_wall").limit(5000)
      .onSnapshot((snap) => {
        S.segments = snap.docs.map((d) => d.data());
        renderTranscript();
      }, (err) => { S.segError = err.message || String(err); renderTranscript(); });
  }

  function onErr(err) {
    S.error = err.message || String(err);
    render();
  }

  // ---------- derived ----------
  function streamKey(a) {
    if (a.stream_id) return a.stream_id;
    const src = a.source || "";
    return "replay:" + src.split("/").pop();
  }
  function streamLabel(a) {
    if (a.stream_title) return a.stream_title;
    return a.stream_id || ((a.source || "").split("/").pop() || "unknown") + " (replay)";
  }
  // Heads-ups are the parents; confirmations/retractions merge their verdict into them.
  function groupAlerts(alerts) {
    const byId = new Map(alerts.map((a) => [a.id, a]));
    const children = new Map();
    for (const a of alerts) {
      if (a.parent_id && byId.has(a.parent_id)) {
        if (!children.has(a.parent_id)) children.set(a.parent_id, []);
        children.get(a.parent_id).push(a);
      }
    }
    const roots = alerts.filter((a) => !a.parent_id || !byId.has(a.parent_id));
    return roots.map((root) => {
      const kids = (children.get(root.id) || []).sort((x, y) => (y.t_alert || 0) - (x.t_alert || 0));
      const verdict = kids[0] || (root.state !== "headsup" ? root : null);
      return { root, verdict, time: toDate(root.t_alert) || toDate(root.created_at) };
    }).sort((x, y) => (y.time?.getTime() || 0) - (x.time?.getTime() || 0));
  }

  // Streams known from the `streams` collection, then any extra ones only alerts mention (replays).
  function streamList() {
    const out = [], seen = new Set();
    for (const st of S.streams) {
      if (seen.has(st.id)) continue;
      seen.add(st.id);
      out.push({ key: st.id, label: st.title || st.id, live: st.state === "live", started: toDate(st.started_at) });
    }
    for (const g of groupAlerts(S.alerts)) {
      const k = streamKey(g.root);
      if (seen.has(k)) continue;
      seen.add(k);
      out.push({ key: k, label: streamLabel(g.root), live: false, started: g.time });
    }
    return out;
  }
  function pickStream() {
    const list = streamList();
    if (!list.length) { S.stream = null; return list; }
    const keys = new Set(list.map((s) => s.key));
    if (S.streamUserPick && keys.has(S.stream)) return list;
    const st = S.status;
    if (st && st.state === "listening" && st.video_id && keys.has(st.video_id)) S.stream = st.video_id;
    else if (!keys.has(S.stream) || !S.streamUserPick) S.stream = list[0].key;
    return list;
  }

  // ---------- render ----------
  function render() {
    pickStream();
    subscribeTranscript(S.stream);
    renderStatus();
    renderSchedule();
    renderAlerts();
    renderQuotes();
    renderTranscript();
    renderBar();
  }

  function renderStatus() {
    const st = S.status;
    const out = $("status-out");
    if (S.error) { out.innerHTML = `<span class="err">error: ${esc(S.error)}</span>`; return; }
    if (!S.connected) { out.textContent = "connecting to feed…"; return; }
    if (!st) { out.innerHTML = `<span class="dim">no listener has reported yet</span>`; return; }
    const updated = toDate(st.updated_at);
    const stale = updated && Date.now() - updated.getTime() > 5 * 60 * 1000;
    const lines = [];
    const state = st.state || "unknown";
    lines.push(`listener   <span class="tag ${state === "listening" ? "live" : stale ? "retracted" : "state"}">${esc(state)}</span>${stale ? ` <span class="err">(no heartbeat for ${esc(ago(updated))})</span>` : ""}`);
    if (st.title) lines.push(`stream     <span class="hl">${esc(st.title)}</span>`);
    if (st.source) lines.push(`source     <a href="${esc(st.source)}" target="_blank" rel="noopener">${esc(st.source)}</a>`);
    if (st.reason) lines.push(`ended      <span class="dim">${esc(st.reason)}</span>`);
    const lp = toDate(st.last_poll);
    if (lp) lines.push(`last poll  ${clock(lp)} <span class="dim">(${esc(ago(lp))})</span>`);
    if (updated) lines.push(`heartbeat  ${clock(updated)} <span class="dim">(${esc(ago(updated))})</span>`);
    if (Array.isArray(st.channels) && st.channels.length) {
      lines.push(`channels   ${st.channels.map((c) => `<a href="${esc(c)}" target="_blank" rel="noopener">${esc(c.replace(/^https?:\/\/(www\.)?youtube\.com\//, "").replace(/\/live$/, ""))}</a>`).join("  ")}`);
    }
    lines.push(`alerts     ${S.alerts.length}<span class="dim"> stored</span>`);
    out.innerHTML = lines.join("\n");
  }

  function renderSchedule() {
    $("schedule-flag").textContent = "--tz " + TZ;
    const out = $("schedule-out");
    if (!S.events.length) { out.innerHTML = `<span class="dim">no events on file. Add them to data/schedule.yaml and run scripts/push_schedule.py.</span>`; return; }
    const now = Date.now();
    const rows = S.events.map((ev) => {
      const start = toDate(ev.starts_at);
      const doors = toDate(ev.doors_at);
      const delta = start.getTime() - now;
      let tag, cls;
      if (delta < -4 * 3600 * 1000) { tag = "past"; cls = "past"; }
      else if (delta <= 0) { tag = "now"; cls = "live"; }
      else if (delta < 3 * 3600 * 1000) { tag = "soon"; cls = "soon"; }
      else { tag = relative(delta); cls = "next"; }
      const venueTz = ev.tz || TZ;
      const venueTime = `${hm(start, venueTz)} ${zoneAbbr(start, venueTz)}`;
      const localTime = `${hm(start)}`;
      const dayLocal = dayLabel(start);
      const dayVenue = dayLabel(start, venueTz);
      const dayNote = dayLocal !== dayVenue ? ` <span class="dim">(${esc(dayVenue)} there)</span>` : "";
      const doorsNote = doors ? ` <span class="dim">doors ${hm(doors)}</span>` : "";
      const src = ev.source_url ? ` <a href="${esc(ev.source_url)}" target="_blank" rel="noopener">source</a>` : "";
      return `<div class="event">` +
        `<div class="when"><span class="d">${esc(dayLocal)}</span> ${esc(localTime)}\n<span class="tag ${cls}">${esc(tag)}</span></div>` +
        `<div class="what"><span class="title">${esc(ev.title)}</span>\n` +
        `<span class="dim">${esc(ev.venue)}, ${esc(ev.city)}</span>\n` +
        `<span class="dim">venue time</span> ${esc(venueTime)}${dayNote}${doorsNote}${src}</div>` +
        `</div>`;
    });
    out.innerHTML = rows.join("");
  }

  function alertRow(g) {
    const a = g.root, v = g.verdict;
    const t = g.time ? clock(g.time) : "--:--:--";
    const tickers = (a.tickers || []).slice(0, 4).join(" ");
    const state = v ? v.state : a.state;
    const stateCls = state === "confirmed" ? "confirmed" : state === "retracted" ? "retracted" : "headsup";
    const stateTxt = state === "headsup" ? "heads-up" : state;
    let html = `<div class="row"><span class="t">${esc(t)}</span><span class="body">` +
      `<span class="tag ${stateCls}">${esc(pad(stateTxt, 9))}</span> ` +
      `<span class="ent">${esc(a.entity)}</span>${tickers ? ` <span class="tick">${esc(tickers)}</span>` : ""}` +
      (a.quote ? `  <span class="quote">${esc(a.quote)}</span>` : "") +
      `</span></div>`;
    if (v) {
      const stance = v.stance || "neutral";
      const sc = stance === "positive" ? "pos" : stance === "negative" ? "neg" : "neu";
      const lat = v.t_alert && a.t_spoken ? ` +${(v.t_alert - a.t_spoken).toFixed(1)}s` : "";
      const who = v.speaker && v.speaker !== "figure" ? ` <span class="err">spoken by ${esc(v.speaker)}</span>` : "";
      html += `<div class="row sub"><span class="t">${esc(t)}</span><span class="body">` +
        `<span class="${sc}">${esc(stance)}</span> / ${esc(v.action || "other")}` +
        (typeof v.confidence === "number" ? ` ${Math.round(v.confidence * 100)}%` : "") + esc(lat) + who +
        (v.summary ? `  ${esc(v.summary)}` : "") +
        `</span></div>`;
    }
    return html;
  }

  function renderAlerts() {
    const out = $("alerts-out");
    if (!S.alerts.length) { out.innerHTML = `<span class="dim">no alerts yet. The listener writes here the moment ${esc(figureName())} mentions a company, sector or country.</span>`; return; }
    const groups = groupAlerts(S.alerts);
    const shown = groups.slice(0, S.tailN);
    let html = "", lastStream = null, lastDay = null;
    for (const g of shown) {
      const key = streamKey(g.root);
      if (key !== lastStream) {
        html += `${html ? "\n" : ""}<span class="dim">── </span><span class="hl">${esc(streamLabel(g.root))}</span>\n`;
        lastStream = key; lastDay = null;
      }
      const day = g.time ? dayLabel(g.time) : "";
      if (day !== lastDay) { html += `<span class="dim">${esc(day)}</span>\n`; lastDay = day; }
      html += alertRow(g);
    }
    out.innerHTML = html;
    $("alerts-n").textContent = String(Math.min(S.tailN, groups.length));
    const more = $("alerts-more");
    more.hidden = groups.length <= S.tailN;
    $("alerts-more-btn").textContent = `… ${groups.length - shown.length} more (show all)`;
  }

  function figureName() {
    const a = S.alerts[0];
    const f = (a && a.figure) || "The President";
    return f.charAt(0).toUpperCase() + f.slice(1);
  }

  function renderQuotes() {
    const out = $("quotes-out");
    const groups = groupAlerts(S.alerts);
    const streams = streamList();
    if (!streams.length || !S.stream) { out.innerHTML = `<span class="dim">nothing captured yet</span>`; $("quotes-streams").innerHTML = ""; return; }
    const cur = streams.find((s) => s.key === S.stream) || streams[0];
    $("quotes-stream").textContent = S.stream.startsWith("replay:") ? S.stream.slice(7) : S.stream;
    const items = groups.filter((g) => streamKey(g.root) === S.stream)
      .sort((x, y) => (x.root.t_audio || 0) - (y.root.t_audio || 0));
    let html = `<span class="hl">${esc(cur.label)}</span>\n`;
    if (!items.length) html += `<span class="dim">no alerts on this stream yet</span>\n`;
    for (const g of items) {
      const v = g.verdict;
      const state = v ? v.state : g.root.state;
      const cls = state === "confirmed" ? "confirmed" : state === "retracted" ? "retracted" : "headsup";
      const who = (v && v.speaker && v.speaker !== "figure") ? `${v.speaker}` : figureName();
      html += `<div class="row"><span class="t">${esc(mmss(g.root.t_audio))}</span><span class="body">` +
        `<span class="${cls === "retracted" ? "dim" : "hl"}">${esc(who)}</span><span class="dim">:</span> <span class="quote">${esc(g.root.quote || "")}</span>` +
        `  <span class="tag ${cls}">${esc(g.root.entity)}</span></span></div>`;
    }
    out.innerHTML = html;
    $("quotes-streams").innerHTML = streams.slice(0, 12).map((s) =>
      `<button type="button" class="link${s.key === S.stream ? " on" : ""}" data-stream="${esc(s.key)}">${esc(s.label.length > 70 ? s.label.slice(0, 69) + "…" : s.label)}</button>`
    ).join("\n");
  }

  function renderTranscript() {
    const out = $("transcript-out");
    const list = streamList();
    const cur = list.find((s) => s.key === S.stream);
    $("transcript-stream").textContent = S.stream ? (S.stream.startsWith("replay:") ? S.stream.slice(7) : S.stream) : "…";
    $("transcript-title").textContent = cur ? cur.label : "";
    if (S.segError) { out.innerHTML = `<span class="err">error: ${esc(S.segError)}</span>`; return; }
    if (!S.stream) { out.innerHTML = `<span class="dim">no stream yet</span>`; return; }
    if (S.stream.startsWith("replay:")) { out.innerHTML = `<span class="dim">replays keep their transcript on the listener machine</span>`; return; }
    if (!S.segments.length) { out.innerHTML = `<span class="dim">${cur && cur.live ? "listening, waiting for the first sentence…" : "no transcript stored for this stream"}</span>`; return; }
    const n = S.segments.length;
    let html = "", lastDay = null;
    S.segments.forEach((seg, i) => {
      const d = toDate(seg.t_wall);
      const day = d ? dayLabel(d) : "";
      if (day !== lastDay) { html += `<span class="dim">${esc(day)}</span>\n`; lastDay = day; }
      const q = seg.speaker_label === "Q";
      html += `<div class="seg${q ? " q" : ""}${i === n - 1 ? " last" : ""}"><span class="t">${esc(d ? clock(d) : "")}</span>` +
        `<span class="who">${esc(seg.speaker_label || "")}</span><span class="txt">${esc(seg.text)}</span></div>`;
    });
    out.innerHTML = html;
    const box = $("tscroll");
    if (S.follow && window.matchMedia("(min-width: 1000px)").matches) box.scrollTop = box.scrollHeight;
    $("follow-btn").hidden = S.follow;
  }

  function renderBar() {
    const st = S.status;
    const left = $("sb-left");
    if (S.error) { left.textContent = "[watch] error"; left.className = "sb-left off"; }
    else if (!st) { left.textContent = "[watch] " + (S.connected ? "no listener" : "connecting"); left.className = "sb-left"; }
    else {
      const updated = toDate(st.updated_at);
      const stale = updated && Date.now() - updated.getTime() > 5 * 60 * 1000;
      if (stale) { left.textContent = "[watch] offline"; left.className = "sb-left off"; }
      else if (st.state === "listening") { left.textContent = "[watch] listening"; left.className = "sb-left live"; }
      else { left.textContent = `[watch] ${st.state || "?"}${Array.isArray(st.channels) ? " " + st.channels.length + " ch" : ""}`; left.className = "sb-left"; }
    }
    const now = Date.now();
    const next = S.events.map((ev) => ({ ev, d: toDate(ev.starts_at).getTime() - now })).filter((x) => x.d > -3 * 3600 * 1000).sort((a, b) => a.d - b.d)[0];
    $("sb-mid").textContent = next ? `${next.ev.city.split(",")[0]} ${next.d <= 0 ? "underway" : relative(next.d)}` : "";
    $("sb-right").textContent = `${TZ} ${clock(new Date())}`;
  }

  // ---------- interaction ----------
  $("alerts-more-btn").addEventListener("click", () => { S.tailN = 10000; renderAlerts(); });
  $("quotes-streams").addEventListener("click", (e) => {
    const b = e.target.closest("[data-stream]");
    if (!b) return;
    S.stream = b.dataset.stream; S.streamUserPick = true; S.follow = true;
    subscribeTranscript(S.stream); renderQuotes(); renderTranscript();
  });
  $("tscroll").addEventListener("scroll", () => {
    const box = $("tscroll");
    if (!window.matchMedia("(min-width: 1000px)").matches) return;
    const atBottom = box.scrollHeight - box.scrollTop - box.clientHeight < 40;
    if (atBottom !== S.follow) { S.follow = atBottom; $("follow-btn").hidden = S.follow; }
  });
  $("follow-btn").addEventListener("click", () => { S.follow = true; renderTranscript(); });

  setInterval(() => { renderBar(); }, 1000);
  setInterval(() => { renderSchedule(); renderStatus(); }, 30000);
  render();
})();
