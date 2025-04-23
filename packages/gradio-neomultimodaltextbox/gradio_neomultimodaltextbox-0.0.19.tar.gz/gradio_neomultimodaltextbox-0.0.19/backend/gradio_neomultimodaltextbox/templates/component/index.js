var ol = (n) => {
  throw TypeError(n);
};
var al = (n, e, t) => e.has(n) || ol("Cannot " + t);
var sn = (n, e, t) => (al(n, e, "read from private field"), t ? t.call(n) : e.get(n)), sl = (n, e, t) => e.has(n) ? ol("Cannot add the same private member more than once") : e instanceof WeakSet ? e.add(n) : e.set(n, t), rl = (n, e, t, i) => (al(n, e, "write to private field"), i ? i.call(n, t) : e.set(n, t), t);
new Intl.Collator(0, { numeric: 1 }).compare;
async function ia(n, e) {
  return n.map(
    (t) => new la({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class la {
  constructor({
    path: e,
    url: t,
    orig_name: i,
    size: l,
    blob: o,
    is_stream: a,
    mime_type: r,
    alt_text: s,
    b64: f
  }) {
    this.meta = { _type: "gradio.FileData" }, this.path = e, this.url = t, this.orig_name = i, this.size = l, this.blob = t ? void 0 : o, this.is_stream = a, this.mime_type = r, this.alt_text = s, this.b64 = f;
  }
}
typeof process < "u" && process.versions && process.versions.node;
var Et;
class Gf extends TransformStream {
  /** Constructs a new instance. */
  constructor(t = { allowCR: !1 }) {
    super({
      transform: (i, l) => {
        for (i = sn(this, Et) + i; ; ) {
          const o = i.indexOf(`
`), a = t.allowCR ? i.indexOf("\r") : -1;
          if (a !== -1 && a !== i.length - 1 && (o === -1 || o - 1 > a)) {
            l.enqueue(i.slice(0, a)), i = i.slice(a + 1);
            continue;
          }
          if (o === -1)
            break;
          const r = i[o - 1] === "\r" ? o - 1 : o;
          l.enqueue(i.slice(0, r)), i = i.slice(o + 1);
        }
        rl(this, Et, i);
      },
      flush: (i) => {
        if (sn(this, Et) === "")
          return;
        const l = t.allowCR && sn(this, Et).endsWith("\r") ? sn(this, Et).slice(0, -1) : sn(this, Et);
        i.enqueue(l);
      }
    });
    sl(this, Et, "");
  }
}
Et = new WeakMap();
const {
  SvelteComponent: oa,
  append_hydration: Ue,
  attr: Wt,
  children: Vt,
  claim_element: Gt,
  claim_space: Ri,
  claim_text: fn,
  detach: yt,
  element: jt,
  init: aa,
  insert_hydration: bo,
  noop: fl,
  safe_not_equal: sa,
  set_data: si,
  set_style: vi,
  space: Mi,
  text: un,
  toggle_class: ul
} = window.__gradio__svelte__internal, { onMount: ra, createEventDispatcher: fa, onDestroy: ua } = window.__gradio__svelte__internal;
function cl(n) {
  let e, t, i, l, o = Rn(
    /*file_to_display*/
    n[2]
  ) + "", a, r, s, f, _ = (
    /*file_to_display*/
    n[2].orig_name + ""
  ), d;
  return {
    c() {
      e = jt("div"), t = jt("span"), i = jt("div"), l = jt("progress"), a = un(o), s = Mi(), f = jt("span"), d = un(_), this.h();
    },
    l(c) {
      e = Gt(c, "DIV", { class: !0 });
      var u = Vt(e);
      t = Gt(u, "SPAN", {});
      var h = Vt(t);
      i = Gt(h, "DIV", { class: !0 });
      var w = Vt(i);
      l = Gt(w, "PROGRESS", { style: !0, max: !0, class: !0 });
      var T = Vt(l);
      a = fn(T, o), T.forEach(yt), w.forEach(yt), h.forEach(yt), s = Ri(u), f = Gt(u, "SPAN", { class: !0 });
      var k = Vt(f);
      d = fn(k, _), k.forEach(yt), u.forEach(yt), this.h();
    },
    h() {
      vi(l, "visibility", "hidden"), vi(l, "height", "0"), vi(l, "width", "0"), l.value = r = Rn(
        /*file_to_display*/
        n[2]
      ), Wt(l, "max", "100"), Wt(l, "class", "svelte-cr2edf"), Wt(i, "class", "progress-bar svelte-cr2edf"), Wt(f, "class", "file-name svelte-cr2edf"), Wt(e, "class", "file svelte-cr2edf");
    },
    m(c, u) {
      bo(c, e, u), Ue(e, t), Ue(t, i), Ue(i, l), Ue(l, a), Ue(e, s), Ue(e, f), Ue(f, d);
    },
    p(c, u) {
      u & /*file_to_display*/
      4 && o !== (o = Rn(
        /*file_to_display*/
        c[2]
      ) + "") && si(a, o), u & /*file_to_display*/
      4 && r !== (r = Rn(
        /*file_to_display*/
        c[2]
      )) && (l.value = r), u & /*file_to_display*/
      4 && _ !== (_ = /*file_to_display*/
      c[2].orig_name + "") && si(d, _);
    },
    d(c) {
      c && yt(e);
    }
  };
}
function ca(n) {
  let e, t, i, l = (
    /*files_with_progress*/
    n[0].length + ""
  ), o, a, r = (
    /*files_with_progress*/
    n[0].length > 1 ? "files" : "file"
  ), s, f, _, d = (
    /*file_to_display*/
    n[2] && cl(n)
  );
  return {
    c() {
      e = jt("div"), t = jt("span"), i = un("Uploading "), o = un(l), a = Mi(), s = un(r), f = un("..."), _ = Mi(), d && d.c(), this.h();
    },
    l(c) {
      e = Gt(c, "DIV", { class: !0 });
      var u = Vt(e);
      t = Gt(u, "SPAN", { class: !0 });
      var h = Vt(t);
      i = fn(h, "Uploading "), o = fn(h, l), a = Ri(h), s = fn(h, r), f = fn(h, "..."), h.forEach(yt), _ = Ri(u), d && d.l(u), u.forEach(yt), this.h();
    },
    h() {
      Wt(t, "class", "uploading svelte-cr2edf"), Wt(e, "class", "wrap svelte-cr2edf"), ul(
        e,
        "progress",
        /*progress*/
        n[1]
      );
    },
    m(c, u) {
      bo(c, e, u), Ue(e, t), Ue(t, i), Ue(t, o), Ue(t, a), Ue(t, s), Ue(t, f), Ue(e, _), d && d.m(e, null);
    },
    p(c, [u]) {
      u & /*files_with_progress*/
      1 && l !== (l = /*files_with_progress*/
      c[0].length + "") && si(o, l), u & /*files_with_progress*/
      1 && r !== (r = /*files_with_progress*/
      c[0].length > 1 ? "files" : "file") && si(s, r), /*file_to_display*/
      c[2] ? d ? d.p(c, u) : (d = cl(c), d.c(), d.m(e, null)) : d && (d.d(1), d = null), u & /*progress*/
      2 && ul(
        e,
        "progress",
        /*progress*/
        c[1]
      );
    },
    i: fl,
    o: fl,
    d(c) {
      c && yt(e), d && d.d();
    }
  };
}
function Rn(n) {
  return n.progress * 100 / (n.size || 0) || 0;
}
function _a(n) {
  let e = 0;
  return n.forEach((t) => {
    e += Rn(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / n.length).toFixed(2) + "%"), e / n.length;
}
function da(n, e, t) {
  var i = this && this.__awaiter || function(w, T, k, v) {
    function g(b) {
      return b instanceof k ? b : new k(function(O) {
        O(b);
      });
    }
    return new (k || (k = Promise))(function(b, O) {
      function P(F) {
        try {
          Y(v.next(F));
        } catch (C) {
          O(C);
        }
      }
      function U(F) {
        try {
          Y(v.throw(F));
        } catch (C) {
          O(C);
        }
      }
      function Y(F) {
        F.done ? b(F.value) : g(F.value).then(P, U);
      }
      Y((v = v.apply(w, T || [])).next());
    });
  };
  let { upload_id: l } = e, { root: o } = e, { files: a } = e, { stream_handler: r } = e, s, f = !1, _, d, c = a.map((w) => Object.assign(Object.assign({}, w), { progress: 0 }));
  const u = fa();
  function h(w, T) {
    t(0, c = c.map((k) => (k.orig_name === w && (k.progress += T), k)));
  }
  return ra(() => i(void 0, void 0, void 0, function* () {
    if (s = yield r(new URL(`${o}/gradio_api/upload_progress?upload_id=${l}`)), s == null)
      throw new Error("Event source is not defined");
    s.onmessage = function(w) {
      return i(this, void 0, void 0, function* () {
        const T = JSON.parse(w.data);
        f || t(1, f = !0), T.msg === "done" ? (s == null || s.close(), u("done")) : (t(7, _ = T), h(T.orig_name, T.chunk_size));
      });
    };
  })), ua(() => {
    (s != null || s != null) && s.close();
  }), n.$$set = (w) => {
    "upload_id" in w && t(3, l = w.upload_id), "root" in w && t(4, o = w.root), "files" in w && t(5, a = w.files), "stream_handler" in w && t(6, r = w.stream_handler);
  }, n.$$.update = () => {
    n.$$.dirty & /*files_with_progress*/
    1 && _a(c), n.$$.dirty & /*current_file_upload, files_with_progress*/
    129 && t(2, d = _ || c[0]);
  }, [
    c,
    f,
    d,
    l,
    o,
    a,
    r,
    _
  ];
}
class ma extends oa {
  constructor(e) {
    super(), aa(this, e, da, ca, sa, {
      upload_id: 3,
      root: 4,
      files: 5,
      stream_handler: 6
    });
  }
}
const {
  SvelteComponent: ha,
  append_hydration: _l,
  attr: De,
  binding_callbacks: ga,
  bubble: zt,
  check_outros: po,
  children: vo,
  claim_component: ba,
  claim_element: Pi,
  claim_space: pa,
  create_component: va,
  create_slot: wo,
  destroy_component: wa,
  detach: gn,
  element: Fi,
  empty: ri,
  get_all_dirty_from_scope: ko,
  get_slot_changes: yo,
  group_outros: Eo,
  init: ka,
  insert_hydration: di,
  listen: He,
  mount_component: ya,
  prevent_default: qt,
  run_all: Ea,
  safe_not_equal: Ta,
  set_style: To,
  space: Aa,
  stop_propagation: Bt,
  toggle_class: pe,
  transition_in: Rt,
  transition_out: en,
  update_slot_base: Ao
} = window.__gradio__svelte__internal, { createEventDispatcher: Sa, tick: Da } = window.__gradio__svelte__internal;
function Ca(n) {
  let e, t, i, l, o, a, r, s, f, _, d;
  const c = (
    /*#slots*/
    n[27].default
  ), u = wo(
    c,
    n,
    /*$$scope*/
    n[26],
    null
  );
  return {
    c() {
      e = Fi("button"), u && u.c(), t = Aa(), i = Fi("input"), this.h();
    },
    l(h) {
      e = Pi(h, "BUTTON", { tabindex: !0, class: !0 });
      var w = vo(e);
      u && u.l(w), t = pa(w), i = Pi(w, "INPUT", {
        "aria-label": !0,
        "data-testid": !0,
        type: !0,
        accept: !0,
        webkitdirectory: !0,
        mozdirectory: !0,
        class: !0
      }), w.forEach(gn), this.h();
    },
    h() {
      De(i, "aria-label", "file upload"), De(i, "data-testid", "file-upload"), De(i, "type", "file"), De(i, "accept", l = /*accept_file_types*/
      n[16] || void 0), i.multiple = o = /*file_count*/
      n[6] === "multiple" || void 0, De(i, "webkitdirectory", a = /*file_count*/
      n[6] === "directory" || void 0), De(i, "mozdirectory", r = /*file_count*/
      n[6] === "directory" || void 0), De(i, "class", "svelte-ks67v6"), De(e, "tabindex", s = /*hidden*/
      n[9] ? -1 : 0), De(e, "class", "svelte-ks67v6"), pe(
        e,
        "hidden",
        /*hidden*/
        n[9]
      ), pe(
        e,
        "center",
        /*center*/
        n[4]
      ), pe(
        e,
        "boundedheight",
        /*boundedheight*/
        n[3]
      ), pe(
        e,
        "flex",
        /*flex*/
        n[5]
      ), pe(
        e,
        "disable_click",
        /*disable_click*/
        n[7]
      ), To(e, "height", "100%");
    },
    m(h, w) {
      di(h, e, w), u && u.m(e, null), _l(e, t), _l(e, i), n[35](i), f = !0, _ || (d = [
        He(
          i,
          "change",
          /*load_files_from_upload*/
          n[18]
        ),
        He(e, "drag", Bt(qt(
          /*drag_handler*/
          n[28]
        ))),
        He(e, "dragstart", Bt(qt(
          /*dragstart_handler*/
          n[29]
        ))),
        He(e, "dragend", Bt(qt(
          /*dragend_handler*/
          n[30]
        ))),
        He(e, "dragover", Bt(qt(
          /*dragover_handler*/
          n[31]
        ))),
        He(e, "dragenter", Bt(qt(
          /*dragenter_handler*/
          n[32]
        ))),
        He(e, "dragleave", Bt(qt(
          /*dragleave_handler*/
          n[33]
        ))),
        He(e, "drop", Bt(qt(
          /*drop_handler*/
          n[34]
        ))),
        He(
          e,
          "click",
          /*open_file_upload*/
          n[13]
        ),
        He(
          e,
          "drop",
          /*loadFilesFromDrop*/
          n[19]
        ),
        He(
          e,
          "dragenter",
          /*updateDragging*/
          n[17]
        ),
        He(
          e,
          "dragleave",
          /*updateDragging*/
          n[17]
        )
      ], _ = !0);
    },
    p(h, w) {
      u && u.p && (!f || w[0] & /*$$scope*/
      67108864) && Ao(
        u,
        c,
        h,
        /*$$scope*/
        h[26],
        f ? yo(
          c,
          /*$$scope*/
          h[26],
          w,
          null
        ) : ko(
          /*$$scope*/
          h[26]
        ),
        null
      ), (!f || w[0] & /*accept_file_types*/
      65536 && l !== (l = /*accept_file_types*/
      h[16] || void 0)) && De(i, "accept", l), (!f || w[0] & /*file_count*/
      64 && o !== (o = /*file_count*/
      h[6] === "multiple" || void 0)) && (i.multiple = o), (!f || w[0] & /*file_count*/
      64 && a !== (a = /*file_count*/
      h[6] === "directory" || void 0)) && De(i, "webkitdirectory", a), (!f || w[0] & /*file_count*/
      64 && r !== (r = /*file_count*/
      h[6] === "directory" || void 0)) && De(i, "mozdirectory", r), (!f || w[0] & /*hidden*/
      512 && s !== (s = /*hidden*/
      h[9] ? -1 : 0)) && De(e, "tabindex", s), (!f || w[0] & /*hidden*/
      512) && pe(
        e,
        "hidden",
        /*hidden*/
        h[9]
      ), (!f || w[0] & /*center*/
      16) && pe(
        e,
        "center",
        /*center*/
        h[4]
      ), (!f || w[0] & /*boundedheight*/
      8) && pe(
        e,
        "boundedheight",
        /*boundedheight*/
        h[3]
      ), (!f || w[0] & /*flex*/
      32) && pe(
        e,
        "flex",
        /*flex*/
        h[5]
      ), (!f || w[0] & /*disable_click*/
      128) && pe(
        e,
        "disable_click",
        /*disable_click*/
        h[7]
      );
    },
    i(h) {
      f || (Rt(u, h), f = !0);
    },
    o(h) {
      en(u, h), f = !1;
    },
    d(h) {
      h && gn(e), u && u.d(h), n[35](null), _ = !1, Ea(d);
    }
  };
}
function La(n) {
  let e, t, i = !/*hidden*/
  n[9] && dl(n);
  return {
    c() {
      i && i.c(), e = ri();
    },
    l(l) {
      i && i.l(l), e = ri();
    },
    m(l, o) {
      i && i.m(l, o), di(l, e, o), t = !0;
    },
    p(l, o) {
      /*hidden*/
      l[9] ? i && (Eo(), en(i, 1, 1, () => {
        i = null;
      }), po()) : i ? (i.p(l, o), o[0] & /*hidden*/
      512 && Rt(i, 1)) : (i = dl(l), i.c(), Rt(i, 1), i.m(e.parentNode, e));
    },
    i(l) {
      t || (Rt(i), t = !0);
    },
    o(l) {
      en(i), t = !1;
    },
    d(l) {
      l && gn(e), i && i.d(l);
    }
  };
}
function Ia(n) {
  let e, t, i, l, o;
  const a = (
    /*#slots*/
    n[27].default
  ), r = wo(
    a,
    n,
    /*$$scope*/
    n[26],
    null
  );
  return {
    c() {
      e = Fi("button"), r && r.c(), this.h();
    },
    l(s) {
      e = Pi(s, "BUTTON", { tabindex: !0, class: !0 });
      var f = vo(e);
      r && r.l(f), f.forEach(gn), this.h();
    },
    h() {
      De(e, "tabindex", t = /*hidden*/
      n[9] ? -1 : 0), De(e, "class", "svelte-ks67v6"), pe(
        e,
        "hidden",
        /*hidden*/
        n[9]
      ), pe(
        e,
        "center",
        /*center*/
        n[4]
      ), pe(
        e,
        "boundedheight",
        /*boundedheight*/
        n[3]
      ), pe(
        e,
        "flex",
        /*flex*/
        n[5]
      ), To(e, "height", "100%");
    },
    m(s, f) {
      di(s, e, f), r && r.m(e, null), i = !0, l || (o = He(
        e,
        "click",
        /*paste_clipboard*/
        n[12]
      ), l = !0);
    },
    p(s, f) {
      r && r.p && (!i || f[0] & /*$$scope*/
      67108864) && Ao(
        r,
        a,
        s,
        /*$$scope*/
        s[26],
        i ? yo(
          a,
          /*$$scope*/
          s[26],
          f,
          null
        ) : ko(
          /*$$scope*/
          s[26]
        ),
        null
      ), (!i || f[0] & /*hidden*/
      512 && t !== (t = /*hidden*/
      s[9] ? -1 : 0)) && De(e, "tabindex", t), (!i || f[0] & /*hidden*/
      512) && pe(
        e,
        "hidden",
        /*hidden*/
        s[9]
      ), (!i || f[0] & /*center*/
      16) && pe(
        e,
        "center",
        /*center*/
        s[4]
      ), (!i || f[0] & /*boundedheight*/
      8) && pe(
        e,
        "boundedheight",
        /*boundedheight*/
        s[3]
      ), (!i || f[0] & /*flex*/
      32) && pe(
        e,
        "flex",
        /*flex*/
        s[5]
      );
    },
    i(s) {
      i || (Rt(r, s), i = !0);
    },
    o(s) {
      en(r, s), i = !1;
    },
    d(s) {
      s && gn(e), r && r.d(s), l = !1, o();
    }
  };
}
function dl(n) {
  let e, t;
  return e = new ma({
    props: {
      root: (
        /*root*/
        n[8]
      ),
      upload_id: (
        /*upload_id*/
        n[14]
      ),
      files: (
        /*file_data*/
        n[15]
      ),
      stream_handler: (
        /*stream_handler*/
        n[11]
      )
    }
  }), {
    c() {
      va(e.$$.fragment);
    },
    l(i) {
      ba(e.$$.fragment, i);
    },
    m(i, l) {
      ya(e, i, l), t = !0;
    },
    p(i, l) {
      const o = {};
      l[0] & /*root*/
      256 && (o.root = /*root*/
      i[8]), l[0] & /*upload_id*/
      16384 && (o.upload_id = /*upload_id*/
      i[14]), l[0] & /*file_data*/
      32768 && (o.files = /*file_data*/
      i[15]), l[0] & /*stream_handler*/
      2048 && (o.stream_handler = /*stream_handler*/
      i[11]), e.$set(o);
    },
    i(i) {
      t || (Rt(e.$$.fragment, i), t = !0);
    },
    o(i) {
      en(e.$$.fragment, i), t = !1;
    },
    d(i) {
      wa(e, i);
    }
  };
}
function Na(n) {
  let e, t, i, l;
  const o = [Ia, La, Ca], a = [];
  function r(s, f) {
    return (
      /*filetype*/
      s[0] === "clipboard" ? 0 : (
        /*uploading*/
        s[1] && /*show_progress*/
        s[10] ? 1 : 2
      )
    );
  }
  return e = r(n), t = a[e] = o[e](n), {
    c() {
      t.c(), i = ri();
    },
    l(s) {
      t.l(s), i = ri();
    },
    m(s, f) {
      a[e].m(s, f), di(s, i, f), l = !0;
    },
    p(s, f) {
      let _ = e;
      e = r(s), e === _ ? a[e].p(s, f) : (Eo(), en(a[_], 1, 1, () => {
        a[_] = null;
      }), po(), t = a[e], t ? t.p(s, f) : (t = a[e] = o[e](s), t.c()), Rt(t, 1), t.m(i.parentNode, i));
    },
    i(s) {
      l || (Rt(t), l = !0);
    },
    o(s) {
      en(t), l = !1;
    },
    d(s) {
      s && gn(i), a[e].d(s);
    }
  };
}
function Oa(n, e, t) {
  if (!n || n === "*" || n === "file/*" || Array.isArray(n) && n.some((l) => l === "*" || l === "file/*"))
    return !0;
  let i;
  if (typeof n == "string")
    i = n.split(",").map((l) => l.trim());
  else if (Array.isArray(n))
    i = n;
  else
    return !1;
  return i.includes(e) || i.some((l) => {
    const [o] = l.split("/").map((a) => a.trim());
    return l.endsWith("/*") && t.startsWith(o + "/");
  });
}
function Ra(n, e, t) {
  let i, { $$slots: l = {}, $$scope: o } = e;
  var a = this && this.__awaiter || function(y, M, W, B) {
    function x(ce) {
      return ce instanceof W ? ce : new W(function(_e) {
        _e(ce);
      });
    }
    return new (W || (W = Promise))(function(ce, _e) {
      function me(Re) {
        try {
          fe(B.next(Re));
        } catch (wt) {
          _e(wt);
        }
      }
      function Ae(Re) {
        try {
          fe(B.throw(Re));
        } catch (wt) {
          _e(wt);
        }
      }
      function fe(Re) {
        Re.done ? ce(Re.value) : x(Re.value).then(me, Ae);
      }
      fe((B = B.apply(y, M || [])).next());
    });
  };
  let { filetype: r = null } = e, { dragging: s = !1 } = e, { boundedheight: f = !0 } = e, { center: _ = !0 } = e, { flex: d = !0 } = e, { file_count: c = "single" } = e, { disable_click: u = !1 } = e, { root: h } = e, { hidden: w = !1 } = e, { format: T = "file" } = e, { uploading: k = !1 } = e, { hidden_upload: v = null } = e, { show_progress: g = !0 } = e, { max_file_size: b = null } = e, { upload: O } = e, { stream_handler: P } = e, U, Y, F, C = null;
  const J = () => {
    if (typeof navigator < "u") {
      const y = navigator.userAgent.toLowerCase();
      return y.indexOf("iphone") > -1 || y.indexOf("ipad") > -1;
    }
    return !1;
  }, q = Sa(), ne = ["image", "video", "audio", "text", "file"], H = (y) => i && y.startsWith(".") ? (C = !0, y) : i && y.includes("file/*") ? "*" : y.startsWith(".") || y.endsWith("/*") ? y : ne.includes(y) ? y + "/*" : "." + y;
  function ie() {
    t(20, s = !s);
  }
  function re() {
    navigator.clipboard.read().then((y) => a(this, void 0, void 0, function* () {
      for (let M = 0; M < y.length; M++) {
        const W = y[M].types.find((B) => B.startsWith("image/"));
        if (W) {
          y[M].getType(W).then((B) => a(this, void 0, void 0, function* () {
            const x = new File([B], `clipboard.${W.replace("image/", "")}`);
            yield ve([x]);
          }));
          break;
        }
      }
    }));
  }
  function Oe() {
    u || v && (t(2, v.value = "", v), v.click());
  }
  function de(y) {
    return a(this, void 0, void 0, function* () {
      yield Da(), t(14, U = Math.random().toString(36).substring(2, 15)), t(1, k = !0);
      try {
        const M = yield O(y, h, U, b ?? 1 / 0);
        return q("load", c === "single" ? M == null ? void 0 : M[0] : M), t(1, k = !1), M || [];
      } catch (M) {
        return q("error", M.message), t(1, k = !1), [];
      }
    });
  }
  function ve(y) {
    return a(this, void 0, void 0, function* () {
      if (!y.length)
        return;
      let M = y.map((W) => new File([W], W instanceof File ? W.name : "file", { type: W.type }));
      return i && C && (M = M.filter((W) => Ce(W) ? !0 : (q("error", `Invalid file type: ${W.name}. Only ${r} allowed.`), !1)), M.length === 0) ? [] : (t(15, Y = yield ia(M)), yield de(Y));
    });
  }
  function Ce(y) {
    return r ? (Array.isArray(r) ? r : [r]).some((W) => {
      const B = H(W);
      if (B.startsWith("."))
        return y.name.toLowerCase().endsWith(B.toLowerCase());
      if (B === "*")
        return !0;
      if (B.endsWith("/*")) {
        const [x] = B.split("/");
        return y.type.startsWith(x + "/");
      }
      return y.type === B;
    }) : !0;
  }
  function K(y) {
    return a(this, void 0, void 0, function* () {
      const M = y.target;
      if (M.files)
        if (T != "blob")
          yield ve(Array.from(M.files));
        else {
          if (c === "single") {
            q("load", M.files[0]);
            return;
          }
          q("load", M.files);
        }
    });
  }
  function we(y) {
    return a(this, void 0, void 0, function* () {
      var M;
      if (t(20, s = !1), !(!((M = y.dataTransfer) === null || M === void 0) && M.files)) return;
      const W = Array.from(y.dataTransfer.files).filter((B) => {
        const x = "." + B.name.split(".").pop();
        return x && Oa(F, x, B.type) || (x && Array.isArray(r) ? r.includes(x) : x === r) ? !0 : (q("error", `Invalid file type only ${r} allowed.`), !1);
      });
      if (T != "blob")
        yield ve(W);
      else {
        if (c === "single") {
          q("load", W[0]);
          return;
        }
        q("load", W);
      }
    });
  }
  function X(y) {
    zt.call(this, n, y);
  }
  function le(y) {
    zt.call(this, n, y);
  }
  function S(y) {
    zt.call(this, n, y);
  }
  function Te(y) {
    zt.call(this, n, y);
  }
  function be(y) {
    zt.call(this, n, y);
  }
  function D(y) {
    zt.call(this, n, y);
  }
  function Z(y) {
    zt.call(this, n, y);
  }
  function ee(y) {
    ga[y ? "unshift" : "push"](() => {
      v = y, t(2, v);
    });
  }
  return n.$$set = (y) => {
    "filetype" in y && t(0, r = y.filetype), "dragging" in y && t(20, s = y.dragging), "boundedheight" in y && t(3, f = y.boundedheight), "center" in y && t(4, _ = y.center), "flex" in y && t(5, d = y.flex), "file_count" in y && t(6, c = y.file_count), "disable_click" in y && t(7, u = y.disable_click), "root" in y && t(8, h = y.root), "hidden" in y && t(9, w = y.hidden), "format" in y && t(21, T = y.format), "uploading" in y && t(1, k = y.uploading), "hidden_upload" in y && t(2, v = y.hidden_upload), "show_progress" in y && t(10, g = y.show_progress), "max_file_size" in y && t(22, b = y.max_file_size), "upload" in y && t(23, O = y.upload), "stream_handler" in y && t(11, P = y.stream_handler), "$$scope" in y && t(26, o = y.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*filetype, ios*/
    33554433 && (r == null ? t(16, F = null) : typeof r == "string" ? t(16, F = H(r)) : i && r.includes("file/*") ? t(16, F = "*") : (t(0, r = r.map(H)), t(16, F = r.join(", "))));
  }, t(25, i = J()), [
    r,
    k,
    v,
    f,
    _,
    d,
    c,
    u,
    h,
    w,
    g,
    P,
    re,
    Oe,
    U,
    Y,
    F,
    ie,
    K,
    we,
    s,
    T,
    b,
    O,
    ve,
    i,
    o,
    l,
    X,
    le,
    S,
    Te,
    be,
    D,
    Z,
    ee
  ];
}
class Ma extends ha {
  constructor(e) {
    super(), ka(
      this,
      e,
      Ra,
      Na,
      Ta,
      {
        filetype: 0,
        dragging: 20,
        boundedheight: 3,
        center: 4,
        flex: 5,
        file_count: 6,
        disable_click: 7,
        root: 8,
        hidden: 9,
        format: 21,
        uploading: 1,
        hidden_upload: 2,
        show_progress: 10,
        max_file_size: 22,
        upload: 23,
        stream_handler: 11,
        paste_clipboard: 12,
        open_file_upload: 13,
        load_files: 24
      },
      null,
      [-1, -1]
    );
  }
  get paste_clipboard() {
    return this.$$.ctx[12];
  }
  get open_file_upload() {
    return this.$$.ctx[13];
  }
  get load_files() {
    return this.$$.ctx[24];
  }
}
const {
  SvelteComponent: Pa,
  assign: Fa,
  children: Ua,
  claim_element: za,
  create_slot: qa,
  detach: ml,
  element: Ba,
  get_all_dirty_from_scope: Ha,
  get_slot_changes: Wa,
  get_spread_update: Va,
  init: Ga,
  insert_hydration: ja,
  safe_not_equal: Ya,
  set_dynamic_element_data: hl,
  set_style: ye,
  toggle_class: Ge,
  transition_in: So,
  transition_out: Do,
  update_slot_base: Xa
} = window.__gradio__svelte__internal;
function Za(n) {
  let e, t, i;
  const l = (
    /*#slots*/
    n[22].default
  ), o = qa(
    l,
    n,
    /*$$scope*/
    n[21],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      n[10]
    ) },
    { id: (
      /*elem_id*/
      n[5]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[6].join(" ") + " svelte-1ezsyiy"
    }
  ], r = {};
  for (let s = 0; s < a.length; s += 1)
    r = Fa(r, a[s]);
  return {
    c() {
      e = Ba(
        /*tag*/
        n[18]
      ), o && o.c(), this.h();
    },
    l(s) {
      e = za(
        s,
        /*tag*/
        (n[18] || "null").toUpperCase(),
        {
          "data-testid": !0,
          id: !0,
          class: !0
        }
      );
      var f = Ua(e);
      o && o.l(f), f.forEach(ml), this.h();
    },
    h() {
      hl(
        /*tag*/
        n[18]
      )(e, r), Ge(
        e,
        "hidden",
        /*visible*/
        n[13] === !1
      ), Ge(
        e,
        "padded",
        /*padding*/
        n[9]
      ), Ge(
        e,
        "flex",
        /*flex*/
        n[0]
      ), Ge(
        e,
        "border_focus",
        /*border_mode*/
        n[8] === "focus"
      ), Ge(
        e,
        "border_contrast",
        /*border_mode*/
        n[8] === "contrast"
      ), Ge(e, "hide-container", !/*explicit_call*/
      n[11] && !/*container*/
      n[12]), ye(
        e,
        "height",
        /*get_dimension*/
        n[19](
          /*height*/
          n[1]
        )
      ), ye(
        e,
        "min-height",
        /*get_dimension*/
        n[19](
          /*min_height*/
          n[2]
        )
      ), ye(
        e,
        "max-height",
        /*get_dimension*/
        n[19](
          /*max_height*/
          n[3]
        )
      ), ye(e, "width", typeof /*width*/
      n[4] == "number" ? `calc(min(${/*width*/
      n[4]}px, 100%))` : (
        /*get_dimension*/
        n[19](
          /*width*/
          n[4]
        )
      )), ye(
        e,
        "border-style",
        /*variant*/
        n[7]
      ), ye(
        e,
        "overflow",
        /*allow_overflow*/
        n[14] ? (
          /*overflow_behavior*/
          n[15]
        ) : "hidden"
      ), ye(
        e,
        "flex-grow",
        /*scale*/
        n[16]
      ), ye(e, "min-width", `calc(min(${/*min_width*/
      n[17]}px, 100%))`), ye(e, "border-width", "var(--block-border-width)");
    },
    m(s, f) {
      ja(s, e, f), o && o.m(e, null), i = !0;
    },
    p(s, f) {
      o && o.p && (!i || f & /*$$scope*/
      2097152) && Xa(
        o,
        l,
        s,
        /*$$scope*/
        s[21],
        i ? Wa(
          l,
          /*$$scope*/
          s[21],
          f,
          null
        ) : Ha(
          /*$$scope*/
          s[21]
        ),
        null
      ), hl(
        /*tag*/
        s[18]
      )(e, r = Va(a, [
        (!i || f & /*test_id*/
        1024) && { "data-testid": (
          /*test_id*/
          s[10]
        ) },
        (!i || f & /*elem_id*/
        32) && { id: (
          /*elem_id*/
          s[5]
        ) },
        (!i || f & /*elem_classes*/
        64 && t !== (t = "block " + /*elem_classes*/
        s[6].join(" ") + " svelte-1ezsyiy")) && { class: t }
      ])), Ge(
        e,
        "hidden",
        /*visible*/
        s[13] === !1
      ), Ge(
        e,
        "padded",
        /*padding*/
        s[9]
      ), Ge(
        e,
        "flex",
        /*flex*/
        s[0]
      ), Ge(
        e,
        "border_focus",
        /*border_mode*/
        s[8] === "focus"
      ), Ge(
        e,
        "border_contrast",
        /*border_mode*/
        s[8] === "contrast"
      ), Ge(e, "hide-container", !/*explicit_call*/
      s[11] && !/*container*/
      s[12]), f & /*height*/
      2 && ye(
        e,
        "height",
        /*get_dimension*/
        s[19](
          /*height*/
          s[1]
        )
      ), f & /*min_height*/
      4 && ye(
        e,
        "min-height",
        /*get_dimension*/
        s[19](
          /*min_height*/
          s[2]
        )
      ), f & /*max_height*/
      8 && ye(
        e,
        "max-height",
        /*get_dimension*/
        s[19](
          /*max_height*/
          s[3]
        )
      ), f & /*width*/
      16 && ye(e, "width", typeof /*width*/
      s[4] == "number" ? `calc(min(${/*width*/
      s[4]}px, 100%))` : (
        /*get_dimension*/
        s[19](
          /*width*/
          s[4]
        )
      )), f & /*variant*/
      128 && ye(
        e,
        "border-style",
        /*variant*/
        s[7]
      ), f & /*allow_overflow, overflow_behavior*/
      49152 && ye(
        e,
        "overflow",
        /*allow_overflow*/
        s[14] ? (
          /*overflow_behavior*/
          s[15]
        ) : "hidden"
      ), f & /*scale*/
      65536 && ye(
        e,
        "flex-grow",
        /*scale*/
        s[16]
      ), f & /*min_width*/
      131072 && ye(e, "min-width", `calc(min(${/*min_width*/
      s[17]}px, 100%))`);
    },
    i(s) {
      i || (So(o, s), i = !0);
    },
    o(s) {
      Do(o, s), i = !1;
    },
    d(s) {
      s && ml(e), o && o.d(s);
    }
  };
}
function Ka(n) {
  let e, t = (
    /*tag*/
    n[18] && Za(n)
  );
  return {
    c() {
      t && t.c();
    },
    l(i) {
      t && t.l(i);
    },
    m(i, l) {
      t && t.m(i, l), e = !0;
    },
    p(i, [l]) {
      /*tag*/
      i[18] && t.p(i, l);
    },
    i(i) {
      e || (So(t, i), e = !0);
    },
    o(i) {
      Do(t, i), e = !1;
    },
    d(i) {
      t && t.d(i);
    }
  };
}
function Ja(n, e, t) {
  let { $$slots: i = {}, $$scope: l } = e, { height: o = void 0 } = e, { min_height: a = void 0 } = e, { max_height: r = void 0 } = e, { width: s = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: _ = [] } = e, { variant: d = "solid" } = e, { border_mode: c = "base" } = e, { padding: u = !0 } = e, { type: h = "normal" } = e, { test_id: w = void 0 } = e, { explicit_call: T = !1 } = e, { container: k = !0 } = e, { visible: v = !0 } = e, { allow_overflow: g = !0 } = e, { overflow_behavior: b = "auto" } = e, { scale: O = null } = e, { min_width: P = 0 } = e, { flex: U = !1 } = e;
  v || (U = !1);
  let Y = h === "fieldset" ? "fieldset" : "div";
  const F = (C) => {
    if (C !== void 0) {
      if (typeof C == "number")
        return C + "px";
      if (typeof C == "string")
        return C;
    }
  };
  return n.$$set = (C) => {
    "height" in C && t(1, o = C.height), "min_height" in C && t(2, a = C.min_height), "max_height" in C && t(3, r = C.max_height), "width" in C && t(4, s = C.width), "elem_id" in C && t(5, f = C.elem_id), "elem_classes" in C && t(6, _ = C.elem_classes), "variant" in C && t(7, d = C.variant), "border_mode" in C && t(8, c = C.border_mode), "padding" in C && t(9, u = C.padding), "type" in C && t(20, h = C.type), "test_id" in C && t(10, w = C.test_id), "explicit_call" in C && t(11, T = C.explicit_call), "container" in C && t(12, k = C.container), "visible" in C && t(13, v = C.visible), "allow_overflow" in C && t(14, g = C.allow_overflow), "overflow_behavior" in C && t(15, b = C.overflow_behavior), "scale" in C && t(16, O = C.scale), "min_width" in C && t(17, P = C.min_width), "flex" in C && t(0, U = C.flex), "$$scope" in C && t(21, l = C.$$scope);
  }, [
    U,
    o,
    a,
    r,
    s,
    f,
    _,
    d,
    c,
    u,
    w,
    T,
    k,
    v,
    g,
    b,
    O,
    P,
    Y,
    F,
    h,
    l,
    i
  ];
}
class Qa extends Pa {
  constructor(e) {
    super(), Ga(this, e, Ja, Ka, Ya, {
      height: 1,
      min_height: 2,
      max_height: 3,
      width: 4,
      elem_id: 5,
      elem_classes: 6,
      variant: 7,
      border_mode: 8,
      padding: 9,
      type: 20,
      test_id: 10,
      explicit_call: 11,
      container: 12,
      visible: 13,
      allow_overflow: 14,
      overflow_behavior: 15,
      scale: 16,
      min_width: 17,
      flex: 0
    });
  }
}
const {
  SvelteComponent: xa,
  append_hydration: Ui,
  attr: kt,
  bubble: $a,
  check_outros: es,
  children: zi,
  claim_component: ts,
  claim_element: qi,
  claim_space: ns,
  claim_text: is,
  construct_svelte_component: gl,
  create_component: bl,
  destroy_component: pl,
  detach: Fn,
  element: Bi,
  group_outros: ls,
  init: os,
  insert_hydration: Co,
  listen: as,
  mount_component: vl,
  safe_not_equal: ss,
  set_data: rs,
  set_style: Zn,
  space: fs,
  text: us,
  toggle_class: Pe,
  transition_in: wl,
  transition_out: kl
} = window.__gradio__svelte__internal;
function yl(n) {
  let e, t;
  return {
    c() {
      e = Bi("span"), t = us(
        /*label*/
        n[1]
      ), this.h();
    },
    l(i) {
      e = qi(i, "SPAN", { class: !0 });
      var l = zi(e);
      t = is(
        l,
        /*label*/
        n[1]
      ), l.forEach(Fn), this.h();
    },
    h() {
      kt(e, "class", "svelte-vk34kx");
    },
    m(i, l) {
      Co(i, e, l), Ui(e, t);
    },
    p(i, l) {
      l & /*label*/
      2 && rs(
        t,
        /*label*/
        i[1]
      );
    },
    d(i) {
      i && Fn(e);
    }
  };
}
function cs(n) {
  let e, t, i, l, o, a, r, s = (
    /*show_label*/
    n[2] && yl(n)
  );
  var f = (
    /*Icon*/
    n[0]
  );
  function _(d, c) {
    return {};
  }
  return f && (l = gl(f, _())), {
    c() {
      e = Bi("button"), s && s.c(), t = fs(), i = Bi("div"), l && bl(l.$$.fragment), this.h();
    },
    l(d) {
      e = qi(d, "BUTTON", {
        "aria-label": !0,
        "aria-haspopup": !0,
        title: !0,
        class: !0
      });
      var c = zi(e);
      s && s.l(c), t = ns(c), i = qi(c, "DIV", { class: !0 });
      var u = zi(i);
      l && ts(l.$$.fragment, u), u.forEach(Fn), c.forEach(Fn), this.h();
    },
    h() {
      kt(i, "class", "svelte-vk34kx"), Pe(
        i,
        "small",
        /*size*/
        n[4] === "small"
      ), Pe(
        i,
        "large",
        /*size*/
        n[4] === "large"
      ), Pe(
        i,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], kt(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), kt(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), kt(
        e,
        "title",
        /*label*/
        n[1]
      ), kt(e, "class", "svelte-vk34kx"), Pe(
        e,
        "pending",
        /*pending*/
        n[3]
      ), Pe(
        e,
        "padded",
        /*padded*/
        n[5]
      ), Pe(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), Pe(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), Zn(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[11] ? (
        /*_color*/
        n[11]
      ) : "var(--block-label-text-color)"), Zn(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      ));
    },
    m(d, c) {
      Co(d, e, c), s && s.m(e, null), Ui(e, t), Ui(e, i), l && vl(l, i, null), o = !0, a || (r = as(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), a = !0);
    },
    p(d, [c]) {
      if (/*show_label*/
      d[2] ? s ? s.p(d, c) : (s = yl(d), s.c(), s.m(e, t)) : s && (s.d(1), s = null), c & /*Icon*/
      1 && f !== (f = /*Icon*/
      d[0])) {
        if (l) {
          ls();
          const u = l;
          kl(u.$$.fragment, 1, 0, () => {
            pl(u, 1);
          }), es();
        }
        f ? (l = gl(f, _()), bl(l.$$.fragment), wl(l.$$.fragment, 1), vl(l, i, null)) : l = null;
      }
      (!o || c & /*size*/
      16) && Pe(
        i,
        "small",
        /*size*/
        d[4] === "small"
      ), (!o || c & /*size*/
      16) && Pe(
        i,
        "large",
        /*size*/
        d[4] === "large"
      ), (!o || c & /*size*/
      16) && Pe(
        i,
        "medium",
        /*size*/
        d[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      d[7]), (!o || c & /*label*/
      2) && kt(
        e,
        "aria-label",
        /*label*/
        d[1]
      ), (!o || c & /*hasPopup*/
      256) && kt(
        e,
        "aria-haspopup",
        /*hasPopup*/
        d[8]
      ), (!o || c & /*label*/
      2) && kt(
        e,
        "title",
        /*label*/
        d[1]
      ), (!o || c & /*pending*/
      8) && Pe(
        e,
        "pending",
        /*pending*/
        d[3]
      ), (!o || c & /*padded*/
      32) && Pe(
        e,
        "padded",
        /*padded*/
        d[5]
      ), (!o || c & /*highlight*/
      64) && Pe(
        e,
        "highlight",
        /*highlight*/
        d[6]
      ), (!o || c & /*transparent*/
      512) && Pe(
        e,
        "transparent",
        /*transparent*/
        d[9]
      ), c & /*disabled, _color*/
      2176 && Zn(e, "color", !/*disabled*/
      d[7] && /*_color*/
      d[11] ? (
        /*_color*/
        d[11]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && Zn(e, "--bg-color", /*disabled*/
      d[7] ? "auto" : (
        /*background*/
        d[10]
      ));
    },
    i(d) {
      o || (l && wl(l.$$.fragment, d), o = !0);
    },
    o(d) {
      l && kl(l.$$.fragment, d), o = !1;
    },
    d(d) {
      d && Fn(e), s && s.d(), l && pl(l), a = !1, r();
    }
  };
}
function _s(n, e, t) {
  let i, { Icon: l } = e, { label: o = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: f = !0 } = e, { highlight: _ = !1 } = e, { disabled: d = !1 } = e, { hasPopup: c = !1 } = e, { color: u = "var(--block-label-text-color)" } = e, { transparent: h = !1 } = e, { background: w = "var(--block-background-fill)" } = e;
  function T(k) {
    $a.call(this, n, k);
  }
  return n.$$set = (k) => {
    "Icon" in k && t(0, l = k.Icon), "label" in k && t(1, o = k.label), "show_label" in k && t(2, a = k.show_label), "pending" in k && t(3, r = k.pending), "size" in k && t(4, s = k.size), "padded" in k && t(5, f = k.padded), "highlight" in k && t(6, _ = k.highlight), "disabled" in k && t(7, d = k.disabled), "hasPopup" in k && t(8, c = k.hasPopup), "color" in k && t(12, u = k.color), "transparent" in k && t(9, h = k.transparent), "background" in k && t(10, w = k.background);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    4160 && t(11, i = _ ? "var(--color-accent)" : u);
  }, [
    l,
    o,
    a,
    r,
    s,
    f,
    _,
    d,
    c,
    h,
    w,
    i,
    u,
    T
  ];
}
class ds extends xa {
  constructor(e) {
    super(), os(this, e, _s, cs, ss, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 12,
      transparent: 9,
      background: 10
    });
  }
}
const {
  SvelteComponent: ms,
  append_hydration: wi,
  attr: et,
  children: Kn,
  claim_svg_element: Jn,
  detach: Dn,
  init: hs,
  insert_hydration: gs,
  noop: ki,
  safe_not_equal: bs,
  set_style: ct,
  svg_element: Qn
} = window.__gradio__svelte__internal;
function ps(n) {
  let e, t, i, l;
  return {
    c() {
      e = Qn("svg"), t = Qn("g"), i = Qn("path"), l = Qn("path"), this.h();
    },
    l(o) {
      e = Jn(o, "svg", {
        width: !0,
        height: !0,
        viewBox: !0,
        version: !0,
        xmlns: !0,
        "xmlns:xlink": !0,
        "xml:space": !0,
        stroke: !0,
        style: !0
      });
      var a = Kn(e);
      t = Jn(a, "g", { transform: !0 });
      var r = Kn(t);
      i = Jn(r, "path", { d: !0, style: !0 }), Kn(i).forEach(Dn), r.forEach(Dn), l = Jn(a, "path", { d: !0, style: !0 }), Kn(l).forEach(Dn), a.forEach(Dn), this.h();
    },
    h() {
      et(i, "d", "M18,6L6.087,17.913"), ct(i, "fill", "none"), ct(i, "fill-rule", "nonzero"), ct(i, "stroke-width", "2px"), et(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), et(l, "d", "M4.364,4.364L19.636,19.636"), ct(l, "fill", "none"), ct(l, "fill-rule", "nonzero"), ct(l, "stroke-width", "2px"), et(e, "width", "100%"), et(e, "height", "100%"), et(e, "viewBox", "0 0 24 24"), et(e, "version", "1.1"), et(e, "xmlns", "http://www.w3.org/2000/svg"), et(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), et(e, "xml:space", "preserve"), et(e, "stroke", "currentColor"), ct(e, "fill-rule", "evenodd"), ct(e, "clip-rule", "evenodd"), ct(e, "stroke-linecap", "round"), ct(e, "stroke-linejoin", "round");
    },
    m(o, a) {
      gs(o, e, a), wi(e, t), wi(t, i), wi(e, l);
    },
    p: ki,
    i: ki,
    o: ki,
    d(o) {
      o && Dn(e);
    }
  };
}
class vs extends ms {
  constructor(e) {
    super(), hs(this, e, null, ps, bs, {});
  }
}
const ws = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], El = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
ws.reduce(
  (n, { color: e, primary: t, secondary: i }) => ({
    ...n,
    [e]: {
      primary: El[e][t],
      secondary: El[e][i]
    }
  }),
  {}
);
const { tick: ks } = window.__gradio__svelte__internal;
async function Hi(n, e, t, i) {
  if (await ks(), i || e === t) return;
  const l = window.getComputedStyle(n), o = parseFloat(l.paddingTop), a = parseFloat(l.paddingBottom), r = parseFloat(l.lineHeight);
  let s = t === void 0 ? !1 : o + a + r * t, f = o + a + e * r;
  n.style.height = "1px";
  let _;
  s && n.scrollHeight > s ? _ = s : n.scrollHeight < f ? _ = f : _ = n.scrollHeight, n.style.height = `${_}px`;
}
function ys(n, e) {
  if (e.lines === e.max_lines) return;
  n.style.overflowY = "scroll";
  function t(i) {
    Hi(i.target, e.lines, e.max_lines, !1);
  }
  if (n.addEventListener("input", t), !!e.text.trim())
    return Hi(n, e.lines, e.max_lines, !1), {
      destroy: () => n.removeEventListener("input", t)
    };
}
function Es(n, e) {
  return n.addEventListener(
    "icegatheringstatechange",
    () => {
      console.debug(n.iceGatheringState);
    },
    !1
  ), n.addEventListener(
    "iceconnectionstatechange",
    () => {
      console.debug(n.iceConnectionState);
    },
    !1
  ), n.addEventListener(
    "signalingstatechange",
    () => {
      console.debug(n.signalingState);
    },
    !1
  ), n.addEventListener("track", (t) => {
    console.debug("track event listener"), e && e.srcObject !== t.streams[0] && (console.debug("streams", t.streams), e.srcObject = t.streams[0], console.debug("node.srcOject", e.srcObject), t.track.kind === "audio" && (e.volume = 1, e.muted = !1, e.autoplay = !0, console.debug(e), console.debug("autoplay track"), e.play().catch((i) => console.debug("Autoplay failed:", i))));
  }), n;
}
async function Ts(n, e, t, i, l, o = "video", a = () => {
}, r = {}) {
  e = Es(e, t);
  const s = e.createDataChannel("text");
  return s.onopen = () => {
    console.debug("Data channel is open"), s.send("handshake");
  }, s.onmessage = (f) => {
    console.debug("Received message:", f.data), (f.data === "change" || f.data === "tick" || f.data === "stopword") && (console.debug(`${f.data} event received`), console.debug(`${f}`), a(f.data));
  }, n ? n.getTracks().forEach(async (f) => {
    console.debug("Track stream callback", f);
    const _ = e.addTrack(f, n), c = { ..._.getParameters(), ...r };
    await _.setParameters(c), console.debug("sender params", _.getParameters());
  }) : (console.debug("Creating transceiver!"), e.addTransceiver(o, { direction: "recvonly" })), await Ss(e, i, l), e;
}
function As(n, e) {
  return new Promise((t, i) => {
    n(e).then((l) => {
      console.debug("data", l), (l == null ? void 0 : l.status) === "failed" && (console.debug("rejecting"), i("error")), t(l);
    });
  });
}
async function Ss(n, e, t) {
  return n.createOffer().then((i) => n.setLocalDescription(i)).then(() => new Promise((i) => {
    if (console.debug("ice gathering state", n.iceGatheringState), n.iceGatheringState === "complete")
      i();
    else {
      const l = () => {
        n.iceGatheringState === "complete" && (console.debug("ice complete"), n.removeEventListener("icegatheringstatechange", l), i());
      };
      n.addEventListener("icegatheringstatechange", l);
    }
  })).then(() => {
    var i = n.localDescription;
    return As(e, {
      sdp: i.sdp,
      type: i.type,
      webrtc_id: t
    });
  }).then((i) => i).then((i) => n.setRemoteDescription(i));
}
function yi(n) {
  console.debug("Stopping peer connection"), n.getTransceivers && n.getTransceivers().forEach((e) => {
    e.stop && e.stop();
  }), n.getSenders() && n.getSenders().forEach((e) => {
    console.debug("sender", e), e.track && e.track.stop && e.track.stop();
  }), setTimeout(() => {
    n.close();
  }, 500);
}
function Ds() {
  return navigator.mediaDevices.enumerateDevices();
}
function Cs(n, e = "videoinput") {
  return n.filter(
    (i) => i.kind === e
  );
}
async function Ls(n) {
  const e = await navigator.mediaDevices.enumerateDevices();
  console.log("Devices:", e);
  const i = e.filter((l) => l.kind === "audiooutput").find(
    (l) => /headset|casque|earphone|headphones|AirPods/i.test(l.label)
  );
  if (i && typeof n.setSinkId == "function")
    try {
      await n.setSinkId(i.deviceId), console.log("Sortie audio définie sur le casque");
    } catch (l) {
      console.warn("Erreur setSinkId:", l);
    }
  else
    console.log("Casque non détecté ou setSinkId non supporté");
}
const {
  SvelteComponent: Is,
  append_hydration: Ei,
  attr: _t,
  children: bn,
  claim_element: Kt,
  claim_space: Ns,
  destroy_each: Lo,
  detach: Ke,
  element: Jt,
  empty: Tl,
  ensure_array_like: fi,
  init: Os,
  insert_hydration: kn,
  noop: Wi,
  safe_not_equal: Rs,
  set_style: ht,
  space: Ms,
  src_url_equal: Al
} = window.__gradio__svelte__internal, { onDestroy: Ps } = window.__gradio__svelte__internal;
function Sl(n, e, t) {
  const i = n.slice();
  return i[17] = e[t], i;
}
function Dl(n, e, t) {
  const i = n.slice();
  return i[17] = e[t], i[19] = t, i;
}
function Fs(n) {
  let e, t = fi(Array(
    /*numBars*/
    n[0]
  )), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = Cl(Sl(n, t, l));
  return {
    c() {
      e = Jt("div");
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      this.h();
    },
    l(l) {
      e = Kt(l, "DIV", { class: !0 });
      var o = bn(e);
      for (let a = 0; a < i.length; a += 1)
        i[a].l(o);
      o.forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "gradio-audio-boxContainer svelte-1cqbdpi"), ht(
        e,
        "width",
        /*containerWidth*/
        n[6]
      );
    },
    m(l, o) {
      kn(l, e, o);
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(e, null);
    },
    p(l, o) {
      if (o & /*numBars*/
      1) {
        t = fi(Array(
          /*numBars*/
          l[0]
        ));
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = Sl(l, t, a);
          i[a] ? i[a].p(r, o) : (i[a] = Cl(), i[a].c(), i[a].m(e, null));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
      o & /*containerWidth*/
      64 && ht(
        e,
        "width",
        /*containerWidth*/
        l[6]
      );
    },
    d(l) {
      l && Ke(e), Lo(i, l);
    }
  };
}
function Us(n) {
  let e, t, i, l, o, a = (
    /*pulseIntensity*/
    n[5] > 0 && Ll(n)
  );
  return {
    c() {
      e = Jt("div"), a && a.c(), t = Ms(), i = Jt("div"), l = Jt("img"), this.h();
    },
    l(r) {
      e = Kt(r, "DIV", { class: !0 });
      var s = bn(e);
      a && a.l(s), t = Ns(s), i = Kt(s, "DIV", { class: !0 });
      var f = bn(i);
      l = Kt(f, "IMG", { src: !0, alt: !0, class: !0 }), f.forEach(Ke), s.forEach(Ke), this.h();
    },
    h() {
      Al(l.src, o = /*icon*/
      n[1]) || _t(l, "src", o), _t(l, "alt", "Audio visualization icon"), _t(l, "class", "icon-image svelte-1cqbdpi"), _t(i, "class", "gradio-audio-icon svelte-1cqbdpi"), ht(i, "transform", `scale(${/*pulseScale*/
      n[4]})`), ht(
        i,
        "background",
        /*icon_button_color*/
        n[2]
      ), _t(e, "class", "gradio-audio-icon-container svelte-1cqbdpi");
    },
    m(r, s) {
      kn(r, e, s), a && a.m(e, null), Ei(e, t), Ei(e, i), Ei(i, l);
    },
    p(r, s) {
      /*pulseIntensity*/
      r[5] > 0 ? a ? a.p(r, s) : (a = Ll(r), a.c(), a.m(e, t)) : a && (a.d(1), a = null), s & /*icon*/
      2 && !Al(l.src, o = /*icon*/
      r[1]) && _t(l, "src", o), s & /*pulseScale*/
      16 && ht(i, "transform", `scale(${/*pulseScale*/
      r[4]})`), s & /*icon_button_color*/
      4 && ht(
        i,
        "background",
        /*icon_button_color*/
        r[2]
      );
    },
    d(r) {
      r && Ke(e), a && a.d();
    }
  };
}
function Cl(n) {
  let e;
  return {
    c() {
      e = Jt("div"), this.h();
    },
    l(t) {
      e = Kt(t, "DIV", { class: !0, style: !0 }), bn(e).forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "gradio-audio-box svelte-1cqbdpi"), ht(e, "transform", "scaleY(0.1)");
    },
    m(t, i) {
      kn(t, e, i);
    },
    p: Wi,
    d(t) {
      t && Ke(e);
    }
  };
}
function Ll(n) {
  let e, t = fi(Array(3)), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = Il(Dl(n, t, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      e = Tl();
    },
    l(l) {
      for (let o = 0; o < i.length; o += 1)
        i[o].l(l);
      e = Tl();
    },
    m(l, o) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, o);
      kn(l, e, o);
    },
    p(l, o) {
      if (o & /*pulse_color*/
      8) {
        t = fi(Array(3));
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = Dl(l, t, a);
          i[a] ? i[a].p(r, o) : (i[a] = Il(r), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(l) {
      l && Ke(e), Lo(i, l);
    }
  };
}
function Il(n) {
  let e;
  return {
    c() {
      e = Jt("div"), this.h();
    },
    l(t) {
      e = Kt(t, "DIV", { class: !0 }), bn(e).forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "pulse-ring svelte-1cqbdpi"), ht(
        e,
        "background",
        /*pulse_color*/
        n[3]
      ), ht(e, "animation-delay", `${/*i*/
      n[19] * 0.4}s`);
    },
    m(t, i) {
      kn(t, e, i);
    },
    p(t, i) {
      i & /*pulse_color*/
      8 && ht(
        e,
        "background",
        /*pulse_color*/
        t[3]
      );
    },
    d(t) {
      t && Ke(e);
    }
  };
}
function zs(n) {
  let e;
  function t(o, a) {
    return (
      /*icon*/
      o[1] ? Us : Fs
    );
  }
  let i = t(n), l = i(n);
  return {
    c() {
      e = Jt("div"), l.c(), this.h();
    },
    l(o) {
      e = Kt(o, "DIV", { class: !0 });
      var a = bn(e);
      l.l(a), a.forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "gradio-audio-waveContainer svelte-1cqbdpi");
    },
    m(o, a) {
      kn(o, e, a), l.m(e, null);
    },
    p(o, [a]) {
      i === (i = t(o)) && l ? l.p(o, a) : (l.d(1), l = i(o), l && (l.c(), l.m(e, null)));
    },
    i: Wi,
    o: Wi,
    d(o) {
      o && Ke(e), l.d();
    }
  };
}
function qs(n, e, t) {
  let i;
  var l = this && this.__awaiter || function(b, O, P, U) {
    function Y(F) {
      return F instanceof P ? F : new P(function(C) {
        C(F);
      });
    }
    return new (P || (P = Promise))(function(F, C) {
      function J(H) {
        try {
          ne(U.next(H));
        } catch (ie) {
          C(ie);
        }
      }
      function q(H) {
        try {
          ne(U.throw(H));
        } catch (ie) {
          C(ie);
        }
      }
      function ne(H) {
        H.done ? F(H.value) : Y(H.value).then(J, q);
      }
      ne((U = U.apply(b, O || [])).next());
    });
  };
  let { numBars: o = 16 } = e, { stream_state: a = "closed" } = e, { audio_source_callback: r } = e, { icon: s = void 0 } = e, { icon_button_color: f = "var(--body-text-color)" } = e, { pulse_color: _ = "var(--body-text-color)" } = e, d, c, u, h, w = 1, T = 0;
  Ps(() => {
    h && cancelAnimationFrame(h), d && d.close();
  });
  function k() {
    return l(this, void 0, void 0, function* () {
      const b = new (window.AudioContext || window.webkitAudioContext)(), O = yield navigator.mediaDevices.getUserMedia({ audio: !0 }), P = yield r(), U = b.createMediaStreamSource(O), Y = b.createMediaStreamSource(P), F = b.createMediaStreamDestination();
      return U.connect(F), Y.connect(F), F.stream;
    });
  }
  function v() {
    return l(this, void 0, void 0, function* () {
      d = new (window.AudioContext || window.webkitAudioContext)(), c = d.createAnalyser();
      const b = yield k();
      d.createMediaStreamSource(b).connect(c), c.fftSize = 64, c.smoothingTimeConstant = 0.8, u = new Uint8Array(c.frequencyBinCount), g();
    });
  }
  function g() {
    if (c.getByteFrequencyData(u), s) {
      const O = Array.from(u).reduce((P, U) => P + U, 0) / u.length / 255;
      t(4, w = 1 + O * 0.15), t(5, T = O);
    } else {
      const b = document.querySelectorAll(".gradio-audio-waveContainer .gradio-audio-box");
      for (let O = 0; O < b.length; O++) {
        const P = u[O] / 255;
        b[O].style.transform = `scaleY(${Math.max(0.1, P)})`;
      }
    }
    h = requestAnimationFrame(g);
  }
  return n.$$set = (b) => {
    "numBars" in b && t(0, o = b.numBars), "stream_state" in b && t(7, a = b.stream_state), "audio_source_callback" in b && t(8, r = b.audio_source_callback), "icon" in b && t(1, s = b.icon), "icon_button_color" in b && t(2, f = b.icon_button_color), "pulse_color" in b && t(3, _ = b.pulse_color);
  }, n.$$.update = () => {
    n.$$.dirty & /*icon, numBars*/
    3 && t(6, i = s ? "128px" : `calc((var(--boxSize) + var(--gutter)) * ${o})`), n.$$.dirty & /*stream_state*/
    128 && a === "open" && v();
  }, [
    o,
    s,
    f,
    _,
    w,
    T,
    i,
    a,
    r
  ];
}
class Bs extends Is {
  constructor(e) {
    super(), Os(this, e, qs, zs, Rs, {
      numBars: 0,
      stream_state: 7,
      audio_source_callback: 8,
      icon: 1,
      icon_button_color: 2,
      pulse_color: 3
    });
  }
}
const {
  SvelteComponent: Hs,
  append_hydration: It,
  attr: V,
  binding_callbacks: Nl,
  check_outros: Io,
  children: ot,
  claim_component: Ws,
  claim_element: pn,
  claim_space: No,
  claim_svg_element: cn,
  create_component: Vs,
  destroy_component: Gs,
  detach: Ee,
  element: vn,
  get_svelte_dataset: js,
  group_outros: Oo,
  init: Ys,
  insert_hydration: wn,
  listen: ui,
  mount_component: Xs,
  noop: Un,
  run_all: Zs,
  safe_not_equal: Ks,
  space: Ro,
  svg_element: _n,
  toggle_class: ci,
  transition_in: qn,
  transition_out: Bn
} = window.__gradio__svelte__internal, { createEventDispatcher: Js, onMount: Qs } = window.__gradio__svelte__internal;
function xs(n) {
  let e, t, i, l, o, a, r, s, f;
  const _ = [tr, er], d = [];
  function c(u, h) {
    return (
      /*stream_state*/
      u[8] === "open" ? 0 : 1
    );
  }
  return e = c(n), t = d[e] = _[e](n), {
    c() {
      t.c(), i = Ro(), l = vn("button"), o = _n("svg"), a = _n("rect"), this.h();
    },
    l(u) {
      t.l(u), i = No(u), l = pn(u, "BUTTON", { class: !0, title: !0 });
      var h = ot(l);
      o = cn(h, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var w = ot(o);
      a = cn(w, "rect", {
        x: !0,
        y: !0,
        width: !0,
        height: !0,
        rx: !0,
        ry: !0
      }), ot(a).forEach(Ee), w.forEach(Ee), h.forEach(Ee), this.h();
    },
    h() {
      V(a, "x", "8"), V(a, "y", "8"), V(a, "width", "8"), V(a, "height", "8"), V(a, "rx", "1"), V(a, "ry", "1"), V(o, "xmlns", "http://www.w3.org/2000/svg"), V(o, "width", "100%"), V(o, "height", "100%"), V(o, "viewBox", "0 0 24 24"), V(o, "stroke-linecap", "round"), V(o, "stroke-linejoin", "round"), V(o, "class", "svelte-gqmcuu"), V(l, "class", "stop-audio-button svelte-gqmcuu"), V(
        l,
        "title",
        /*stop_audio_btn_title*/
        n[6]
      ), l.disabled = /*disabled*/
      n[7];
    },
    m(u, h) {
      d[e].m(u, h), wn(u, i, h), wn(u, l, h), It(l, o), It(o, a), r = !0, s || (f = ui(
        l,
        "click",
        /*handle_end_streaming_click*/
        n[14]
      ), s = !0);
    },
    p(u, h) {
      let w = e;
      e = c(u), e === w ? d[e].p(u, h) : (Oo(), Bn(d[w], 1, 1, () => {
        d[w] = null;
      }), Io(), t = d[e], t ? t.p(u, h) : (t = d[e] = _[e](u), t.c()), qn(t, 1), t.m(i.parentNode, i)), (!r || h[0] & /*stop_audio_btn_title*/
      64) && V(
        l,
        "title",
        /*stop_audio_btn_title*/
        u[6]
      ), (!r || h[0] & /*disabled*/
      128) && (l.disabled = /*disabled*/
      u[7]);
    },
    i(u) {
      r || (qn(t), r = !0);
    },
    o(u) {
      Bn(t), r = !1;
    },
    d(u) {
      u && (Ee(i), Ee(l)), d[e].d(u), s = !1, f();
    }
  };
}
function $s(n) {
  let e, t, i, l, o, a, r;
  return {
    c() {
      e = vn("button"), t = _n("svg"), i = _n("path"), l = _n("path"), o = _n("line"), this.h();
    },
    l(s) {
      e = pn(s, "BUTTON", { class: !0, title: !0 });
      var f = ot(e);
      t = cn(f, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        fill: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0
      });
      var _ = ot(t);
      i = cn(_, "path", { d: !0 }), ot(i).forEach(Ee), l = cn(_, "path", { d: !0 }), ot(l).forEach(Ee), o = cn(_, "line", { x1: !0, x2: !0, y1: !0, y2: !0 }), ot(o).forEach(Ee), _.forEach(Ee), f.forEach(Ee), this.h();
    },
    h() {
      V(i, "d", "M12 4a2.4 2.4 0 0 0-2.4 2.4v5.6a2.4 2.4 0 0 0 4.8 0V6.4a2.4 2.4 0 0 0-2.4-2.4Z"), V(l, "d", "M17.6 10.4v1.6a5.6 5.6 0 0 1-11.2 0v-1.6"), V(o, "x1", "12"), V(o, "x2", "12"), V(o, "y1", "17.6"), V(o, "y2", "20"), V(t, "xmlns", "http://www.w3.org/2000/svg"), V(t, "width", "100%"), V(t, "height", "100%"), V(t, "viewBox", "0 0 24 24"), V(t, "fill", "none"), V(t, "stroke", "currentColor"), V(t, "stroke-width", "1.5"), V(t, "stroke-linecap", "round"), V(t, "stroke-linejoin", "round"), V(e, "class", "audio-button svelte-gqmcuu"), V(
        e,
        "title",
        /*audio_btn_title*/
        n[5]
      ), e.disabled = /*disabled*/
      n[7], ci(
        e,
        "padded-button",
        /*audio_btn*/
        n[4] !== !0
      );
    },
    m(s, f) {
      wn(s, e, f), It(e, t), It(t, i), It(t, l), It(t, o), a || (r = ui(
        e,
        "click",
        /*handle_audio_click*/
        n[13]
      ), a = !0);
    },
    p(s, f) {
      f[0] & /*audio_btn_title*/
      32 && V(
        e,
        "title",
        /*audio_btn_title*/
        s[5]
      ), f[0] & /*disabled*/
      128 && (e.disabled = /*disabled*/
      s[7]), f[0] & /*audio_btn*/
      16 && ci(
        e,
        "padded-button",
        /*audio_btn*/
        s[4] !== !0
      );
    },
    i: Un,
    o: Un,
    d(s) {
      s && Ee(e), a = !1, r();
    }
  };
}
function er(n) {
  let e, t = '<span class="svelte-gqmcuu">·</span><span class="svelte-gqmcuu">·</span><span class="svelte-gqmcuu">·</span>';
  return {
    c() {
      e = vn("div"), e.innerHTML = t, this.h();
    },
    l(i) {
      e = pn(i, "DIV", { class: !0, "data-svelte-h": !0 }), js(e) !== "svelte-y8y9ab" && (e.innerHTML = t), this.h();
    },
    h() {
      V(e, "class", "audio-blinker svelte-gqmcuu");
    },
    m(i, l) {
      wn(i, e, l);
    },
    p: Un,
    i: Un,
    o: Un,
    d(i) {
      i && Ee(e);
    }
  };
}
function tr(n) {
  let e, t, i;
  return t = new Bs({
    props: {
      audio_source_callback: (
        /*audio_source_callback*/
        n[11]
      ),
      stream_state: (
        /*stream_state*/
        n[8]
      ),
      icon: (
        /*icon*/
        n[1]
      ),
      icon_button_color: (
        /*icon_button_color*/
        n[2]
      ),
      pulse_color: (
        /*pulse_color*/
        n[3]
      )
    }
  }), {
    c() {
      e = vn("div"), Vs(t.$$.fragment), this.h();
    },
    l(l) {
      e = pn(l, "DIV", { class: !0 });
      var o = ot(e);
      Ws(t.$$.fragment, o), o.forEach(Ee), this.h();
    },
    h() {
      V(e, "class", "audiowave svelte-gqmcuu");
    },
    m(l, o) {
      wn(l, e, o), Xs(t, e, null), i = !0;
    },
    p(l, o) {
      const a = {};
      o[0] & /*stream_state*/
      256 && (a.stream_state = /*stream_state*/
      l[8]), o[0] & /*icon*/
      2 && (a.icon = /*icon*/
      l[1]), o[0] & /*icon_button_color*/
      4 && (a.icon_button_color = /*icon_button_color*/
      l[2]), o[0] & /*pulse_color*/
      8 && (a.pulse_color = /*pulse_color*/
      l[3]), t.$set(a);
    },
    i(l) {
      i || (qn(t.$$.fragment, l), i = !0);
    },
    o(l) {
      Bn(t.$$.fragment, l), i = !1;
    },
    d(l) {
      l && Ee(e), Gs(t);
    }
  };
}
function nr(n) {
  let e, t, i, l, o, a, r, s, f;
  const _ = [$s, xs], d = [];
  function c(u, h) {
    return (
      /*audio_btn*/
      u[4] ? 0 : (
        /*stream_state*/
        u[8] === "open" || /*stream_state*/
        u[8] === "waiting" ? 1 : -1
      )
    );
  }
  return ~(l = c(n)) && (o = d[l] = _[l](n)), {
    c() {
      e = vn("div"), t = vn("audio"), i = Ro(), o && o.c(), this.h();
    },
    l(u) {
      e = pn(u, "DIV", { class: !0 });
      var h = ot(e);
      t = pn(h, "AUDIO", { class: !0 }), ot(t).forEach(Ee), i = No(h), o && o.l(h), h.forEach(Ee), this.h();
    },
    h() {
      V(t, "class", "standard-player svelte-gqmcuu"), ci(
        t,
        "hidden",
        /*value*/
        n[0] === "__webrtc_value__"
      ), V(e, "class", a = "audio-container" + /*audio_btn*/
      (n[4] ? "" : " large") + " svelte-gqmcuu");
    },
    m(u, h) {
      wn(u, e, h), It(e, t), n[27](t), It(e, i), ~l && d[l].m(e, null), n[30](e), r = !0, s || (f = [
        ui(
          t,
          "ended",
          /*ended_handler*/
          n[28]
        ),
        ui(
          t,
          "play",
          /*play_handler*/
          n[29]
        )
      ], s = !0);
    },
    p(u, h) {
      (!r || h[0] & /*value*/
      1) && ci(
        t,
        "hidden",
        /*value*/
        u[0] === "__webrtc_value__"
      );
      let w = l;
      l = c(u), l === w ? ~l && d[l].p(u, h) : (o && (Oo(), Bn(d[w], 1, 1, () => {
        d[w] = null;
      }), Io()), ~l ? (o = d[l], o ? o.p(u, h) : (o = d[l] = _[l](u), o.c()), qn(o, 1), o.m(e, null)) : o = null), (!r || h[0] & /*audio_btn*/
      16 && a !== (a = "audio-container" + /*audio_btn*/
      (u[4] ? "" : " large") + " svelte-gqmcuu")) && V(e, "class", a);
    },
    i(u) {
      r || (qn(o), r = !0);
    },
    o(u) {
      Bn(o), r = !1;
    },
    d(u) {
      u && Ee(e), n[27](null), ~l && d[l].d(), n[30](null), s = !1, Zs(f);
    }
  };
}
function ir(n, e, t) {
  var i = this && this.__awaiter || function(D, Z, ee, y) {
    function M(W) {
      return W instanceof ee ? W : new ee(function(B) {
        B(W);
      });
    }
    return new (ee || (ee = Promise))(function(W, B) {
      function x(me) {
        try {
          _e(y.next(me));
        } catch (Ae) {
          B(Ae);
        }
      }
      function ce(me) {
        try {
          _e(y.throw(me));
        } catch (Ae) {
          B(Ae);
        }
      }
      function _e(me) {
        me.done ? W(me.value) : M(me.value).then(x, ce);
      }
      _e((y = y.apply(D, Z || [])).next());
    });
  };
  let { mode: l } = e, { value: o = null } = e, { rtc_configuration: a = null } = e, { i18n: r } = e, { time_limit: s = null } = e, { track_constraints: f = {} } = e, { rtp_params: _ = {} } = e, { on_change_cb: d } = e, { icon: c = void 0 } = e, { icon_button_color: u = "var(--body-text-color)" } = e, { pulse_color: h = "var(--body-text-color)" } = e, { audio_btn: w = !1 } = e, { audio_btn_title: T = "" } = e, { handle_audio_click_visibility: k = function() {
  } } = e, { stop_audio_btn_title: v = "" } = e, { handle_end_streaming_click_visibility: g = function() {
  } } = e, { disabled: b = !1 } = e, O = !1, P;
  Qs(() => {
    o === "__webrtc_value__" && t(26, P = new Audio("https://huggingface.co/datasets/freddyaboulton/bucket/resolve/main/pop-sounds.mp3"));
  });
  let U = (D) => {
    D === "stopword" ? (console.log("stopword recognized"), t(25, O = !0), setTimeout(
      () => {
        t(25, O = !1);
      },
      3e3
    )) : d(D);
  }, { server: Y } = e, F = "closed", C, J, q, ne = null, H, ie, re = null;
  const Oe = () => (console.log("stream in callback", H), l === "send" ? H : C.srcObject), de = Js();
  function ve() {
    return i(this, void 0, void 0, function* () {
      try {
        const Z = re ? Object.assign(
          {
            deviceId: { exact: re.deviceId }
          },
          f
        ) : f;
        H = yield navigator.mediaDevices.getUserMedia({ audio: Z });
      } catch (Z) {
        if (!navigator.mediaDevices) {
          de("error", r("audio.no_device_support"));
          return;
        }
        if (Z instanceof DOMException && Z.name == "NotAllowedError") {
          de("error", r("audio.allow_recording_access"));
          return;
        }
        throw Z;
      }
      ie = Cs(yield Ds(), "audioinput");
      const D = H.getTracks().map((Z) => {
        var ee;
        return (ee = Z.getSettings()) === null || ee === void 0 ? void 0 : ee.deviceId;
      })[0];
      re = D && ie.find((Z) => Z.deviceId === D) || ie[0];
    });
  }
  function Ce() {
    return i(this, void 0, void 0, function* () {
      H && (H.getTracks().forEach((D) => D.stop()), H = null);
    });
  }
  function K() {
    return i(this, void 0, void 0, function* () {
      if (F === "open" || F === "waiting") {
        t(8, F = "waiting"), yi(q), yield Ce(), t(8, F = "closed");
        return;
      }
      t(8, F = "waiting"), ne = Math.random().toString(36).substring(2), t(0, o = ne), console.log(o), q = new RTCPeerConnection(a), q.addEventListener("connectionstatechange", (D) => i(this, void 0, void 0, function* () {
        switch (console.log("connection state change:", q.connectionState), q.connectionState) {
          case "connected":
            console.info("connected"), t(8, F = "open");
            break;
          case "disconnected":
          case "failed":
          case "closed":
            console.info("closed"), t(8, F = "closed"), yi(q);
            break;
        }
      })), q.addEventListener("iceconnectionstatechange", (D) => i(this, void 0, void 0, function* () {
        console.info("ICE connection state change:", q.iceConnectionState), (q.iceConnectionState === "failed" || q.iceConnectionState === "disconnected" || q.iceConnectionState === "closed") && (yield yi(q));
      })), H = null;
      try {
        yield ve();
      } catch (D) {
        if (!navigator.mediaDevices) {
          de("error", r("audio.no_device_support"));
          return;
        }
        if (D instanceof DOMException && D.name == "NotAllowedError") {
          de("error", r("audio.allow_recording_access"));
          return;
        }
        throw D;
      }
      H != null && (Ls(C), Ts(H, q, l === "send" ? null : C, Y.offer, ne, "audio", U, _).then((D) => {
        q = D;
      }).catch((D) => {
        console.error("interactive audio error: ", D);
      }));
    });
  }
  function we() {
    k(), K();
  }
  function X() {
    g(), F === "open" || F === "waiting" ? K() : t(8, F = "closed");
  }
  function le(D) {
    Nl[D ? "unshift" : "push"](() => {
      C = D, t(9, C);
    });
  }
  const S = () => de("stop"), Te = () => de("play");
  function be(D) {
    Nl[D ? "unshift" : "push"](() => {
      J = D, t(10, J);
    });
  }
  return n.$$set = (D) => {
    "mode" in D && t(15, l = D.mode), "value" in D && t(0, o = D.value), "rtc_configuration" in D && t(16, a = D.rtc_configuration), "i18n" in D && t(17, r = D.i18n), "time_limit" in D && t(18, s = D.time_limit), "track_constraints" in D && t(19, f = D.track_constraints), "rtp_params" in D && t(20, _ = D.rtp_params), "on_change_cb" in D && t(21, d = D.on_change_cb), "icon" in D && t(1, c = D.icon), "icon_button_color" in D && t(2, u = D.icon_button_color), "pulse_color" in D && t(3, h = D.pulse_color), "audio_btn" in D && t(4, w = D.audio_btn), "audio_btn_title" in D && t(5, T = D.audio_btn_title), "handle_audio_click_visibility" in D && t(22, k = D.handle_audio_click_visibility), "stop_audio_btn_title" in D && t(6, v = D.stop_audio_btn_title), "handle_end_streaming_click_visibility" in D && t(23, g = D.handle_end_streaming_click_visibility), "disabled" in D && t(7, b = D.disabled), "server" in D && t(24, Y = D.server);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*stopword_recognized, notification_sound*/
    100663296 && O && P.play();
  }, [
    o,
    c,
    u,
    h,
    w,
    T,
    v,
    b,
    F,
    C,
    J,
    Oe,
    de,
    we,
    X,
    l,
    a,
    r,
    s,
    f,
    _,
    d,
    k,
    g,
    Y,
    O,
    P,
    le,
    S,
    Te,
    be
  ];
}
class lr extends Hs {
  constructor(e) {
    super(), Ys(
      this,
      e,
      ir,
      nr,
      Ks,
      {
        mode: 15,
        value: 0,
        rtc_configuration: 16,
        i18n: 17,
        time_limit: 18,
        track_constraints: 19,
        rtp_params: 20,
        on_change_cb: 21,
        icon: 1,
        icon_button_color: 2,
        pulse_color: 3,
        audio_btn: 4,
        audio_btn_title: 5,
        handle_audio_click_visibility: 22,
        stop_audio_btn_title: 6,
        handle_end_streaming_click_visibility: 23,
        disabled: 7,
        server: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: or,
  action_destroyer: ar,
  add_flush_callback: ii,
  append_hydration: We,
  attr: N,
  bind: li,
  binding_callbacks: Qt,
  bubble: xn,
  check_outros: Vi,
  children: ze,
  claim_component: Mo,
  claim_element: Yt,
  claim_space: Mn,
  claim_svg_element: xt,
  claim_text: sr,
  create_component: Po,
  destroy_component: Fo,
  detach: ue,
  element: Xt,
  empty: Ol,
  group_outros: Gi,
  init: rr,
  insert_hydration: Mt,
  is_function: fr,
  listen: Fe,
  mount_component: Uo,
  noop: Lt,
  prevent_default: ur,
  run_all: cr,
  safe_not_equal: _r,
  set_data: dr,
  set_input_value: Rl,
  space: Pn,
  svg_element: $t,
  text: mr,
  toggle_class: dt,
  transition_in: mt,
  transition_out: Nt
} = window.__gradio__svelte__internal, { beforeUpdate: hr, afterUpdate: gr, createEventDispatcher: br, tick: Ml } = window.__gradio__svelte__internal;
function Pl(n) {
  let e, t, i, l, o, a, r, s, f, _;
  function d(v) {
    n[66](v);
  }
  function c(v) {
    n[67](v);
  }
  function u(v) {
    n[68](v);
  }
  let h = {
    file_count: (
      /*file_count*/
      n[19]
    ),
    filetype: (
      /*file_types*/
      n[15]
    ),
    root: (
      /*root*/
      n[14]
    ),
    max_file_size: (
      /*max_file_size*/
      n[16]
    ),
    show_progress: !1,
    disable_click: !0,
    hidden: !0,
    upload: (
      /*upload*/
      n[17]
    ),
    stream_handler: (
      /*stream_handler*/
      n[18]
    )
  };
  /*dragging*/
  n[2] !== void 0 && (h.dragging = /*dragging*/
  n[2]), /*uploading*/
  n[32] !== void 0 && (h.uploading = /*uploading*/
  n[32]), /*hidden_upload*/
  n[35] !== void 0 && (h.hidden_upload = /*hidden_upload*/
  n[35]), e = new Ma({ props: h }), n[65](e), Qt.push(() => li(e, "dragging", d)), Qt.push(() => li(e, "uploading", c)), Qt.push(() => li(e, "hidden_upload", u)), e.$on(
    "load",
    /*handle_upload*/
    n[45]
  ), e.$on(
    "error",
    /*error_handler*/
    n[69]
  );
  function w(v, g) {
    return (
      /*upload_btn*/
      v[8] === !0 ? vr : pr
    );
  }
  let T = w(n), k = T(n);
  return {
    c() {
      Po(e.$$.fragment), o = Pn(), a = Xt("button"), k.c(), this.h();
    },
    l(v) {
      Mo(e.$$.fragment, v), o = Mn(v), a = Yt(v, "BUTTON", {
        "data-testid": !0,
        class: !0,
        title: !0,
        style: !0
      });
      var g = ze(a);
      k.l(g), g.forEach(ue), this.h();
    },
    h() {
      N(a, "data-testid", "upload-button"), N(a, "class", "upload-button svelte-1mynk12"), N(
        a,
        "title",
        /*upload_btn_title*/
        n[37]
      ), a.disabled = /*disabled*/
      n[1], N(a, "style", r = `${/*stop_audio_btn*/
      n[21] ? "display: none;" : ""}`);
    },
    m(v, g) {
      Uo(e, v, g), Mt(v, o, g), Mt(v, a, g), k.m(a, null), s = !0, f || (_ = Fe(
        a,
        "click",
        /*handle_upload_click*/
        n[46]
      ), f = !0);
    },
    p(v, g) {
      const b = {};
      g[0] & /*file_count*/
      524288 && (b.file_count = /*file_count*/
      v[19]), g[0] & /*file_types*/
      32768 && (b.filetype = /*file_types*/
      v[15]), g[0] & /*root*/
      16384 && (b.root = /*root*/
      v[14]), g[0] & /*max_file_size*/
      65536 && (b.max_file_size = /*max_file_size*/
      v[16]), g[0] & /*upload*/
      131072 && (b.upload = /*upload*/
      v[17]), g[0] & /*stream_handler*/
      262144 && (b.stream_handler = /*stream_handler*/
      v[18]), !t && g[0] & /*dragging*/
      4 && (t = !0, b.dragging = /*dragging*/
      v[2], ii(() => t = !1)), !i && g[1] & /*uploading*/
      2 && (i = !0, b.uploading = /*uploading*/
      v[32], ii(() => i = !1)), !l && g[1] & /*hidden_upload*/
      16 && (l = !0, b.hidden_upload = /*hidden_upload*/
      v[35], ii(() => l = !1)), e.$set(b), T === (T = w(v)) && k ? k.p(v, g) : (k.d(1), k = T(v), k && (k.c(), k.m(a, null))), (!s || g[1] & /*upload_btn_title*/
      64) && N(
        a,
        "title",
        /*upload_btn_title*/
        v[37]
      ), (!s || g[0] & /*disabled*/
      2) && (a.disabled = /*disabled*/
      v[1]), (!s || g[0] & /*stop_audio_btn*/
      2097152 && r !== (r = `${/*stop_audio_btn*/
      v[21] ? "display: none;" : ""}`)) && N(a, "style", r);
    },
    i(v) {
      s || (mt(e.$$.fragment, v), s = !0);
    },
    o(v) {
      Nt(e.$$.fragment, v), s = !1;
    },
    d(v) {
      v && (ue(o), ue(a)), n[65](null), Fo(e, v), k.d(), f = !1, _();
    }
  };
}
function pr(n) {
  let e;
  return {
    c() {
      e = mr(
        /*upload_btn*/
        n[8]
      );
    },
    l(t) {
      e = sr(
        t,
        /*upload_btn*/
        n[8]
      );
    },
    m(t, i) {
      Mt(t, e, i);
    },
    p(t, i) {
      i[0] & /*upload_btn*/
      256 && dr(
        e,
        /*upload_btn*/
        t[8]
      );
    },
    d(t) {
      t && ue(e);
    }
  };
}
function vr(n) {
  let e, t, i;
  return {
    c() {
      e = $t("svg"), t = $t("path"), i = $t("path"), this.h();
    },
    l(l) {
      e = xt(l, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0
      });
      var o = ze(e);
      t = xt(o, "path", { d: !0, "stroke-width": !0 }), ze(t).forEach(ue), i = xt(o, "path", { d: !0, "stroke-width": !0 }), ze(i).forEach(ue), o.forEach(ue), this.h();
    },
    h() {
      N(t, "d", "M12 5L12 19"), N(t, "stroke-width", "1.3"), N(i, "d", "M5 12L19 12"), N(i, "stroke-width", "1.3"), N(e, "xmlns", "http://www.w3.org/2000/svg"), N(e, "width", "100%"), N(e, "height", "100%"), N(e, "viewBox", "0 0 24 24"), N(e, "stroke-linecap", "round"), N(e, "stroke-linejoin", "round");
    },
    m(l, o) {
      Mt(l, e, o), We(e, t), We(e, i);
    },
    p: Lt,
    d(l) {
      l && ue(e);
    }
  };
}
function Fl(n) {
  let e, t, i, l;
  const o = [kr, wr], a = [];
  function r(s, f) {
    return (
      /*mode*/
      (s[26] === "send-receive" || /*mode*/
      s[26] == "send") && /*modality*/
      s[25] === "video" ? 0 : (
        /*mode*/
        (s[26] === "send-receive" || /*mode*/
        s[26] === "send") && /*modality*/
        s[25] === "audio" ? 1 : -1
      )
    );
  }
  return ~(e = r(n)) && (t = a[e] = o[e](n)), {
    c() {
      t && t.c(), i = Ol();
    },
    l(s) {
      t && t.l(s), i = Ol();
    },
    m(s, f) {
      ~e && a[e].m(s, f), Mt(s, i, f), l = !0;
    },
    p(s, f) {
      let _ = e;
      e = r(s), e === _ ? ~e && a[e].p(s, f) : (t && (Gi(), Nt(a[_], 1, 1, () => {
        a[_] = null;
      }), Vi()), ~e ? (t = a[e], t ? t.p(s, f) : (t = a[e] = o[e](s), t.c()), mt(t, 1), t.m(i.parentNode, i)) : t = null);
    },
    i(s) {
      l || (mt(t), l = !0);
    },
    o(s) {
      Nt(t), l = !1;
    },
    d(s) {
      s && ue(i), ~e && a[e].d(s);
    }
  };
}
function wr(n) {
  let e, t, i;
  function l(a) {
    n[72](a);
  }
  let o = {
    mode: (
      /*mode*/
      n[26]
    ),
    rtc_configuration: (
      /*rtc_configuration*/
      n[23]
    ),
    i18n: (
      /*gradio*/
      n[22].i18n
    ),
    time_limit: (
      /*time_limit*/
      n[24]
    ),
    track_constraints: (
      /*track_constraints*/
      n[28]
    ),
    rtp_params: (
      /*rtp_params*/
      n[27]
    ),
    on_change_cb: (
      /*on_change_cb*/
      n[29]
    ),
    server: (
      /*server*/
      n[30]
    ),
    audio_btn: (
      /*audio_btn*/
      n[20]
    ),
    audio_btn_title: (
      /*audio_btn_title*/
      n[40]
    ),
    handle_audio_click_visibility: (
      /*handle_audio_click_visibility*/
      n[53]
    ),
    stop_audio_btn: (
      /*stop_audio_btn*/
      n[21]
    ),
    stop_audio_btn_title: (
      /*stop_audio_btn_title*/
      n[41]
    ),
    handle_end_streaming_click_visibility: (
      /*handle_end_streaming_click_visibility*/
      n[54]
    ),
    disabled: (
      /*disabled*/
      n[1]
    )
  };
  return (
    /*value*/
    n[0].audio !== void 0 && (o.value = /*value*/
    n[0].audio), e = new lr({ props: o }), Qt.push(() => li(e, "value", l)), e.$on(
      "tick",
      /*tick_handler*/
      n[73]
    ), e.$on(
      "error",
      /*error_handler_1*/
      n[74]
    ), {
      c() {
        Po(e.$$.fragment);
      },
      l(a) {
        Mo(e.$$.fragment, a);
      },
      m(a, r) {
        Uo(e, a, r), i = !0;
      },
      p(a, r) {
        const s = {};
        r[0] & /*mode*/
        67108864 && (s.mode = /*mode*/
        a[26]), r[0] & /*rtc_configuration*/
        8388608 && (s.rtc_configuration = /*rtc_configuration*/
        a[23]), r[0] & /*gradio*/
        4194304 && (s.i18n = /*gradio*/
        a[22].i18n), r[0] & /*time_limit*/
        16777216 && (s.time_limit = /*time_limit*/
        a[24]), r[0] & /*track_constraints*/
        268435456 && (s.track_constraints = /*track_constraints*/
        a[28]), r[0] & /*rtp_params*/
        134217728 && (s.rtp_params = /*rtp_params*/
        a[27]), r[0] & /*on_change_cb*/
        536870912 && (s.on_change_cb = /*on_change_cb*/
        a[29]), r[0] & /*server*/
        1073741824 && (s.server = /*server*/
        a[30]), r[0] & /*audio_btn*/
        1048576 && (s.audio_btn = /*audio_btn*/
        a[20]), r[1] & /*audio_btn_title*/
        512 && (s.audio_btn_title = /*audio_btn_title*/
        a[40]), r[0] & /*stop_audio_btn*/
        2097152 && (s.stop_audio_btn = /*stop_audio_btn*/
        a[21]), r[1] & /*stop_audio_btn_title*/
        1024 && (s.stop_audio_btn_title = /*stop_audio_btn_title*/
        a[41]), r[0] & /*disabled*/
        2 && (s.disabled = /*disabled*/
        a[1]), !t && r[0] & /*value*/
        1 && (t = !0, s.value = /*value*/
        a[0].audio, ii(() => t = !1)), e.$set(s);
      },
      i(a) {
        i || (mt(e.$$.fragment, a), i = !0);
      },
      o(a) {
        Nt(e.$$.fragment, a), i = !1;
      },
      d(a) {
        Fo(e, a);
      }
    }
  );
}
function kr(n) {
  return {
    c: Lt,
    l: Lt,
    m: Lt,
    p: Lt,
    i: Lt,
    o: Lt,
    d: Lt
  };
}
function Ul(n) {
  let e, t, i, l, o;
  return {
    c() {
      e = Xt("button"), t = $t("svg"), i = $t("path"), this.h();
    },
    l(a) {
      e = Yt(a, "BUTTON", { class: !0, title: !0 });
      var r = ze(e);
      t = xt(r, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0
      });
      var s = ze(t);
      i = xt(s, "path", {
        d: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0
      }), ze(i).forEach(ue), s.forEach(ue), r.forEach(ue), this.h();
    },
    h() {
      N(i, "d", "M12 5V18M12 5L7 10M12 5L17 10"), N(i, "stroke-width", "1.6"), N(i, "stroke-linecap", "round"), N(i, "stroke-linejoin", "round"), N(t, "xmlns", "http://www.w3.org/2000/svg"), N(t, "width", "100%"), N(t, "height", "100%"), N(t, "viewBox", "0 0 24 24"), N(e, "class", "submit-button svelte-1mynk12"), N(
        e,
        "title",
        /*submit_btn_title*/
        n[38]
      ), e.disabled = /*disabled*/
      n[1], dt(
        e,
        "padded-button",
        /*submit_btn*/
        n[9] !== !0
      );
    },
    m(a, r) {
      Mt(a, e, r), We(e, t), We(t, i), l || (o = Fe(
        e,
        "click",
        /*handle_submit*/
        n[48]
      ), l = !0);
    },
    p(a, r) {
      r[1] & /*submit_btn_title*/
      128 && N(
        e,
        "title",
        /*submit_btn_title*/
        a[38]
      ), r[0] & /*disabled*/
      2 && (e.disabled = /*disabled*/
      a[1]), r[0] & /*submit_btn*/
      512 && dt(
        e,
        "padded-button",
        /*submit_btn*/
        a[9] !== !0
      );
    },
    d(a) {
      a && ue(e), l = !1, o();
    }
  };
}
function zl(n) {
  let e, t, i, l, o;
  return {
    c() {
      e = Xt("button"), t = $t("svg"), i = $t("rect"), this.h();
    },
    l(a) {
      e = Yt(a, "BUTTON", { class: !0, title: !0 });
      var r = ze(e);
      t = xt(r, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var s = ze(t);
      i = xt(s, "rect", {
        x: !0,
        y: !0,
        width: !0,
        height: !0,
        rx: !0,
        ry: !0
      }), ze(i).forEach(ue), s.forEach(ue), r.forEach(ue), this.h();
    },
    h() {
      N(i, "x", "8"), N(i, "y", "8"), N(i, "width", "8"), N(i, "height", "8"), N(i, "rx", "1"), N(i, "ry", "1"), N(t, "xmlns", "http://www.w3.org/2000/svg"), N(t, "width", "100%"), N(t, "height", "100%"), N(t, "viewBox", "0 0 24 24"), N(t, "stroke-linecap", "round"), N(t, "stroke-linejoin", "round"), N(t, "class", "svelte-1mynk12"), N(e, "class", "stop-button svelte-1mynk12"), N(
        e,
        "title",
        /*stop_btn_title*/
        n[39]
      ), dt(
        e,
        "padded-button",
        /*stop_btn*/
        n[10] !== !0
      );
    },
    m(a, r) {
      Mt(a, e, r), We(e, t), We(t, i), l || (o = Fe(
        e,
        "click",
        /*handle_stop*/
        n[47]
      ), l = !0);
    },
    p(a, r) {
      r[1] & /*stop_btn_title*/
      256 && N(
        e,
        "title",
        /*stop_btn_title*/
        a[39]
      ), r[0] & /*stop_btn*/
      1024 && dt(
        e,
        "padded-button",
        /*stop_btn*/
        a[10] !== !0
      );
    },
    d(a) {
      a && ue(e), l = !1, o();
    }
  };
}
function yr(n) {
  let e, t, i, l, o, a, r, s, f, _, d, c, u, h, w = (
    /*upload_btn*/
    n[8] && Pl(n)
  ), T = (
    /*use_audio_video_recording*/
    n[33] && Fl(n)
  ), k = (
    /*submit_btn*/
    n[9] && Ul(n)
  ), v = (
    /*stop_btn*/
    n[10] && zl(n)
  );
  return {
    c() {
      e = Xt("div"), t = Xt("label"), i = Xt("div"), w && w.c(), l = Pn(), o = Xt("textarea"), f = Pn(), T && T.c(), _ = Pn(), k && k.c(), d = Pn(), v && v.c(), this.h();
    },
    l(g) {
      e = Yt(g, "DIV", {
        class: !0,
        role: !0,
        "aria-label": !0
      });
      var b = ze(e);
      t = Yt(b, "LABEL", {});
      var O = ze(t);
      i = Yt(O, "DIV", { class: !0 });
      var P = ze(i);
      w && w.l(P), l = Mn(P), o = Yt(P, "TEXTAREA", {
        "data-testid": !0,
        class: !0,
        dir: !0,
        placeholder: !0,
        rows: !0,
        style: !0
      }), ze(o).forEach(ue), f = Mn(P), T && T.l(P), _ = Mn(P), k && k.l(P), d = Mn(P), v && v.l(P), P.forEach(ue), O.forEach(ue), b.forEach(ue), this.h();
    },
    h() {
      N(o, "data-testid", "textbox"), N(o, "class", "scroll-hide svelte-1mynk12"), N(o, "dir", a = /*rtl*/
      n[11] ? "rtl" : "ltr"), N(
        o,
        "placeholder",
        /*placeholder*/
        n[4]
      ), o.disabled = /*disabled*/
      n[1], N(
        o,
        "rows",
        /*lines*/
        n[3]
      ), o.autofocus = /*autofocus*/
      n[12], N(o, "style", r = `${/*stop_audio_btn*/
      n[21] ? "display: none; " : ""}${/*text_align*/
      n[13] ? "text-align: " + /*text_align*/
      n[13] + "; " : ""}flex-grow: 1;`), dt(o, "no-label", !/*show_label*/
      n[5]), N(i, "class", "input-container svelte-1mynk12"), dt(
        t,
        "container",
        /*container*/
        n[6]
      ), N(e, "class", "full-container svelte-1mynk12"), N(e, "role", "group"), N(e, "aria-label", "Multimedia input field"), dt(
        e,
        "dragging",
        /*dragging*/
        n[2]
      );
    },
    m(g, b) {
      Mt(g, e, b), We(e, t), We(t, i), w && w.m(i, null), We(i, l), We(i, o), Rl(
        o,
        /*value*/
        n[0].text
      ), n[71](o), We(i, f), T && T.m(i, null), We(i, _), k && k.m(i, null), We(i, d), v && v.m(i, null), n[75](e), c = !0, /*autofocus*/
      n[12] && o.focus(), u || (h = [
        ar(s = ys.call(null, o, {
          text: (
            /*value*/
            n[0].text
          ),
          lines: (
            /*lines*/
            n[3]
          ),
          max_lines: (
            /*max_lines*/
            n[7]
          )
        })),
        Fe(
          o,
          "input",
          /*textarea_input_handler*/
          n[70]
        ),
        Fe(
          o,
          "keypress",
          /*handle_keypress*/
          n[43]
        ),
        Fe(
          o,
          "blur",
          /*blur_handler*/
          n[63]
        ),
        Fe(
          o,
          "select",
          /*handle_select*/
          n[42]
        ),
        Fe(
          o,
          "focus",
          /*focus_handler*/
          n[64]
        ),
        Fe(
          o,
          "scroll",
          /*handle_scroll*/
          n[44]
        ),
        Fe(
          o,
          "paste",
          /*handle_paste*/
          n[49]
        ),
        Fe(
          e,
          "dragenter",
          /*handle_dragenter*/
          n[50]
        ),
        Fe(
          e,
          "dragleave",
          /*handle_dragleave*/
          n[51]
        ),
        Fe(e, "dragover", ur(
          /*dragover_handler*/
          n[62]
        )),
        Fe(
          e,
          "drop",
          /*handle_drop*/
          n[52]
        )
      ], u = !0);
    },
    p(g, b) {
      /*upload_btn*/
      g[8] ? w ? (w.p(g, b), b[0] & /*upload_btn*/
      256 && mt(w, 1)) : (w = Pl(g), w.c(), mt(w, 1), w.m(i, l)) : w && (Gi(), Nt(w, 1, 1, () => {
        w = null;
      }), Vi()), (!c || b[0] & /*rtl*/
      2048 && a !== (a = /*rtl*/
      g[11] ? "rtl" : "ltr")) && N(o, "dir", a), (!c || b[0] & /*placeholder*/
      16) && N(
        o,
        "placeholder",
        /*placeholder*/
        g[4]
      ), (!c || b[0] & /*disabled*/
      2) && (o.disabled = /*disabled*/
      g[1]), (!c || b[0] & /*lines*/
      8) && N(
        o,
        "rows",
        /*lines*/
        g[3]
      ), (!c || b[0] & /*autofocus*/
      4096) && (o.autofocus = /*autofocus*/
      g[12]), (!c || b[0] & /*stop_audio_btn, text_align*/
      2105344 && r !== (r = `${/*stop_audio_btn*/
      g[21] ? "display: none; " : ""}${/*text_align*/
      g[13] ? "text-align: " + /*text_align*/
      g[13] + "; " : ""}flex-grow: 1;`)) && N(o, "style", r), s && fr(s.update) && b[0] & /*value, lines, max_lines*/
      137 && s.update.call(null, {
        text: (
          /*value*/
          g[0].text
        ),
        lines: (
          /*lines*/
          g[3]
        ),
        max_lines: (
          /*max_lines*/
          g[7]
        )
      }), b[0] & /*value*/
      1 && Rl(
        o,
        /*value*/
        g[0].text
      ), (!c || b[0] & /*show_label*/
      32) && dt(o, "no-label", !/*show_label*/
      g[5]), /*use_audio_video_recording*/
      g[33] ? T ? (T.p(g, b), b[1] & /*use_audio_video_recording*/
      4 && mt(T, 1)) : (T = Fl(g), T.c(), mt(T, 1), T.m(i, _)) : T && (Gi(), Nt(T, 1, 1, () => {
        T = null;
      }), Vi()), /*submit_btn*/
      g[9] ? k ? k.p(g, b) : (k = Ul(g), k.c(), k.m(i, d)) : k && (k.d(1), k = null), /*stop_btn*/
      g[10] ? v ? v.p(g, b) : (v = zl(g), v.c(), v.m(i, null)) : v && (v.d(1), v = null), (!c || b[0] & /*container*/
      64) && dt(
        t,
        "container",
        /*container*/
        g[6]
      ), (!c || b[0] & /*dragging*/
      4) && dt(
        e,
        "dragging",
        /*dragging*/
        g[2]
      );
    },
    i(g) {
      c || (mt(w), mt(T), c = !0);
    },
    o(g) {
      Nt(w), Nt(T), c = !1;
    },
    d(g) {
      g && ue(e), w && w.d(), n[71](null), T && T.d(), k && k.d(), v && v.d(), n[75](null), u = !1, cr(h);
    }
  };
}
function Er(n, e, t) {
  var i = this && this.__awaiter || function(p, te, ge, $) {
    function rt(Ct) {
      return Ct instanceof ge ? Ct : new ge(function(Ut) {
        Ut(Ct);
      });
    }
    return new (ge || (ge = Promise))(function(Ct, Ut) {
      function Yn(ft) {
        try {
          qe($.next(ft));
        } catch (an) {
          Ut(an);
        }
      }
      function Xn(ft) {
        try {
          qe($.throw(ft));
        } catch (an) {
          Ut(an);
        }
      }
      function qe(ft) {
        ft.done ? Ct(ft.value) : rt(ft.value).then(Yn, Xn);
      }
      qe(($ = $.apply(p, te || [])).next());
    });
  };
  let { value: l = {
    text: "",
    files: [],
    audio: "__webrtc_value__"
  } } = e, { value_is_output: o = !1 } = e, { lines: a = 1 } = e, { placeholder: r = "Type here..." } = e, { disabled: s = !1 } = e, { interactive: f } = e, { loading_message: _ } = e, { show_label: d = !0 } = e, { container: c = !0 } = e, { max_lines: u } = e, { upload_btn: h = null } = e, { submit_btn: w = null } = e, { stop_btn: T = null } = e, { rtl: k = !1 } = e, { autofocus: v = !1 } = e, { text_align: g = void 0 } = e, { autoscroll: b = !0 } = e, { root: O } = e, { file_types: P = null } = e, { max_file_size: U = null } = e, { upload: Y } = e, { stream_handler: F } = e, { file_count: C = "multiple" } = e, { audio_btn: J = !1 } = e, { stop_audio_btn: q = !1 } = e, { gradio: ne } = e, { rtc_configuration: H } = e, { time_limit: ie = null } = e, { modality: re = "audio" } = e, { mode: Oe = "send-receive" } = e, { rtp_params: de = {} } = e, { track_constraints: ve = {} } = e, { on_change_cb: Ce } = e, { server: K } = e, we, X, le, S, Te = 0, be = !1, { dragging: D = !1 } = e, Z = !1, ee = l.text, y, M = !1, W = !1, B, x, ce, _e, me, Ae;
  navigator.language.startsWith("fr") ? (x = "Ajouter un fichier", ce = "Poser une question", _e = "Arrêter", me = "Activer Neo audio", Ae = "Arreter Neo audio") : (x = "Add a file", ce = "Ask a question", _e = "Stop", me = "Launch Neo audio", Ae = "Stop Neo audio");
  const fe = br();
  hr(() => {
    S = le && le.offsetHeight + le.scrollTop > le.scrollHeight - 100;
  });
  const Re = () => {
    S && b && !be && le.scrollTo(0, le.scrollHeight);
  };
  function wt() {
    return i(this, void 0, void 0, function* () {
      fe("change", l), o || fe("input");
    });
  }
  gr(() => {
    v && le !== null && le.focus(), S && b && Re(), t(55, o = !1);
  });
  function Pt(p) {
    const te = p.target, ge = te.value, $ = [te.selectionStart, te.selectionEnd];
    fe("select", { value: ge.substring(...$), index: $ });
  }
  function E(p) {
    return i(this, void 0, void 0, function* () {
      yield Ml(), (p.key === "Enter" && p.shiftKey && a > 1 || p.key === "Enter" && !p.shiftKey && a === 1 && u >= 1) && (p.preventDefault(), fe("submit"));
    });
  }
  function Tt(p) {
    const te = p.target, ge = te.scrollTop;
    ge < Te && (be = !0), Te = ge;
    const $ = te.scrollHeight - te.clientHeight;
    ge >= $ && (be = !1);
  }
  function At(p) {
    return i(this, arguments, void 0, function* ({ detail: te }) {
      if (wt(), Array.isArray(te)) {
        for (let ge of te)
          l.files.push(ge);
        t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y);
      } else
        l.files.push(te), t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y);
      yield Ml(), fe("change", l), fe("upload", te);
    });
  }
  function Hn() {
    X && (t(35, X.value = "", X), X.click());
  }
  function Wn() {
    fe("stop");
  }
  function Vn() {
    fe("submit");
  }
  function yn(p) {
    if (!p.clipboardData) return;
    const te = p.clipboardData.items;
    for (let ge in te) {
      const $ = te[ge];
      if ($.type.includes("text/plain"))
        break;
      if ($.kind === "file" && $.type.includes("image")) {
        const rt = $.getAsFile();
        rt && we.load_files([rt]);
      }
    }
  }
  function Gn(p) {
    p.preventDefault(), t(2, D = !0);
  }
  function tn(p) {
    p.preventDefault();
    const te = B.getBoundingClientRect(), { clientX: ge, clientY: $ } = p;
    (ge <= te.left || ge >= te.right || $ <= te.top || $ >= te.bottom) && t(2, D = !1);
  }
  function nn(p) {
    p.preventDefault(), t(2, D = !1), p.dataTransfer && p.dataTransfer.files && we.load_files(Array.from(p.dataTransfer.files));
  }
  function $e() {
    fe("start_recording");
  }
  function St() {
    fe("stop_recording");
  }
  function En(p) {
    xn.call(this, n, p);
  }
  function Tn(p) {
    xn.call(this, n, p);
  }
  function mi(p) {
    xn.call(this, n, p);
  }
  function ln(p) {
    Qt[p ? "unshift" : "push"](() => {
      we = p, t(34, we);
    });
  }
  function on(p) {
    D = p, t(2, D);
  }
  function hi(p) {
    Z = p, t(32, Z);
  }
  function Ft(p) {
    X = p, t(35, X);
  }
  function gi(p) {
    xn.call(this, n, p);
  }
  function bi() {
    l.text = this.value, t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y);
  }
  function he(p) {
    Qt[p ? "unshift" : "push"](() => {
      le = p, t(31, le);
    });
  }
  function Dt(p) {
    n.$$.not_equal(l.audio, p) && (l.audio = p, t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y));
  }
  const pi = () => ne.dispatch("tick"), jn = ({ detail: p }) => ne.dispatch("error", p);
  function An(p) {
    Qt[p ? "unshift" : "push"](() => {
      B = p, t(36, B);
    });
  }
  return n.$$set = (p) => {
    "value" in p && t(0, l = p.value), "value_is_output" in p && t(55, o = p.value_is_output), "lines" in p && t(3, a = p.lines), "placeholder" in p && t(4, r = p.placeholder), "disabled" in p && t(1, s = p.disabled), "interactive" in p && t(56, f = p.interactive), "loading_message" in p && t(57, _ = p.loading_message), "show_label" in p && t(5, d = p.show_label), "container" in p && t(6, c = p.container), "max_lines" in p && t(7, u = p.max_lines), "upload_btn" in p && t(8, h = p.upload_btn), "submit_btn" in p && t(9, w = p.submit_btn), "stop_btn" in p && t(10, T = p.stop_btn), "rtl" in p && t(11, k = p.rtl), "autofocus" in p && t(12, v = p.autofocus), "text_align" in p && t(13, g = p.text_align), "autoscroll" in p && t(58, b = p.autoscroll), "root" in p && t(14, O = p.root), "file_types" in p && t(15, P = p.file_types), "max_file_size" in p && t(16, U = p.max_file_size), "upload" in p && t(17, Y = p.upload), "stream_handler" in p && t(18, F = p.stream_handler), "file_count" in p && t(19, C = p.file_count), "audio_btn" in p && t(20, J = p.audio_btn), "stop_audio_btn" in p && t(21, q = p.stop_audio_btn), "gradio" in p && t(22, ne = p.gradio), "rtc_configuration" in p && t(23, H = p.rtc_configuration), "time_limit" in p && t(24, ie = p.time_limit), "modality" in p && t(25, re = p.modality), "mode" in p && t(26, Oe = p.mode), "rtp_params" in p && t(27, de = p.rtp_params), "track_constraints" in p && t(28, ve = p.track_constraints), "on_change_cb" in p && t(29, Ce = p.on_change_cb), "server" in p && t(30, K = p.server), "dragging" in p && t(2, D = p.dragging);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*dragging*/
    4 && fe("drag", D), n.$$.dirty[0] & /*audio_btn*/
    1048576 | n.$$.dirty[1] & /*use_audio_video_recording*/
    4 && J && !W && t(33, W = J), n.$$.dirty[0] & /*value*/
    1 && l === null && t(0, l = { text: "", files: [], audio: null }), n.$$.dirty[0] & /*value*/
    1 | n.$$.dirty[1] & /*uploading, retrieve_saved_message, loading_message, saved_message*/
    1677721602 && (Z && !M ? (t(60, y = l.text), t(61, M = !0), t(0, l.text = _, l), console.log("value.text uploading", l.text)) : !Z && M && (t(0, l.text = y, l), t(61, M = !1), console.log("value.text end of uploading", l.text))), n.$$.dirty[0] & /*value*/
    1 | n.$$.dirty[1] & /*oldValue, uploading, retrieve_saved_message*/
    1342177282 && ee !== l.text && !Z && !M && (t(59, ee = l.text), fe("change", l)), n.$$.dirty[1] & /*uploading*/
    2 && Z && console.log("uploading"), n.$$.dirty[1] & /*interactive, uploading*/
    33554434 && t(1, s = !f || Z), n.$$.dirty[0] & /*disabled*/
    2 && s && console.log("disabled"), n.$$.dirty[0] & /*value, lines, max_lines*/
    137 | n.$$.dirty[1] & /*el, uploading*/
    3 && le && a !== u && Hi(le, a, u, Z);
  }, [
    l,
    s,
    D,
    a,
    r,
    d,
    c,
    u,
    h,
    w,
    T,
    k,
    v,
    g,
    O,
    P,
    U,
    Y,
    F,
    C,
    J,
    q,
    ne,
    H,
    ie,
    re,
    Oe,
    de,
    ve,
    Ce,
    K,
    le,
    Z,
    W,
    we,
    X,
    B,
    x,
    ce,
    _e,
    me,
    Ae,
    Pt,
    E,
    Tt,
    At,
    Hn,
    Wn,
    Vn,
    yn,
    Gn,
    tn,
    nn,
    $e,
    St,
    o,
    f,
    _,
    b,
    ee,
    y,
    M,
    En,
    Tn,
    mi,
    ln,
    on,
    hi,
    Ft,
    gi,
    bi,
    he,
    Dt,
    pi,
    jn,
    An
  ];
}
class Tr extends or {
  constructor(e) {
    super(), rr(
      this,
      e,
      Er,
      yr,
      _r,
      {
        value: 0,
        value_is_output: 55,
        lines: 3,
        placeholder: 4,
        disabled: 1,
        interactive: 56,
        loading_message: 57,
        show_label: 5,
        container: 6,
        max_lines: 7,
        upload_btn: 8,
        submit_btn: 9,
        stop_btn: 10,
        rtl: 11,
        autofocus: 12,
        text_align: 13,
        autoscroll: 58,
        root: 14,
        file_types: 15,
        max_file_size: 16,
        upload: 17,
        stream_handler: 18,
        file_count: 19,
        audio_btn: 20,
        stop_audio_btn: 21,
        gradio: 22,
        rtc_configuration: 23,
        time_limit: 24,
        modality: 25,
        mode: 26,
        rtp_params: 27,
        track_constraints: 28,
        on_change_cb: 29,
        server: 30,
        dragging: 2
      },
      null,
      [-1, -1, -1]
    );
  }
}
function dn(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let i = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + i;
}
function oi() {
}
function Ar(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const zo = typeof window < "u";
let ql = zo ? () => window.performance.now() : () => Date.now(), qo = zo ? (n) => requestAnimationFrame(n) : oi;
const hn = /* @__PURE__ */ new Set();
function Bo(n) {
  hn.forEach((e) => {
    e.c(n) || (hn.delete(e), e.f());
  }), hn.size !== 0 && qo(Bo);
}
function Sr(n) {
  let e;
  return hn.size === 0 && qo(Bo), {
    promise: new Promise((t) => {
      hn.add(e = { c: n, f: t });
    }),
    abort() {
      hn.delete(e);
    }
  };
}
const rn = [];
function Dr(n, e = oi) {
  let t;
  const i = /* @__PURE__ */ new Set();
  function l(r) {
    if (Ar(n, r) && (n = r, t)) {
      const s = !rn.length;
      for (const f of i)
        f[1](), rn.push(f, n);
      if (s) {
        for (let f = 0; f < rn.length; f += 2)
          rn[f][0](rn[f + 1]);
        rn.length = 0;
      }
    }
  }
  function o(r) {
    l(r(n));
  }
  function a(r, s = oi) {
    const f = [r, s];
    return i.add(f), i.size === 1 && (t = e(l, o) || oi), r(n), () => {
      i.delete(f), i.size === 0 && t && (t(), t = null);
    };
  }
  return { set: l, update: o, subscribe: a };
}
function Bl(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function ji(n, e, t, i) {
  if (typeof t == "number" || Bl(t)) {
    const l = i - t, o = (t - e) / (n.dt || 1 / 60), a = n.opts.stiffness * l, r = n.opts.damping * o, s = (a - r) * n.inv_mass, f = (o + s) * n.dt;
    return Math.abs(f) < n.opts.precision && Math.abs(l) < n.opts.precision ? i : (n.settled = !1, Bl(t) ? new Date(t.getTime() + f) : t + f);
  } else {
    if (Array.isArray(t))
      return t.map(
        (l, o) => ji(n, e[o], t[o], i[o])
      );
    if (typeof t == "object") {
      const l = {};
      for (const o in t)
        l[o] = ji(n, e[o], t[o], i[o]);
      return l;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Hl(n, e = {}) {
  const t = Dr(n), { stiffness: i = 0.15, damping: l = 0.8, precision: o = 0.01 } = e;
  let a, r, s, f = n, _ = n, d = 1, c = 0, u = !1;
  function h(T, k = {}) {
    _ = T;
    const v = s = {};
    return n == null || k.hard || w.stiffness >= 1 && w.damping >= 1 ? (u = !0, a = ql(), f = T, t.set(n = _), Promise.resolve()) : (k.soft && (c = 1 / ((k.soft === !0 ? 0.5 : +k.soft) * 60), d = 0), r || (a = ql(), u = !1, r = Sr((g) => {
      if (u)
        return u = !1, r = null, !1;
      d = Math.min(d + c, 1);
      const b = {
        inv_mass: d,
        opts: w,
        settled: !0,
        dt: (g - a) * 60 / 1e3
      }, O = ji(b, f, n, _);
      return a = g, f = n, t.set(n = O), b.settled && (r = null), !b.settled;
    })), new Promise((g) => {
      r.promise.then(() => {
        v === s && g();
      });
    }));
  }
  const w = {
    set: h,
    update: (T, k) => h(T(_, n), k),
    subscribe: t.subscribe,
    stiffness: i,
    damping: l,
    precision: o
  };
  return w;
}
const {
  SvelteComponent: Cr,
  append_hydration: tt,
  attr: Q,
  children: je,
  claim_element: Lr,
  claim_svg_element: nt,
  component_subscribe: Wl,
  detach: Be,
  element: Ir,
  init: Nr,
  insert_hydration: Or,
  noop: Vl,
  safe_not_equal: Rr,
  set_style: $n,
  svg_element: it,
  toggle_class: Gl
} = window.__gradio__svelte__internal, { onMount: Mr } = window.__gradio__svelte__internal;
function Pr(n) {
  let e, t, i, l, o, a, r, s, f, _, d, c;
  return {
    c() {
      e = Ir("div"), t = it("svg"), i = it("g"), l = it("path"), o = it("path"), a = it("path"), r = it("path"), s = it("g"), f = it("path"), _ = it("path"), d = it("path"), c = it("path"), this.h();
    },
    l(u) {
      e = Lr(u, "DIV", { class: !0 });
      var h = je(e);
      t = nt(h, "svg", {
        viewBox: !0,
        fill: !0,
        xmlns: !0,
        class: !0
      });
      var w = je(t);
      i = nt(w, "g", { style: !0 });
      var T = je(i);
      l = nt(T, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(l).forEach(Be), o = nt(T, "path", { d: !0, fill: !0, class: !0 }), je(o).forEach(Be), a = nt(T, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(a).forEach(Be), r = nt(T, "path", { d: !0, fill: !0, class: !0 }), je(r).forEach(Be), T.forEach(Be), s = nt(w, "g", { style: !0 });
      var k = je(s);
      f = nt(k, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(f).forEach(Be), _ = nt(k, "path", { d: !0, fill: !0, class: !0 }), je(_).forEach(Be), d = nt(k, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(d).forEach(Be), c = nt(k, "path", { d: !0, fill: !0, class: !0 }), je(c).forEach(Be), k.forEach(Be), w.forEach(Be), h.forEach(Be), this.h();
    },
    h() {
      Q(l, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), Q(l, "fill", "#FF7C00"), Q(l, "fill-opacity", "0.4"), Q(l, "class", "svelte-43sxxs"), Q(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), Q(o, "fill", "#FF7C00"), Q(o, "class", "svelte-43sxxs"), Q(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), Q(a, "fill", "#FF7C00"), Q(a, "fill-opacity", "0.4"), Q(a, "class", "svelte-43sxxs"), Q(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), Q(r, "fill", "#FF7C00"), Q(r, "class", "svelte-43sxxs"), $n(i, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), Q(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), Q(f, "fill", "#FF7C00"), Q(f, "fill-opacity", "0.4"), Q(f, "class", "svelte-43sxxs"), Q(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), Q(_, "fill", "#FF7C00"), Q(_, "class", "svelte-43sxxs"), Q(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), Q(d, "fill", "#FF7C00"), Q(d, "fill-opacity", "0.4"), Q(d, "class", "svelte-43sxxs"), Q(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), Q(c, "fill", "#FF7C00"), Q(c, "class", "svelte-43sxxs"), $n(s, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), Q(t, "viewBox", "-1200 -1200 3000 3000"), Q(t, "fill", "none"), Q(t, "xmlns", "http://www.w3.org/2000/svg"), Q(t, "class", "svelte-43sxxs"), Q(e, "class", "svelte-43sxxs"), Gl(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(u, h) {
      Or(u, e, h), tt(e, t), tt(t, i), tt(i, l), tt(i, o), tt(i, a), tt(i, r), tt(t, s), tt(s, f), tt(s, _), tt(s, d), tt(s, c);
    },
    p(u, [h]) {
      h & /*$top*/
      2 && $n(i, "transform", "translate(" + /*$top*/
      u[1][0] + "px, " + /*$top*/
      u[1][1] + "px)"), h & /*$bottom*/
      4 && $n(s, "transform", "translate(" + /*$bottom*/
      u[2][0] + "px, " + /*$bottom*/
      u[2][1] + "px)"), h & /*margin*/
      1 && Gl(
        e,
        "margin",
        /*margin*/
        u[0]
      );
    },
    i: Vl,
    o: Vl,
    d(u) {
      u && Be(e);
    }
  };
}
function Fr(n, e, t) {
  let i, l;
  var o = this && this.__awaiter || function(u, h, w, T) {
    function k(v) {
      return v instanceof w ? v : new w(function(g) {
        g(v);
      });
    }
    return new (w || (w = Promise))(function(v, g) {
      function b(U) {
        try {
          P(T.next(U));
        } catch (Y) {
          g(Y);
        }
      }
      function O(U) {
        try {
          P(T.throw(U));
        } catch (Y) {
          g(Y);
        }
      }
      function P(U) {
        U.done ? v(U.value) : k(U.value).then(b, O);
      }
      P((T = T.apply(u, h || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = Hl([0, 0]);
  Wl(n, r, (u) => t(1, i = u));
  const s = Hl([0, 0]);
  Wl(n, s, (u) => t(2, l = u));
  let f;
  function _() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield _(), f || d();
    });
  }
  function c() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), d();
    });
  }
  return Mr(() => (c(), () => f = !0)), n.$$set = (u) => {
    "margin" in u && t(0, a = u.margin);
  }, [a, i, l, r, s];
}
class Ur extends Cr {
  constructor(e) {
    super(), Nr(this, e, Fr, Pr, Rr, { margin: 0 });
  }
}
const {
  SvelteComponent: zr,
  append_hydration: Zt,
  attr: st,
  binding_callbacks: jl,
  check_outros: Yi,
  children: gt,
  claim_component: Ho,
  claim_element: bt,
  claim_space: Xe,
  claim_text: ae,
  create_component: Wo,
  create_slot: Vo,
  destroy_component: Go,
  destroy_each: jo,
  detach: R,
  element: pt,
  empty: Je,
  ensure_array_like: _i,
  get_all_dirty_from_scope: Yo,
  get_slot_changes: Xo,
  group_outros: Xi,
  init: qr,
  insert_hydration: z,
  mount_component: Zo,
  noop: Zi,
  safe_not_equal: Br,
  set_data: Qe,
  set_style: Ot,
  space: Ze,
  text: se,
  toggle_class: Ye,
  transition_in: at,
  transition_out: vt,
  update_slot_base: Ko
} = window.__gradio__svelte__internal, { tick: Hr } = window.__gradio__svelte__internal, { onDestroy: Wr } = window.__gradio__svelte__internal, { createEventDispatcher: Vr } = window.__gradio__svelte__internal, Gr = (n) => ({}), Yl = (n) => ({}), jr = (n) => ({}), Xl = (n) => ({});
function Zl(n, e, t) {
  const i = n.slice();
  return i[41] = e[t], i[43] = t, i;
}
function Kl(n, e, t) {
  const i = n.slice();
  return i[41] = e[t], i;
}
function Yr(n) {
  let e, t, i, l, o = (
    /*i18n*/
    n[1]("common.error") + ""
  ), a, r, s;
  t = new ds({
    props: {
      Icon: vs,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const f = (
    /*#slots*/
    n[30].error
  ), _ = Vo(
    f,
    n,
    /*$$scope*/
    n[29],
    Yl
  );
  return {
    c() {
      e = pt("div"), Wo(t.$$.fragment), i = Ze(), l = pt("span"), a = se(o), r = Ze(), _ && _.c(), this.h();
    },
    l(d) {
      e = bt(d, "DIV", { class: !0 });
      var c = gt(e);
      Ho(t.$$.fragment, c), c.forEach(R), i = Xe(d), l = bt(d, "SPAN", { class: !0 });
      var u = gt(l);
      a = ae(u, o), u.forEach(R), r = Xe(d), _ && _.l(d), this.h();
    },
    h() {
      st(e, "class", "clear-status svelte-17v219f"), st(l, "class", "error svelte-17v219f");
    },
    m(d, c) {
      z(d, e, c), Zo(t, e, null), z(d, i, c), z(d, l, c), Zt(l, a), z(d, r, c), _ && _.m(d, c), s = !0;
    },
    p(d, c) {
      const u = {};
      c[0] & /*i18n*/
      2 && (u.label = /*i18n*/
      d[1]("common.clear")), t.$set(u), (!s || c[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      d[1]("common.error") + "") && Qe(a, o), _ && _.p && (!s || c[0] & /*$$scope*/
      536870912) && Ko(
        _,
        f,
        d,
        /*$$scope*/
        d[29],
        s ? Xo(
          f,
          /*$$scope*/
          d[29],
          c,
          Gr
        ) : Yo(
          /*$$scope*/
          d[29]
        ),
        Yl
      );
    },
    i(d) {
      s || (at(t.$$.fragment, d), at(_, d), s = !0);
    },
    o(d) {
      vt(t.$$.fragment, d), vt(_, d), s = !1;
    },
    d(d) {
      d && (R(e), R(i), R(l), R(r)), Go(t), _ && _.d(d);
    }
  };
}
function Xr(n) {
  let e, t, i, l, o, a, r, s, f, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Jl(n)
  );
  function d(g, b) {
    if (
      /*progress*/
      g[7]
    ) return Jr;
    if (
      /*queue_position*/
      g[2] !== null && /*queue_size*/
      g[3] !== void 0 && /*queue_position*/
      g[2] >= 0
    ) return Kr;
    if (
      /*queue_position*/
      g[2] === 0
    ) return Zr;
  }
  let c = d(n), u = c && c(n), h = (
    /*timer*/
    n[5] && $l(n)
  );
  const w = [ef, $r], T = [];
  function k(g, b) {
    return (
      /*last_progress_level*/
      g[15] != null ? 0 : (
        /*show_progress*/
        g[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = k(n)) && (a = T[o] = w[o](n));
  let v = !/*timer*/
  n[5] && ao(n);
  return {
    c() {
      _ && _.c(), e = Ze(), t = pt("div"), u && u.c(), i = Ze(), h && h.c(), l = Ze(), a && a.c(), r = Ze(), v && v.c(), s = Je(), this.h();
    },
    l(g) {
      _ && _.l(g), e = Xe(g), t = bt(g, "DIV", { class: !0 });
      var b = gt(t);
      u && u.l(b), i = Xe(b), h && h.l(b), b.forEach(R), l = Xe(g), a && a.l(g), r = Xe(g), v && v.l(g), s = Je(), this.h();
    },
    h() {
      st(t, "class", "progress-text svelte-17v219f"), Ye(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), Ye(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(g, b) {
      _ && _.m(g, b), z(g, e, b), z(g, t, b), u && u.m(t, null), Zt(t, i), h && h.m(t, null), z(g, l, b), ~o && T[o].m(g, b), z(g, r, b), v && v.m(g, b), z(g, s, b), f = !0;
    },
    p(g, b) {
      /*variant*/
      g[8] === "default" && /*show_eta_bar*/
      g[18] && /*show_progress*/
      g[6] === "full" ? _ ? _.p(g, b) : (_ = Jl(g), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), c === (c = d(g)) && u ? u.p(g, b) : (u && u.d(1), u = c && c(g), u && (u.c(), u.m(t, i))), /*timer*/
      g[5] ? h ? h.p(g, b) : (h = $l(g), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!f || b[0] & /*variant*/
      256) && Ye(
        t,
        "meta-text-center",
        /*variant*/
        g[8] === "center"
      ), (!f || b[0] & /*variant*/
      256) && Ye(
        t,
        "meta-text",
        /*variant*/
        g[8] === "default"
      );
      let O = o;
      o = k(g), o === O ? ~o && T[o].p(g, b) : (a && (Xi(), vt(T[O], 1, 1, () => {
        T[O] = null;
      }), Yi()), ~o ? (a = T[o], a ? a.p(g, b) : (a = T[o] = w[o](g), a.c()), at(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      g[5] ? v && (Xi(), vt(v, 1, 1, () => {
        v = null;
      }), Yi()) : v ? (v.p(g, b), b[0] & /*timer*/
      32 && at(v, 1)) : (v = ao(g), v.c(), at(v, 1), v.m(s.parentNode, s));
    },
    i(g) {
      f || (at(a), at(v), f = !0);
    },
    o(g) {
      vt(a), vt(v), f = !1;
    },
    d(g) {
      g && (R(e), R(t), R(l), R(r), R(s)), _ && _.d(g), u && u.d(), h && h.d(), ~o && T[o].d(g), v && v.d(g);
    }
  };
}
function Jl(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = pt("div"), this.h();
    },
    l(i) {
      e = bt(i, "DIV", { class: !0 }), gt(e).forEach(R), this.h();
    },
    h() {
      st(e, "class", "eta-bar svelte-17v219f"), Ot(e, "transform", t);
    },
    m(i, l) {
      z(i, e, l);
    },
    p(i, l) {
      l[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (i[17] || 0) * 100 - 100}%)`) && Ot(e, "transform", t);
    },
    d(i) {
      i && R(e);
    }
  };
}
function Zr(n) {
  let e;
  return {
    c() {
      e = se("processing |");
    },
    l(t) {
      e = ae(t, "processing |");
    },
    m(t, i) {
      z(t, e, i);
    },
    p: Zi,
    d(t) {
      t && R(e);
    }
  };
}
function Kr(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), i, l, o, a;
  return {
    c() {
      e = se("queue: "), i = se(t), l = se("/"), o = se(
        /*queue_size*/
        n[3]
      ), a = se(" |");
    },
    l(r) {
      e = ae(r, "queue: "), i = ae(r, t), l = ae(r, "/"), o = ae(
        r,
        /*queue_size*/
        n[3]
      ), a = ae(r, " |");
    },
    m(r, s) {
      z(r, e, s), z(r, i, s), z(r, l, s), z(r, o, s), z(r, a, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && Qe(i, t), s[0] & /*queue_size*/
      8 && Qe(
        o,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (R(e), R(i), R(l), R(o), R(a));
    }
  };
}
function Jr(n) {
  let e, t = _i(
    /*progress*/
    n[7]
  ), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = xl(Kl(n, t, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      e = Je();
    },
    l(l) {
      for (let o = 0; o < i.length; o += 1)
        i[o].l(l);
      e = Je();
    },
    m(l, o) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, o);
      z(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*progress*/
      128) {
        t = _i(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = Kl(l, t, a);
          i[a] ? i[a].p(r, o) : (i[a] = xl(r), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(l) {
      l && R(e), jo(i, l);
    }
  };
}
function Ql(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), i, l, o = " ", a;
  function r(_, d) {
    return (
      /*p*/
      _[41].length != null ? xr : Qr
    );
  }
  let s = r(n), f = s(n);
  return {
    c() {
      f.c(), e = Ze(), i = se(t), l = se(" | "), a = se(o);
    },
    l(_) {
      f.l(_), e = Xe(_), i = ae(_, t), l = ae(_, " | "), a = ae(_, o);
    },
    m(_, d) {
      f.m(_, d), z(_, e, d), z(_, i, d), z(_, l, d), z(_, a, d);
    },
    p(_, d) {
      s === (s = r(_)) && f ? f.p(_, d) : (f.d(1), f = s(_), f && (f.c(), f.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && Qe(i, t);
    },
    d(_) {
      _ && (R(e), R(i), R(l), R(a)), f.d(_);
    }
  };
}
function Qr(n) {
  let e = dn(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = se(e);
    },
    l(i) {
      t = ae(i, e);
    },
    m(i, l) {
      z(i, t, l);
    },
    p(i, l) {
      l[0] & /*progress*/
      128 && e !== (e = dn(
        /*p*/
        i[41].index || 0
      ) + "") && Qe(t, e);
    },
    d(i) {
      i && R(t);
    }
  };
}
function xr(n) {
  let e = dn(
    /*p*/
    n[41].index || 0
  ) + "", t, i, l = dn(
    /*p*/
    n[41].length
  ) + "", o;
  return {
    c() {
      t = se(e), i = se("/"), o = se(l);
    },
    l(a) {
      t = ae(a, e), i = ae(a, "/"), o = ae(a, l);
    },
    m(a, r) {
      z(a, t, r), z(a, i, r), z(a, o, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = dn(
        /*p*/
        a[41].index || 0
      ) + "") && Qe(t, e), r[0] & /*progress*/
      128 && l !== (l = dn(
        /*p*/
        a[41].length
      ) + "") && Qe(o, l);
    },
    d(a) {
      a && (R(t), R(i), R(o));
    }
  };
}
function xl(n) {
  let e, t = (
    /*p*/
    n[41].index != null && Ql(n)
  );
  return {
    c() {
      t && t.c(), e = Je();
    },
    l(i) {
      t && t.l(i), e = Je();
    },
    m(i, l) {
      t && t.m(i, l), z(i, e, l);
    },
    p(i, l) {
      /*p*/
      i[41].index != null ? t ? t.p(i, l) : (t = Ql(i), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(i) {
      i && R(e), t && t.d(i);
    }
  };
}
function $l(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), i, l;
  return {
    c() {
      e = se(
        /*formatted_timer*/
        n[20]
      ), i = se(t), l = se("s");
    },
    l(o) {
      e = ae(
        o,
        /*formatted_timer*/
        n[20]
      ), i = ae(o, t), l = ae(o, "s");
    },
    m(o, a) {
      z(o, e, a), z(o, i, a), z(o, l, a);
    },
    p(o, a) {
      a[0] & /*formatted_timer*/
      1048576 && Qe(
        e,
        /*formatted_timer*/
        o[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && Qe(i, t);
    },
    d(o) {
      o && (R(e), R(i), R(l));
    }
  };
}
function $r(n) {
  let e, t;
  return e = new Ur({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Wo(e.$$.fragment);
    },
    l(i) {
      Ho(e.$$.fragment, i);
    },
    m(i, l) {
      Zo(e, i, l), t = !0;
    },
    p(i, l) {
      const o = {};
      l[0] & /*variant*/
      256 && (o.margin = /*variant*/
      i[8] === "default"), e.$set(o);
    },
    i(i) {
      t || (at(e.$$.fragment, i), t = !0);
    },
    o(i) {
      vt(e.$$.fragment, i), t = !1;
    },
    d(i) {
      Go(e, i);
    }
  };
}
function ef(n) {
  let e, t, i, l, o, a = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && eo(n)
  );
  return {
    c() {
      e = pt("div"), t = pt("div"), r && r.c(), i = Ze(), l = pt("div"), o = pt("div"), this.h();
    },
    l(s) {
      e = bt(s, "DIV", { class: !0 });
      var f = gt(e);
      t = bt(f, "DIV", { class: !0 });
      var _ = gt(t);
      r && r.l(_), _.forEach(R), i = Xe(f), l = bt(f, "DIV", { class: !0 });
      var d = gt(l);
      o = bt(d, "DIV", { class: !0 }), gt(o).forEach(R), d.forEach(R), f.forEach(R), this.h();
    },
    h() {
      st(t, "class", "progress-level-inner svelte-17v219f"), st(o, "class", "progress-bar svelte-17v219f"), Ot(o, "width", a), st(l, "class", "progress-bar-wrap svelte-17v219f"), st(e, "class", "progress-level svelte-17v219f");
    },
    m(s, f) {
      z(s, e, f), Zt(e, t), r && r.m(t, null), Zt(e, i), Zt(e, l), Zt(l, o), n[31](o);
    },
    p(s, f) {
      /*progress*/
      s[7] != null ? r ? r.p(s, f) : (r = eo(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), f[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      s[15] * 100}%`) && Ot(o, "width", a);
    },
    i: Zi,
    o: Zi,
    d(s) {
      s && R(e), r && r.d(), n[31](null);
    }
  };
}
function eo(n) {
  let e, t = _i(
    /*progress*/
    n[7]
  ), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = oo(Zl(n, t, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      e = Je();
    },
    l(l) {
      for (let o = 0; o < i.length; o += 1)
        i[o].l(l);
      e = Je();
    },
    m(l, o) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, o);
      z(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = _i(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = Zl(l, t, a);
          i[a] ? i[a].p(r, o) : (i[a] = oo(r), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(l) {
      l && R(e), jo(i, l);
    }
  };
}
function to(n) {
  let e, t, i, l, o = (
    /*i*/
    n[43] !== 0 && tf()
  ), a = (
    /*p*/
    n[41].desc != null && no(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && io()
  ), s = (
    /*progress_level*/
    n[14] != null && lo(n)
  );
  return {
    c() {
      o && o.c(), e = Ze(), a && a.c(), t = Ze(), r && r.c(), i = Ze(), s && s.c(), l = Je();
    },
    l(f) {
      o && o.l(f), e = Xe(f), a && a.l(f), t = Xe(f), r && r.l(f), i = Xe(f), s && s.l(f), l = Je();
    },
    m(f, _) {
      o && o.m(f, _), z(f, e, _), a && a.m(f, _), z(f, t, _), r && r.m(f, _), z(f, i, _), s && s.m(f, _), z(f, l, _);
    },
    p(f, _) {
      /*p*/
      f[41].desc != null ? a ? a.p(f, _) : (a = no(f), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      f[41].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[43]
      ] != null ? r || (r = io(), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null), /*progress_level*/
      f[14] != null ? s ? s.p(f, _) : (s = lo(f), s.c(), s.m(l.parentNode, l)) : s && (s.d(1), s = null);
    },
    d(f) {
      f && (R(e), R(t), R(i), R(l)), o && o.d(f), a && a.d(f), r && r.d(f), s && s.d(f);
    }
  };
}
function tf(n) {
  let e;
  return {
    c() {
      e = se(" /");
    },
    l(t) {
      e = ae(t, " /");
    },
    m(t, i) {
      z(t, e, i);
    },
    d(t) {
      t && R(e);
    }
  };
}
function no(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = se(e);
    },
    l(i) {
      t = ae(i, e);
    },
    m(i, l) {
      z(i, t, l);
    },
    p(i, l) {
      l[0] & /*progress*/
      128 && e !== (e = /*p*/
      i[41].desc + "") && Qe(t, e);
    },
    d(i) {
      i && R(t);
    }
  };
}
function io(n) {
  let e;
  return {
    c() {
      e = se("-");
    },
    l(t) {
      e = ae(t, "-");
    },
    m(t, i) {
      z(t, e, i);
    },
    d(t) {
      t && R(e);
    }
  };
}
function lo(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, i;
  return {
    c() {
      t = se(e), i = se("%");
    },
    l(l) {
      t = ae(l, e), i = ae(l, "%");
    },
    m(l, o) {
      z(l, t, o), z(l, i, o);
    },
    p(l, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (l[14][
        /*i*/
        l[43]
      ] || 0)).toFixed(1) + "") && Qe(t, e);
    },
    d(l) {
      l && (R(t), R(i));
    }
  };
}
function oo(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && to(n)
  );
  return {
    c() {
      t && t.c(), e = Je();
    },
    l(i) {
      t && t.l(i), e = Je();
    },
    m(i, l) {
      t && t.m(i, l), z(i, e, l);
    },
    p(i, l) {
      /*p*/
      i[41].desc != null || /*progress_level*/
      i[14] && /*progress_level*/
      i[14][
        /*i*/
        i[43]
      ] != null ? t ? t.p(i, l) : (t = to(i), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(i) {
      i && R(e), t && t.d(i);
    }
  };
}
function ao(n) {
  let e, t, i, l;
  const o = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), a = Vo(
    o,
    n,
    /*$$scope*/
    n[29],
    Xl
  );
  return {
    c() {
      e = pt("p"), t = se(
        /*loading_text*/
        n[9]
      ), i = Ze(), a && a.c(), this.h();
    },
    l(r) {
      e = bt(r, "P", { class: !0 });
      var s = gt(e);
      t = ae(
        s,
        /*loading_text*/
        n[9]
      ), s.forEach(R), i = Xe(r), a && a.l(r), this.h();
    },
    h() {
      st(e, "class", "loading svelte-17v219f");
    },
    m(r, s) {
      z(r, e, s), Zt(e, t), z(r, i, s), a && a.m(r, s), l = !0;
    },
    p(r, s) {
      (!l || s[0] & /*loading_text*/
      512) && Qe(
        t,
        /*loading_text*/
        r[9]
      ), a && a.p && (!l || s[0] & /*$$scope*/
      536870912) && Ko(
        a,
        o,
        r,
        /*$$scope*/
        r[29],
        l ? Xo(
          o,
          /*$$scope*/
          r[29],
          s,
          jr
        ) : Yo(
          /*$$scope*/
          r[29]
        ),
        Xl
      );
    },
    i(r) {
      l || (at(a, r), l = !0);
    },
    o(r) {
      vt(a, r), l = !1;
    },
    d(r) {
      r && (R(e), R(i)), a && a.d(r);
    }
  };
}
function nf(n) {
  let e, t, i, l, o;
  const a = [Xr, Yr], r = [];
  function s(f, _) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(n)) && (i = r[t] = a[t](n)), {
    c() {
      e = pt("div"), i && i.c(), this.h();
    },
    l(f) {
      e = bt(f, "DIV", { class: !0 });
      var _ = gt(e);
      i && i.l(_), _.forEach(R), this.h();
    },
    h() {
      st(e, "class", l = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-17v219f"), Ye(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden" || /*status*/
      n[4] == "streaming"), Ye(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), Ye(
        e,
        "generating",
        /*status*/
        n[4] === "generating" && /*show_progress*/
        n[6] === "full"
      ), Ye(
        e,
        "border",
        /*border*/
        n[12]
      ), Ot(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Ot(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, _) {
      z(f, e, _), ~t && r[t].m(e, null), n[33](e), o = !0;
    },
    p(f, _) {
      let d = t;
      t = s(f), t === d ? ~t && r[t].p(f, _) : (i && (Xi(), vt(r[d], 1, 1, () => {
        r[d] = null;
      }), Yi()), ~t ? (i = r[t], i ? i.p(f, _) : (i = r[t] = a[t](f), i.c()), at(i, 1), i.m(e, null)) : i = null), (!o || _[0] & /*variant, show_progress*/
      320 && l !== (l = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-17v219f")) && st(e, "class", l), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Ye(e, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden" || /*status*/
      f[4] == "streaming"), (!o || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Ye(
        e,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Ye(
        e,
        "generating",
        /*status*/
        f[4] === "generating" && /*show_progress*/
        f[6] === "full"
      ), (!o || _[0] & /*variant, show_progress, border*/
      4416) && Ye(
        e,
        "border",
        /*border*/
        f[12]
      ), _[0] & /*absolute*/
      1024 && Ot(
        e,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && Ot(
        e,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      o || (at(i), o = !0);
    },
    o(f) {
      vt(i), o = !1;
    },
    d(f) {
      f && R(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var lf = function(n, e, t, i) {
  function l(o) {
    return o instanceof t ? o : new t(function(a) {
      a(o);
    });
  }
  return new (t || (t = Promise))(function(o, a) {
    function r(_) {
      try {
        f(i.next(_));
      } catch (d) {
        a(d);
      }
    }
    function s(_) {
      try {
        f(i.throw(_));
      } catch (d) {
        a(d);
      }
    }
    function f(_) {
      _.done ? o(_.value) : l(_.value).then(r, s);
    }
    f((i = i.apply(n, e || [])).next());
  });
};
let ei = [], Ti = !1;
const of = typeof window < "u", Jo = of ? window.requestAnimationFrame : (n) => {
};
function af(n) {
  return lf(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (ei.push(e), !Ti) Ti = !0;
      else return;
      yield Hr(), Jo(() => {
        let i = [0, 0];
        for (let l = 0; l < ei.length; l++) {
          const a = ei[l].getBoundingClientRect();
          (l === 0 || a.top + window.scrollY <= i[0]) && (i[0] = a.top + window.scrollY, i[1] = l);
        }
        window.scrollTo({ top: i[0] - 20, behavior: "smooth" }), Ti = !1, ei = [];
      });
    }
  });
}
function sf(n, e, t) {
  let i, { $$slots: l = {}, $$scope: o } = e;
  this && this.__awaiter;
  const a = Vr();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: f } = e, { queue_size: _ } = e, { status: d } = e, { scroll_to_output: c = !1 } = e, { timer: u = !0 } = e, { show_progress: h = "full" } = e, { message: w = null } = e, { progress: T = null } = e, { variant: k = "default" } = e, { loading_text: v = "Loading..." } = e, { absolute: g = !0 } = e, { translucent: b = !1 } = e, { border: O = !1 } = e, { autoscroll: P } = e, U, Y = !1, F = 0, C = 0, J = null, q = null, ne = 0, H = null, ie, re = null, Oe = !0;
  const de = () => {
    t(0, s = t(27, J = t(19, K = null))), t(25, F = performance.now()), t(26, C = 0), Y = !0, ve();
  };
  function ve() {
    Jo(() => {
      t(26, C = (performance.now() - F) / 1e3), Y && ve();
    });
  }
  function Ce() {
    t(26, C = 0), t(0, s = t(27, J = t(19, K = null))), Y && (Y = !1);
  }
  Wr(() => {
    Y && Ce();
  });
  let K = null;
  function we(S) {
    jl[S ? "unshift" : "push"](() => {
      re = S, t(16, re), t(7, T), t(14, H), t(15, ie);
    });
  }
  const X = () => {
    a("clear_status");
  };
  function le(S) {
    jl[S ? "unshift" : "push"](() => {
      U = S, t(13, U);
    });
  }
  return n.$$set = (S) => {
    "i18n" in S && t(1, r = S.i18n), "eta" in S && t(0, s = S.eta), "queue_position" in S && t(2, f = S.queue_position), "queue_size" in S && t(3, _ = S.queue_size), "status" in S && t(4, d = S.status), "scroll_to_output" in S && t(22, c = S.scroll_to_output), "timer" in S && t(5, u = S.timer), "show_progress" in S && t(6, h = S.show_progress), "message" in S && t(23, w = S.message), "progress" in S && t(7, T = S.progress), "variant" in S && t(8, k = S.variant), "loading_text" in S && t(9, v = S.loading_text), "absolute" in S && t(10, g = S.absolute), "translucent" in S && t(11, b = S.translucent), "border" in S && t(12, O = S.border), "autoscroll" in S && t(24, P = S.autoscroll), "$$scope" in S && t(29, o = S.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = J), s != null && J !== s && (t(28, q = (performance.now() - F) / 1e3 + s), t(19, K = q.toFixed(1)), t(27, J = s))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ne = q === null || q <= 0 || !C ? null : Math.min(C / q, 1)), n.$$.dirty[0] & /*progress*/
    128 && T != null && t(18, Oe = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (T != null ? t(14, H = T.map((S) => {
      if (S.index != null && S.length != null)
        return S.index / S.length;
      if (S.progress != null)
        return S.progress;
    })) : t(14, H = null), H ? (t(15, ie = H[H.length - 1]), re && (ie === 0 ? t(16, re.style.transition = "0", re) : t(16, re.style.transition = "150ms", re))) : t(15, ie = void 0)), n.$$.dirty[0] & /*status*/
    16 && (d === "pending" ? de() : Ce()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && U && c && (d === "pending" || d === "complete") && af(U, P), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, i = C.toFixed(1));
  }, [
    s,
    r,
    f,
    _,
    d,
    u,
    h,
    T,
    k,
    v,
    g,
    b,
    O,
    U,
    H,
    ie,
    re,
    ne,
    Oe,
    K,
    i,
    a,
    c,
    w,
    P,
    F,
    C,
    J,
    q,
    o,
    l,
    we,
    X,
    le
  ];
}
class rf extends zr {
  constructor(e) {
    super(), qr(
      this,
      e,
      sf,
      nf,
      Br,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
/*! @license DOMPurify 3.2.1 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.2.1/LICENSE */
const {
  entries: Qo,
  setPrototypeOf: so,
  isFrozen: ff,
  getPrototypeOf: uf,
  getOwnPropertyDescriptor: cf
} = Object;
let {
  freeze: Ne,
  seal: xe,
  create: xo
} = Object, {
  apply: Ki,
  construct: Ji
} = typeof Reflect < "u" && Reflect;
Ne || (Ne = function(e) {
  return e;
});
xe || (xe = function(e) {
  return e;
});
Ki || (Ki = function(e, t, i) {
  return e.apply(t, i);
});
Ji || (Ji = function(e, t) {
  return new e(...t);
});
const ti = Ve(Array.prototype.forEach), ro = Ve(Array.prototype.pop), Cn = Ve(Array.prototype.push), ai = Ve(String.prototype.toLowerCase), Ai = Ve(String.prototype.toString), fo = Ve(String.prototype.match), Ln = Ve(String.prototype.replace), _f = Ve(String.prototype.indexOf), df = Ve(String.prototype.trim), lt = Ve(Object.prototype.hasOwnProperty), Ie = Ve(RegExp.prototype.test), In = mf(TypeError);
function Ve(n) {
  return function(e) {
    for (var t = arguments.length, i = new Array(t > 1 ? t - 1 : 0), l = 1; l < t; l++)
      i[l - 1] = arguments[l];
    return Ki(n, e, i);
  };
}
function mf(n) {
  return function() {
    for (var e = arguments.length, t = new Array(e), i = 0; i < e; i++)
      t[i] = arguments[i];
    return Ji(n, t);
  };
}
function G(n, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : ai;
  so && so(n, null);
  let i = e.length;
  for (; i--; ) {
    let l = e[i];
    if (typeof l == "string") {
      const o = t(l);
      o !== l && (ff(e) || (e[i] = o), l = o);
    }
    n[l] = !0;
  }
  return n;
}
function hf(n) {
  for (let e = 0; e < n.length; e++)
    lt(n, e) || (n[e] = null);
  return n;
}
function Ht(n) {
  const e = xo(null);
  for (const [t, i] of Qo(n))
    lt(n, t) && (Array.isArray(i) ? e[t] = hf(i) : i && typeof i == "object" && i.constructor === Object ? e[t] = Ht(i) : e[t] = i);
  return e;
}
function Nn(n, e) {
  for (; n !== null; ) {
    const i = cf(n, e);
    if (i) {
      if (i.get)
        return Ve(i.get);
      if (typeof i.value == "function")
        return Ve(i.value);
    }
    n = uf(n);
  }
  function t() {
    return null;
  }
  return t;
}
const uo = Ne(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), Si = Ne(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), Di = Ne(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), gf = Ne(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), Ci = Ne(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), bf = Ne(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), co = Ne(["#text"]), _o = Ne(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), Li = Ne(["accent-height", "accumulate", "additive", "alignment-baseline", "amplitude", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "exponent", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "intercept", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "slope", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "tablevalues", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), mo = Ne(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), ni = Ne(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), pf = xe(/\{\{[\w\W]*|[\w\W]*\}\}/gm), vf = xe(/<%[\w\W]*|[\w\W]*%>/gm), wf = xe(/\${[\w\W]*}/gm), kf = xe(/^data-[\-\w.\u00B7-\uFFFF]/), yf = xe(/^aria-[\-\w]+$/), $o = xe(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), Ef = xe(/^(?:\w+script|data):/i), Tf = xe(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), ea = xe(/^html$/i), Af = xe(/^[a-z][.\w]*(-[.\w]+)+$/i);
var ho = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  ARIA_ATTR: yf,
  ATTR_WHITESPACE: Tf,
  CUSTOM_ELEMENT: Af,
  DATA_ATTR: kf,
  DOCTYPE_NAME: ea,
  ERB_EXPR: vf,
  IS_ALLOWED_URI: $o,
  IS_SCRIPT_OR_DATA: Ef,
  MUSTACHE_EXPR: pf,
  TMPLIT_EXPR: wf
});
const On = {
  element: 1,
  attribute: 2,
  text: 3,
  cdataSection: 4,
  entityReference: 5,
  // Deprecated
  entityNode: 6,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9,
  documentType: 10,
  documentFragment: 11,
  notation: 12
  // Deprecated
}, Sf = function() {
  return typeof window > "u" ? null : window;
}, Df = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let i = null;
  const l = "data-tt-policy-suffix";
  t && t.hasAttribute(l) && (i = t.getAttribute(l));
  const o = "dompurify" + (i ? "#" + i : "");
  try {
    return e.createPolicy(o, {
      createHTML(a) {
        return a;
      },
      createScriptURL(a) {
        return a;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function ta() {
  let n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : Sf();
  const e = (I) => ta(I);
  if (e.version = "3.2.1", e.removed = [], !n || !n.document || n.document.nodeType !== On.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = n;
  const i = t, l = i.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: a,
    Node: r,
    Element: s,
    NodeFilter: f,
    NamedNodeMap: _ = n.NamedNodeMap || n.MozNamedAttrMap,
    HTMLFormElement: d,
    DOMParser: c,
    trustedTypes: u
  } = n, h = s.prototype, w = Nn(h, "cloneNode"), T = Nn(h, "remove"), k = Nn(h, "nextSibling"), v = Nn(h, "childNodes"), g = Nn(h, "parentNode");
  if (typeof a == "function") {
    const I = t.createElement("template");
    I.content && I.content.ownerDocument && (t = I.content.ownerDocument);
  }
  let b, O = "";
  const {
    implementation: P,
    createNodeIterator: U,
    createDocumentFragment: Y,
    getElementsByTagName: F
  } = t, {
    importNode: C
  } = i;
  let J = {};
  e.isSupported = typeof Qo == "function" && typeof g == "function" && P && P.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: q,
    ERB_EXPR: ne,
    TMPLIT_EXPR: H,
    DATA_ATTR: ie,
    ARIA_ATTR: re,
    IS_SCRIPT_OR_DATA: Oe,
    ATTR_WHITESPACE: de,
    CUSTOM_ELEMENT: ve
  } = ho;
  let {
    IS_ALLOWED_URI: Ce
  } = ho, K = null;
  const we = G({}, [...uo, ...Si, ...Di, ...Ci, ...co]);
  let X = null;
  const le = G({}, [..._o, ...Li, ...mo, ...ni]);
  let S = Object.seal(xo(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), Te = null, be = null, D = !0, Z = !0, ee = !1, y = !0, M = !1, W = !0, B = !1, x = !1, ce = !1, _e = !1, me = !1, Ae = !1, fe = !0, Re = !1;
  const wt = "user-content-";
  let Pt = !0, E = !1, Tt = {}, At = null;
  const Hn = G({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let Wn = null;
  const Vn = G({}, ["audio", "video", "img", "source", "image", "track"]);
  let yn = null;
  const Gn = G({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), tn = "http://www.w3.org/1998/Math/MathML", nn = "http://www.w3.org/2000/svg", $e = "http://www.w3.org/1999/xhtml";
  let St = $e, En = !1, Tn = null;
  const mi = G({}, [tn, nn, $e], Ai);
  let ln = G({}, ["mi", "mo", "mn", "ms", "mtext"]), on = G({}, ["annotation-xml"]);
  const hi = G({}, ["title", "style", "font", "a", "script"]);
  let Ft = null;
  const gi = ["application/xhtml+xml", "text/html"], bi = "text/html";
  let he = null, Dt = null;
  const pi = t.createElement("form"), jn = function(m) {
    return m instanceof RegExp || m instanceof Function;
  }, An = function() {
    let m = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(Dt && Dt === m)) {
      if ((!m || typeof m != "object") && (m = {}), m = Ht(m), Ft = // eslint-disable-next-line unicorn/prefer-includes
      gi.indexOf(m.PARSER_MEDIA_TYPE) === -1 ? bi : m.PARSER_MEDIA_TYPE, he = Ft === "application/xhtml+xml" ? Ai : ai, K = lt(m, "ALLOWED_TAGS") ? G({}, m.ALLOWED_TAGS, he) : we, X = lt(m, "ALLOWED_ATTR") ? G({}, m.ALLOWED_ATTR, he) : le, Tn = lt(m, "ALLOWED_NAMESPACES") ? G({}, m.ALLOWED_NAMESPACES, Ai) : mi, yn = lt(m, "ADD_URI_SAFE_ATTR") ? G(Ht(Gn), m.ADD_URI_SAFE_ATTR, he) : Gn, Wn = lt(m, "ADD_DATA_URI_TAGS") ? G(Ht(Vn), m.ADD_DATA_URI_TAGS, he) : Vn, At = lt(m, "FORBID_CONTENTS") ? G({}, m.FORBID_CONTENTS, he) : Hn, Te = lt(m, "FORBID_TAGS") ? G({}, m.FORBID_TAGS, he) : {}, be = lt(m, "FORBID_ATTR") ? G({}, m.FORBID_ATTR, he) : {}, Tt = lt(m, "USE_PROFILES") ? m.USE_PROFILES : !1, D = m.ALLOW_ARIA_ATTR !== !1, Z = m.ALLOW_DATA_ATTR !== !1, ee = m.ALLOW_UNKNOWN_PROTOCOLS || !1, y = m.ALLOW_SELF_CLOSE_IN_ATTR !== !1, M = m.SAFE_FOR_TEMPLATES || !1, W = m.SAFE_FOR_XML !== !1, B = m.WHOLE_DOCUMENT || !1, _e = m.RETURN_DOM || !1, me = m.RETURN_DOM_FRAGMENT || !1, Ae = m.RETURN_TRUSTED_TYPE || !1, ce = m.FORCE_BODY || !1, fe = m.SANITIZE_DOM !== !1, Re = m.SANITIZE_NAMED_PROPS || !1, Pt = m.KEEP_CONTENT !== !1, E = m.IN_PLACE || !1, Ce = m.ALLOWED_URI_REGEXP || $o, St = m.NAMESPACE || $e, ln = m.MATHML_TEXT_INTEGRATION_POINTS || ln, on = m.HTML_INTEGRATION_POINTS || on, S = m.CUSTOM_ELEMENT_HANDLING || {}, m.CUSTOM_ELEMENT_HANDLING && jn(m.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (S.tagNameCheck = m.CUSTOM_ELEMENT_HANDLING.tagNameCheck), m.CUSTOM_ELEMENT_HANDLING && jn(m.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (S.attributeNameCheck = m.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), m.CUSTOM_ELEMENT_HANDLING && typeof m.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (S.allowCustomizedBuiltInElements = m.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), M && (Z = !1), me && (_e = !0), Tt && (K = G({}, co), X = [], Tt.html === !0 && (G(K, uo), G(X, _o)), Tt.svg === !0 && (G(K, Si), G(X, Li), G(X, ni)), Tt.svgFilters === !0 && (G(K, Di), G(X, Li), G(X, ni)), Tt.mathMl === !0 && (G(K, Ci), G(X, mo), G(X, ni))), m.ADD_TAGS && (K === we && (K = Ht(K)), G(K, m.ADD_TAGS, he)), m.ADD_ATTR && (X === le && (X = Ht(X)), G(X, m.ADD_ATTR, he)), m.ADD_URI_SAFE_ATTR && G(yn, m.ADD_URI_SAFE_ATTR, he), m.FORBID_CONTENTS && (At === Hn && (At = Ht(At)), G(At, m.FORBID_CONTENTS, he)), Pt && (K["#text"] = !0), B && G(K, ["html", "head", "body"]), K.table && (G(K, ["tbody"]), delete Te.tbody), m.TRUSTED_TYPES_POLICY) {
        if (typeof m.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw In('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof m.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw In('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        b = m.TRUSTED_TYPES_POLICY, O = b.createHTML("");
      } else
        b === void 0 && (b = Df(u, l)), b !== null && typeof O == "string" && (O = b.createHTML(""));
      Ne && Ne(m), Dt = m;
    }
  }, p = G({}, [...Si, ...Di, ...gf]), te = G({}, [...Ci, ...bf]), ge = function(m) {
    let A = g(m);
    (!A || !A.tagName) && (A = {
      namespaceURI: St,
      tagName: "template"
    });
    const L = ai(m.tagName), oe = ai(A.tagName);
    return Tn[m.namespaceURI] ? m.namespaceURI === nn ? A.namespaceURI === $e ? L === "svg" : A.namespaceURI === tn ? L === "svg" && (oe === "annotation-xml" || ln[oe]) : !!p[L] : m.namespaceURI === tn ? A.namespaceURI === $e ? L === "math" : A.namespaceURI === nn ? L === "math" && on[oe] : !!te[L] : m.namespaceURI === $e ? A.namespaceURI === nn && !on[oe] || A.namespaceURI === tn && !ln[oe] ? !1 : !te[L] && (hi[L] || !p[L]) : !!(Ft === "application/xhtml+xml" && Tn[m.namespaceURI]) : !1;
  }, $ = function(m) {
    Cn(e.removed, {
      element: m
    });
    try {
      g(m).removeChild(m);
    } catch {
      T(m);
    }
  }, rt = function(m, A) {
    try {
      Cn(e.removed, {
        attribute: A.getAttributeNode(m),
        from: A
      });
    } catch {
      Cn(e.removed, {
        attribute: null,
        from: A
      });
    }
    if (A.removeAttribute(m), m === "is" && !X[m])
      if (_e || me)
        try {
          $(A);
        } catch {
        }
      else
        try {
          A.setAttribute(m, "");
        } catch {
        }
  }, Ct = function(m) {
    let A = null, L = null;
    if (ce)
      m = "<remove></remove>" + m;
    else {
      const ke = fo(m, /^[\r\n\t ]+/);
      L = ke && ke[0];
    }
    Ft === "application/xhtml+xml" && St === $e && (m = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + m + "</body></html>");
    const oe = b ? b.createHTML(m) : m;
    if (St === $e)
      try {
        A = new c().parseFromString(oe, Ft);
      } catch {
      }
    if (!A || !A.documentElement) {
      A = P.createDocument(St, "template", null);
      try {
        A.documentElement.innerHTML = En ? O : oe;
      } catch {
      }
    }
    const Se = A.body || A.documentElement;
    return m && L && Se.insertBefore(t.createTextNode(L), Se.childNodes[0] || null), St === $e ? F.call(A, B ? "html" : "body")[0] : B ? A.documentElement : Se;
  }, Ut = function(m) {
    return U.call(
      m.ownerDocument || m,
      m,
      // eslint-disable-next-line no-bitwise
      f.SHOW_ELEMENT | f.SHOW_COMMENT | f.SHOW_TEXT | f.SHOW_PROCESSING_INSTRUCTION | f.SHOW_CDATA_SECTION,
      null
    );
  }, Yn = function(m) {
    return m instanceof d && (typeof m.nodeName != "string" || typeof m.textContent != "string" || typeof m.removeChild != "function" || !(m.attributes instanceof _) || typeof m.removeAttribute != "function" || typeof m.setAttribute != "function" || typeof m.namespaceURI != "string" || typeof m.insertBefore != "function" || typeof m.hasChildNodes != "function");
  }, Xn = function(m) {
    return typeof r == "function" && m instanceof r;
  };
  function qe(I, m, A) {
    J[I] && ti(J[I], (L) => {
      L.call(e, m, A, Dt);
    });
  }
  const ft = function(m) {
    let A = null;
    if (qe("beforeSanitizeElements", m, null), Yn(m))
      return $(m), !0;
    const L = he(m.nodeName);
    if (qe("uponSanitizeElement", m, {
      tagName: L,
      allowedTags: K
    }), m.hasChildNodes() && !Xn(m.firstElementChild) && Ie(/<[/\w]/g, m.innerHTML) && Ie(/<[/\w]/g, m.textContent) || m.nodeType === On.progressingInstruction || W && m.nodeType === On.comment && Ie(/<[/\w]/g, m.data))
      return $(m), !0;
    if (!K[L] || Te[L]) {
      if (!Te[L] && tl(L) && (S.tagNameCheck instanceof RegExp && Ie(S.tagNameCheck, L) || S.tagNameCheck instanceof Function && S.tagNameCheck(L)))
        return !1;
      if (Pt && !At[L]) {
        const oe = g(m) || m.parentNode, Se = v(m) || m.childNodes;
        if (Se && oe) {
          const ke = Se.length;
          for (let Me = ke - 1; Me >= 0; --Me) {
            const ut = w(Se[Me], !0);
            ut.__removalCount = (m.__removalCount || 0) + 1, oe.insertBefore(ut, k(m));
          }
        }
      }
      return $(m), !0;
    }
    return m instanceof s && !ge(m) || (L === "noscript" || L === "noembed" || L === "noframes") && Ie(/<\/no(script|embed|frames)/i, m.innerHTML) ? ($(m), !0) : (M && m.nodeType === On.text && (A = m.textContent, ti([q, ne, H], (oe) => {
      A = Ln(A, oe, " ");
    }), m.textContent !== A && (Cn(e.removed, {
      element: m.cloneNode()
    }), m.textContent = A)), qe("afterSanitizeElements", m, null), !1);
  }, an = function(m, A, L) {
    if (fe && (A === "id" || A === "name") && (L in t || L in pi))
      return !1;
    if (!(Z && !be[A] && Ie(ie, A))) {
      if (!(D && Ie(re, A))) {
        if (!X[A] || be[A]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(tl(m) && (S.tagNameCheck instanceof RegExp && Ie(S.tagNameCheck, m) || S.tagNameCheck instanceof Function && S.tagNameCheck(m)) && (S.attributeNameCheck instanceof RegExp && Ie(S.attributeNameCheck, A) || S.attributeNameCheck instanceof Function && S.attributeNameCheck(A)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            A === "is" && S.allowCustomizedBuiltInElements && (S.tagNameCheck instanceof RegExp && Ie(S.tagNameCheck, L) || S.tagNameCheck instanceof Function && S.tagNameCheck(L)))
          ) return !1;
        } else if (!yn[A]) {
          if (!Ie(Ce, Ln(L, de, ""))) {
            if (!((A === "src" || A === "xlink:href" || A === "href") && m !== "script" && _f(L, "data:") === 0 && Wn[m])) {
              if (!(ee && !Ie(Oe, Ln(L, de, "")))) {
                if (L)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, tl = function(m) {
    return m !== "annotation-xml" && fo(m, ve);
  }, nl = function(m) {
    qe("beforeSanitizeAttributes", m, null);
    const {
      attributes: A
    } = m;
    if (!A)
      return;
    const L = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: X,
      forceKeepAttr: void 0
    };
    let oe = A.length;
    for (; oe--; ) {
      const Se = A[oe], {
        name: ke,
        namespaceURI: Me,
        value: ut
      } = Se, Sn = he(ke);
      let Le = ke === "value" ? ut : df(ut);
      if (L.attrName = Sn, L.attrValue = Le, L.keepAttr = !0, L.forceKeepAttr = void 0, qe("uponSanitizeAttribute", m, L), Le = L.attrValue, Re && (Sn === "id" || Sn === "name") && (rt(ke, m), Le = wt + Le), W && Ie(/((--!?|])>)|<\/(style|title)/i, Le)) {
        rt(ke, m);
        continue;
      }
      if (L.forceKeepAttr || (rt(ke, m), !L.keepAttr))
        continue;
      if (!y && Ie(/\/>/i, Le)) {
        rt(ke, m);
        continue;
      }
      M && ti([q, ne, H], (ll) => {
        Le = Ln(Le, ll, " ");
      });
      const il = he(m.nodeName);
      if (an(il, Sn, Le)) {
        if (b && typeof u == "object" && typeof u.getAttributeType == "function" && !Me)
          switch (u.getAttributeType(il, Sn)) {
            case "TrustedHTML": {
              Le = b.createHTML(Le);
              break;
            }
            case "TrustedScriptURL": {
              Le = b.createScriptURL(Le);
              break;
            }
          }
        try {
          Me ? m.setAttributeNS(Me, ke, Le) : m.setAttribute(ke, Le), Yn(m) ? $(m) : ro(e.removed);
        } catch {
        }
      }
    }
    qe("afterSanitizeAttributes", m, null);
  }, na = function I(m) {
    let A = null;
    const L = Ut(m);
    for (qe("beforeSanitizeShadowDOM", m, null); A = L.nextNode(); )
      qe("uponSanitizeShadowNode", A, null), !ft(A) && (A.content instanceof o && I(A.content), nl(A));
    qe("afterSanitizeShadowDOM", m, null);
  };
  return e.sanitize = function(I) {
    let m = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, A = null, L = null, oe = null, Se = null;
    if (En = !I, En && (I = "<!-->"), typeof I != "string" && !Xn(I))
      if (typeof I.toString == "function") {
        if (I = I.toString(), typeof I != "string")
          throw In("dirty is not a string, aborting");
      } else
        throw In("toString is not a function");
    if (!e.isSupported)
      return I;
    if (x || An(m), e.removed = [], typeof I == "string" && (E = !1), E) {
      if (I.nodeName) {
        const ut = he(I.nodeName);
        if (!K[ut] || Te[ut])
          throw In("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (I instanceof r)
      A = Ct("<!---->"), L = A.ownerDocument.importNode(I, !0), L.nodeType === On.element && L.nodeName === "BODY" || L.nodeName === "HTML" ? A = L : A.appendChild(L);
    else {
      if (!_e && !M && !B && // eslint-disable-next-line unicorn/prefer-includes
      I.indexOf("<") === -1)
        return b && Ae ? b.createHTML(I) : I;
      if (A = Ct(I), !A)
        return _e ? null : Ae ? O : "";
    }
    A && ce && $(A.firstChild);
    const ke = Ut(E ? I : A);
    for (; oe = ke.nextNode(); )
      ft(oe) || (oe.content instanceof o && na(oe.content), nl(oe));
    if (E)
      return I;
    if (_e) {
      if (me)
        for (Se = Y.call(A.ownerDocument); A.firstChild; )
          Se.appendChild(A.firstChild);
      else
        Se = A;
      return (X.shadowroot || X.shadowrootmode) && (Se = C.call(i, Se, !0)), Se;
    }
    let Me = B ? A.outerHTML : A.innerHTML;
    return B && K["!doctype"] && A.ownerDocument && A.ownerDocument.doctype && A.ownerDocument.doctype.name && Ie(ea, A.ownerDocument.doctype.name) && (Me = "<!DOCTYPE " + A.ownerDocument.doctype.name + `>
` + Me), M && ti([q, ne, H], (ut) => {
      Me = Ln(Me, ut, " ");
    }), b && Ae ? b.createHTML(Me) : Me;
  }, e.setConfig = function() {
    let I = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    An(I), x = !0;
  }, e.clearConfig = function() {
    Dt = null, x = !1;
  }, e.isValidAttribute = function(I, m, A) {
    Dt || An({});
    const L = he(I), oe = he(m);
    return an(L, oe, A);
  }, e.addHook = function(I, m) {
    typeof m == "function" && (J[I] = J[I] || [], Cn(J[I], m));
  }, e.removeHook = function(I) {
    if (J[I])
      return ro(J[I]);
  }, e.removeHooks = function(I) {
    J[I] && (J[I] = []);
  }, e.removeAllHooks = function() {
    J = {};
  }, e;
}
ta();
const {
  SvelteComponent: Cf,
  add_flush_callback: Ii,
  assign: Lf,
  bind: Ni,
  binding_callbacks: Oi,
  check_outros: If,
  claim_component: Qi,
  claim_space: Nf,
  create_component: xi,
  destroy_component: $i,
  detach: Of,
  flush: j,
  get_spread_object: Rf,
  get_spread_update: Mf,
  group_outros: Pf,
  init: Ff,
  insert_hydration: Uf,
  mount_component: el,
  safe_not_equal: zf,
  space: qf,
  transition_in: mn,
  transition_out: zn
} = window.__gradio__svelte__internal;
function go(n) {
  let e, t;
  const i = [
    { autoscroll: (
      /*gradio*/
      n[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[2].i18n
    ) },
    /*loading_status*/
    n[20]
  ];
  let l = {};
  for (let o = 0; o < i.length; o += 1)
    l = Lf(l, i[o]);
  return e = new rf({ props: l }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[39]
  ), {
    c() {
      xi(e.$$.fragment);
    },
    l(o) {
      Qi(e.$$.fragment, o);
    },
    m(o, a) {
      el(e, o, a), t = !0;
    },
    p(o, a) {
      const r = a[0] & /*gradio, loading_status*/
      1048580 ? Mf(i, [
        a[0] & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          o[2].autoscroll
        ) },
        a[0] & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          o[2].i18n
        ) },
        a[0] & /*loading_status*/
        1048576 && Rf(
          /*loading_status*/
          o[20]
        )
      ]) : {};
      e.$set(r);
    },
    i(o) {
      t || (mn(e.$$.fragment, o), t = !0);
    },
    o(o) {
      zn(e.$$.fragment, o), t = !1;
    },
    d(o) {
      $i(e, o);
    }
  };
}
function Bf(n) {
  let e, t, i, l, o, a, r = (
    /*loading_status*/
    n[20] && go(n)
  );
  function s(c) {
    n[42](c);
  }
  function f(c) {
    n[43](c);
  }
  function _(c) {
    n[44](c);
  }
  let d = {
    file_types: (
      /*file_types*/
      n[6]
    ),
    root: (
      /*root*/
      n[26]
    ),
    label: (
      /*label*/
      n[9]
    ),
    info: (
      /*info*/
      n[10]
    ),
    show_label: (
      /*show_label*/
      n[11]
    ),
    lines: (
      /*lines*/
      n[7]
    ),
    rtl: (
      /*rtl*/
      n[21]
    ),
    text_align: (
      /*text_align*/
      n[22]
    ),
    max_lines: /*max_lines*/ n[12] ? (
      /*max_lines*/
      n[12]
    ) : (
      /*lines*/
      n[7] + 1
    ),
    placeholder: (
      /*placeholder*/
      n[8]
    ),
    upload_btn: (
      /*upload_btn*/
      n[16]
    ),
    submit_btn: (
      /*submit_btn*/
      n[17]
    ),
    stop_btn: (
      /*stop_btn*/
      n[18]
    ),
    autofocus: (
      /*autofocus*/
      n[23]
    ),
    container: (
      /*container*/
      n[13]
    ),
    autoscroll: (
      /*autoscroll*/
      n[24]
    ),
    file_count: (
      /*file_count*/
      n[27]
    ),
    interactive: (
      /*interactive*/
      n[25]
    ),
    loading_message: (
      /*loading_message*/
      n[19]
    ),
    audio_btn: (
      /*audio_btn*/
      n[28]
    ),
    stop_audio_btn: (
      /*stop_audio_btn*/
      n[29]
    ),
    max_file_size: (
      /*gradio*/
      n[2].max_file_size
    ),
    on_change_cb: (
      /*on_change_cb*/
      n[38]
    ),
    server: (
      /*server*/
      n[36]
    ),
    rtc_configuration: (
      /*rtc_configuration*/
      n[30]
    ),
    time_limit: (
      /*time_limit*/
      n[31]
    ),
    track_constraints: (
      /*track_constraints*/
      n[35]
    ),
    mode: (
      /*mode*/
      n[33]
    ),
    rtp_params: (
      /*rtp_params*/
      n[34]
    ),
    modality: (
      /*modality*/
      n[32]
    ),
    gradio: (
      /*gradio*/
      n[2]
    ),
    upload: (
      /*func*/
      n[40]
    ),
    stream_handler: (
      /*func_1*/
      n[41]
    )
  };
  return (
    /*value*/
    n[0] !== void 0 && (d.value = /*value*/
    n[0]), /*value_is_output*/
    n[1] !== void 0 && (d.value_is_output = /*value_is_output*/
    n[1]), /*dragging*/
    n[37] !== void 0 && (d.dragging = /*dragging*/
    n[37]), t = new Tr({ props: d }), Oi.push(() => Ni(t, "value", s)), Oi.push(() => Ni(t, "value_is_output", f)), Oi.push(() => Ni(t, "dragging", _)), t.$on(
      "tick",
      /*tick_handler*/
      n[45]
    ), t.$on(
      "change",
      /*change_handler*/
      n[46]
    ), t.$on(
      "input",
      /*input_handler*/
      n[47]
    ), t.$on(
      "submit",
      /*submit_handler*/
      n[48]
    ), t.$on(
      "stop",
      /*stop_handler*/
      n[49]
    ), t.$on(
      "blur",
      /*blur_handler*/
      n[50]
    ), t.$on(
      "select",
      /*select_handler*/
      n[51]
    ), t.$on(
      "focus",
      /*focus_handler*/
      n[52]
    ), t.$on(
      "upload",
      /*upload_handler*/
      n[53]
    ), t.$on(
      "error",
      /*error_handler*/
      n[54]
    ), t.$on(
      "start_recording",
      /*start_recording_handler*/
      n[55]
    ), t.$on(
      "stop_recording",
      /*stop_recording_handler*/
      n[56]
    ), {
      c() {
        r && r.c(), e = qf(), xi(t.$$.fragment);
      },
      l(c) {
        r && r.l(c), e = Nf(c), Qi(t.$$.fragment, c);
      },
      m(c, u) {
        r && r.m(c, u), Uf(c, e, u), el(t, c, u), a = !0;
      },
      p(c, u) {
        /*loading_status*/
        c[20] ? r ? (r.p(c, u), u[0] & /*loading_status*/
        1048576 && mn(r, 1)) : (r = go(c), r.c(), mn(r, 1), r.m(e.parentNode, e)) : r && (Pf(), zn(r, 1, 1, () => {
          r = null;
        }), If());
        const h = {};
        u[0] & /*file_types*/
        64 && (h.file_types = /*file_types*/
        c[6]), u[0] & /*root*/
        67108864 && (h.root = /*root*/
        c[26]), u[0] & /*label*/
        512 && (h.label = /*label*/
        c[9]), u[0] & /*info*/
        1024 && (h.info = /*info*/
        c[10]), u[0] & /*show_label*/
        2048 && (h.show_label = /*show_label*/
        c[11]), u[0] & /*lines*/
        128 && (h.lines = /*lines*/
        c[7]), u[0] & /*rtl*/
        2097152 && (h.rtl = /*rtl*/
        c[21]), u[0] & /*text_align*/
        4194304 && (h.text_align = /*text_align*/
        c[22]), u[0] & /*max_lines, lines*/
        4224 && (h.max_lines = /*max_lines*/
        c[12] ? (
          /*max_lines*/
          c[12]
        ) : (
          /*lines*/
          c[7] + 1
        )), u[0] & /*placeholder*/
        256 && (h.placeholder = /*placeholder*/
        c[8]), u[0] & /*upload_btn*/
        65536 && (h.upload_btn = /*upload_btn*/
        c[16]), u[0] & /*submit_btn*/
        131072 && (h.submit_btn = /*submit_btn*/
        c[17]), u[0] & /*stop_btn*/
        262144 && (h.stop_btn = /*stop_btn*/
        c[18]), u[0] & /*autofocus*/
        8388608 && (h.autofocus = /*autofocus*/
        c[23]), u[0] & /*container*/
        8192 && (h.container = /*container*/
        c[13]), u[0] & /*autoscroll*/
        16777216 && (h.autoscroll = /*autoscroll*/
        c[24]), u[0] & /*file_count*/
        134217728 && (h.file_count = /*file_count*/
        c[27]), u[0] & /*interactive*/
        33554432 && (h.interactive = /*interactive*/
        c[25]), u[0] & /*loading_message*/
        524288 && (h.loading_message = /*loading_message*/
        c[19]), u[0] & /*audio_btn*/
        268435456 && (h.audio_btn = /*audio_btn*/
        c[28]), u[0] & /*stop_audio_btn*/
        536870912 && (h.stop_audio_btn = /*stop_audio_btn*/
        c[29]), u[0] & /*gradio*/
        4 && (h.max_file_size = /*gradio*/
        c[2].max_file_size), u[1] & /*server*/
        32 && (h.server = /*server*/
        c[36]), u[0] & /*rtc_configuration*/
        1073741824 && (h.rtc_configuration = /*rtc_configuration*/
        c[30]), u[1] & /*time_limit*/
        1 && (h.time_limit = /*time_limit*/
        c[31]), u[1] & /*track_constraints*/
        16 && (h.track_constraints = /*track_constraints*/
        c[35]), u[1] & /*mode*/
        4 && (h.mode = /*mode*/
        c[33]), u[1] & /*rtp_params*/
        8 && (h.rtp_params = /*rtp_params*/
        c[34]), u[1] & /*modality*/
        2 && (h.modality = /*modality*/
        c[32]), u[0] & /*gradio*/
        4 && (h.gradio = /*gradio*/
        c[2]), u[0] & /*gradio*/
        4 && (h.upload = /*func*/
        c[40]), u[0] & /*gradio*/
        4 && (h.stream_handler = /*func_1*/
        c[41]), !i && u[0] & /*value*/
        1 && (i = !0, h.value = /*value*/
        c[0], Ii(() => i = !1)), !l && u[0] & /*value_is_output*/
        2 && (l = !0, h.value_is_output = /*value_is_output*/
        c[1], Ii(() => l = !1)), !o && u[1] & /*dragging*/
        64 && (o = !0, h.dragging = /*dragging*/
        c[37], Ii(() => o = !1)), t.$set(h);
      },
      i(c) {
        a || (mn(r), mn(t.$$.fragment, c), a = !0);
      },
      o(c) {
        zn(r), zn(t.$$.fragment, c), a = !1;
      },
      d(c) {
        c && Of(e), r && r.d(c), $i(t, c);
      }
    }
  );
}
function Hf(n) {
  let e, t;
  return e = new Qa({
    props: {
      visible: (
        /*visible*/
        n[5]
      ),
      elem_id: (
        /*elem_id*/
        n[3]
      ),
      elem_classes: [.../*elem_classes*/
      n[4], "multimodal-textbox"],
      scale: (
        /*scale*/
        n[14]
      ),
      min_width: (
        /*min_width*/
        n[15]
      ),
      allow_overflow: !1,
      padding: (
        /*container*/
        n[13]
      ),
      border_mode: (
        /*dragging*/
        n[37] ? "focus" : "base"
      ),
      $$slots: { default: [Bf] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      xi(e.$$.fragment);
    },
    l(i) {
      Qi(e.$$.fragment, i);
    },
    m(i, l) {
      el(e, i, l), t = !0;
    },
    p(i, l) {
      const o = {};
      l[0] & /*visible*/
      32 && (o.visible = /*visible*/
      i[5]), l[0] & /*elem_id*/
      8 && (o.elem_id = /*elem_id*/
      i[3]), l[0] & /*elem_classes*/
      16 && (o.elem_classes = [.../*elem_classes*/
      i[4], "multimodal-textbox"]), l[0] & /*scale*/
      16384 && (o.scale = /*scale*/
      i[14]), l[0] & /*min_width*/
      32768 && (o.min_width = /*min_width*/
      i[15]), l[0] & /*container*/
      8192 && (o.padding = /*container*/
      i[13]), l[1] & /*dragging*/
      64 && (o.border_mode = /*dragging*/
      i[37] ? "focus" : "base"), l[0] & /*file_types, root, label, info, show_label, lines, rtl, text_align, max_lines, placeholder, upload_btn, submit_btn, stop_btn, autofocus, container, autoscroll, file_count, interactive, loading_message, audio_btn, stop_audio_btn, gradio, rtc_configuration, value, value_is_output, loading_status*/
      2147434439 | l[1] & /*$$scope, server, time_limit, track_constraints, mode, rtp_params, modality, dragging*/
      67108991 && (o.$$scope = { dirty: l, ctx: i }), e.$set(o);
    },
    i(i) {
      t || (mn(e.$$.fragment, i), t = !0);
    },
    o(i) {
      zn(e.$$.fragment, i), t = !1;
    },
    d(i) {
      $i(e, i);
    }
  };
}
function Wf(n, e, t) {
  let { gradio: i } = e, { elem_id: l = "" } = e, { elem_classes: o = [] } = e, { visible: a = !0 } = e, { value: r = {
    text: "",
    files: [],
    audio: "__webrtc_value__"
  } } = e, { file_types: s = null } = e, { lines: f } = e, { placeholder: _ = "" } = e, { label: d = "MultimodalTextbox" } = e, { info: c = void 0 } = e, { show_label: u } = e, { max_lines: h } = e, { container: w = !0 } = e, { scale: T = null } = e, { min_width: k = void 0 } = e, { upload_btn: v = null } = e, { submit_btn: g = null } = e, { stop_btn: b = null } = e, { loading_message: O = "... Loading files ..." } = e, { loading_status: P = void 0 } = e, { value_is_output: U = !1 } = e, { rtl: Y = !1 } = e, { text_align: F = void 0 } = e, { autofocus: C = !1 } = e, { autoscroll: J = !0 } = e, { interactive: q } = e, { root: ne } = e, { file_count: H } = e, { audio_btn: ie } = e, { stop_audio_btn: re } = e, { rtc_configuration: Oe } = e, { time_limit: de = null } = e, { modality: ve = "audio" } = e, { mode: Ce = "send-receive" } = e, { rtp_params: K = {} } = e, { track_constraints: we = {} } = e, { server: X } = e;
  const le = (E) => {
    i.dispatch(E === "change" ? "state_change" : "tick");
  };
  let S;
  const Te = () => i.dispatch("clear_status", P), be = (...E) => i.client.upload(...E), D = (...E) => i.client.stream(...E);
  function Z(E) {
    r = E, t(0, r);
  }
  function ee(E) {
    U = E, t(1, U);
  }
  function y(E) {
    S = E, t(37, S);
  }
  const M = () => i.dispatch("tick"), W = () => i.dispatch("change", r), B = () => i.dispatch("input"), x = () => i.dispatch("submit"), ce = () => i.dispatch("stop"), _e = () => i.dispatch("blur"), me = (E) => i.dispatch("select", E.detail), Ae = () => i.dispatch("focus"), fe = ({ detail: E }) => i.dispatch("upload", E), Re = ({ detail: E }) => {
    i.dispatch("error", E);
  }, wt = () => i.dispatch("start_recording"), Pt = () => i.dispatch("stop_recording");
  return n.$$set = (E) => {
    "gradio" in E && t(2, i = E.gradio), "elem_id" in E && t(3, l = E.elem_id), "elem_classes" in E && t(4, o = E.elem_classes), "visible" in E && t(5, a = E.visible), "value" in E && t(0, r = E.value), "file_types" in E && t(6, s = E.file_types), "lines" in E && t(7, f = E.lines), "placeholder" in E && t(8, _ = E.placeholder), "label" in E && t(9, d = E.label), "info" in E && t(10, c = E.info), "show_label" in E && t(11, u = E.show_label), "max_lines" in E && t(12, h = E.max_lines), "container" in E && t(13, w = E.container), "scale" in E && t(14, T = E.scale), "min_width" in E && t(15, k = E.min_width), "upload_btn" in E && t(16, v = E.upload_btn), "submit_btn" in E && t(17, g = E.submit_btn), "stop_btn" in E && t(18, b = E.stop_btn), "loading_message" in E && t(19, O = E.loading_message), "loading_status" in E && t(20, P = E.loading_status), "value_is_output" in E && t(1, U = E.value_is_output), "rtl" in E && t(21, Y = E.rtl), "text_align" in E && t(22, F = E.text_align), "autofocus" in E && t(23, C = E.autofocus), "autoscroll" in E && t(24, J = E.autoscroll), "interactive" in E && t(25, q = E.interactive), "root" in E && t(26, ne = E.root), "file_count" in E && t(27, H = E.file_count), "audio_btn" in E && t(28, ie = E.audio_btn), "stop_audio_btn" in E && t(29, re = E.stop_audio_btn), "rtc_configuration" in E && t(30, Oe = E.rtc_configuration), "time_limit" in E && t(31, de = E.time_limit), "modality" in E && t(32, ve = E.modality), "mode" in E && t(33, Ce = E.mode), "rtp_params" in E && t(34, K = E.rtp_params), "track_constraints" in E && t(35, we = E.track_constraints), "server" in E && t(36, X = E.server);
  }, [
    r,
    U,
    i,
    l,
    o,
    a,
    s,
    f,
    _,
    d,
    c,
    u,
    h,
    w,
    T,
    k,
    v,
    g,
    b,
    O,
    P,
    Y,
    F,
    C,
    J,
    q,
    ne,
    H,
    ie,
    re,
    Oe,
    de,
    ve,
    Ce,
    K,
    we,
    X,
    S,
    le,
    Te,
    be,
    D,
    Z,
    ee,
    y,
    M,
    W,
    B,
    x,
    ce,
    _e,
    me,
    Ae,
    fe,
    Re,
    wt,
    Pt
  ];
}
class jf extends Cf {
  constructor(e) {
    super(), Ff(
      this,
      e,
      Wf,
      Hf,
      zf,
      {
        gradio: 2,
        elem_id: 3,
        elem_classes: 4,
        visible: 5,
        value: 0,
        file_types: 6,
        lines: 7,
        placeholder: 8,
        label: 9,
        info: 10,
        show_label: 11,
        max_lines: 12,
        container: 13,
        scale: 14,
        min_width: 15,
        upload_btn: 16,
        submit_btn: 17,
        stop_btn: 18,
        loading_message: 19,
        loading_status: 20,
        value_is_output: 1,
        rtl: 21,
        text_align: 22,
        autofocus: 23,
        autoscroll: 24,
        interactive: 25,
        root: 26,
        file_count: 27,
        audio_btn: 28,
        stop_audio_btn: 29,
        rtc_configuration: 30,
        time_limit: 31,
        modality: 32,
        mode: 33,
        rtp_params: 34,
        track_constraints: 35,
        server: 36
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[2];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), j();
  }
  get elem_id() {
    return this.$$.ctx[3];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), j();
  }
  get elem_classes() {
    return this.$$.ctx[4];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), j();
  }
  get visible() {
    return this.$$.ctx[5];
  }
  set visible(e) {
    this.$$set({ visible: e }), j();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), j();
  }
  get file_types() {
    return this.$$.ctx[6];
  }
  set file_types(e) {
    this.$$set({ file_types: e }), j();
  }
  get lines() {
    return this.$$.ctx[7];
  }
  set lines(e) {
    this.$$set({ lines: e }), j();
  }
  get placeholder() {
    return this.$$.ctx[8];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), j();
  }
  get label() {
    return this.$$.ctx[9];
  }
  set label(e) {
    this.$$set({ label: e }), j();
  }
  get info() {
    return this.$$.ctx[10];
  }
  set info(e) {
    this.$$set({ info: e }), j();
  }
  get show_label() {
    return this.$$.ctx[11];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), j();
  }
  get max_lines() {
    return this.$$.ctx[12];
  }
  set max_lines(e) {
    this.$$set({ max_lines: e }), j();
  }
  get container() {
    return this.$$.ctx[13];
  }
  set container(e) {
    this.$$set({ container: e }), j();
  }
  get scale() {
    return this.$$.ctx[14];
  }
  set scale(e) {
    this.$$set({ scale: e }), j();
  }
  get min_width() {
    return this.$$.ctx[15];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), j();
  }
  get upload_btn() {
    return this.$$.ctx[16];
  }
  set upload_btn(e) {
    this.$$set({ upload_btn: e }), j();
  }
  get submit_btn() {
    return this.$$.ctx[17];
  }
  set submit_btn(e) {
    this.$$set({ submit_btn: e }), j();
  }
  get stop_btn() {
    return this.$$.ctx[18];
  }
  set stop_btn(e) {
    this.$$set({ stop_btn: e }), j();
  }
  get loading_message() {
    return this.$$.ctx[19];
  }
  set loading_message(e) {
    this.$$set({ loading_message: e }), j();
  }
  get loading_status() {
    return this.$$.ctx[20];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), j();
  }
  get value_is_output() {
    return this.$$.ctx[1];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), j();
  }
  get rtl() {
    return this.$$.ctx[21];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), j();
  }
  get text_align() {
    return this.$$.ctx[22];
  }
  set text_align(e) {
    this.$$set({ text_align: e }), j();
  }
  get autofocus() {
    return this.$$.ctx[23];
  }
  set autofocus(e) {
    this.$$set({ autofocus: e }), j();
  }
  get autoscroll() {
    return this.$$.ctx[24];
  }
  set autoscroll(e) {
    this.$$set({ autoscroll: e }), j();
  }
  get interactive() {
    return this.$$.ctx[25];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), j();
  }
  get root() {
    return this.$$.ctx[26];
  }
  set root(e) {
    this.$$set({ root: e }), j();
  }
  get file_count() {
    return this.$$.ctx[27];
  }
  set file_count(e) {
    this.$$set({ file_count: e }), j();
  }
  get audio_btn() {
    return this.$$.ctx[28];
  }
  set audio_btn(e) {
    this.$$set({ audio_btn: e }), j();
  }
  get stop_audio_btn() {
    return this.$$.ctx[29];
  }
  set stop_audio_btn(e) {
    this.$$set({ stop_audio_btn: e }), j();
  }
  get rtc_configuration() {
    return this.$$.ctx[30];
  }
  set rtc_configuration(e) {
    this.$$set({ rtc_configuration: e }), j();
  }
  get time_limit() {
    return this.$$.ctx[31];
  }
  set time_limit(e) {
    this.$$set({ time_limit: e }), j();
  }
  get modality() {
    return this.$$.ctx[32];
  }
  set modality(e) {
    this.$$set({ modality: e }), j();
  }
  get mode() {
    return this.$$.ctx[33];
  }
  set mode(e) {
    this.$$set({ mode: e }), j();
  }
  get rtp_params() {
    return this.$$.ctx[34];
  }
  set rtp_params(e) {
    this.$$set({ rtp_params: e }), j();
  }
  get track_constraints() {
    return this.$$.ctx[35];
  }
  set track_constraints(e) {
    this.$$set({ track_constraints: e }), j();
  }
  get server() {
    return this.$$.ctx[36];
  }
  set server(e) {
    this.$$set({ server: e }), j();
  }
}
export {
  jf as default
};
