const {
  SvelteComponent: Ho,
  assign: Zo,
  create_slot: Xo,
  detach: Yo,
  element: Ko,
  get_all_dirty_from_scope: Jo,
  get_slot_changes: Qo,
  get_spread_update: xo,
  init: $o,
  insert: er,
  safe_not_equal: tr,
  set_dynamic_element_data: El,
  set_style: pe,
  toggle_class: Le,
  transition_in: Hi,
  transition_out: Zi,
  update_slot_base: nr
} = window.__gradio__svelte__internal;
function lr(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = Xo(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let r = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], f = {};
  for (let a = 0; a < r.length; a += 1)
    f = Zo(f, r[a]);
  return {
    c() {
      e = Ko(
        /*tag*/
        l[14]
      ), o && o.c(), El(
        /*tag*/
        l[14]
      )(e, f), Le(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), Le(
        e,
        "padded",
        /*padding*/
        l[6]
      ), Le(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), Le(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), Le(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), pe(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), pe(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), pe(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), pe(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), pe(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), pe(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), pe(e, "border-width", "var(--block-border-width)");
    },
    m(a, s) {
      er(a, e, s), o && o.m(e, null), n = !0;
    },
    p(a, s) {
      o && o.p && (!n || s & /*$$scope*/
      131072) && nr(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? Qo(
          i,
          /*$$scope*/
          a[17],
          s,
          null
        ) : Jo(
          /*$$scope*/
          a[17]
        ),
        null
      ), El(
        /*tag*/
        a[14]
      )(e, f = xo(r, [
        (!n || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!n || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!n || s & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Le(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), Le(
        e,
        "padded",
        /*padding*/
        a[6]
      ), Le(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), Le(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), Le(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), s & /*height*/
      1 && pe(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), s & /*width*/
      2 && pe(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), s & /*variant*/
      16 && pe(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), s & /*allow_overflow*/
      2048 && pe(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && pe(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), s & /*min_width*/
      8192 && pe(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (Hi(o, a), n = !0);
    },
    o(a) {
      Zi(o, a), n = !1;
    },
    d(a) {
      a && Yo(e), o && o.d(a);
    }
  };
}
function ir(l) {
  let e, t = (
    /*tag*/
    l[14] && lr(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Hi(t, n), e = !0);
    },
    o(n) {
      Zi(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function or(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: r = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: s = "solid" } = e, { border_mode: c = "base" } = e, { padding: u = !0 } = e, { type: d = "normal" } = e, { test_id: _ = void 0 } = e, { explicit_call: m = !1 } = e, { container: h = !0 } = e, { visible: p = !0 } = e, { allow_overflow: w = !0 } = e, { scale: g = null } = e, { min_width: b = 0 } = e, S = d === "fieldset" ? "fieldset" : "div";
  const L = (C) => {
    if (C !== void 0) {
      if (typeof C == "number")
        return C + "px";
      if (typeof C == "string")
        return C;
    }
  };
  return l.$$set = (C) => {
    "height" in C && t(0, o = C.height), "width" in C && t(1, r = C.width), "elem_id" in C && t(2, f = C.elem_id), "elem_classes" in C && t(3, a = C.elem_classes), "variant" in C && t(4, s = C.variant), "border_mode" in C && t(5, c = C.border_mode), "padding" in C && t(6, u = C.padding), "type" in C && t(16, d = C.type), "test_id" in C && t(7, _ = C.test_id), "explicit_call" in C && t(8, m = C.explicit_call), "container" in C && t(9, h = C.container), "visible" in C && t(10, p = C.visible), "allow_overflow" in C && t(11, w = C.allow_overflow), "scale" in C && t(12, g = C.scale), "min_width" in C && t(13, b = C.min_width), "$$scope" in C && t(17, i = C.$$scope);
  }, [
    o,
    r,
    f,
    a,
    s,
    c,
    u,
    _,
    m,
    h,
    p,
    w,
    g,
    b,
    S,
    L,
    d,
    i,
    n
  ];
}
class rr extends Ho {
  constructor(e) {
    super(), $o(this, e, or, ir, tr, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: ar,
  append: Tn,
  attr: en,
  create_component: sr,
  destroy_component: fr,
  detach: cr,
  element: Il,
  init: ur,
  insert: _r,
  mount_component: dr,
  safe_not_equal: mr,
  set_data: hr,
  space: gr,
  text: br,
  toggle_class: Xe,
  transition_in: pr,
  transition_out: wr
} = window.__gradio__svelte__internal;
function vr(l) {
  let e, t, n, i, o, r;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = Il("label"), t = Il("span"), sr(n.$$.fragment), i = gr(), o = br(
        /*label*/
        l[0]
      ), en(t, "class", "svelte-9gxdi0"), en(e, "for", ""), en(e, "data-testid", "block-label"), en(e, "class", "svelte-9gxdi0"), Xe(e, "hide", !/*show_label*/
      l[2]), Xe(e, "sr-only", !/*show_label*/
      l[2]), Xe(
        e,
        "float",
        /*float*/
        l[4]
      ), Xe(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, a) {
      _r(f, e, a), Tn(e, t), dr(n, t, null), Tn(e, i), Tn(e, o), r = !0;
    },
    p(f, [a]) {
      (!r || a & /*label*/
      1) && hr(
        o,
        /*label*/
        f[0]
      ), (!r || a & /*show_label*/
      4) && Xe(e, "hide", !/*show_label*/
      f[2]), (!r || a & /*show_label*/
      4) && Xe(e, "sr-only", !/*show_label*/
      f[2]), (!r || a & /*float*/
      16) && Xe(
        e,
        "float",
        /*float*/
        f[4]
      ), (!r || a & /*disable*/
      8) && Xe(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      r || (pr(n.$$.fragment, f), r = !0);
    },
    o(f) {
      wr(n.$$.fragment, f), r = !1;
    },
    d(f) {
      f && cr(e), fr(n);
    }
  };
}
function kr(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: r = !1 } = e, { float: f = !0 } = e;
  return l.$$set = (a) => {
    "label" in a && t(0, n = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, r = a.disable), "float" in a && t(4, f = a.float);
  }, [n, i, o, r, f];
}
class yr extends ar {
  constructor(e) {
    super(), ur(this, e, kr, vr, mr, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: Sr,
  append: sl,
  attr: Pe,
  bubble: Cr,
  create_component: zr,
  destroy_component: qr,
  detach: Xi,
  element: fl,
  init: Mr,
  insert: Yi,
  listen: Er,
  mount_component: Ir,
  safe_not_equal: Dr,
  set_data: Br,
  set_style: St,
  space: Lr,
  text: jr,
  toggle_class: ue,
  transition_in: Fr,
  transition_out: Rr
} = window.__gradio__svelte__internal;
function Dl(l) {
  let e, t;
  return {
    c() {
      e = fl("span"), t = jr(
        /*label*/
        l[1]
      ), Pe(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Yi(n, e, i), sl(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Br(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Xi(e);
    }
  };
}
function Ar(l) {
  let e, t, n, i, o, r, f, a = (
    /*show_label*/
    l[2] && Dl(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = fl("button"), a && a.c(), t = Lr(), n = fl("div"), zr(i.$$.fragment), Pe(n, "class", "svelte-1lrphxw"), ue(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), ue(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), ue(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], Pe(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), Pe(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), Pe(
        e,
        "title",
        /*label*/
        l[1]
      ), Pe(e, "class", "svelte-1lrphxw"), ue(
        e,
        "pending",
        /*pending*/
        l[3]
      ), ue(
        e,
        "padded",
        /*padded*/
        l[5]
      ), ue(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), ue(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), St(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), St(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), St(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(s, c) {
      Yi(s, e, c), a && a.m(e, null), sl(e, t), sl(e, n), Ir(i, n, null), o = !0, r || (f = Er(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), r = !0);
    },
    p(s, [c]) {
      /*show_label*/
      s[2] ? a ? a.p(s, c) : (a = Dl(s), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || c & /*size*/
      16) && ue(
        n,
        "small",
        /*size*/
        s[4] === "small"
      ), (!o || c & /*size*/
      16) && ue(
        n,
        "large",
        /*size*/
        s[4] === "large"
      ), (!o || c & /*size*/
      16) && ue(
        n,
        "medium",
        /*size*/
        s[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      s[7]), (!o || c & /*label*/
      2) && Pe(
        e,
        "aria-label",
        /*label*/
        s[1]
      ), (!o || c & /*hasPopup*/
      256) && Pe(
        e,
        "aria-haspopup",
        /*hasPopup*/
        s[8]
      ), (!o || c & /*label*/
      2) && Pe(
        e,
        "title",
        /*label*/
        s[1]
      ), (!o || c & /*pending*/
      8) && ue(
        e,
        "pending",
        /*pending*/
        s[3]
      ), (!o || c & /*padded*/
      32) && ue(
        e,
        "padded",
        /*padded*/
        s[5]
      ), (!o || c & /*highlight*/
      64) && ue(
        e,
        "highlight",
        /*highlight*/
        s[6]
      ), (!o || c & /*transparent*/
      512) && ue(
        e,
        "transparent",
        /*transparent*/
        s[9]
      ), c & /*disabled, _color*/
      4224 && St(e, "color", !/*disabled*/
      s[7] && /*_color*/
      s[12] ? (
        /*_color*/
        s[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && St(e, "--bg-color", /*disabled*/
      s[7] ? "auto" : (
        /*background*/
        s[10]
      )), c & /*offset*/
      2048 && St(
        e,
        "margin-left",
        /*offset*/
        s[11] + "px"
      );
    },
    i(s) {
      o || (Fr(i.$$.fragment, s), o = !0);
    },
    o(s) {
      Rr(i.$$.fragment, s), o = !1;
    },
    d(s) {
      s && Xi(e), a && a.d(), qr(i), r = !1, f();
    }
  };
}
function Tr(l, e, t) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: r = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: s = !0 } = e, { highlight: c = !1 } = e, { disabled: u = !1 } = e, { hasPopup: d = !1 } = e, { color: _ = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: h = "var(--background-fill-primary)" } = e, { offset: p = 0 } = e;
  function w(g) {
    Cr.call(this, l, g);
  }
  return l.$$set = (g) => {
    "Icon" in g && t(0, i = g.Icon), "label" in g && t(1, o = g.label), "show_label" in g && t(2, r = g.show_label), "pending" in g && t(3, f = g.pending), "size" in g && t(4, a = g.size), "padded" in g && t(5, s = g.padded), "highlight" in g && t(6, c = g.highlight), "disabled" in g && t(7, u = g.disabled), "hasPopup" in g && t(8, d = g.hasPopup), "color" in g && t(13, _ = g.color), "transparent" in g && t(9, m = g.transparent), "background" in g && t(10, h = g.background), "offset" in g && t(11, p = g.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = c ? "var(--color-accent)" : _);
  }, [
    i,
    o,
    r,
    f,
    a,
    s,
    c,
    u,
    d,
    m,
    h,
    p,
    n,
    _,
    w
  ];
}
class qn extends Sr {
  constructor(e) {
    super(), Mr(this, e, Tr, Ar, Dr, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: Wr,
  append: Pr,
  attr: Wn,
  binding_callbacks: Nr,
  create_slot: Vr,
  detach: Ur,
  element: Bl,
  get_all_dirty_from_scope: Or,
  get_slot_changes: Gr,
  init: Hr,
  insert: Zr,
  safe_not_equal: Xr,
  toggle_class: Ye,
  transition_in: Yr,
  transition_out: Kr,
  update_slot_base: Jr
} = window.__gradio__svelte__internal;
function Qr(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), o = Vr(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = Bl("div"), t = Bl("div"), o && o.c(), Wn(t, "class", "icon svelte-3w3rth"), Wn(e, "class", "empty svelte-3w3rth"), Wn(e, "aria-label", "Empty value"), Ye(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), Ye(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), Ye(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), Ye(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(r, f) {
      Zr(r, e, f), Pr(e, t), o && o.m(t, null), l[6](e), n = !0;
    },
    p(r, [f]) {
      o && o.p && (!n || f & /*$$scope*/
      16) && Jr(
        o,
        i,
        r,
        /*$$scope*/
        r[4],
        n ? Gr(
          i,
          /*$$scope*/
          r[4],
          f,
          null
        ) : Or(
          /*$$scope*/
          r[4]
        ),
        null
      ), (!n || f & /*size*/
      1) && Ye(
        e,
        "small",
        /*size*/
        r[0] === "small"
      ), (!n || f & /*size*/
      1) && Ye(
        e,
        "large",
        /*size*/
        r[0] === "large"
      ), (!n || f & /*unpadded_box*/
      2) && Ye(
        e,
        "unpadded_box",
        /*unpadded_box*/
        r[1]
      ), (!n || f & /*parent_height*/
      8) && Ye(
        e,
        "small_parent",
        /*parent_height*/
        r[3]
      );
    },
    i(r) {
      n || (Yr(o, r), n = !0);
    },
    o(r) {
      Kr(o, r), n = !1;
    },
    d(r) {
      r && Ur(e), o && o.d(r), l[6](null);
    }
  };
}
function xr(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e, { size: r = "small" } = e, { unpadded_box: f = !1 } = e, a;
  function s(u) {
    var d;
    if (!u) return !1;
    const { height: _ } = u.getBoundingClientRect(), { height: m } = ((d = u.parentElement) === null || d === void 0 ? void 0 : d.getBoundingClientRect()) || { height: _ };
    return _ > m + 2;
  }
  function c(u) {
    Nr[u ? "unshift" : "push"](() => {
      a = u, t(2, a);
    });
  }
  return l.$$set = (u) => {
    "size" in u && t(0, r = u.size), "unpadded_box" in u && t(1, f = u.unpadded_box), "$$scope" in u && t(4, o = u.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = s(a));
  }, [r, f, a, n, o, i, c];
}
class $r extends Wr {
  constructor(e) {
    super(), Hr(this, e, xr, Qr, Xr, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: ea,
  append: Ll,
  attr: _e,
  detach: ta,
  init: na,
  insert: la,
  noop: Pn,
  safe_not_equal: ia,
  svg_element: Nn
} = window.__gradio__svelte__internal;
function oa(l) {
  let e, t, n;
  return {
    c() {
      e = Nn("svg"), t = Nn("path"), n = Nn("circle"), _e(t, "d", "M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"), _e(n, "cx", "12"), _e(n, "cy", "13"), _e(n, "r", "4"), _e(e, "xmlns", "http://www.w3.org/2000/svg"), _e(e, "width", "100%"), _e(e, "height", "100%"), _e(e, "viewBox", "0 0 24 24"), _e(e, "fill", "none"), _e(e, "stroke", "currentColor"), _e(e, "stroke-width", "1.5"), _e(e, "stroke-linecap", "round"), _e(e, "stroke-linejoin", "round"), _e(e, "class", "feather feather-camera");
    },
    m(i, o) {
      la(i, e, o), Ll(e, t), Ll(e, n);
    },
    p: Pn,
    i: Pn,
    o: Pn,
    d(i) {
      i && ta(e);
    }
  };
}
class ra extends ea {
  constructor(e) {
    super(), na(this, e, null, oa, ia, {});
  }
}
const {
  SvelteComponent: aa,
  append: sa,
  attr: qe,
  detach: fa,
  init: ca,
  insert: ua,
  noop: Vn,
  safe_not_equal: _a,
  svg_element: jl
} = window.__gradio__svelte__internal;
function da(l) {
  let e, t;
  return {
    c() {
      e = jl("svg"), t = jl("circle"), qe(t, "cx", "12"), qe(t, "cy", "12"), qe(t, "r", "10"), qe(e, "xmlns", "http://www.w3.org/2000/svg"), qe(e, "width", "100%"), qe(e, "height", "100%"), qe(e, "viewBox", "0 0 24 24"), qe(e, "stroke-width", "1.5"), qe(e, "stroke-linecap", "round"), qe(e, "stroke-linejoin", "round"), qe(e, "class", "feather feather-circle");
    },
    m(n, i) {
      ua(n, e, i), sa(e, t);
    },
    p: Vn,
    i: Vn,
    o: Vn,
    d(n) {
      n && fa(e);
    }
  };
}
class ma extends aa {
  constructor(e) {
    super(), ca(this, e, null, da, _a, {});
  }
}
const {
  SvelteComponent: ha,
  append: Un,
  attr: Me,
  detach: ga,
  init: ba,
  insert: pa,
  noop: On,
  safe_not_equal: wa,
  set_style: je,
  svg_element: tn
} = window.__gradio__svelte__internal;
function va(l) {
  let e, t, n, i;
  return {
    c() {
      e = tn("svg"), t = tn("g"), n = tn("path"), i = tn("path"), Me(n, "d", "M18,6L6.087,17.913"), je(n, "fill", "none"), je(n, "fill-rule", "nonzero"), je(n, "stroke-width", "2px"), Me(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Me(i, "d", "M4.364,4.364L19.636,19.636"), je(i, "fill", "none"), je(i, "fill-rule", "nonzero"), je(i, "stroke-width", "2px"), Me(e, "width", "100%"), Me(e, "height", "100%"), Me(e, "viewBox", "0 0 24 24"), Me(e, "version", "1.1"), Me(e, "xmlns", "http://www.w3.org/2000/svg"), Me(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Me(e, "xml:space", "preserve"), Me(e, "stroke", "currentColor"), je(e, "fill-rule", "evenodd"), je(e, "clip-rule", "evenodd"), je(e, "stroke-linecap", "round"), je(e, "stroke-linejoin", "round");
    },
    m(o, r) {
      pa(o, e, r), Un(e, t), Un(t, n), Un(e, i);
    },
    p: On,
    i: On,
    o: On,
    d(o) {
      o && ga(e);
    }
  };
}
class Ki extends ha {
  constructor(e) {
    super(), ba(this, e, null, va, wa, {});
  }
}
const {
  SvelteComponent: ka,
  append: ya,
  attr: Pt,
  detach: Sa,
  init: Ca,
  insert: za,
  noop: Gn,
  safe_not_equal: qa,
  svg_element: Fl
} = window.__gradio__svelte__internal;
function Ma(l) {
  let e, t;
  return {
    c() {
      e = Fl("svg"), t = Fl("path"), Pt(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), Pt(t, "fill", "currentColor"), Pt(e, "id", "icon"), Pt(e, "xmlns", "http://www.w3.org/2000/svg"), Pt(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      za(n, e, i), ya(e, t);
    },
    p: Gn,
    i: Gn,
    o: Gn,
    d(n) {
      n && Sa(e);
    }
  };
}
class Ea extends ka {
  constructor(e) {
    super(), Ca(this, e, null, Ma, qa, {});
  }
}
const {
  SvelteComponent: Ia,
  append: Da,
  attr: Ct,
  detach: Ba,
  init: La,
  insert: ja,
  noop: Hn,
  safe_not_equal: Fa,
  svg_element: Rl
} = window.__gradio__svelte__internal;
function Ra(l) {
  let e, t;
  return {
    c() {
      e = Rl("svg"), t = Rl("path"), Ct(t, "fill", "currentColor"), Ct(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Ct(e, "xmlns", "http://www.w3.org/2000/svg"), Ct(e, "width", "100%"), Ct(e, "height", "100%"), Ct(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      ja(n, e, i), Da(e, t);
    },
    p: Hn,
    i: Hn,
    o: Hn,
    d(n) {
      n && Ba(e);
    }
  };
}
class Aa extends Ia {
  constructor(e) {
    super(), La(this, e, null, Ra, Fa, {});
  }
}
const {
  SvelteComponent: Ta,
  append: Wa,
  attr: zt,
  detach: Pa,
  init: Na,
  insert: Va,
  noop: Zn,
  safe_not_equal: Ua,
  svg_element: Al
} = window.__gradio__svelte__internal;
function Oa(l) {
  let e, t;
  return {
    c() {
      e = Al("svg"), t = Al("path"), zt(t, "d", "M5 8l4 4 4-4z"), zt(e, "class", "dropdown-arrow svelte-145leq6"), zt(e, "xmlns", "http://www.w3.org/2000/svg"), zt(e, "width", "100%"), zt(e, "height", "100%"), zt(e, "viewBox", "0 0 18 18");
    },
    m(n, i) {
      Va(n, e, i), Wa(e, t);
    },
    p: Zn,
    i: Zn,
    o: Zn,
    d(n) {
      n && Pa(e);
    }
  };
}
class Ji extends Ta {
  constructor(e) {
    super(), Na(this, e, null, Oa, Ua, {});
  }
}
const {
  SvelteComponent: Ga,
  append: Xn,
  attr: J,
  detach: Ha,
  init: Za,
  insert: Xa,
  noop: Yn,
  safe_not_equal: Ya,
  svg_element: nn
} = window.__gradio__svelte__internal;
function Ka(l) {
  let e, t, n, i;
  return {
    c() {
      e = nn("svg"), t = nn("rect"), n = nn("circle"), i = nn("polyline"), J(t, "x", "3"), J(t, "y", "3"), J(t, "width", "18"), J(t, "height", "18"), J(t, "rx", "2"), J(t, "ry", "2"), J(n, "cx", "8.5"), J(n, "cy", "8.5"), J(n, "r", "1.5"), J(i, "points", "21 15 16 10 5 21"), J(e, "xmlns", "http://www.w3.org/2000/svg"), J(e, "width", "100%"), J(e, "height", "100%"), J(e, "viewBox", "0 0 24 24"), J(e, "fill", "none"), J(e, "stroke", "currentColor"), J(e, "stroke-width", "1.5"), J(e, "stroke-linecap", "round"), J(e, "stroke-linejoin", "round"), J(e, "class", "feather feather-image");
    },
    m(o, r) {
      Xa(o, e, r), Xn(e, t), Xn(e, n), Xn(e, i);
    },
    p: Yn,
    i: Yn,
    o: Yn,
    d(o) {
      o && Ha(e);
    }
  };
}
let Qi = class extends Ga {
  constructor(e) {
    super(), Za(this, e, null, Ka, Ya, {});
  }
};
const {
  SvelteComponent: Ja,
  append: Qa,
  attr: ln,
  detach: xa,
  init: $a,
  insert: es,
  noop: Kn,
  safe_not_equal: ts,
  svg_element: Tl
} = window.__gradio__svelte__internal;
function ns(l) {
  let e, t;
  return {
    c() {
      e = Tl("svg"), t = Tl("path"), ln(t, "fill", "currentColor"), ln(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a4 4 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2zm2.245 2.096L16 4.25q0-.078-.005-.154M13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5M15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3zm0 11a3 3 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A3 3 0 0 1 20 23zm5-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2"), ln(e, "xmlns", "http://www.w3.org/2000/svg"), ln(e, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      es(n, e, i), Qa(e, t);
    },
    p: Kn,
    i: Kn,
    o: Kn,
    d(n) {
      n && xa(e);
    }
  };
}
class xi extends Ja {
  constructor(e) {
    super(), $a(this, e, null, ns, ts, {});
  }
}
const {
  SvelteComponent: ls,
  append: on,
  attr: Q,
  detach: is,
  init: os,
  insert: rs,
  noop: Jn,
  safe_not_equal: as,
  svg_element: Nt
} = window.__gradio__svelte__internal;
function ss(l) {
  let e, t, n, i, o;
  return {
    c() {
      e = Nt("svg"), t = Nt("path"), n = Nt("path"), i = Nt("line"), o = Nt("line"), Q(t, "d", "M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"), Q(n, "d", "M19 10v2a7 7 0 0 1-14 0v-2"), Q(i, "x1", "12"), Q(i, "y1", "19"), Q(i, "x2", "12"), Q(i, "y2", "23"), Q(o, "x1", "8"), Q(o, "y1", "23"), Q(o, "x2", "16"), Q(o, "y2", "23"), Q(e, "xmlns", "http://www.w3.org/2000/svg"), Q(e, "width", "100%"), Q(e, "height", "100%"), Q(e, "viewBox", "0 0 24 24"), Q(e, "fill", "none"), Q(e, "stroke", "currentColor"), Q(e, "stroke-width", "2"), Q(e, "stroke-linecap", "round"), Q(e, "stroke-linejoin", "round"), Q(e, "class", "feather feather-mic");
    },
    m(r, f) {
      rs(r, e, f), on(e, t), on(e, n), on(e, i), on(e, o);
    },
    p: Jn,
    i: Jn,
    o: Jn,
    d(r) {
      r && is(e);
    }
  };
}
class fs extends ls {
  constructor(e) {
    super(), os(this, e, null, ss, as, {});
  }
}
const {
  SvelteComponent: cs,
  append: us,
  attr: de,
  detach: _s,
  init: ds,
  insert: ms,
  noop: Qn,
  safe_not_equal: hs,
  svg_element: Wl
} = window.__gradio__svelte__internal;
function gs(l) {
  let e, t;
  return {
    c() {
      e = Wl("svg"), t = Wl("rect"), de(t, "x", "3"), de(t, "y", "3"), de(t, "width", "18"), de(t, "height", "18"), de(t, "rx", "2"), de(t, "ry", "2"), de(e, "xmlns", "http://www.w3.org/2000/svg"), de(e, "width", "100%"), de(e, "height", "100%"), de(e, "viewBox", "0 0 24 24"), de(e, "stroke-width", "1.5"), de(e, "stroke-linecap", "round"), de(e, "stroke-linejoin", "round"), de(e, "class", "feather feather-square");
    },
    m(n, i) {
      ms(n, e, i), us(e, t);
    },
    p: Qn,
    i: Qn,
    o: Qn,
    d(n) {
      n && _s(e);
    }
  };
}
class bs extends cs {
  constructor(e) {
    super(), ds(this, e, null, gs, hs, {});
  }
}
const {
  SvelteComponent: ps,
  append: xn,
  attr: re,
  detach: ws,
  init: vs,
  insert: ks,
  noop: $n,
  safe_not_equal: ys,
  svg_element: rn
} = window.__gradio__svelte__internal;
function Ss(l) {
  let e, t, n, i;
  return {
    c() {
      e = rn("svg"), t = rn("path"), n = rn("polyline"), i = rn("line"), re(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), re(n, "points", "17 8 12 3 7 8"), re(i, "x1", "12"), re(i, "y1", "3"), re(i, "x2", "12"), re(i, "y2", "15"), re(e, "xmlns", "http://www.w3.org/2000/svg"), re(e, "width", "90%"), re(e, "height", "90%"), re(e, "viewBox", "0 0 24 24"), re(e, "fill", "none"), re(e, "stroke", "currentColor"), re(e, "stroke-width", "2"), re(e, "stroke-linecap", "round"), re(e, "stroke-linejoin", "round"), re(e, "class", "feather feather-upload");
    },
    m(o, r) {
      ks(o, e, r), xn(e, t), xn(e, n), xn(e, i);
    },
    p: $n,
    i: $n,
    o: $n,
    d(o) {
      o && ws(e);
    }
  };
}
let $i = class extends ps {
  constructor(e) {
    super(), vs(this, e, null, Ss, ys, {});
  }
};
const {
  SvelteComponent: Cs,
  append: Pl,
  attr: Ke,
  detach: zs,
  init: qs,
  insert: Ms,
  noop: el,
  safe_not_equal: Es,
  svg_element: tl
} = window.__gradio__svelte__internal;
function Is(l) {
  let e, t, n;
  return {
    c() {
      e = tl("svg"), t = tl("path"), n = tl("path"), Ke(t, "fill", "currentColor"), Ke(t, "d", "M12 2c-4.963 0-9 4.038-9 9c0 3.328 1.82 6.232 4.513 7.79l-2.067 1.378A1 1 0 0 0 6 22h12a1 1 0 0 0 .555-1.832l-2.067-1.378C19.18 17.232 21 14.328 21 11c0-4.962-4.037-9-9-9zm0 16c-3.859 0-7-3.141-7-7c0-3.86 3.141-7 7-7s7 3.14 7 7c0 3.859-3.141 7-7 7z"), Ke(n, "fill", "currentColor"), Ke(n, "d", "M12 6c-2.757 0-5 2.243-5 5s2.243 5 5 5s5-2.243 5-5s-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3s3 1.346 3 3s-1.346 3-3 3z"), Ke(e, "xmlns", "http://www.w3.org/2000/svg"), Ke(e, "width", "100%"), Ke(e, "height", "100%"), Ke(e, "viewBox", "0 0 24 24");
    },
    m(i, o) {
      Ms(i, e, o), Pl(e, t), Pl(e, n);
    },
    p: el,
    i: el,
    o: el,
    d(i) {
      i && zs(e);
    }
  };
}
let eo = class extends Cs {
  constructor(e) {
    super(), qs(this, e, null, Is, Es, {});
  }
};
const Ds = [
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
], Nl = {
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
Ds.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Nl[e][t],
      secondary: Nl[e][n]
    }
  }),
  {}
);
class _n extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
async function Bs(l, e) {
  var a;
  if (window.__gradio_space__ == null)
    throw new _n("Must be on Spaces to share.");
  let t, n, i;
  t = Ls(l), n = l.split(";")[0].split(":")[1], i = "file" + n.split("/")[1];
  const o = new File([t], i, { type: n }), r = await fetch("https://huggingface.co/uploads", {
    method: "POST",
    body: o,
    headers: {
      "Content-Type": o.type,
      "X-Requested-With": "XMLHttpRequest"
    }
  });
  if (!r.ok) {
    if ((a = r.headers.get("content-type")) != null && a.includes("application/json")) {
      const s = await r.json();
      throw new _n(`Upload failed: ${s.error}`);
    }
    throw new _n("Upload failed.");
  }
  return await r.text();
}
function Ls(l) {
  for (var e = l.split(","), t = e[0].match(/:(.*?);/)[1], n = atob(e[1]), i = n.length, o = new Uint8Array(i); i--; )
    o[i] = n.charCodeAt(i);
  return new Blob([o], { type: t });
}
const {
  SvelteComponent: js,
  create_component: Fs,
  destroy_component: Rs,
  init: As,
  mount_component: Ts,
  safe_not_equal: Ws,
  transition_in: Ps,
  transition_out: Ns
} = window.__gradio__svelte__internal, { createEventDispatcher: Vs } = window.__gradio__svelte__internal;
function Us(l) {
  let e, t;
  return e = new qn({
    props: {
      Icon: Ea,
      label: (
        /*i18n*/
        l[2]("common.share")
      ),
      pending: (
        /*pending*/
        l[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[5]
  ), {
    c() {
      Fs(e.$$.fragment);
    },
    m(n, i) {
      Ts(e, n, i), t = !0;
    },
    p(n, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      n[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      n[3]), e.$set(o);
    },
    i(n) {
      t || (Ps(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ns(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Rs(e, n);
    }
  };
}
function Os(l, e, t) {
  const n = Vs();
  let { formatter: i } = e, { value: o } = e, { i18n: r } = e, f = !1;
  const a = async () => {
    try {
      t(3, f = !0);
      const s = await i(o);
      n("share", { description: s });
    } catch (s) {
      console.error(s);
      let c = s instanceof _n ? s.message : "Share failed.";
      n("error", c);
    } finally {
      t(3, f = !1);
    }
  };
  return l.$$set = (s) => {
    "formatter" in s && t(0, i = s.formatter), "value" in s && t(1, o = s.value), "i18n" in s && t(2, r = s.i18n);
  }, [i, o, r, f, n, a];
}
class Gs extends js {
  constructor(e) {
    super(), As(this, e, Os, Us, Ws, { formatter: 0, value: 1, i18n: 2 });
  }
}
const {
  SvelteComponent: Hs,
  append: dt,
  attr: cl,
  check_outros: Zs,
  create_component: to,
  destroy_component: no,
  detach: dn,
  element: ul,
  group_outros: Xs,
  init: Ys,
  insert: mn,
  mount_component: lo,
  safe_not_equal: Ks,
  set_data: _l,
  space: dl,
  text: Ot,
  toggle_class: Vl,
  transition_in: bn,
  transition_out: pn
} = window.__gradio__svelte__internal;
function Js(l) {
  let e, t;
  return e = new $i({}), {
    c() {
      to(e.$$.fragment);
    },
    m(n, i) {
      lo(e, n, i), t = !0;
    },
    i(n) {
      t || (bn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      pn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      no(e, n);
    }
  };
}
function Qs(l) {
  let e, t;
  return e = new xi({}), {
    c() {
      to(e.$$.fragment);
    },
    m(n, i) {
      lo(e, n, i), t = !0;
    },
    i(n) {
      t || (bn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      pn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      no(e, n);
    }
  };
}
function Ul(l) {
  let e, t, n = (
    /*i18n*/
    l[1]("common.or") + ""
  ), i, o, r, f = (
    /*message*/
    (l[2] || /*i18n*/
    l[1]("upload_text.click_to_upload")) + ""
  ), a;
  return {
    c() {
      e = ul("span"), t = Ot("- "), i = Ot(n), o = Ot(" -"), r = dl(), a = Ot(f), cl(e, "class", "or svelte-kzcjhc");
    },
    m(s, c) {
      mn(s, e, c), dt(e, t), dt(e, i), dt(e, o), mn(s, r, c), mn(s, a, c);
    },
    p(s, c) {
      c & /*i18n*/
      2 && n !== (n = /*i18n*/
      s[1]("common.or") + "") && _l(i, n), c & /*message, i18n*/
      6 && f !== (f = /*message*/
      (s[2] || /*i18n*/
      s[1]("upload_text.click_to_upload")) + "") && _l(a, f);
    },
    d(s) {
      s && (dn(e), dn(r), dn(a));
    }
  };
}
function xs(l) {
  let e, t, n, i, o, r = (
    /*i18n*/
    l[1](
      /*defs*/
      l[5][
        /*type*/
        l[0]
      ] || /*defs*/
      l[5].file
    ) + ""
  ), f, a, s;
  const c = [Qs, Js], u = [];
  function d(m, h) {
    return (
      /*type*/
      m[0] === "clipboard" ? 0 : 1
    );
  }
  n = d(l), i = u[n] = c[n](l);
  let _ = (
    /*mode*/
    l[3] !== "short" && Ul(l)
  );
  return {
    c() {
      e = ul("div"), t = ul("span"), i.c(), o = dl(), f = Ot(r), a = dl(), _ && _.c(), cl(t, "class", "icon-wrap svelte-kzcjhc"), Vl(
        t,
        "hovered",
        /*hovered*/
        l[4]
      ), cl(e, "class", "wrap svelte-kzcjhc");
    },
    m(m, h) {
      mn(m, e, h), dt(e, t), u[n].m(t, null), dt(e, o), dt(e, f), dt(e, a), _ && _.m(e, null), s = !0;
    },
    p(m, [h]) {
      let p = n;
      n = d(m), n !== p && (Xs(), pn(u[p], 1, 1, () => {
        u[p] = null;
      }), Zs(), i = u[n], i || (i = u[n] = c[n](m), i.c()), bn(i, 1), i.m(t, null)), (!s || h & /*hovered*/
      16) && Vl(
        t,
        "hovered",
        /*hovered*/
        m[4]
      ), (!s || h & /*i18n, type*/
      3) && r !== (r = /*i18n*/
      m[1](
        /*defs*/
        m[5][
          /*type*/
          m[0]
        ] || /*defs*/
        m[5].file
      ) + "") && _l(f, r), /*mode*/
      m[3] !== "short" ? _ ? _.p(m, h) : (_ = Ul(m), _.c(), _.m(e, null)) : _ && (_.d(1), _ = null);
    },
    i(m) {
      s || (bn(i), s = !0);
    },
    o(m) {
      pn(i), s = !1;
    },
    d(m) {
      m && dn(e), u[n].d(), _ && _.d();
    }
  };
}
function $s(l, e, t) {
  let { type: n = "file" } = e, { i18n: i } = e, { message: o = void 0 } = e, { mode: r = "full" } = e, { hovered: f = !1 } = e;
  const a = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  return l.$$set = (s) => {
    "type" in s && t(0, n = s.type), "i18n" in s && t(1, i = s.i18n), "message" in s && t(2, o = s.message), "mode" in s && t(3, r = s.mode), "hovered" in s && t(4, f = s.hovered);
  }, [n, i, o, r, f, a];
}
class io extends Hs {
  constructor(e) {
    super(), Ys(this, e, $s, xs, Ks, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4
    });
  }
}
const {
  SvelteComponent: ef,
  append: nl,
  attr: Ae,
  check_outros: Gt,
  create_component: Mn,
  destroy_component: En,
  detach: Lt,
  element: Qt,
  empty: tf,
  group_outros: Ht,
  init: nf,
  insert: jt,
  listen: In,
  mount_component: Dn,
  safe_not_equal: lf,
  space: ll,
  toggle_class: et,
  transition_in: ee,
  transition_out: me
} = window.__gradio__svelte__internal;
function Ol(l) {
  let e, t = (
    /*sources*/
    l[1].includes("upload")
  ), n, i = (
    /*sources*/
    l[1].includes("microphone")
  ), o, r = (
    /*sources*/
    l[1].includes("webcam")
  ), f, a = (
    /*sources*/
    l[1].includes("clipboard")
  ), s, c = t && Gl(l), u = i && Hl(l), d = r && Zl(l), _ = a && Xl(l);
  return {
    c() {
      e = Qt("span"), c && c.c(), n = ll(), u && u.c(), o = ll(), d && d.c(), f = ll(), _ && _.c(), Ae(e, "class", "source-selection svelte-1jp3vgd"), Ae(e, "data-testid", "source-select");
    },
    m(m, h) {
      jt(m, e, h), c && c.m(e, null), nl(e, n), u && u.m(e, null), nl(e, o), d && d.m(e, null), nl(e, f), _ && _.m(e, null), s = !0;
    },
    p(m, h) {
      h & /*sources*/
      2 && (t = /*sources*/
      m[1].includes("upload")), t ? c ? (c.p(m, h), h & /*sources*/
      2 && ee(c, 1)) : (c = Gl(m), c.c(), ee(c, 1), c.m(e, n)) : c && (Ht(), me(c, 1, 1, () => {
        c = null;
      }), Gt()), h & /*sources*/
      2 && (i = /*sources*/
      m[1].includes("microphone")), i ? u ? (u.p(m, h), h & /*sources*/
      2 && ee(u, 1)) : (u = Hl(m), u.c(), ee(u, 1), u.m(e, o)) : u && (Ht(), me(u, 1, 1, () => {
        u = null;
      }), Gt()), h & /*sources*/
      2 && (r = /*sources*/
      m[1].includes("webcam")), r ? d ? (d.p(m, h), h & /*sources*/
      2 && ee(d, 1)) : (d = Zl(m), d.c(), ee(d, 1), d.m(e, f)) : d && (Ht(), me(d, 1, 1, () => {
        d = null;
      }), Gt()), h & /*sources*/
      2 && (a = /*sources*/
      m[1].includes("clipboard")), a ? _ ? (_.p(m, h), h & /*sources*/
      2 && ee(_, 1)) : (_ = Xl(m), _.c(), ee(_, 1), _.m(e, null)) : _ && (Ht(), me(_, 1, 1, () => {
        _ = null;
      }), Gt());
    },
    i(m) {
      s || (ee(c), ee(u), ee(d), ee(_), s = !0);
    },
    o(m) {
      me(c), me(u), me(d), me(_), s = !1;
    },
    d(m) {
      m && Lt(e), c && c.d(), u && u.d(), d && d.d(), _ && _.d();
    }
  };
}
function Gl(l) {
  let e, t, n, i, o;
  return t = new $i({}), {
    c() {
      e = Qt("button"), Mn(t.$$.fragment), Ae(e, "class", "icon svelte-1jp3vgd"), Ae(e, "aria-label", "Upload file"), et(
        e,
        "selected",
        /*active_source*/
        l[0] === "upload" || !/*active_source*/
        l[0]
      );
    },
    m(r, f) {
      jt(r, e, f), Dn(t, e, null), n = !0, i || (o = In(
        e,
        "click",
        /*click_handler*/
        l[6]
      ), i = !0);
    },
    p(r, f) {
      (!n || f & /*active_source*/
      1) && et(
        e,
        "selected",
        /*active_source*/
        r[0] === "upload" || !/*active_source*/
        r[0]
      );
    },
    i(r) {
      n || (ee(t.$$.fragment, r), n = !0);
    },
    o(r) {
      me(t.$$.fragment, r), n = !1;
    },
    d(r) {
      r && Lt(e), En(t), i = !1, o();
    }
  };
}
function Hl(l) {
  let e, t, n, i, o;
  return t = new fs({}), {
    c() {
      e = Qt("button"), Mn(t.$$.fragment), Ae(e, "class", "icon svelte-1jp3vgd"), Ae(e, "aria-label", "Record audio"), et(
        e,
        "selected",
        /*active_source*/
        l[0] === "microphone"
      );
    },
    m(r, f) {
      jt(r, e, f), Dn(t, e, null), n = !0, i || (o = In(
        e,
        "click",
        /*click_handler_1*/
        l[7]
      ), i = !0);
    },
    p(r, f) {
      (!n || f & /*active_source*/
      1) && et(
        e,
        "selected",
        /*active_source*/
        r[0] === "microphone"
      );
    },
    i(r) {
      n || (ee(t.$$.fragment, r), n = !0);
    },
    o(r) {
      me(t.$$.fragment, r), n = !1;
    },
    d(r) {
      r && Lt(e), En(t), i = !1, o();
    }
  };
}
function Zl(l) {
  let e, t, n, i, o;
  return t = new eo({}), {
    c() {
      e = Qt("button"), Mn(t.$$.fragment), Ae(e, "class", "icon svelte-1jp3vgd"), Ae(e, "aria-label", "Capture from camera"), et(
        e,
        "selected",
        /*active_source*/
        l[0] === "webcam"
      );
    },
    m(r, f) {
      jt(r, e, f), Dn(t, e, null), n = !0, i || (o = In(
        e,
        "click",
        /*click_handler_2*/
        l[8]
      ), i = !0);
    },
    p(r, f) {
      (!n || f & /*active_source*/
      1) && et(
        e,
        "selected",
        /*active_source*/
        r[0] === "webcam"
      );
    },
    i(r) {
      n || (ee(t.$$.fragment, r), n = !0);
    },
    o(r) {
      me(t.$$.fragment, r), n = !1;
    },
    d(r) {
      r && Lt(e), En(t), i = !1, o();
    }
  };
}
function Xl(l) {
  let e, t, n, i, o;
  return t = new xi({}), {
    c() {
      e = Qt("button"), Mn(t.$$.fragment), Ae(e, "class", "icon svelte-1jp3vgd"), Ae(e, "aria-label", "Paste from clipboard"), et(
        e,
        "selected",
        /*active_source*/
        l[0] === "clipboard"
      );
    },
    m(r, f) {
      jt(r, e, f), Dn(t, e, null), n = !0, i || (o = In(
        e,
        "click",
        /*click_handler_3*/
        l[9]
      ), i = !0);
    },
    p(r, f) {
      (!n || f & /*active_source*/
      1) && et(
        e,
        "selected",
        /*active_source*/
        r[0] === "clipboard"
      );
    },
    i(r) {
      n || (ee(t.$$.fragment, r), n = !0);
    },
    o(r) {
      me(t.$$.fragment, r), n = !1;
    },
    d(r) {
      r && Lt(e), En(t), i = !1, o();
    }
  };
}
function of(l) {
  let e, t, n = (
    /*unique_sources*/
    l[2].length > 1 && Ol(l)
  );
  return {
    c() {
      n && n.c(), e = tf();
    },
    m(i, o) {
      n && n.m(i, o), jt(i, e, o), t = !0;
    },
    p(i, [o]) {
      /*unique_sources*/
      i[2].length > 1 ? n ? (n.p(i, o), o & /*unique_sources*/
      4 && ee(n, 1)) : (n = Ol(i), n.c(), ee(n, 1), n.m(e.parentNode, e)) : n && (Ht(), me(n, 1, 1, () => {
        n = null;
      }), Gt());
    },
    i(i) {
      t || (ee(n), t = !0);
    },
    o(i) {
      me(n), t = !1;
    },
    d(i) {
      i && Lt(e), n && n.d(i);
    }
  };
}
function rf(l, e, t) {
  let n;
  var i = this && this.__awaiter || function(m, h, p, w) {
    function g(b) {
      return b instanceof p ? b : new p(function(S) {
        S(b);
      });
    }
    return new (p || (p = Promise))(function(b, S) {
      function L(q) {
        try {
          M(w.next(q));
        } catch (D) {
          S(D);
        }
      }
      function C(q) {
        try {
          M(w.throw(q));
        } catch (D) {
          S(D);
        }
      }
      function M(q) {
        q.done ? b(q.value) : g(q.value).then(L, C);
      }
      M((w = w.apply(m, h || [])).next());
    });
  };
  let { sources: o } = e, { active_source: r } = e, { handle_clear: f = () => {
  } } = e, { handle_select: a = () => {
  } } = e;
  function s(m) {
    return i(this, void 0, void 0, function* () {
      f(), t(0, r = m), a(m);
    });
  }
  const c = () => s("upload"), u = () => s("microphone"), d = () => s("webcam"), _ = () => s("clipboard");
  return l.$$set = (m) => {
    "sources" in m && t(1, o = m.sources), "active_source" in m && t(0, r = m.active_source), "handle_clear" in m && t(4, f = m.handle_clear), "handle_select" in m && t(5, a = m.handle_select);
  }, l.$$.update = () => {
    l.$$.dirty & /*sources*/
    2 && t(2, n = [...new Set(o)]);
  }, [
    r,
    o,
    n,
    s,
    f,
    a,
    c,
    u,
    d,
    _
  ];
}
class af extends ef {
  constructor(e) {
    super(), nf(this, e, rf, of, lf, {
      sources: 1,
      active_source: 0,
      handle_clear: 4,
      handle_select: 5
    });
  }
}
function Mt(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function hn() {
}
const sf = (l) => l;
function ff(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const oo = typeof window < "u";
let Yl = oo ? () => window.performance.now() : () => Date.now(), ro = oo ? (l) => requestAnimationFrame(l) : hn;
const Dt = /* @__PURE__ */ new Set();
function ao(l) {
  Dt.forEach((e) => {
    e.c(l) || (Dt.delete(e), e.f());
  }), Dt.size !== 0 && ro(ao);
}
function cf(l) {
  let e;
  return Dt.size === 0 && ro(ao), {
    promise: new Promise((t) => {
      Dt.add(e = { c: l, f: t });
    }),
    abort() {
      Dt.delete(e);
    }
  };
}
function uf(l, { delay: e = 0, duration: t = 400, easing: n = sf } = {}) {
  const i = +getComputedStyle(l).opacity;
  return {
    delay: e,
    duration: t,
    easing: n,
    css: (o) => `opacity: ${o * i}`
  };
}
const qt = [];
function _f(l, e = hn) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (ff(l, f) && (l = f, t)) {
      const a = !qt.length;
      for (const s of n)
        s[1](), qt.push(s, l);
      if (a) {
        for (let s = 0; s < qt.length; s += 2)
          qt[s][0](qt[s + 1]);
        qt.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function r(f, a = hn) {
    const s = [f, a];
    return n.add(s), n.size === 1 && (t = e(i, o) || hn), f(l), () => {
      n.delete(s), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: r };
}
function Kl(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function ml(l, e, t, n) {
  if (typeof t == "number" || Kl(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), r = l.opts.stiffness * i, f = l.opts.damping * o, a = (r - f) * l.inv_mass, s = (o + a) * l.dt;
    return Math.abs(s) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Kl(t) ? new Date(t.getTime() + s) : t + s);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => ml(l, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = ml(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Jl(l, e = {}) {
  const t = _f(l), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let r, f, a, s = l, c = l, u = 1, d = 0, _ = !1;
  function m(p, w = {}) {
    c = p;
    const g = a = {};
    return l == null || w.hard || h.stiffness >= 1 && h.damping >= 1 ? (_ = !0, r = Yl(), s = p, t.set(l = c), Promise.resolve()) : (w.soft && (d = 1 / ((w.soft === !0 ? 0.5 : +w.soft) * 60), u = 0), f || (r = Yl(), _ = !1, f = cf((b) => {
      if (_)
        return _ = !1, f = null, !1;
      u = Math.min(u + d, 1);
      const S = {
        inv_mass: u,
        opts: h,
        settled: !0,
        dt: (b - r) * 60 / 1e3
      }, L = ml(S, s, l, c);
      return r = b, s = l, t.set(l = L), S.settled && (f = null), !S.settled;
    })), new Promise((b) => {
      f.promise.then(() => {
        g === a && b();
      });
    }));
  }
  const h = {
    set: m,
    update: (p, w) => m(p(c, l), w),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return h;
}
const {
  SvelteComponent: df,
  append: Ee,
  attr: W,
  component_subscribe: Ql,
  detach: mf,
  element: hf,
  init: gf,
  insert: bf,
  noop: xl,
  safe_not_equal: pf,
  set_style: an,
  svg_element: Ie,
  toggle_class: $l
} = window.__gradio__svelte__internal, { onMount: wf } = window.__gradio__svelte__internal;
function vf(l) {
  let e, t, n, i, o, r, f, a, s, c, u, d;
  return {
    c() {
      e = hf("div"), t = Ie("svg"), n = Ie("g"), i = Ie("path"), o = Ie("path"), r = Ie("path"), f = Ie("path"), a = Ie("g"), s = Ie("path"), c = Ie("path"), u = Ie("path"), d = Ie("path"), W(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), W(i, "fill", "#FF7C00"), W(i, "fill-opacity", "0.4"), W(i, "class", "svelte-43sxxs"), W(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), W(o, "fill", "#FF7C00"), W(o, "class", "svelte-43sxxs"), W(r, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), W(r, "fill", "#FF7C00"), W(r, "fill-opacity", "0.4"), W(r, "class", "svelte-43sxxs"), W(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), W(f, "fill", "#FF7C00"), W(f, "class", "svelte-43sxxs"), an(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), W(s, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), W(s, "fill", "#FF7C00"), W(s, "fill-opacity", "0.4"), W(s, "class", "svelte-43sxxs"), W(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), W(c, "fill", "#FF7C00"), W(c, "class", "svelte-43sxxs"), W(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), W(u, "fill", "#FF7C00"), W(u, "fill-opacity", "0.4"), W(u, "class", "svelte-43sxxs"), W(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), W(d, "fill", "#FF7C00"), W(d, "class", "svelte-43sxxs"), an(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), W(t, "viewBox", "-1200 -1200 3000 3000"), W(t, "fill", "none"), W(t, "xmlns", "http://www.w3.org/2000/svg"), W(t, "class", "svelte-43sxxs"), W(e, "class", "svelte-43sxxs"), $l(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(_, m) {
      bf(_, e, m), Ee(e, t), Ee(t, n), Ee(n, i), Ee(n, o), Ee(n, r), Ee(n, f), Ee(t, a), Ee(a, s), Ee(a, c), Ee(a, u), Ee(a, d);
    },
    p(_, [m]) {
      m & /*$top*/
      2 && an(n, "transform", "translate(" + /*$top*/
      _[1][0] + "px, " + /*$top*/
      _[1][1] + "px)"), m & /*$bottom*/
      4 && an(a, "transform", "translate(" + /*$bottom*/
      _[2][0] + "px, " + /*$bottom*/
      _[2][1] + "px)"), m & /*margin*/
      1 && $l(
        e,
        "margin",
        /*margin*/
        _[0]
      );
    },
    i: xl,
    o: xl,
    d(_) {
      _ && mf(e);
    }
  };
}
function kf(l, e, t) {
  let n, i;
  var o = this && this.__awaiter || function(_, m, h, p) {
    function w(g) {
      return g instanceof h ? g : new h(function(b) {
        b(g);
      });
    }
    return new (h || (h = Promise))(function(g, b) {
      function S(M) {
        try {
          C(p.next(M));
        } catch (q) {
          b(q);
        }
      }
      function L(M) {
        try {
          C(p.throw(M));
        } catch (q) {
          b(q);
        }
      }
      function C(M) {
        M.done ? g(M.value) : w(M.value).then(S, L);
      }
      C((p = p.apply(_, m || [])).next());
    });
  };
  let { margin: r = !0 } = e;
  const f = Jl([0, 0]);
  Ql(l, f, (_) => t(1, n = _));
  const a = Jl([0, 0]);
  Ql(l, a, (_) => t(2, i = _));
  let s;
  function c() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 140]), a.set([-125, -140])]), yield Promise.all([f.set([-125, 140]), a.set([125, -140])]), yield Promise.all([f.set([-125, 0]), a.set([125, -0])]), yield Promise.all([f.set([125, 0]), a.set([-125, 0])]);
    });
  }
  function u() {
    return o(this, void 0, void 0, function* () {
      yield c(), s || u();
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 0]), a.set([-125, 0])]), u();
    });
  }
  return wf(() => (d(), () => s = !0)), l.$$set = (_) => {
    "margin" in _ && t(0, r = _.margin);
  }, [r, n, i, f, a];
}
class yf extends df {
  constructor(e) {
    super(), gf(this, e, kf, vf, pf, { margin: 0 });
  }
}
const {
  SvelteComponent: Sf,
  append: mt,
  attr: Be,
  binding_callbacks: ei,
  check_outros: hl,
  create_component: so,
  create_slot: fo,
  destroy_component: co,
  destroy_each: uo,
  detach: F,
  element: Fe,
  empty: Ft,
  ensure_array_like: wn,
  get_all_dirty_from_scope: _o,
  get_slot_changes: mo,
  group_outros: gl,
  init: Cf,
  insert: R,
  mount_component: ho,
  noop: bl,
  safe_not_equal: zf,
  set_data: Se,
  set_style: xe,
  space: ye,
  text: K,
  toggle_class: ke,
  transition_in: De,
  transition_out: Re,
  update_slot_base: go
} = window.__gradio__svelte__internal, { tick: qf } = window.__gradio__svelte__internal, { onDestroy: Mf } = window.__gradio__svelte__internal, { createEventDispatcher: Ef } = window.__gradio__svelte__internal, If = (l) => ({}), ti = (l) => ({}), Df = (l) => ({}), ni = (l) => ({});
function li(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function ii(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Bf(l) {
  let e, t, n, i, o = (
    /*i18n*/
    l[1]("common.error") + ""
  ), r, f, a;
  t = new qn({
    props: {
      Icon: Ki,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const s = (
    /*#slots*/
    l[30].error
  ), c = fo(
    s,
    l,
    /*$$scope*/
    l[29],
    ti
  );
  return {
    c() {
      e = Fe("div"), so(t.$$.fragment), n = ye(), i = Fe("span"), r = K(o), f = ye(), c && c.c(), Be(e, "class", "clear-status svelte-16nch4a"), Be(i, "class", "error svelte-16nch4a");
    },
    m(u, d) {
      R(u, e, d), ho(t, e, null), R(u, n, d), R(u, i, d), mt(i, r), R(u, f, d), c && c.m(u, d), a = !0;
    },
    p(u, d) {
      const _ = {};
      d[0] & /*i18n*/
      2 && (_.label = /*i18n*/
      u[1]("common.clear")), t.$set(_), (!a || d[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      u[1]("common.error") + "") && Se(r, o), c && c.p && (!a || d[0] & /*$$scope*/
      536870912) && go(
        c,
        s,
        u,
        /*$$scope*/
        u[29],
        a ? mo(
          s,
          /*$$scope*/
          u[29],
          d,
          If
        ) : _o(
          /*$$scope*/
          u[29]
        ),
        ti
      );
    },
    i(u) {
      a || (De(t.$$.fragment, u), De(c, u), a = !0);
    },
    o(u) {
      Re(t.$$.fragment, u), Re(c, u), a = !1;
    },
    d(u) {
      u && (F(e), F(n), F(i), F(f)), co(t), c && c.d(u);
    }
  };
}
function Lf(l) {
  let e, t, n, i, o, r, f, a, s, c = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && oi(l)
  );
  function u(b, S) {
    if (
      /*progress*/
      b[7]
    ) return Rf;
    if (
      /*queue_position*/
      b[2] !== null && /*queue_size*/
      b[3] !== void 0 && /*queue_position*/
      b[2] >= 0
    ) return Ff;
    if (
      /*queue_position*/
      b[2] === 0
    ) return jf;
  }
  let d = u(l), _ = d && d(l), m = (
    /*timer*/
    l[5] && si(l)
  );
  const h = [Pf, Wf], p = [];
  function w(b, S) {
    return (
      /*last_progress_level*/
      b[15] != null ? 0 : (
        /*show_progress*/
        b[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = w(l)) && (r = p[o] = h[o](l));
  let g = !/*timer*/
  l[5] && hi(l);
  return {
    c() {
      c && c.c(), e = ye(), t = Fe("div"), _ && _.c(), n = ye(), m && m.c(), i = ye(), r && r.c(), f = ye(), g && g.c(), a = Ft(), Be(t, "class", "progress-text svelte-16nch4a"), ke(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), ke(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(b, S) {
      c && c.m(b, S), R(b, e, S), R(b, t, S), _ && _.m(t, null), mt(t, n), m && m.m(t, null), R(b, i, S), ~o && p[o].m(b, S), R(b, f, S), g && g.m(b, S), R(b, a, S), s = !0;
    },
    p(b, S) {
      /*variant*/
      b[8] === "default" && /*show_eta_bar*/
      b[18] && /*show_progress*/
      b[6] === "full" ? c ? c.p(b, S) : (c = oi(b), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), d === (d = u(b)) && _ ? _.p(b, S) : (_ && _.d(1), _ = d && d(b), _ && (_.c(), _.m(t, n))), /*timer*/
      b[5] ? m ? m.p(b, S) : (m = si(b), m.c(), m.m(t, null)) : m && (m.d(1), m = null), (!s || S[0] & /*variant*/
      256) && ke(
        t,
        "meta-text-center",
        /*variant*/
        b[8] === "center"
      ), (!s || S[0] & /*variant*/
      256) && ke(
        t,
        "meta-text",
        /*variant*/
        b[8] === "default"
      );
      let L = o;
      o = w(b), o === L ? ~o && p[o].p(b, S) : (r && (gl(), Re(p[L], 1, 1, () => {
        p[L] = null;
      }), hl()), ~o ? (r = p[o], r ? r.p(b, S) : (r = p[o] = h[o](b), r.c()), De(r, 1), r.m(f.parentNode, f)) : r = null), /*timer*/
      b[5] ? g && (gl(), Re(g, 1, 1, () => {
        g = null;
      }), hl()) : g ? (g.p(b, S), S[0] & /*timer*/
      32 && De(g, 1)) : (g = hi(b), g.c(), De(g, 1), g.m(a.parentNode, a));
    },
    i(b) {
      s || (De(r), De(g), s = !0);
    },
    o(b) {
      Re(r), Re(g), s = !1;
    },
    d(b) {
      b && (F(e), F(t), F(i), F(f), F(a)), c && c.d(b), _ && _.d(), m && m.d(), ~o && p[o].d(b), g && g.d(b);
    }
  };
}
function oi(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Fe("div"), Be(e, "class", "eta-bar svelte-16nch4a"), xe(e, "transform", t);
    },
    m(n, i) {
      R(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && xe(e, "transform", t);
    },
    d(n) {
      n && F(e);
    }
  };
}
function jf(l) {
  let e;
  return {
    c() {
      e = K("processing |");
    },
    m(t, n) {
      R(t, e, n);
    },
    p: bl,
    d(t) {
      t && F(e);
    }
  };
}
function Ff(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, r;
  return {
    c() {
      e = K("queue: "), n = K(t), i = K("/"), o = K(
        /*queue_size*/
        l[3]
      ), r = K(" |");
    },
    m(f, a) {
      R(f, e, a), R(f, n, a), R(f, i, a), R(f, o, a), R(f, r, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && Se(n, t), a[0] & /*queue_size*/
      8 && Se(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (F(e), F(n), F(i), F(o), F(r));
    }
  };
}
function Rf(l) {
  let e, t = wn(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = ai(ii(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Ft();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      R(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = wn(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = ii(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = ai(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && F(e), uo(n, i);
    }
  };
}
function ri(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, o = " ", r;
  function f(c, u) {
    return (
      /*p*/
      c[41].length != null ? Tf : Af
    );
  }
  let a = f(l), s = a(l);
  return {
    c() {
      s.c(), e = ye(), n = K(t), i = K(" | "), r = K(o);
    },
    m(c, u) {
      s.m(c, u), R(c, e, u), R(c, n, u), R(c, i, u), R(c, r, u);
    },
    p(c, u) {
      a === (a = f(c)) && s ? s.p(c, u) : (s.d(1), s = a(c), s && (s.c(), s.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[41].unit + "") && Se(n, t);
    },
    d(c) {
      c && (F(e), F(n), F(i), F(r)), s.d(c);
    }
  };
}
function Af(l) {
  let e = Mt(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = K(e);
    },
    m(n, i) {
      R(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Mt(
        /*p*/
        n[41].index || 0
      ) + "") && Se(t, e);
    },
    d(n) {
      n && F(t);
    }
  };
}
function Tf(l) {
  let e = Mt(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = Mt(
    /*p*/
    l[41].length
  ) + "", o;
  return {
    c() {
      t = K(e), n = K("/"), o = K(i);
    },
    m(r, f) {
      R(r, t, f), R(r, n, f), R(r, o, f);
    },
    p(r, f) {
      f[0] & /*progress*/
      128 && e !== (e = Mt(
        /*p*/
        r[41].index || 0
      ) + "") && Se(t, e), f[0] & /*progress*/
      128 && i !== (i = Mt(
        /*p*/
        r[41].length
      ) + "") && Se(o, i);
    },
    d(r) {
      r && (F(t), F(n), F(o));
    }
  };
}
function ai(l) {
  let e, t = (
    /*p*/
    l[41].index != null && ri(l)
  );
  return {
    c() {
      t && t.c(), e = Ft();
    },
    m(n, i) {
      t && t.m(n, i), R(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = ri(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && F(e), t && t.d(n);
    }
  };
}
function si(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = K(
        /*formatted_timer*/
        l[20]
      ), n = K(t), i = K("s");
    },
    m(o, r) {
      R(o, e, r), R(o, n, r), R(o, i, r);
    },
    p(o, r) {
      r[0] & /*formatted_timer*/
      1048576 && Se(
        e,
        /*formatted_timer*/
        o[20]
      ), r[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && Se(n, t);
    },
    d(o) {
      o && (F(e), F(n), F(i));
    }
  };
}
function Wf(l) {
  let e, t;
  return e = new yf({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      so(e.$$.fragment);
    },
    m(n, i) {
      ho(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (De(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Re(e.$$.fragment, n), t = !1;
    },
    d(n) {
      co(e, n);
    }
  };
}
function Pf(l) {
  let e, t, n, i, o, r = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && fi(l)
  );
  return {
    c() {
      e = Fe("div"), t = Fe("div"), f && f.c(), n = ye(), i = Fe("div"), o = Fe("div"), Be(t, "class", "progress-level-inner svelte-16nch4a"), Be(o, "class", "progress-bar svelte-16nch4a"), xe(o, "width", r), Be(i, "class", "progress-bar-wrap svelte-16nch4a"), Be(e, "class", "progress-level svelte-16nch4a");
    },
    m(a, s) {
      R(a, e, s), mt(e, t), f && f.m(t, null), mt(e, n), mt(e, i), mt(i, o), l[31](o);
    },
    p(a, s) {
      /*progress*/
      a[7] != null ? f ? f.p(a, s) : (f = fi(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), s[0] & /*last_progress_level*/
      32768 && r !== (r = `${/*last_progress_level*/
      a[15] * 100}%`) && xe(o, "width", r);
    },
    i: bl,
    o: bl,
    d(a) {
      a && F(e), f && f.d(), l[31](null);
    }
  };
}
function fi(l) {
  let e, t = wn(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = mi(li(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Ft();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      R(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = wn(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = li(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = mi(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && F(e), uo(n, i);
    }
  };
}
function ci(l) {
  let e, t, n, i, o = (
    /*i*/
    l[43] !== 0 && Nf()
  ), r = (
    /*p*/
    l[41].desc != null && ui(l)
  ), f = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && _i()
  ), a = (
    /*progress_level*/
    l[14] != null && di(l)
  );
  return {
    c() {
      o && o.c(), e = ye(), r && r.c(), t = ye(), f && f.c(), n = ye(), a && a.c(), i = Ft();
    },
    m(s, c) {
      o && o.m(s, c), R(s, e, c), r && r.m(s, c), R(s, t, c), f && f.m(s, c), R(s, n, c), a && a.m(s, c), R(s, i, c);
    },
    p(s, c) {
      /*p*/
      s[41].desc != null ? r ? r.p(s, c) : (r = ui(s), r.c(), r.m(t.parentNode, t)) : r && (r.d(1), r = null), /*p*/
      s[41].desc != null && /*progress_level*/
      s[14] && /*progress_level*/
      s[14][
        /*i*/
        s[43]
      ] != null ? f || (f = _i(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      s[14] != null ? a ? a.p(s, c) : (a = di(s), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(s) {
      s && (F(e), F(t), F(n), F(i)), o && o.d(s), r && r.d(s), f && f.d(s), a && a.d(s);
    }
  };
}
function Nf(l) {
  let e;
  return {
    c() {
      e = K(" /");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && F(e);
    }
  };
}
function ui(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = K(e);
    },
    m(n, i) {
      R(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && Se(t, e);
    },
    d(n) {
      n && F(t);
    }
  };
}
function _i(l) {
  let e;
  return {
    c() {
      e = K("-");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && F(e);
    }
  };
}
function di(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = K(e), n = K("%");
    },
    m(i, o) {
      R(i, t, o), R(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && Se(t, e);
    },
    d(i) {
      i && (F(t), F(n));
    }
  };
}
function mi(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && ci(l)
  );
  return {
    c() {
      t && t.c(), e = Ft();
    },
    m(n, i) {
      t && t.m(n, i), R(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = ci(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && F(e), t && t.d(n);
    }
  };
}
function hi(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), r = fo(
    o,
    l,
    /*$$scope*/
    l[29],
    ni
  );
  return {
    c() {
      e = Fe("p"), t = K(
        /*loading_text*/
        l[9]
      ), n = ye(), r && r.c(), Be(e, "class", "loading svelte-16nch4a");
    },
    m(f, a) {
      R(f, e, a), mt(e, t), R(f, n, a), r && r.m(f, a), i = !0;
    },
    p(f, a) {
      (!i || a[0] & /*loading_text*/
      512) && Se(
        t,
        /*loading_text*/
        f[9]
      ), r && r.p && (!i || a[0] & /*$$scope*/
      536870912) && go(
        r,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? mo(
          o,
          /*$$scope*/
          f[29],
          a,
          Df
        ) : _o(
          /*$$scope*/
          f[29]
        ),
        ni
      );
    },
    i(f) {
      i || (De(r, f), i = !0);
    },
    o(f) {
      Re(r, f), i = !1;
    },
    d(f) {
      f && (F(e), F(n)), r && r.d(f);
    }
  };
}
function Vf(l) {
  let e, t, n, i, o;
  const r = [Lf, Bf], f = [];
  function a(s, c) {
    return (
      /*status*/
      s[4] === "pending" ? 0 : (
        /*status*/
        s[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(l)) && (n = f[t] = r[t](l)), {
    c() {
      e = Fe("div"), n && n.c(), Be(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-16nch4a"), ke(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), ke(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), ke(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), ke(
        e,
        "border",
        /*border*/
        l[12]
      ), xe(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), xe(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(s, c) {
      R(s, e, c), ~t && f[t].m(e, null), l[33](e), o = !0;
    },
    p(s, c) {
      let u = t;
      t = a(s), t === u ? ~t && f[t].p(s, c) : (n && (gl(), Re(f[u], 1, 1, () => {
        f[u] = null;
      }), hl()), ~t ? (n = f[t], n ? n.p(s, c) : (n = f[t] = r[t](s), n.c()), De(n, 1), n.m(e, null)) : n = null), (!o || c[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      s[8] + " " + /*show_progress*/
      s[6] + " svelte-16nch4a")) && Be(e, "class", i), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && ke(e, "hide", !/*status*/
      s[4] || /*status*/
      s[4] === "complete" || /*show_progress*/
      s[6] === "hidden"), (!o || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && ke(
        e,
        "translucent",
        /*variant*/
        s[8] === "center" && /*status*/
        (s[4] === "pending" || /*status*/
        s[4] === "error") || /*translucent*/
        s[11] || /*show_progress*/
        s[6] === "minimal"
      ), (!o || c[0] & /*variant, show_progress, status*/
      336) && ke(
        e,
        "generating",
        /*status*/
        s[4] === "generating"
      ), (!o || c[0] & /*variant, show_progress, border*/
      4416) && ke(
        e,
        "border",
        /*border*/
        s[12]
      ), c[0] & /*absolute*/
      1024 && xe(
        e,
        "position",
        /*absolute*/
        s[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && xe(
        e,
        "padding",
        /*absolute*/
        s[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(s) {
      o || (De(n), o = !0);
    },
    o(s) {
      Re(n), o = !1;
    },
    d(s) {
      s && F(e), ~t && f[t].d(), l[33](null);
    }
  };
}
var Uf = function(l, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(r) {
      r(o);
    });
  }
  return new (t || (t = Promise))(function(o, r) {
    function f(c) {
      try {
        s(n.next(c));
      } catch (u) {
        r(u);
      }
    }
    function a(c) {
      try {
        s(n.throw(c));
      } catch (u) {
        r(u);
      }
    }
    function s(c) {
      c.done ? o(c.value) : i(c.value).then(f, a);
    }
    s((n = n.apply(l, e || [])).next());
  });
};
let sn = [], il = !1;
function Of(l) {
  return Uf(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (sn.push(e), !il) il = !0;
      else return;
      yield qf(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < sn.length; i++) {
          const r = sn[i].getBoundingClientRect();
          (i === 0 || r.top + window.scrollY <= n[0]) && (n[0] = r.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), il = !1, sn = [];
      });
    }
  });
}
function Gf(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  const r = Ef();
  let { i18n: f } = e, { eta: a = null } = e, { queue_position: s } = e, { queue_size: c } = e, { status: u } = e, { scroll_to_output: d = !1 } = e, { timer: _ = !0 } = e, { show_progress: m = "full" } = e, { message: h = null } = e, { progress: p = null } = e, { variant: w = "default" } = e, { loading_text: g = "Loading..." } = e, { absolute: b = !0 } = e, { translucent: S = !1 } = e, { border: L = !1 } = e, { autoscroll: C } = e, M, q = !1, D = 0, v = 0, I = null, V = null, U = 0, le = null, j, T = null, X = !0;
  const E = () => {
    t(0, a = t(27, I = t(19, O = null))), t(25, D = performance.now()), t(26, v = 0), q = !0, N();
  };
  function N() {
    requestAnimationFrame(() => {
      t(26, v = (performance.now() - D) / 1e3), q && N();
    });
  }
  function G() {
    t(26, v = 0), t(0, a = t(27, I = t(19, O = null))), q && (q = !1);
  }
  Mf(() => {
    q && G();
  });
  let O = null;
  function ie(B) {
    ei[B ? "unshift" : "push"](() => {
      T = B, t(16, T), t(7, p), t(14, le), t(15, j);
    });
  }
  const fe = () => {
    r("clear_status");
  };
  function z(B) {
    ei[B ? "unshift" : "push"](() => {
      M = B, t(13, M);
    });
  }
  return l.$$set = (B) => {
    "i18n" in B && t(1, f = B.i18n), "eta" in B && t(0, a = B.eta), "queue_position" in B && t(2, s = B.queue_position), "queue_size" in B && t(3, c = B.queue_size), "status" in B && t(4, u = B.status), "scroll_to_output" in B && t(22, d = B.scroll_to_output), "timer" in B && t(5, _ = B.timer), "show_progress" in B && t(6, m = B.show_progress), "message" in B && t(23, h = B.message), "progress" in B && t(7, p = B.progress), "variant" in B && t(8, w = B.variant), "loading_text" in B && t(9, g = B.loading_text), "absolute" in B && t(10, b = B.absolute), "translucent" in B && t(11, S = B.translucent), "border" in B && t(12, L = B.border), "autoscroll" in B && t(24, C = B.autoscroll), "$$scope" in B && t(29, o = B.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (a === null && t(0, a = I), a != null && I !== a && (t(28, V = (performance.now() - D) / 1e3 + a), t(19, O = V.toFixed(1)), t(27, I = a))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, U = V === null || V <= 0 || !v ? null : Math.min(v / V, 1)), l.$$.dirty[0] & /*progress*/
    128 && p != null && t(18, X = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (p != null ? t(14, le = p.map((B) => {
      if (B.index != null && B.length != null)
        return B.index / B.length;
      if (B.progress != null)
        return B.progress;
    })) : t(14, le = null), le ? (t(15, j = le[le.length - 1]), T && (j === 0 ? t(16, T.style.transition = "0", T) : t(16, T.style.transition = "150ms", T))) : t(15, j = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? E() : G()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && M && d && (u === "pending" || u === "complete") && Of(M, C), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = v.toFixed(1));
  }, [
    a,
    f,
    s,
    c,
    u,
    _,
    m,
    p,
    w,
    g,
    b,
    S,
    L,
    M,
    le,
    j,
    T,
    U,
    X,
    O,
    n,
    r,
    d,
    h,
    C,
    D,
    v,
    I,
    V,
    o,
    i,
    ie,
    fe,
    z
  ];
}
class Hf extends Sf {
  constructor(e) {
    super(), Cf(
      this,
      e,
      Gf,
      Vf,
      zf,
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
const { setContext: A_, getContext: Zf } = window.__gradio__svelte__internal, Xf = "WORKER_PROXY_CONTEXT_KEY";
function Yf() {
  return Zf(Xf);
}
function Kf(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function Jf(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function Qf(l) {
  if (l == null)
    return !1;
  const e = new URL(l, window.location.href);
  return !(!Kf(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
const {
  SvelteComponent: xf,
  assign: vn,
  check_outros: bo,
  compute_rest_props: gi,
  create_slot: kl,
  detach: Bn,
  element: po,
  empty: wo,
  exclude_internal_props: $f,
  get_all_dirty_from_scope: yl,
  get_slot_changes: Sl,
  get_spread_update: vo,
  group_outros: ko,
  init: ec,
  insert: Ln,
  listen: yo,
  prevent_default: tc,
  safe_not_equal: nc,
  set_attributes: kn,
  transition_in: bt,
  transition_out: pt,
  update_slot_base: Cl
} = window.__gradio__svelte__internal, { createEventDispatcher: lc } = window.__gradio__svelte__internal;
function ic(l) {
  let e, t, n, i, o;
  const r = (
    /*#slots*/
    l[8].default
  ), f = kl(
    r,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let a = [
    { href: (
      /*href*/
      l[0]
    ) },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    { rel: "noopener noreferrer" },
    { download: (
      /*download*/
      l[1]
    ) },
    /*$$restProps*/
    l[6]
  ], s = {};
  for (let c = 0; c < a.length; c += 1)
    s = vn(s, a[c]);
  return {
    c() {
      e = po("a"), f && f.c(), kn(e, s);
    },
    m(c, u) {
      Ln(c, e, u), f && f.m(e, null), n = !0, i || (o = yo(
        e,
        "click",
        /*dispatch*/
        l[3].bind(null, "click")
      ), i = !0);
    },
    p(c, u) {
      f && f.p && (!n || u & /*$$scope*/
      128) && Cl(
        f,
        r,
        c,
        /*$$scope*/
        c[7],
        n ? Sl(
          r,
          /*$$scope*/
          c[7],
          u,
          null
        ) : yl(
          /*$$scope*/
          c[7]
        ),
        null
      ), kn(e, s = vo(a, [
        (!n || u & /*href*/
        1) && { href: (
          /*href*/
          c[0]
        ) },
        { target: t },
        { rel: "noopener noreferrer" },
        (!n || u & /*download*/
        2) && { download: (
          /*download*/
          c[1]
        ) },
        u & /*$$restProps*/
        64 && /*$$restProps*/
        c[6]
      ]));
    },
    i(c) {
      n || (bt(f, c), n = !0);
    },
    o(c) {
      pt(f, c), n = !1;
    },
    d(c) {
      c && Bn(e), f && f.d(c), i = !1, o();
    }
  };
}
function oc(l) {
  let e, t, n, i;
  const o = [ac, rc], r = [];
  function f(a, s) {
    return (
      /*is_downloading*/
      a[2] ? 0 : 1
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = wo();
    },
    m(a, s) {
      r[e].m(a, s), Ln(a, n, s), i = !0;
    },
    p(a, s) {
      let c = e;
      e = f(a), e === c ? r[e].p(a, s) : (ko(), pt(r[c], 1, 1, () => {
        r[c] = null;
      }), bo(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), bt(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (bt(t), i = !0);
    },
    o(a) {
      pt(t), i = !1;
    },
    d(a) {
      a && Bn(n), r[e].d(a);
    }
  };
}
function rc(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[8].default
  ), r = kl(
    o,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let f = [
    /*$$restProps*/
    l[6],
    { href: (
      /*href*/
      l[0]
    ) }
  ], a = {};
  for (let s = 0; s < f.length; s += 1)
    a = vn(a, f[s]);
  return {
    c() {
      e = po("a"), r && r.c(), kn(e, a);
    },
    m(s, c) {
      Ln(s, e, c), r && r.m(e, null), t = !0, n || (i = yo(e, "click", tc(
        /*wasm_click_handler*/
        l[5]
      )), n = !0);
    },
    p(s, c) {
      r && r.p && (!t || c & /*$$scope*/
      128) && Cl(
        r,
        o,
        s,
        /*$$scope*/
        s[7],
        t ? Sl(
          o,
          /*$$scope*/
          s[7],
          c,
          null
        ) : yl(
          /*$$scope*/
          s[7]
        ),
        null
      ), kn(e, a = vo(f, [
        c & /*$$restProps*/
        64 && /*$$restProps*/
        s[6],
        (!t || c & /*href*/
        1) && { href: (
          /*href*/
          s[0]
        ) }
      ]));
    },
    i(s) {
      t || (bt(r, s), t = !0);
    },
    o(s) {
      pt(r, s), t = !1;
    },
    d(s) {
      s && Bn(e), r && r.d(s), n = !1, i();
    }
  };
}
function ac(l) {
  let e;
  const t = (
    /*#slots*/
    l[8].default
  ), n = kl(
    t,
    l,
    /*$$scope*/
    l[7],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      128) && Cl(
        n,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? Sl(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : yl(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (bt(n, i), e = !0);
    },
    o(i) {
      pt(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function sc(l) {
  let e, t, n, i, o;
  const r = [oc, ic], f = [];
  function a(s, c) {
    return c & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (s[4] && Qf(
      /*href*/
      s[0]
    ))), e ? 0 : 1;
  }
  return t = a(l, -1), n = f[t] = r[t](l), {
    c() {
      n.c(), i = wo();
    },
    m(s, c) {
      f[t].m(s, c), Ln(s, i, c), o = !0;
    },
    p(s, [c]) {
      let u = t;
      t = a(s, c), t === u ? f[t].p(s, c) : (ko(), pt(f[u], 1, 1, () => {
        f[u] = null;
      }), bo(), n = f[t], n ? n.p(s, c) : (n = f[t] = r[t](s), n.c()), bt(n, 1), n.m(i.parentNode, i));
    },
    i(s) {
      o || (bt(n), o = !0);
    },
    o(s) {
      pt(n), o = !1;
    },
    d(s) {
      s && Bn(i), f[t].d(s);
    }
  };
}
function fc(l, e, t) {
  const n = ["href", "download"];
  let i = gi(e, n), { $$slots: o = {}, $$scope: r } = e;
  var f = this && this.__awaiter || function(m, h, p, w) {
    function g(b) {
      return b instanceof p ? b : new p(function(S) {
        S(b);
      });
    }
    return new (p || (p = Promise))(function(b, S) {
      function L(q) {
        try {
          M(w.next(q));
        } catch (D) {
          S(D);
        }
      }
      function C(q) {
        try {
          M(w.throw(q));
        } catch (D) {
          S(D);
        }
      }
      function M(q) {
        q.done ? b(q.value) : g(q.value).then(L, C);
      }
      M((w = w.apply(m, h || [])).next());
    });
  };
  let { href: a = void 0 } = e, { download: s } = e;
  const c = lc();
  let u = !1;
  const d = Yf();
  function _() {
    return f(this, void 0, void 0, function* () {
      if (u)
        return;
      if (c("click"), a == null)
        throw new Error("href is not defined.");
      if (d == null)
        throw new Error("Wasm worker proxy is not available.");
      const h = new URL(a, window.location.href).pathname;
      t(2, u = !0), d.httpRequest({
        method: "GET",
        path: h,
        headers: {},
        query_string: ""
      }).then((p) => {
        if (p.status !== 200)
          throw new Error(`Failed to get file ${h} from the Wasm worker.`);
        const w = new Blob(
          [p.body],
          {
            type: Jf(p.headers, "content-type")
          }
        ), g = URL.createObjectURL(w), b = document.createElement("a");
        b.href = g, b.download = s, b.click(), URL.revokeObjectURL(g);
      }).finally(() => {
        t(2, u = !1);
      });
    });
  }
  return l.$$set = (m) => {
    e = vn(vn({}, e), $f(m)), t(6, i = gi(e, n)), "href" in m && t(0, a = m.href), "download" in m && t(1, s = m.download), "$$scope" in m && t(7, r = m.$$scope);
  }, [
    a,
    s,
    u,
    c,
    d,
    _,
    i,
    r,
    o
  ];
}
class cc extends xf {
  constructor(e) {
    super(), ec(this, e, fc, sc, nc, { href: 0, download: 1 });
  }
}
var uc = Object.defineProperty, _c = (l, e, t) => e in l ? uc(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t, We = (l, e, t) => (_c(l, typeof e != "symbol" ? e + "" : e, t), t), So = (l, e, t) => {
  if (!e.has(l))
    throw TypeError("Cannot " + t);
}, Vt = (l, e, t) => (So(l, e, "read from private field"), t ? t.call(l) : e.get(l)), dc = (l, e, t) => {
  if (e.has(l))
    throw TypeError("Cannot add the same private member more than once");
  e instanceof WeakSet ? e.add(l) : e.set(l, t);
}, mc = (l, e, t, n) => (So(l, e, "write to private field"), e.set(l, t), t), Qe;
new Intl.Collator(0, { numeric: 1 }).compare;
async function Co(l, e) {
  return l.map(
    (t) => new hc({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class hc {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: o,
    is_stream: r,
    mime_type: f,
    alt_text: a
  }) {
    We(this, "path"), We(this, "url"), We(this, "orig_name"), We(this, "size"), We(this, "blob"), We(this, "is_stream"), We(this, "mime_type"), We(this, "alt_text"), We(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : o, this.is_stream = r, this.mime_type = f, this.alt_text = a;
  }
}
typeof process < "u" && process.versions && process.versions.node;
class T_ extends TransformStream {
  /** Constructs a new instance. */
  constructor(e = { allowCR: !1 }) {
    super({
      transform: (t, n) => {
        for (t = Vt(this, Qe) + t; ; ) {
          const i = t.indexOf(`
`), o = e.allowCR ? t.indexOf("\r") : -1;
          if (o !== -1 && o !== t.length - 1 && (i === -1 || i - 1 > o)) {
            n.enqueue(t.slice(0, o)), t = t.slice(o + 1);
            continue;
          }
          if (i === -1)
            break;
          const r = t[i - 1] === "\r" ? i - 1 : i;
          n.enqueue(t.slice(0, r)), t = t.slice(i + 1);
        }
        mc(this, Qe, t);
      },
      flush: (t) => {
        if (Vt(this, Qe) === "")
          return;
        const n = e.allowCR && Vt(this, Qe).endsWith("\r") ? Vt(this, Qe).slice(0, -1) : Vt(this, Qe);
        t.enqueue(n);
      }
    }), dc(this, Qe, "");
  }
}
Qe = /* @__PURE__ */ new WeakMap();
const {
  SvelteComponent: gc,
  append: he,
  attr: ut,
  detach: zo,
  element: _t,
  init: bc,
  insert: qo,
  noop: bi,
  safe_not_equal: pc,
  set_data: yn,
  set_style: ol,
  space: pl,
  text: Et,
  toggle_class: pi
} = window.__gradio__svelte__internal, { onMount: wc, createEventDispatcher: vc, onDestroy: kc } = window.__gradio__svelte__internal;
function wi(l) {
  let e, t, n, i, o = Zt(
    /*file_to_display*/
    l[2]
  ) + "", r, f, a, s, c = (
    /*file_to_display*/
    l[2].orig_name + ""
  ), u;
  return {
    c() {
      e = _t("div"), t = _t("span"), n = _t("div"), i = _t("progress"), r = Et(o), a = pl(), s = _t("span"), u = Et(c), ol(i, "visibility", "hidden"), ol(i, "height", "0"), ol(i, "width", "0"), i.value = f = Zt(
        /*file_to_display*/
        l[2]
      ), ut(i, "max", "100"), ut(i, "class", "svelte-cr2edf"), ut(n, "class", "progress-bar svelte-cr2edf"), ut(s, "class", "file-name svelte-cr2edf"), ut(e, "class", "file svelte-cr2edf");
    },
    m(d, _) {
      qo(d, e, _), he(e, t), he(t, n), he(n, i), he(i, r), he(e, a), he(e, s), he(s, u);
    },
    p(d, _) {
      _ & /*file_to_display*/
      4 && o !== (o = Zt(
        /*file_to_display*/
        d[2]
      ) + "") && yn(r, o), _ & /*file_to_display*/
      4 && f !== (f = Zt(
        /*file_to_display*/
        d[2]
      )) && (i.value = f), _ & /*file_to_display*/
      4 && c !== (c = /*file_to_display*/
      d[2].orig_name + "") && yn(u, c);
    },
    d(d) {
      d && zo(e);
    }
  };
}
function yc(l) {
  let e, t, n, i = (
    /*files_with_progress*/
    l[0].length + ""
  ), o, r, f = (
    /*files_with_progress*/
    l[0].length > 1 ? "files" : "file"
  ), a, s, c, u = (
    /*file_to_display*/
    l[2] && wi(l)
  );
  return {
    c() {
      e = _t("div"), t = _t("span"), n = Et("Uploading "), o = Et(i), r = pl(), a = Et(f), s = Et("..."), c = pl(), u && u.c(), ut(t, "class", "uploading svelte-cr2edf"), ut(e, "class", "wrap svelte-cr2edf"), pi(
        e,
        "progress",
        /*progress*/
        l[1]
      );
    },
    m(d, _) {
      qo(d, e, _), he(e, t), he(t, n), he(t, o), he(t, r), he(t, a), he(t, s), he(e, c), u && u.m(e, null);
    },
    p(d, [_]) {
      _ & /*files_with_progress*/
      1 && i !== (i = /*files_with_progress*/
      d[0].length + "") && yn(o, i), _ & /*files_with_progress*/
      1 && f !== (f = /*files_with_progress*/
      d[0].length > 1 ? "files" : "file") && yn(a, f), /*file_to_display*/
      d[2] ? u ? u.p(d, _) : (u = wi(d), u.c(), u.m(e, null)) : u && (u.d(1), u = null), _ & /*progress*/
      2 && pi(
        e,
        "progress",
        /*progress*/
        d[1]
      );
    },
    i: bi,
    o: bi,
    d(d) {
      d && zo(e), u && u.d();
    }
  };
}
function Zt(l) {
  return l.progress * 100 / (l.size || 0) || 0;
}
function Sc(l) {
  let e = 0;
  return l.forEach((t) => {
    e += Zt(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / l.length).toFixed(2) + "%"), e / l.length;
}
function Cc(l, e, t) {
  var n = this && this.__awaiter || function(h, p, w, g) {
    function b(S) {
      return S instanceof w ? S : new w(function(L) {
        L(S);
      });
    }
    return new (w || (w = Promise))(function(S, L) {
      function C(D) {
        try {
          q(g.next(D));
        } catch (v) {
          L(v);
        }
      }
      function M(D) {
        try {
          q(g.throw(D));
        } catch (v) {
          L(v);
        }
      }
      function q(D) {
        D.done ? S(D.value) : b(D.value).then(C, M);
      }
      q((g = g.apply(h, p || [])).next());
    });
  };
  let { upload_id: i } = e, { root: o } = e, { files: r } = e, { stream_handler: f } = e, a, s = !1, c, u, d = r.map((h) => Object.assign(Object.assign({}, h), { progress: 0 }));
  const _ = vc();
  function m(h, p) {
    t(0, d = d.map((w) => (w.orig_name === h && (w.progress += p), w)));
  }
  return wc(() => n(void 0, void 0, void 0, function* () {
    if (a = yield f(new URL(`${o}/upload_progress?upload_id=${i}`)), a == null)
      throw new Error("Event source is not defined");
    a.onmessage = function(h) {
      return n(this, void 0, void 0, function* () {
        const p = JSON.parse(h.data);
        s || t(1, s = !0), p.msg === "done" ? (a == null || a.close(), _("done")) : (t(7, c = p), m(p.orig_name, p.chunk_size));
      });
    };
  })), kc(() => {
    (a != null || a != null) && a.close();
  }), l.$$set = (h) => {
    "upload_id" in h && t(3, i = h.upload_id), "root" in h && t(4, o = h.root), "files" in h && t(5, r = h.files), "stream_handler" in h && t(6, f = h.stream_handler);
  }, l.$$.update = () => {
    l.$$.dirty & /*files_with_progress*/
    1 && Sc(d), l.$$.dirty & /*current_file_upload, files_with_progress*/
    129 && t(2, u = c || d[0]);
  }, [
    d,
    s,
    u,
    i,
    o,
    r,
    f,
    c
  ];
}
class zc extends gc {
  constructor(e) {
    super(), bc(this, e, Cc, yc, pc, {
      upload_id: 3,
      root: 4,
      files: 5,
      stream_handler: 6
    });
  }
}
const {
  SvelteComponent: qc,
  append: vi,
  attr: ae,
  binding_callbacks: Mc,
  bubble: it,
  check_outros: Mo,
  create_component: Ec,
  create_slot: Eo,
  destroy_component: Ic,
  detach: jn,
  element: wl,
  empty: Io,
  get_all_dirty_from_scope: Do,
  get_slot_changes: Bo,
  group_outros: Lo,
  init: Dc,
  insert: Fn,
  listen: we,
  mount_component: Bc,
  prevent_default: ot,
  run_all: Lc,
  safe_not_equal: jc,
  set_style: jo,
  space: Fc,
  stop_propagation: rt,
  toggle_class: te,
  transition_in: $e,
  transition_out: wt,
  update_slot_base: Fo
} = window.__gradio__svelte__internal, { createEventDispatcher: Rc, tick: Ac } = window.__gradio__svelte__internal;
function Tc(l) {
  let e, t, n, i, o, r, f, a, s, c, u;
  const d = (
    /*#slots*/
    l[26].default
  ), _ = Eo(
    d,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = wl("button"), _ && _.c(), t = Fc(), n = wl("input"), ae(n, "aria-label", "file upload"), ae(n, "data-testid", "file-upload"), ae(n, "type", "file"), ae(n, "accept", i = /*accept_file_types*/
      l[16] || void 0), n.multiple = o = /*file_count*/
      l[6] === "multiple" || void 0, ae(n, "webkitdirectory", r = /*file_count*/
      l[6] === "directory" || void 0), ae(n, "mozdirectory", f = /*file_count*/
      l[6] === "directory" || void 0), ae(n, "class", "svelte-1s26xmt"), ae(e, "tabindex", a = /*hidden*/
      l[9] ? -1 : 0), ae(e, "class", "svelte-1s26xmt"), te(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), te(
        e,
        "center",
        /*center*/
        l[4]
      ), te(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), te(
        e,
        "flex",
        /*flex*/
        l[5]
      ), te(
        e,
        "disable_click",
        /*disable_click*/
        l[7]
      ), jo(e, "height", "100%");
    },
    m(m, h) {
      Fn(m, e, h), _ && _.m(e, null), vi(e, t), vi(e, n), l[34](n), s = !0, c || (u = [
        we(
          n,
          "change",
          /*load_files_from_upload*/
          l[18]
        ),
        we(e, "drag", rt(ot(
          /*drag_handler*/
          l[27]
        ))),
        we(e, "dragstart", rt(ot(
          /*dragstart_handler*/
          l[28]
        ))),
        we(e, "dragend", rt(ot(
          /*dragend_handler*/
          l[29]
        ))),
        we(e, "dragover", rt(ot(
          /*dragover_handler*/
          l[30]
        ))),
        we(e, "dragenter", rt(ot(
          /*dragenter_handler*/
          l[31]
        ))),
        we(e, "dragleave", rt(ot(
          /*dragleave_handler*/
          l[32]
        ))),
        we(e, "drop", rt(ot(
          /*drop_handler*/
          l[33]
        ))),
        we(
          e,
          "click",
          /*open_file_upload*/
          l[13]
        ),
        we(
          e,
          "drop",
          /*loadFilesFromDrop*/
          l[19]
        ),
        we(
          e,
          "dragenter",
          /*updateDragging*/
          l[17]
        ),
        we(
          e,
          "dragleave",
          /*updateDragging*/
          l[17]
        )
      ], c = !0);
    },
    p(m, h) {
      _ && _.p && (!s || h[0] & /*$$scope*/
      33554432) && Fo(
        _,
        d,
        m,
        /*$$scope*/
        m[25],
        s ? Bo(
          d,
          /*$$scope*/
          m[25],
          h,
          null
        ) : Do(
          /*$$scope*/
          m[25]
        ),
        null
      ), (!s || h[0] & /*accept_file_types*/
      65536 && i !== (i = /*accept_file_types*/
      m[16] || void 0)) && ae(n, "accept", i), (!s || h[0] & /*file_count*/
      64 && o !== (o = /*file_count*/
      m[6] === "multiple" || void 0)) && (n.multiple = o), (!s || h[0] & /*file_count*/
      64 && r !== (r = /*file_count*/
      m[6] === "directory" || void 0)) && ae(n, "webkitdirectory", r), (!s || h[0] & /*file_count*/
      64 && f !== (f = /*file_count*/
      m[6] === "directory" || void 0)) && ae(n, "mozdirectory", f), (!s || h[0] & /*hidden*/
      512 && a !== (a = /*hidden*/
      m[9] ? -1 : 0)) && ae(e, "tabindex", a), (!s || h[0] & /*hidden*/
      512) && te(
        e,
        "hidden",
        /*hidden*/
        m[9]
      ), (!s || h[0] & /*center*/
      16) && te(
        e,
        "center",
        /*center*/
        m[4]
      ), (!s || h[0] & /*boundedheight*/
      8) && te(
        e,
        "boundedheight",
        /*boundedheight*/
        m[3]
      ), (!s || h[0] & /*flex*/
      32) && te(
        e,
        "flex",
        /*flex*/
        m[5]
      ), (!s || h[0] & /*disable_click*/
      128) && te(
        e,
        "disable_click",
        /*disable_click*/
        m[7]
      );
    },
    i(m) {
      s || ($e(_, m), s = !0);
    },
    o(m) {
      wt(_, m), s = !1;
    },
    d(m) {
      m && jn(e), _ && _.d(m), l[34](null), c = !1, Lc(u);
    }
  };
}
function Wc(l) {
  let e, t, n = !/*hidden*/
  l[9] && ki(l);
  return {
    c() {
      n && n.c(), e = Io();
    },
    m(i, o) {
      n && n.m(i, o), Fn(i, e, o), t = !0;
    },
    p(i, o) {
      /*hidden*/
      i[9] ? n && (Lo(), wt(n, 1, 1, () => {
        n = null;
      }), Mo()) : n ? (n.p(i, o), o[0] & /*hidden*/
      512 && $e(n, 1)) : (n = ki(i), n.c(), $e(n, 1), n.m(e.parentNode, e));
    },
    i(i) {
      t || ($e(n), t = !0);
    },
    o(i) {
      wt(n), t = !1;
    },
    d(i) {
      i && jn(e), n && n.d(i);
    }
  };
}
function Pc(l) {
  let e, t, n, i, o;
  const r = (
    /*#slots*/
    l[26].default
  ), f = Eo(
    r,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = wl("button"), f && f.c(), ae(e, "tabindex", t = /*hidden*/
      l[9] ? -1 : 0), ae(e, "class", "svelte-1s26xmt"), te(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), te(
        e,
        "center",
        /*center*/
        l[4]
      ), te(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), te(
        e,
        "flex",
        /*flex*/
        l[5]
      ), jo(e, "height", "100%");
    },
    m(a, s) {
      Fn(a, e, s), f && f.m(e, null), n = !0, i || (o = we(
        e,
        "click",
        /*paste_clipboard*/
        l[12]
      ), i = !0);
    },
    p(a, s) {
      f && f.p && (!n || s[0] & /*$$scope*/
      33554432) && Fo(
        f,
        r,
        a,
        /*$$scope*/
        a[25],
        n ? Bo(
          r,
          /*$$scope*/
          a[25],
          s,
          null
        ) : Do(
          /*$$scope*/
          a[25]
        ),
        null
      ), (!n || s[0] & /*hidden*/
      512 && t !== (t = /*hidden*/
      a[9] ? -1 : 0)) && ae(e, "tabindex", t), (!n || s[0] & /*hidden*/
      512) && te(
        e,
        "hidden",
        /*hidden*/
        a[9]
      ), (!n || s[0] & /*center*/
      16) && te(
        e,
        "center",
        /*center*/
        a[4]
      ), (!n || s[0] & /*boundedheight*/
      8) && te(
        e,
        "boundedheight",
        /*boundedheight*/
        a[3]
      ), (!n || s[0] & /*flex*/
      32) && te(
        e,
        "flex",
        /*flex*/
        a[5]
      );
    },
    i(a) {
      n || ($e(f, a), n = !0);
    },
    o(a) {
      wt(f, a), n = !1;
    },
    d(a) {
      a && jn(e), f && f.d(a), i = !1, o();
    }
  };
}
function ki(l) {
  let e, t;
  return e = new zc({
    props: {
      root: (
        /*root*/
        l[8]
      ),
      upload_id: (
        /*upload_id*/
        l[14]
      ),
      files: (
        /*file_data*/
        l[15]
      ),
      stream_handler: (
        /*stream_handler*/
        l[11]
      )
    }
  }), {
    c() {
      Ec(e.$$.fragment);
    },
    m(n, i) {
      Bc(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*root*/
      256 && (o.root = /*root*/
      n[8]), i[0] & /*upload_id*/
      16384 && (o.upload_id = /*upload_id*/
      n[14]), i[0] & /*file_data*/
      32768 && (o.files = /*file_data*/
      n[15]), i[0] & /*stream_handler*/
      2048 && (o.stream_handler = /*stream_handler*/
      n[11]), e.$set(o);
    },
    i(n) {
      t || ($e(e.$$.fragment, n), t = !0);
    },
    o(n) {
      wt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ic(e, n);
    }
  };
}
function Nc(l) {
  let e, t, n, i;
  const o = [Pc, Wc, Tc], r = [];
  function f(a, s) {
    return (
      /*filetype*/
      a[0] === "clipboard" ? 0 : (
        /*uploading*/
        a[1] && /*show_progress*/
        a[10] ? 1 : 2
      )
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = Io();
    },
    m(a, s) {
      r[e].m(a, s), Fn(a, n, s), i = !0;
    },
    p(a, s) {
      let c = e;
      e = f(a), e === c ? r[e].p(a, s) : (Lo(), wt(r[c], 1, 1, () => {
        r[c] = null;
      }), Mo(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), $e(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || ($e(t), i = !0);
    },
    o(a) {
      wt(t), i = !1;
    },
    d(a) {
      a && jn(n), r[e].d(a);
    }
  };
}
function Vc(l, e, t) {
  if (!l || l === "*" || l === "file/*" || Array.isArray(l) && l.some((i) => i === "*" || i === "file/*"))
    return !0;
  let n;
  if (typeof l == "string")
    n = l.split(",").map((i) => i.trim());
  else if (Array.isArray(l))
    n = l;
  else
    return !1;
  return n.includes(e) || n.some((i) => {
    const [o] = i.split("/").map((r) => r.trim());
    return i.endsWith("/*") && t.startsWith(o + "/");
  });
}
function Uc(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(y, A, Y, $) {
    function oe(Te) {
      return Te instanceof Y ? Te : new Y(function(Ze) {
        Ze(Te);
      });
    }
    return new (Y || (Y = Promise))(function(Te, Ze) {
      function nt(ce) {
        try {
          k($.next(ce));
        } catch (ze) {
          Ze(ze);
        }
      }
      function Ce(ce) {
        try {
          k($.throw(ce));
        } catch (ze) {
          Ze(ze);
        }
      }
      function k(ce) {
        ce.done ? Te(ce.value) : oe(ce.value).then(nt, Ce);
      }
      k(($ = $.apply(y, A || [])).next());
    });
  };
  let { filetype: r = null } = e, { dragging: f = !1 } = e, { boundedheight: a = !0 } = e, { center: s = !0 } = e, { flex: c = !0 } = e, { file_count: u = "single" } = e, { disable_click: d = !1 } = e, { root: _ } = e, { hidden: m = !1 } = e, { format: h = "file" } = e, { uploading: p = !1 } = e, { hidden_upload: w = null } = e, { show_progress: g = !0 } = e, { max_file_size: b = null } = e, { upload: S } = e, { stream_handler: L } = e, C, M, q;
  const D = Rc(), v = ["image", "video", "audio", "text", "file"], I = (y) => y.startsWith(".") || y.endsWith("/*") ? y : v.includes(y) ? y + "/*" : "." + y;
  function V() {
    t(20, f = !f);
  }
  function U() {
    navigator.clipboard.read().then((y) => o(this, void 0, void 0, function* () {
      for (let A = 0; A < y.length; A++) {
        const Y = y[A].types.find(($) => $.startsWith("image/"));
        if (Y) {
          y[A].getType(Y).then(($) => o(this, void 0, void 0, function* () {
            const oe = new File([$], `clipboard.${Y.replace("image/", "")}`);
            yield T([oe]);
          }));
          break;
        }
      }
    }));
  }
  function le() {
    d || w && (t(2, w.value = "", w), w.click());
  }
  function j(y) {
    return o(this, void 0, void 0, function* () {
      yield Ac(), t(14, C = Math.random().toString(36).substring(2, 15)), t(1, p = !0);
      try {
        const A = yield S(y, _, C, b ?? 1 / 0);
        return D("load", u === "single" ? A == null ? void 0 : A[0] : A), t(1, p = !1), A || [];
      } catch (A) {
        return D("error", A.message), t(1, p = !1), [];
      }
    });
  }
  function T(y) {
    return o(this, void 0, void 0, function* () {
      if (!y.length)
        return;
      let A = y.map((Y) => new File([Y], Y instanceof File ? Y.name : "file", { type: Y.type }));
      return t(15, M = yield Co(A)), yield j(M);
    });
  }
  function X(y) {
    return o(this, void 0, void 0, function* () {
      const A = y.target;
      if (A.files)
        if (h != "blob")
          yield T(Array.from(A.files));
        else {
          if (u === "single") {
            D("load", A.files[0]);
            return;
          }
          D("load", A.files);
        }
    });
  }
  function E(y) {
    return o(this, void 0, void 0, function* () {
      var A;
      if (t(20, f = !1), !(!((A = y.dataTransfer) === null || A === void 0) && A.files)) return;
      const Y = Array.from(y.dataTransfer.files).filter(($) => {
        const oe = "." + $.name.split(".").pop();
        return oe && Vc(q, oe, $.type) || (oe && Array.isArray(r) ? r.includes(oe) : oe === r) ? !0 : (D("error", `Invalid file type only ${r} allowed.`), !1);
      });
      yield T(Y);
    });
  }
  function N(y) {
    it.call(this, l, y);
  }
  function G(y) {
    it.call(this, l, y);
  }
  function O(y) {
    it.call(this, l, y);
  }
  function ie(y) {
    it.call(this, l, y);
  }
  function fe(y) {
    it.call(this, l, y);
  }
  function z(y) {
    it.call(this, l, y);
  }
  function B(y) {
    it.call(this, l, y);
  }
  function tt(y) {
    Mc[y ? "unshift" : "push"](() => {
      w = y, t(2, w);
    });
  }
  return l.$$set = (y) => {
    "filetype" in y && t(0, r = y.filetype), "dragging" in y && t(20, f = y.dragging), "boundedheight" in y && t(3, a = y.boundedheight), "center" in y && t(4, s = y.center), "flex" in y && t(5, c = y.flex), "file_count" in y && t(6, u = y.file_count), "disable_click" in y && t(7, d = y.disable_click), "root" in y && t(8, _ = y.root), "hidden" in y && t(9, m = y.hidden), "format" in y && t(21, h = y.format), "uploading" in y && t(1, p = y.uploading), "hidden_upload" in y && t(2, w = y.hidden_upload), "show_progress" in y && t(10, g = y.show_progress), "max_file_size" in y && t(22, b = y.max_file_size), "upload" in y && t(23, S = y.upload), "stream_handler" in y && t(11, L = y.stream_handler), "$$scope" in y && t(25, i = y.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*filetype*/
    1 && (r == null ? t(16, q = null) : typeof r == "string" ? t(16, q = I(r)) : (t(0, r = r.map(I)), t(16, q = r.join(", "))));
  }, [
    r,
    p,
    w,
    a,
    s,
    c,
    u,
    d,
    _,
    m,
    g,
    L,
    U,
    le,
    C,
    M,
    q,
    V,
    X,
    E,
    f,
    h,
    b,
    S,
    T,
    i,
    n,
    N,
    G,
    O,
    ie,
    fe,
    z,
    B,
    tt
  ];
}
class Oc extends qc {
  constructor(e) {
    super(), Dc(
      this,
      e,
      Uc,
      Nc,
      jc,
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
  SvelteComponent: Gc,
  append: fn,
  attr: rl,
  create_component: Hc,
  destroy_component: Zc,
  detach: Xc,
  element: al,
  init: Yc,
  insert: Kc,
  listen: Jc,
  mount_component: Qc,
  noop: xc,
  safe_not_equal: $c,
  set_style: eu,
  space: tu,
  text: nu,
  transition_in: lu,
  transition_out: iu
} = window.__gradio__svelte__internal, { createEventDispatcher: ou } = window.__gradio__svelte__internal;
function ru(l) {
  let e, t, n, i, o, r = "Click to Access Webcam", f, a, s, c;
  return i = new eo({}), {
    c() {
      e = al("button"), t = al("div"), n = al("span"), Hc(i.$$.fragment), o = tu(), f = nu(r), rl(n, "class", "icon-wrap svelte-fjcd9c"), rl(t, "class", "wrap svelte-fjcd9c"), rl(e, "class", "svelte-fjcd9c"), eu(e, "height", "100%");
    },
    m(u, d) {
      Kc(u, e, d), fn(e, t), fn(t, n), Qc(i, n, null), fn(t, o), fn(t, f), a = !0, s || (c = Jc(
        e,
        "click",
        /*click_handler*/
        l[1]
      ), s = !0);
    },
    p: xc,
    i(u) {
      a || (lu(i.$$.fragment, u), a = !0);
    },
    o(u) {
      iu(i.$$.fragment, u), a = !1;
    },
    d(u) {
      u && Xc(e), Zc(i), s = !1, c();
    }
  };
}
function au(l) {
  const e = ou();
  return [e, () => e("click")];
}
class su extends Gc {
  constructor(e) {
    super(), Yc(this, e, au, ru, $c, {});
  }
}
function fu() {
  return navigator.mediaDevices.enumerateDevices();
}
function cu(l, e) {
  e.srcObject = l, e.muted = !0, e.play();
}
async function yi(l, e, t) {
  const n = {
    width: { ideal: 1920 },
    height: { ideal: 1440 }
  }, i = {
    video: t ? { deviceId: { exact: t }, ...n } : n,
    audio: l
  };
  return navigator.mediaDevices.getUserMedia(i).then((o) => (cu(o, e), o));
}
function uu(l) {
  return l.filter(
    (t) => t.kind === "videoinput"
  );
}
const {
  SvelteComponent: _u,
  action_destroyer: du,
  add_render_callback: mu,
  append: Ne,
  attr: x,
  binding_callbacks: hu,
  check_outros: Xt,
  create_component: Rt,
  create_in_transition: gu,
  destroy_component: At,
  destroy_each: bu,
  detach: ge,
  element: ve,
  empty: zl,
  ensure_array_like: Si,
  group_outros: Yt,
  init: pu,
  insert: be,
  listen: Sn,
  mount_component: Tt,
  noop: ql,
  run_all: wu,
  safe_not_equal: vu,
  set_data: Ro,
  set_input_value: vl,
  space: Kt,
  stop_propagation: ku,
  text: Ao,
  toggle_class: cn,
  transition_in: ne,
  transition_out: se
} = window.__gradio__svelte__internal, { createEventDispatcher: yu, onMount: Su } = window.__gradio__svelte__internal;
function Ci(l, e, t) {
  const n = l.slice();
  return n[32] = e[t], n;
}
function Cu(l) {
  let e, t, n, i, o, r, f, a, s, c, u;
  const d = [Mu, qu], _ = [];
  function m(w, g) {
    return (
      /*mode*/
      w[1] === "video" || /*streaming*/
      w[0] ? 0 : 1
    );
  }
  n = m(l), i = _[n] = d[n](l);
  let h = !/*recording*/
  l[8] && zi(l), p = (
    /*options_open*/
    l[10] && /*selected_device*/
    l[7] && qi(l)
  );
  return {
    c() {
      e = ve("div"), t = ve("button"), i.c(), r = Kt(), h && h.c(), f = Kt(), p && p.c(), a = zl(), x(t, "aria-label", o = /*mode*/
      l[1] === "image" ? "capture photo" : "start recording"), x(t, "class", "svelte-8hqvb6"), x(e, "class", "button-wrap svelte-8hqvb6");
    },
    m(w, g) {
      be(w, e, g), Ne(e, t), _[n].m(t, null), Ne(e, r), h && h.m(e, null), be(w, f, g), p && p.m(w, g), be(w, a, g), s = !0, c || (u = Sn(
        t,
        "click",
        /*record_video_or_photo*/
        l[13]
      ), c = !0);
    },
    p(w, g) {
      let b = n;
      n = m(w), n === b ? _[n].p(w, g) : (Yt(), se(_[b], 1, 1, () => {
        _[b] = null;
      }), Xt(), i = _[n], i ? i.p(w, g) : (i = _[n] = d[n](w), i.c()), ne(i, 1), i.m(t, null)), (!s || g[0] & /*mode*/
      2 && o !== (o = /*mode*/
      w[1] === "image" ? "capture photo" : "start recording")) && x(t, "aria-label", o), /*recording*/
      w[8] ? h && (Yt(), se(h, 1, 1, () => {
        h = null;
      }), Xt()) : h ? (h.p(w, g), g[0] & /*recording*/
      256 && ne(h, 1)) : (h = zi(w), h.c(), ne(h, 1), h.m(e, null)), /*options_open*/
      w[10] && /*selected_device*/
      w[7] ? p ? (p.p(w, g), g[0] & /*options_open, selected_device*/
      1152 && ne(p, 1)) : (p = qi(w), p.c(), ne(p, 1), p.m(a.parentNode, a)) : p && (Yt(), se(p, 1, 1, () => {
        p = null;
      }), Xt());
    },
    i(w) {
      s || (ne(i), ne(h), ne(p), s = !0);
    },
    o(w) {
      se(i), se(h), se(p), s = !1;
    },
    d(w) {
      w && (ge(e), ge(f), ge(a)), _[n].d(), h && h.d(), p && p.d(w), c = !1, u();
    }
  };
}
function zu(l) {
  let e, t, n, i;
  return t = new su({}), t.$on(
    "click",
    /*click_handler*/
    l[20]
  ), {
    c() {
      e = ve("div"), Rt(t.$$.fragment), x(e, "title", "grant webcam access");
    },
    m(o, r) {
      be(o, e, r), Tt(t, e, null), i = !0;
    },
    p: ql,
    i(o) {
      i || (ne(t.$$.fragment, o), o && (n || mu(() => {
        n = gu(e, uf, { delay: 100, duration: 200 }), n.start();
      })), i = !0);
    },
    o(o) {
      se(t.$$.fragment, o), i = !1;
    },
    d(o) {
      o && ge(e), At(t);
    }
  };
}
function qu(l) {
  let e, t, n;
  return t = new ra({}), {
    c() {
      e = ve("div"), Rt(t.$$.fragment), x(e, "class", "icon svelte-8hqvb6"), x(e, "title", "capture photo");
    },
    m(i, o) {
      be(i, e, o), Tt(t, e, null), n = !0;
    },
    p: ql,
    i(i) {
      n || (ne(t.$$.fragment, i), n = !0);
    },
    o(i) {
      se(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ge(e), At(t);
    }
  };
}
function Mu(l) {
  let e, t, n, i;
  const o = [Iu, Eu], r = [];
  function f(a, s) {
    return (
      /*recording*/
      a[8] ? 0 : 1
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = zl();
    },
    m(a, s) {
      r[e].m(a, s), be(a, n, s), i = !0;
    },
    p(a, s) {
      let c = e;
      e = f(a), e !== c && (Yt(), se(r[c], 1, 1, () => {
        r[c] = null;
      }), Xt(), t = r[e], t || (t = r[e] = o[e](a), t.c()), ne(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (ne(t), i = !0);
    },
    o(a) {
      se(t), i = !1;
    },
    d(a) {
      a && ge(n), r[e].d(a);
    }
  };
}
function Eu(l) {
  let e, t, n;
  return t = new ma({}), {
    c() {
      e = ve("div"), Rt(t.$$.fragment), x(e, "class", "icon red svelte-8hqvb6"), x(e, "title", "start recording");
    },
    m(i, o) {
      be(i, e, o), Tt(t, e, null), n = !0;
    },
    i(i) {
      n || (ne(t.$$.fragment, i), n = !0);
    },
    o(i) {
      se(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ge(e), At(t);
    }
  };
}
function Iu(l) {
  let e, t, n;
  return t = new bs({}), {
    c() {
      e = ve("div"), Rt(t.$$.fragment), x(e, "class", "icon red svelte-8hqvb6"), x(e, "title", "stop recording");
    },
    m(i, o) {
      be(i, e, o), Tt(t, e, null), n = !0;
    },
    i(i) {
      n || (ne(t.$$.fragment, i), n = !0);
    },
    o(i) {
      se(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ge(e), At(t);
    }
  };
}
function zi(l) {
  let e, t, n, i, o;
  return t = new Ji({}), {
    c() {
      e = ve("button"), Rt(t.$$.fragment), x(e, "class", "icon svelte-8hqvb6"), x(e, "aria-label", "select input source");
    },
    m(r, f) {
      be(r, e, f), Tt(t, e, null), n = !0, i || (o = Sn(
        e,
        "click",
        /*click_handler_1*/
        l[21]
      ), i = !0);
    },
    p: ql,
    i(r) {
      n || (ne(t.$$.fragment, r), n = !0);
    },
    o(r) {
      se(t.$$.fragment, r), n = !1;
    },
    d(r) {
      r && ge(e), At(t), i = !1, o();
    }
  };
}
function qi(l) {
  let e, t, n, i, o, r, f;
  n = new Ji({});
  function a(u, d) {
    return (
      /*available_video_devices*/
      u[6].length === 0 ? Bu : Du
    );
  }
  let s = a(l), c = s(l);
  return {
    c() {
      e = ve("select"), t = ve("button"), Rt(n.$$.fragment), i = Kt(), c.c(), x(t, "class", "inset-icon svelte-8hqvb6"), x(e, "class", "select-wrap svelte-8hqvb6"), x(e, "aria-label", "select source");
    },
    m(u, d) {
      be(u, e, d), Ne(e, t), Tt(n, t, null), Ne(t, i), c.m(e, null), o = !0, r || (f = [
        Sn(t, "click", ku(
          /*click_handler_2*/
          l[22]
        )),
        du(Ml.call(
          null,
          e,
          /*handle_click_outside*/
          l[14]
        )),
        Sn(
          e,
          "change",
          /*handle_device_change*/
          l[11]
        )
      ], r = !0);
    },
    p(u, d) {
      s === (s = a(u)) && c ? c.p(u, d) : (c.d(1), c = s(u), c && (c.c(), c.m(e, null)));
    },
    i(u) {
      o || (ne(n.$$.fragment, u), o = !0);
    },
    o(u) {
      se(n.$$.fragment, u), o = !1;
    },
    d(u) {
      u && ge(e), At(n), c.d(), r = !1, wu(f);
    }
  };
}
function Du(l) {
  let e, t = Si(
    /*available_video_devices*/
    l[6]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Mi(Ci(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = zl();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      be(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*available_video_devices, selected_device*/
      192) {
        t = Si(
          /*available_video_devices*/
          i[6]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Ci(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = Mi(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && ge(e), bu(n, i);
    }
  };
}
function Bu(l) {
  let e, t = (
    /*i18n*/
    l[3]("common.no_devices") + ""
  ), n;
  return {
    c() {
      e = ve("option"), n = Ao(t), e.__value = "", vl(e, e.__value), x(e, "class", "svelte-8hqvb6");
    },
    m(i, o) {
      be(i, e, o), Ne(e, n);
    },
    p(i, o) {
      o[0] & /*i18n*/
      8 && t !== (t = /*i18n*/
      i[3]("common.no_devices") + "") && Ro(n, t);
    },
    d(i) {
      i && ge(e);
    }
  };
}
function Mi(l) {
  let e, t = (
    /*device*/
    l[32].label + ""
  ), n, i, o, r;
  return {
    c() {
      e = ve("option"), n = Ao(t), i = Kt(), e.__value = o = /*device*/
      l[32].deviceId, vl(e, e.__value), e.selected = r = /*selected_device*/
      l[7].deviceId === /*device*/
      l[32].deviceId, x(e, "class", "svelte-8hqvb6");
    },
    m(f, a) {
      be(f, e, a), Ne(e, n), Ne(e, i);
    },
    p(f, a) {
      a[0] & /*available_video_devices*/
      64 && t !== (t = /*device*/
      f[32].label + "") && Ro(n, t), a[0] & /*available_video_devices*/
      64 && o !== (o = /*device*/
      f[32].deviceId) && (e.__value = o, vl(e, e.__value)), a[0] & /*selected_device, available_video_devices*/
      192 && r !== (r = /*selected_device*/
      f[7].deviceId === /*device*/
      f[32].deviceId) && (e.selected = r);
    },
    d(f) {
      f && ge(e);
    }
  };
}
function Lu(l) {
  let e, t, n, i, o, r;
  const f = [zu, Cu], a = [];
  function s(c, u) {
    return (
      /*webcam_accessed*/
      c[9] ? 1 : 0
    );
  }
  return i = s(l), o = a[i] = f[i](l), {
    c() {
      e = ve("div"), t = ve("video"), n = Kt(), o.c(), x(t, "class", "svelte-8hqvb6"), cn(
        t,
        "flip",
        /*mirror_webcam*/
        l[2]
      ), cn(t, "hide", !/*webcam_accessed*/
      l[9]), x(e, "class", "wrap svelte-8hqvb6");
    },
    m(c, u) {
      be(c, e, u), Ne(e, t), l[19](t), Ne(e, n), a[i].m(e, null), r = !0;
    },
    p(c, u) {
      (!r || u[0] & /*mirror_webcam*/
      4) && cn(
        t,
        "flip",
        /*mirror_webcam*/
        c[2]
      ), (!r || u[0] & /*webcam_accessed*/
      512) && cn(t, "hide", !/*webcam_accessed*/
      c[9]);
      let d = i;
      i = s(c), i === d ? a[i].p(c, u) : (Yt(), se(a[d], 1, 1, () => {
        a[d] = null;
      }), Xt(), o = a[i], o ? o.p(c, u) : (o = a[i] = f[i](c), o.c()), ne(o, 1), o.m(e, null));
    },
    i(c) {
      r || (ne(o), r = !0);
    },
    o(c) {
      se(o), r = !1;
    },
    d(c) {
      c && ge(e), l[19](null), a[i].d();
    }
  };
}
function Ml(l, e) {
  const t = (n) => {
    l && !l.contains(n.target) && !n.defaultPrevented && e(n);
  };
  return document.addEventListener("click", t, !0), {
    destroy() {
      document.removeEventListener("click", t, !0);
    }
  };
}
function ju(l, e, t) {
  var n = this && this.__awaiter || function(E, N, G, O) {
    function ie(fe) {
      return fe instanceof G ? fe : new G(function(z) {
        z(fe);
      });
    }
    return new (G || (G = Promise))(function(fe, z) {
      function B(A) {
        try {
          y(O.next(A));
        } catch (Y) {
          z(Y);
        }
      }
      function tt(A) {
        try {
          y(O.throw(A));
        } catch (Y) {
          z(Y);
        }
      }
      function y(A) {
        A.done ? fe(A.value) : ie(A.value).then(B, tt);
      }
      y((O = O.apply(E, N || [])).next());
    });
  };
  let i, o = [], r = null, f, { streaming: a = !1 } = e, { pending: s = !1 } = e, { root: c = "" } = e, { mode: u = "image" } = e, { mirror_webcam: d } = e, { include_audio: _ } = e, { i18n: m } = e, { upload: h } = e;
  const p = yu();
  Su(() => f = document.createElement("canvas"));
  const w = (E) => n(void 0, void 0, void 0, function* () {
    const G = E.target.value;
    yield yi(_, i, G).then((O) => n(void 0, void 0, void 0, function* () {
      C = O, t(7, r = o.find((ie) => ie.deviceId === G) || null), t(10, V = !1);
    }));
  });
  function g() {
    return n(this, void 0, void 0, function* () {
      try {
        yi(_, i).then((E) => n(this, void 0, void 0, function* () {
          t(9, v = !0), t(6, o = yield fu()), C = E;
        })).then(() => uu(o)).then((E) => {
          t(6, o = E);
          const N = C.getTracks().map((G) => {
            var O;
            return (O = G.getSettings()) === null || O === void 0 ? void 0 : O.deviceId;
          })[0];
          t(7, r = N && E.find((G) => G.deviceId === N) || o[0]);
        }), (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) && p("error", m("image.no_webcam_support"));
      } catch (E) {
        if (E instanceof DOMException && E.name == "NotAllowedError")
          p("error", m("image.allow_webcam_access"));
        else
          throw E;
      }
    });
  }
  function b() {
    var E = f.getContext("2d");
    (!a || a && S) && i.videoWidth && i.videoHeight && (f.width = i.videoWidth, f.height = i.videoHeight, E.drawImage(i, 0, 0, i.videoWidth, i.videoHeight), d && (E.scale(-1, 1), E.drawImage(i, -i.videoWidth, 0)), f.toBlob(
      (N) => {
        p(a ? "stream" : "capture", N);
      },
      "image/png",
      0.8
    ));
  }
  let S = !1, L = [], C, M, q;
  function D() {
    if (S) {
      q.stop();
      let E = new Blob(L, { type: M }), N = new FileReader();
      N.onload = function(G) {
        return n(this, void 0, void 0, function* () {
          var O;
          if (G.target) {
            let ie = new File([E], "sample." + M.substring(6));
            const fe = yield Co([ie]);
            let z = ((O = yield h(fe, c)) === null || O === void 0 ? void 0 : O.filter(Boolean))[0];
            p("capture", z), p("stop_recording");
          }
        });
      }, N.readAsDataURL(E);
    } else {
      p("start_recording"), L = [];
      let E = ["video/webm", "video/mp4"];
      for (let N of E)
        if (MediaRecorder.isTypeSupported(N)) {
          M = N;
          break;
        }
      if (M === null) {
        console.error("No supported MediaRecorder mimeType");
        return;
      }
      q = new MediaRecorder(C, { mimeType: M }), q.addEventListener("dataavailable", function(N) {
        L.push(N.data);
      }), q.start(200);
    }
    t(8, S = !S);
  }
  let v = !1;
  function I() {
    u === "image" && a && t(8, S = !S), u === "image" ? b() : D(), !S && C && (C.getTracks().forEach((E) => E.stop()), t(5, i.srcObject = null, i), t(9, v = !1));
  }
  a && u === "image" && window.setInterval(
    () => {
      i && !s && b();
    },
    500
  );
  let V = !1;
  function U(E) {
    E.preventDefault(), E.stopPropagation(), t(10, V = !1);
  }
  function le(E) {
    hu[E ? "unshift" : "push"](() => {
      i = E, t(5, i);
    });
  }
  const j = async () => g(), T = () => t(10, V = !0), X = () => t(10, V = !1);
  return l.$$set = (E) => {
    "streaming" in E && t(0, a = E.streaming), "pending" in E && t(15, s = E.pending), "root" in E && t(16, c = E.root), "mode" in E && t(1, u = E.mode), "mirror_webcam" in E && t(2, d = E.mirror_webcam), "include_audio" in E && t(17, _ = E.include_audio), "i18n" in E && t(3, m = E.i18n), "upload" in E && t(18, h = E.upload);
  }, [
    a,
    u,
    d,
    m,
    Ml,
    i,
    o,
    r,
    S,
    v,
    V,
    w,
    g,
    I,
    U,
    s,
    c,
    _,
    h,
    le,
    j,
    T,
    X
  ];
}
class Fu extends _u {
  constructor(e) {
    super(), pu(
      this,
      e,
      ju,
      Lu,
      vu,
      {
        streaming: 0,
        pending: 15,
        root: 16,
        mode: 1,
        mirror_webcam: 2,
        include_audio: 17,
        i18n: 3,
        upload: 18,
        click_outside: 4
      },
      null,
      [-1, -1]
    );
  }
  get click_outside() {
    return Ml;
  }
}
const {
  SvelteComponent: Ru,
  append: Au,
  attr: Ei,
  binding_callbacks: Tu,
  detach: Wu,
  element: Ii,
  init: Pu,
  insert: Nu,
  listen: Vu,
  noop: Di,
  safe_not_equal: Uu,
  set_style: un
} = window.__gradio__svelte__internal, { onMount: Ou, createEventDispatcher: Gu } = window.__gradio__svelte__internal;
function Hu(l) {
  let e, t, n, i;
  return {
    c() {
      e = Ii("div"), t = Ii("canvas"), un(
        t,
        "height",
        /*height*/
        l[0]
      ), un(
        t,
        "width",
        /*width*/
        l[1]
      ), Ei(t, "class", "patch-selector-canvas svelte-1gjvtyt"), Ei(e, "class", "patch-selector-container svelte-1gjvtyt");
    },
    m(o, r) {
      Nu(o, e, r), Au(e, t), l[12](t), n || (i = Vu(
        t,
        "click",
        /*handleClick*/
        l[3]
      ), n = !0);
    },
    p(o, [r]) {
      r & /*height*/
      1 && un(
        t,
        "height",
        /*height*/
        o[0]
      ), r & /*width*/
      2 && un(
        t,
        "width",
        /*width*/
        o[1]
      );
    },
    i: Di,
    o: Di,
    d(o) {
      o && Wu(e), l[12](null), n = !1, i();
    }
  };
}
function Zu(l, e, t) {
  let { value: n } = e, { src: i = null } = e, { interactive: o = !0 } = e, { height: r = "100%" } = e, { width: f = "100%" } = e, { imgSize: a = null } = e, { patchSize: s = 16 } = e, { showGrid: c = !0 } = e, { gridColor: u = "rgba(200, 200, 200, 0.5)" } = e, d, _, m = null, h = 0, p = 0, w = 0, g = 0, b = 1, S = 0, L = 0, C = 1, M = 1;
  const q = Gu();
  function D() {
    if (!_ || !m || !c) return;
    _.save(), _.strokeStyle = u, _.lineWidth = 1;
    const j = Math.floor(S / s), T = Math.floor(L / s);
    console.log(`[PatchSelector.svelte:drawGrid] patch size: ${s}`);
    for (let X = 0; X <= T; X++) {
      const E = g + X * s * M;
      _.beginPath(), _.moveTo(w, E), _.lineTo(w + h, E), _.stroke();
    }
    for (let X = 0; X <= j; X++) {
      const E = w + X * s * C;
      _.beginPath(), _.moveTo(E, g), _.lineTo(E, g + p), _.stroke();
    }
    _.restore();
  }
  function v() {
    d && (console.debug("[PatchSelector.svelte:handleImageLoad] Image loaded"), _ = d.getContext("2d"), b = 1, t(2, d.width = d.clientWidth, d), m !== null ? (S = a || m.width, L = a || m.height, a && (S = a, L = a), S > d.width ? (b = d.width / S, h = S * b, p = L * b, w = 0, g = 0) : (h = S, p = L, w = (d.width - h) / 2, g = 0), t(2, d.height = p, d), C = h / S, M = p / L) : t(2, d.height = d.clientHeight, d), I());
  }
  function I() {
    _ && (console.debug("Drawing on canvas"), _.clearRect(0, 0, d.width, d.height), m !== null && (console.debug("[PatchSelector.svelte:draw] Drawing image"), console.debug(`[PatchSelector.svelte:draw] image dimensions: ${m.width}x${m.height}:${a}`), console.debug(`[PatchSelector.svelte:draw] image sizes: ${h}x${p}:${a}`), console.debug(`[PatchSelector.svelte:draw] effective image sizes: ${S}x${L}:${a}`), _.drawImage(m, w, g, h, p), console.debug("Drawing grid"), D()));
  }
  function V(j) {
    if (!o || !m) return;
    const T = d.getBoundingClientRect(), X = j.clientX - T.left, E = j.clientY - T.top, N = Math.floor((X - w) / (s * C)), G = Math.floor((E - g) / (s * M)), O = Math.floor(S / s), ie = G * O + N;
    N >= 0 && N < O && G >= 0 && G < Math.floor(L / s) && (U(N, G), console.debug("[PatchSelector.svelte:handleClick] Patch index:", ie), t(4, n.patchIndex = ie, n), q("patch_select", { patchIndex: ie }));
  }
  function U(j, T) {
    !_ || !m || (I(), _.save(), _.fillStyle = "rgba(255, 255, 0, 0.2)", _.fillRect(w + j * s * C, g + T * s * M, s * C, s * M), _.restore());
  }
  Ou(() => {
    m && m.complete && v();
  });
  function le(j) {
    Tu[j ? "unshift" : "push"](() => {
      d = j, t(2, d);
    });
  }
  return l.$$set = (j) => {
    "value" in j && t(4, n = j.value), "src" in j && t(7, i = j.src), "interactive" in j && t(8, o = j.interactive), "height" in j && t(0, r = j.height), "width" in j && t(1, f = j.width), "imgSize" in j && t(5, a = j.imgSize), "patchSize" in j && t(6, s = j.patchSize), "showGrid" in j && t(9, c = j.showGrid), "gridColor" in j && t(10, u = j.gridColor);
  }, l.$$.update = () => {
    l.$$.dirty & /*value, imgSize*/
    48 && (n == null ? void 0 : n.imgSize) !== void 0 && n.imgSize !== null && (console.log(`[PatchSelector.svelte] Changing patch size: ${a} -> ${n.imgSize}`), t(5, a = n.imgSize)), l.$$.dirty & /*value, patchSize*/
    80 && (n == null ? void 0 : n.patchSize) !== void 0 && n.patchSize !== null && (console.log(`[PatchSelector.svelte] Changing patch size: ${s} -> ${n.patchSize}`), t(6, s = n.patchSize)), l.$$.dirty & /*src*/
    128 && i && (t(11, m = new Image()), t(11, m.src = i, m), t(11, m.onload = v, m)), l.$$.dirty & /*image, patchSize, imgSize*/
    2144 && m && (s || a) && (console.log(`[PatchSelector.svelte] Redrawing canvas with new patch size: ${s}`), v());
  }, [
    r,
    f,
    d,
    V,
    n,
    a,
    s,
    i,
    o,
    c,
    u,
    m,
    le
  ];
}
class Xu extends Ru {
  constructor(e) {
    super(), Pu(this, e, Zu, Hu, Uu, {
      value: 4,
      src: 7,
      interactive: 8,
      height: 0,
      width: 1,
      imgSize: 5,
      patchSize: 6,
      showGrid: 9,
      gridColor: 10
    });
  }
}
class Bi {
  constructor() {
    this.patchIndex = null, this.imgSize = null, this.patchSize = null;
  }
}
const {
  SvelteComponent: Yu,
  add_flush_callback: Cn,
  append: st,
  attr: It,
  bind: zn,
  binding_callbacks: Jt,
  bubble: Ut,
  check_outros: ft,
  create_component: Ve,
  create_slot: Ku,
  destroy_component: Ue,
  detach: ht,
  element: Bt,
  empty: Ju,
  get_all_dirty_from_scope: Qu,
  get_slot_changes: xu,
  group_outros: ct,
  init: $u,
  insert: gt,
  mount_component: Oe,
  noop: e_,
  safe_not_equal: t_,
  space: at,
  transition_in: P,
  transition_out: Z,
  update_slot_base: n_
} = window.__gradio__svelte__internal, { createEventDispatcher: l_, tick: i_ } = window.__gradio__svelte__internal;
function Li(l) {
  let e, t;
  return e = new cc({
    props: {
      href: (
        /*value*/
        l[1].image.url
      ),
      download: (
        /*value*/
        l[1].image.orig_name || "image"
      ),
      $$slots: { default: [o_] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Oe(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*value*/
      2 && (o.href = /*value*/
      n[1].image.url), i[0] & /*value*/
      2 && (o.download = /*value*/
      n[1].image.orig_name || "image"), i[0] & /*i18n*/
      128 | i[1] & /*$$scope*/
      65536 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (P(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ue(e, n);
    }
  };
}
function o_(l) {
  let e, t;
  return e = new qn({
    props: {
      Icon: Aa,
      label: (
        /*i18n*/
        l[7]("common.download")
      )
    }
  }), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Oe(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*i18n*/
      128 && (o.label = /*i18n*/
      n[7]("common.download")), e.$set(o);
    },
    i(n) {
      t || (P(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ue(e, n);
    }
  };
}
function ji(l) {
  let e, t;
  return e = new Gs({
    props: {
      i18n: (
        /*i18n*/
        l[7]
      ),
      formatter: (
        /*func*/
        l[31]
      ),
      value: (
        /*value*/
        l[1]
      )
    }
  }), e.$on(
    "share",
    /*share_handler*/
    l[32]
  ), e.$on(
    "error",
    /*error_handler*/
    l[33]
  ), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Oe(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*i18n*/
      128 && (o.i18n = /*i18n*/
      n[7]), i[0] & /*value*/
      2 && (o.value = /*value*/
      n[1]), e.$set(o);
    },
    i(n) {
      t || (P(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ue(e, n);
    }
  };
}
function Fi(l) {
  let e, t, n;
  return t = new qn({
    props: { Icon: Ki, label: "Remove Image" }
  }), t.$on(
    "click",
    /*clear*/
    l[27]
  ), {
    c() {
      e = Bt("div"), Ve(t.$$.fragment);
    },
    m(i, o) {
      gt(i, e, o), Oe(t, e, null), n = !0;
    },
    p: e_,
    i(i) {
      n || (P(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Z(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ht(e), Ue(t);
    }
  };
}
function Ri(l) {
  let e;
  const t = (
    /*#slots*/
    l[30].default
  ), n = Ku(
    t,
    l,
    /*$$scope*/
    l[47],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o[1] & /*$$scope*/
      65536) && n_(
        n,
        t,
        i,
        /*$$scope*/
        i[47],
        e ? xu(
          t,
          /*$$scope*/
          i[47],
          o,
          null
        ) : Qu(
          /*$$scope*/
          i[47]
        ),
        null
      );
    },
    i(i) {
      e || (P(n, i), e = !0);
    },
    o(i) {
      Z(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function r_(l) {
  let e, t, n = (
    /*value*/
    l[1] === null && Ri(l)
  );
  return {
    c() {
      n && n.c(), e = Ju();
    },
    m(i, o) {
      n && n.m(i, o), gt(i, e, o), t = !0;
    },
    p(i, o) {
      /*value*/
      i[1] === null ? n ? (n.p(i, o), o[0] & /*value*/
      2 && P(n, 1)) : (n = Ri(i), n.c(), P(n, 1), n.m(e.parentNode, e)) : n && (ct(), Z(n, 1, 1, () => {
        n = null;
      }), ft());
    },
    i(i) {
      t || (P(n), t = !0);
    },
    o(i) {
      Z(n), t = !1;
    },
    d(i) {
      i && ht(e), n && n.d(i);
    }
  };
}
function Ai(l) {
  let e, t;
  return e = new Fu({
    props: {
      root: (
        /*root*/
        l[5]
      ),
      mode: "image",
      include_audio: !1,
      i18n: (
        /*i18n*/
        l[7]
      ),
      upload: (
        /*upload*/
        l[20]
      )
    }
  }), e.$on(
    "capture",
    /*capture_handler*/
    l[38]
  ), e.$on(
    "stream",
    /*stream_handler_1*/
    l[39]
  ), e.$on(
    "error",
    /*error_handler_2*/
    l[40]
  ), e.$on(
    "drag",
    /*drag_handler*/
    l[41]
  ), e.$on(
    "upload",
    /*upload_handler*/
    l[42]
  ), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Oe(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*root*/
      32 && (o.root = /*root*/
      n[5]), i[0] & /*i18n*/
      128 && (o.i18n = /*i18n*/
      n[7]), i[0] & /*upload*/
      1048576 && (o.upload = /*upload*/
      n[20]), e.$set(o);
    },
    i(n) {
      t || (P(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ue(e, n);
    }
  };
}
function Ti(l) {
  let e, t, n, i, o;
  function r(a) {
    l[43](a);
  }
  let f = {
    src: (
      /*value*/
      l[1].image.url
    ),
    interactive: (
      /*interactive*/
      l[6]
    ),
    height: (
      /*effectiveHeight*/
      l[22]
    ),
    width: (
      /*effectiveWidth*/
      l[21]
    ),
    imgSize: (
      /*imgSize*/
      l[11]
    ),
    patchSize: (
      /*patchSize*/
      l[15]
    ),
    showGrid: (
      /*showGrid*/
      l[16]
    ),
    gridColor: (
      /*gridColor*/
      l[17]
    )
  };
  return (
    /*value*/
    l[1] !== void 0 && (f.value = /*value*/
    l[1]), n = new Xu({ props: f }), Jt.push(() => zn(n, "value", r)), n.$on(
      "change",
      /*change_handler*/
      l[44]
    ), n.$on(
      "patch_select",
      /*patch_select_handler*/
      l[45]
    ), {
      c() {
        e = Bt("div"), t = Bt("div"), Ve(n.$$.fragment), It(t, "class", "patch-selector-container"), It(e, "class", "image-frame svelte-16nj8qp");
      },
      m(a, s) {
        gt(a, e, s), st(e, t), Oe(n, t, null), o = !0;
      },
      p(a, s) {
        const c = {};
        s[0] & /*value*/
        2 && (c.src = /*value*/
        a[1].image.url), s[0] & /*interactive*/
        64 && (c.interactive = /*interactive*/
        a[6]), s[0] & /*effectiveHeight*/
        4194304 && (c.height = /*effectiveHeight*/
        a[22]), s[0] & /*effectiveWidth*/
        2097152 && (c.width = /*effectiveWidth*/
        a[21]), s[0] & /*imgSize*/
        2048 && (c.imgSize = /*imgSize*/
        a[11]), s[0] & /*patchSize*/
        32768 && (c.patchSize = /*patchSize*/
        a[15]), s[0] & /*showGrid*/
        65536 && (c.showGrid = /*showGrid*/
        a[16]), s[0] & /*gridColor*/
        131072 && (c.gridColor = /*gridColor*/
        a[17]), !i && s[0] & /*value*/
        2 && (i = !0, c.value = /*value*/
        a[1], Cn(() => i = !1)), n.$set(c);
      },
      i(a) {
        o || (P(n.$$.fragment, a), o = !0);
      },
      o(a) {
        Z(n.$$.fragment, a), o = !1;
      },
      d(a) {
        a && ht(e), Ue(n);
      }
    }
  );
}
function Wi(l) {
  let e, t, n;
  function i(r) {
    l[46](r);
  }
  let o = {
    sources: (
      /*sources*/
      l[4]
    ),
    handle_clear: (
      /*clear*/
      l[27]
    ),
    handle_select: (
      /*handle_select_source*/
      l[26]
    )
  };
  return (
    /*active_source*/
    l[0] !== void 0 && (o.active_source = /*active_source*/
    l[0]), e = new af({ props: o }), Jt.push(() => zn(e, "active_source", i)), {
      c() {
        Ve(e.$$.fragment);
      },
      m(r, f) {
        Oe(e, r, f), n = !0;
      },
      p(r, f) {
        const a = {};
        f[0] & /*sources*/
        16 && (a.sources = /*sources*/
        r[4]), !t && f[0] & /*active_source*/
        1 && (t = !0, a.active_source = /*active_source*/
        r[0], Cn(() => t = !1)), e.$set(a);
      },
      i(r) {
        n || (P(e.$$.fragment, r), n = !0);
      },
      o(r) {
        Z(e.$$.fragment, r), n = !1;
      },
      d(r) {
        Ue(e, r);
      }
    }
  );
}
function a_(l) {
  let e, t, n, i, o, r, f, a, s, c, u, d, _, m, h = (
    /*sources*/
    (l[4].length > 1 || /*sources*/
    l[4].includes("clipboard")) && /*value*/
    l[1] === null && /*interactive*/
    l[6]
  ), p;
  e = new yr({
    props: {
      show_label: (
        /*show_label*/
        l[3]
      ),
      Icon: Qi,
      label: (
        /*label*/
        l[2] || "Image Annotator"
      )
    }
  });
  let w = (
    /*showDownloadButton*/
    l[9] && /*value*/
    l[1] !== null && Li(l)
  ), g = (
    /*showShareButton*/
    l[8] && /*value*/
    l[1] !== null && ji(l)
  ), b = (
    /*showClearButton*/
    l[10] && /*value*/
    l[1] !== null && /*interactive*/
    l[6] && Fi(l)
  );
  function S(v) {
    l[35](v);
  }
  function L(v) {
    l[36](v);
  }
  let C = {
    hidden: (
      /*value*/
      l[1] !== null || /*active_source*/
      l[0] === "webcam"
    ),
    filetype: (
      /*active_source*/
      l[0] === "clipboard" ? "clipboard" : "image/*"
    ),
    root: (
      /*root*/
      l[5]
    ),
    max_file_size: (
      /*max_file_size*/
      l[12]
    ),
    disable_click: !/*sources*/
    l[4].includes("upload"),
    upload: (
      /*cli_upload*/
      l[13]
    ),
    stream_handler: (
      /*stream_handler*/
      l[14]
    ),
    $$slots: { default: [r_] },
    $$scope: { ctx: l }
  };
  /*uploading*/
  l[18] !== void 0 && (C.uploading = /*uploading*/
  l[18]), /*dragging*/
  l[19] !== void 0 && (C.dragging = /*dragging*/
  l[19]), s = new Oc({ props: C }), l[34](s), Jt.push(() => zn(s, "uploading", S)), Jt.push(() => zn(s, "dragging", L)), s.$on(
    "load",
    /*handle_upload*/
    l[23]
  ), s.$on(
    "error",
    /*error_handler_1*/
    l[37]
  );
  let M = (
    /*value*/
    l[1] === null && /*active_source*/
    l[0] === "webcam" && Ai(l)
  ), q = (
    /*value*/
    l[1] !== null && Ti(l)
  ), D = h && Wi(l);
  return {
    c() {
      Ve(e.$$.fragment), t = at(), n = Bt("div"), w && w.c(), i = at(), g && g.c(), o = at(), b && b.c(), r = at(), f = Bt("div"), a = Bt("div"), Ve(s.$$.fragment), d = at(), M && M.c(), _ = at(), q && q.c(), m = at(), D && D.c(), It(n, "class", "icon-buttons svelte-16nj8qp"), It(a, "class", "upload-container svelte-16nj8qp"), It(f, "data-testid", "image"), It(f, "class", "image-container svelte-16nj8qp");
    },
    m(v, I) {
      Oe(e, v, I), gt(v, t, I), gt(v, n, I), w && w.m(n, null), st(n, i), g && g.m(n, null), st(n, o), b && b.m(n, null), gt(v, r, I), gt(v, f, I), st(f, a), Oe(s, a, null), st(a, d), M && M.m(a, null), st(a, _), q && q.m(a, null), st(f, m), D && D.m(f, null), p = !0;
    },
    p(v, I) {
      const V = {};
      I[0] & /*show_label*/
      8 && (V.show_label = /*show_label*/
      v[3]), I[0] & /*label*/
      4 && (V.label = /*label*/
      v[2] || "Image Annotator"), e.$set(V), /*showDownloadButton*/
      v[9] && /*value*/
      v[1] !== null ? w ? (w.p(v, I), I[0] & /*showDownloadButton, value*/
      514 && P(w, 1)) : (w = Li(v), w.c(), P(w, 1), w.m(n, i)) : w && (ct(), Z(w, 1, 1, () => {
        w = null;
      }), ft()), /*showShareButton*/
      v[8] && /*value*/
      v[1] !== null ? g ? (g.p(v, I), I[0] & /*showShareButton, value*/
      258 && P(g, 1)) : (g = ji(v), g.c(), P(g, 1), g.m(n, o)) : g && (ct(), Z(g, 1, 1, () => {
        g = null;
      }), ft()), /*showClearButton*/
      v[10] && /*value*/
      v[1] !== null && /*interactive*/
      v[6] ? b ? (b.p(v, I), I[0] & /*showClearButton, value, interactive*/
      1090 && P(b, 1)) : (b = Fi(v), b.c(), P(b, 1), b.m(n, null)) : b && (ct(), Z(b, 1, 1, () => {
        b = null;
      }), ft());
      const U = {};
      I[0] & /*value, active_source*/
      3 && (U.hidden = /*value*/
      v[1] !== null || /*active_source*/
      v[0] === "webcam"), I[0] & /*active_source*/
      1 && (U.filetype = /*active_source*/
      v[0] === "clipboard" ? "clipboard" : "image/*"), I[0] & /*root*/
      32 && (U.root = /*root*/
      v[5]), I[0] & /*max_file_size*/
      4096 && (U.max_file_size = /*max_file_size*/
      v[12]), I[0] & /*sources*/
      16 && (U.disable_click = !/*sources*/
      v[4].includes("upload")), I[0] & /*cli_upload*/
      8192 && (U.upload = /*cli_upload*/
      v[13]), I[0] & /*stream_handler*/
      16384 && (U.stream_handler = /*stream_handler*/
      v[14]), I[0] & /*value*/
      2 | I[1] & /*$$scope*/
      65536 && (U.$$scope = { dirty: I, ctx: v }), !c && I[0] & /*uploading*/
      262144 && (c = !0, U.uploading = /*uploading*/
      v[18], Cn(() => c = !1)), !u && I[0] & /*dragging*/
      524288 && (u = !0, U.dragging = /*dragging*/
      v[19], Cn(() => u = !1)), s.$set(U), /*value*/
      v[1] === null && /*active_source*/
      v[0] === "webcam" ? M ? (M.p(v, I), I[0] & /*value, active_source*/
      3 && P(M, 1)) : (M = Ai(v), M.c(), P(M, 1), M.m(a, _)) : M && (ct(), Z(M, 1, 1, () => {
        M = null;
      }), ft()), /*value*/
      v[1] !== null ? q ? (q.p(v, I), I[0] & /*value*/
      2 && P(q, 1)) : (q = Ti(v), q.c(), P(q, 1), q.m(a, null)) : q && (ct(), Z(q, 1, 1, () => {
        q = null;
      }), ft()), I[0] & /*sources, value, interactive*/
      82 && (h = /*sources*/
      (v[4].length > 1 || /*sources*/
      v[4].includes("clipboard")) && /*value*/
      v[1] === null && /*interactive*/
      v[6]), h ? D ? (D.p(v, I), I[0] & /*sources, value, interactive*/
      82 && P(D, 1)) : (D = Wi(v), D.c(), P(D, 1), D.m(f, null)) : D && (ct(), Z(D, 1, 1, () => {
        D = null;
      }), ft());
    },
    i(v) {
      p || (P(e.$$.fragment, v), P(w), P(g), P(b), P(s.$$.fragment, v), P(M), P(q), P(D), p = !0);
    },
    o(v) {
      Z(e.$$.fragment, v), Z(w), Z(g), Z(b), Z(s.$$.fragment, v), Z(M), Z(q), Z(D), p = !1;
    },
    d(v) {
      v && (ht(t), ht(n), ht(r), ht(f)), Ue(e, v), w && w.d(), g && g.d(), b && b.d(), l[34](null), Ue(s), M && M.d(), q && q.d(), D && D.d();
    }
  };
}
function s_(l, e, t) {
  let n, i, { $$slots: o = {}, $$scope: r } = e;
  var f = this && this.__awaiter || function(k, ce, ze, xt) {
    function Uo(Wt) {
      return Wt instanceof ze ? Wt : new ze(function($t) {
        $t(Wt);
      });
    }
    return new (ze || (ze = Promise))(function(Wt, $t) {
      function Oo(lt) {
        try {
          Rn(xt.next(lt));
        } catch (An) {
          $t(An);
        }
      }
      function Go(lt) {
        try {
          Rn(xt.throw(lt));
        } catch (An) {
          $t(An);
        }
      }
      function Rn(lt) {
        lt.done ? Wt(lt.value) : Uo(lt.value).then(Oo, Go);
      }
      Rn((xt = xt.apply(k, ce || [])).next());
    });
  };
  let { value: a } = e, { label: s = void 0 } = e, { show_label: c } = e, { sources: u = ["upload", "webcam", "clipboard"] } = e, { root: d } = e, { interactive: _ } = e, { i18n: m } = e, { showShareButton: h } = e, { showDownloadButton: p } = e, { showClearButton: w } = e, { height: g } = e, { width: b } = e, { imgSize: S = null } = e, { max_file_size: L = null } = e, { cli_upload: C } = e, { stream_handler: M } = e, { patchSize: q = 16 } = e, { showGrid: D = !0 } = e, { gridColor: v = "rgba(200, 200, 200, 0.5)" } = e, I, V = !1, { active_source: U = null } = e;
  function le({ detail: k }) {
    t(1, a = new Bi()), t(1, a.image = k, a), T("upload");
  }
  function j(k) {
    return f(this, void 0, void 0, function* () {
      const ce = yield I.load_files([new File([k], "webcam.png")]), ze = (ce == null ? void 0 : ce[0]) || null;
      ze ? (t(1, a = new Bi()), t(1, a.image = ze, a)) : t(1, a = null), yield i_(), T("change");
    });
  }
  const T = l_();
  let X = !1;
  function E(k) {
    return f(this, void 0, void 0, function* () {
      switch (k) {
        case "clipboard":
          I.paste_clipboard();
          break;
      }
    });
  }
  function N() {
    t(1, a = null), T("clear"), T("change");
  }
  const G = async (k) => k === null ? "" : `<img src="${await Bs(k.image)}" />`;
  function O(k) {
    Ut.call(this, l, k);
  }
  function ie(k) {
    Ut.call(this, l, k);
  }
  function fe(k) {
    Jt[k ? "unshift" : "push"](() => {
      I = k, t(20, I);
    });
  }
  function z(k) {
    V = k, t(18, V);
  }
  function B(k) {
    X = k, t(19, X);
  }
  function tt(k) {
    Ut.call(this, l, k);
  }
  const y = (k) => j(k.detail), A = (k) => j(k.detail);
  function Y(k) {
    Ut.call(this, l, k);
  }
  function $(k) {
    Ut.call(this, l, k);
  }
  const oe = (k) => j(k.detail);
  function Te(k) {
    a = k, t(1, a);
  }
  const Ze = (k) => {
    T("change");
  }, nt = (k) => {
    T("patch_select", k.detail);
  };
  function Ce(k) {
    U = k, t(0, U), t(4, u);
  }
  return l.$$set = (k) => {
    "value" in k && t(1, a = k.value), "label" in k && t(2, s = k.label), "show_label" in k && t(3, c = k.show_label), "sources" in k && t(4, u = k.sources), "root" in k && t(5, d = k.root), "interactive" in k && t(6, _ = k.interactive), "i18n" in k && t(7, m = k.i18n), "showShareButton" in k && t(8, h = k.showShareButton), "showDownloadButton" in k && t(9, p = k.showDownloadButton), "showClearButton" in k && t(10, w = k.showClearButton), "height" in k && t(28, g = k.height), "width" in k && t(29, b = k.width), "imgSize" in k && t(11, S = k.imgSize), "max_file_size" in k && t(12, L = k.max_file_size), "cli_upload" in k && t(13, C = k.cli_upload), "stream_handler" in k && t(14, M = k.stream_handler), "patchSize" in k && t(15, q = k.patchSize), "showGrid" in k && t(16, D = k.showGrid), "gridColor" in k && t(17, v = k.gridColor), "active_source" in k && t(0, U = k.active_source), "$$scope" in k && t(47, r = k.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*uploading*/
    262144 && V && N(), l.$$.dirty[0] & /*dragging*/
    524288 && T("drag", X), l.$$.dirty[0] & /*active_source, sources*/
    17 && !U && u && t(0, U = u[0]), l.$$.dirty[0] & /*imgSize, height*/
    268437504 && t(22, n = S !== null ? S : g), l.$$.dirty[0] & /*imgSize, width*/
    536872960 && t(21, i = S !== null ? S : b);
  }, [
    U,
    a,
    s,
    c,
    u,
    d,
    _,
    m,
    h,
    p,
    w,
    S,
    L,
    C,
    M,
    q,
    D,
    v,
    V,
    X,
    I,
    i,
    n,
    le,
    j,
    T,
    E,
    N,
    g,
    b,
    o,
    G,
    O,
    ie,
    fe,
    z,
    B,
    tt,
    y,
    A,
    Y,
    $,
    oe,
    Te,
    Ze,
    nt,
    Ce,
    r
  ];
}
class f_ extends Yu {
  constructor(e) {
    super(), $u(
      this,
      e,
      s_,
      a_,
      t_,
      {
        value: 1,
        label: 2,
        show_label: 3,
        sources: 4,
        root: 5,
        interactive: 6,
        i18n: 7,
        showShareButton: 8,
        showDownloadButton: 9,
        showClearButton: 10,
        height: 28,
        width: 29,
        imgSize: 11,
        max_file_size: 12,
        cli_upload: 13,
        stream_handler: 14,
        patchSize: 15,
        showGrid: 16,
        gridColor: 17,
        active_source: 0
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: c_,
  attr: gn,
  detach: To,
  element: Wo,
  init: u_,
  insert: Po,
  noop: Pi,
  safe_not_equal: __,
  src_url_equal: Ni,
  toggle_class: Je
} = window.__gradio__svelte__internal;
function Vi(l) {
  let e, t;
  return {
    c() {
      e = Wo("img"), Ni(e.src, t = /*value*/
      l[0].url) || gn(e, "src", t), gn(e, "alt", "");
    },
    m(n, i) {
      Po(n, e, i);
    },
    p(n, i) {
      i & /*value*/
      1 && !Ni(e.src, t = /*value*/
      n[0].url) && gn(e, "src", t);
    },
    d(n) {
      n && To(e);
    }
  };
}
function d_(l) {
  let e, t = (
    /*value*/
    l[0] && Vi(l)
  );
  return {
    c() {
      e = Wo("div"), t && t.c(), gn(e, "class", "container svelte-1sgcyba"), Je(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), Je(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), Je(
        e,
        "selected",
        /*selected*/
        l[2]
      ), Je(
        e,
        "border",
        /*value*/
        l[0]
      );
    },
    m(n, i) {
      Po(n, e, i), t && t.m(e, null);
    },
    p(n, [i]) {
      /*value*/
      n[0] ? t ? t.p(n, i) : (t = Vi(n), t.c(), t.m(e, null)) : t && (t.d(1), t = null), i & /*type*/
      2 && Je(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), i & /*type*/
      2 && Je(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), i & /*selected*/
      4 && Je(
        e,
        "selected",
        /*selected*/
        n[2]
      ), i & /*value*/
      1 && Je(
        e,
        "border",
        /*value*/
        n[0]
      );
    },
    i: Pi,
    o: Pi,
    d(n) {
      n && To(e), t && t.d();
    }
  };
}
function m_(l, e, t) {
  let { value: n } = e, { type: i } = e, { selected: o = !1 } = e;
  return l.$$set = (r) => {
    "value" in r && t(0, n = r.value), "type" in r && t(1, i = r.type), "selected" in r && t(2, o = r.selected);
  }, [n, i, o];
}
class W_ extends c_ {
  constructor(e) {
    super(), u_(this, e, m_, d_, __, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: h_,
  add_flush_callback: Ui,
  assign: g_,
  bind: Oi,
  binding_callbacks: Gi,
  check_outros: b_,
  create_component: vt,
  destroy_component: kt,
  detach: No,
  empty: p_,
  flush: H,
  get_spread_object: w_,
  get_spread_update: v_,
  group_outros: k_,
  init: y_,
  insert: Vo,
  mount_component: yt,
  safe_not_equal: S_,
  space: C_,
  transition_in: Ge,
  transition_out: He
} = window.__gradio__svelte__internal;
function z_(l) {
  let e, t;
  return e = new $r({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [E_] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      vt(e.$$.fragment);
    },
    m(n, i) {
      yt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      64 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      He(e.$$.fragment, n), t = !1;
    },
    d(n) {
      kt(e, n);
    }
  };
}
function q_(l) {
  let e, t;
  return e = new io({
    props: {
      i18n: (
        /*gradio*/
        l[23].i18n
      ),
      type: "clipboard",
      mode: "short"
    }
  }), {
    c() {
      vt(e.$$.fragment);
    },
    m(n, i) {
      yt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*gradio*/
      8388608 && (o.i18n = /*gradio*/
      n[23].i18n), e.$set(o);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      He(e.$$.fragment, n), t = !1;
    },
    d(n) {
      kt(e, n);
    }
  };
}
function M_(l) {
  let e, t;
  return e = new io({
    props: {
      i18n: (
        /*gradio*/
        l[23].i18n
      ),
      type: "image"
    }
  }), {
    c() {
      vt(e.$$.fragment);
    },
    m(n, i) {
      yt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*gradio*/
      8388608 && (o.i18n = /*gradio*/
      n[23].i18n), e.$set(o);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      He(e.$$.fragment, n), t = !1;
    },
    d(n) {
      kt(e, n);
    }
  };
}
function E_(l) {
  let e, t;
  return e = new Qi({}), {
    c() {
      vt(e.$$.fragment);
    },
    m(n, i) {
      yt(e, n, i), t = !0;
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      He(e.$$.fragment, n), t = !1;
    },
    d(n) {
      kt(e, n);
    }
  };
}
function I_(l) {
  let e, t, n, i;
  const o = [M_, q_, z_], r = [];
  function f(a, s) {
    return (
      /*active_source*/
      a[25] === "upload" ? 0 : (
        /*active_source*/
        a[25] === "clipboard" ? 1 : 2
      )
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = p_();
    },
    m(a, s) {
      r[e].m(a, s), Vo(a, n, s), i = !0;
    },
    p(a, s) {
      let c = e;
      e = f(a), e === c ? r[e].p(a, s) : (k_(), He(r[c], 1, 1, () => {
        r[c] = null;
      }), b_(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), Ge(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (Ge(t), i = !0);
    },
    o(a) {
      He(t), i = !1;
    },
    d(a) {
      a && No(n), r[e].d(a);
    }
  };
}
function D_(l) {
  let e, t, n, i, o, r;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        l[23].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[23].i18n
    ) },
    /*loading_status*/
    l[1]
  ];
  let a = {};
  for (let d = 0; d < f.length; d += 1)
    a = g_(a, f[d]);
  e = new Hf({ props: a });
  function s(d) {
    l[26](d);
  }
  function c(d) {
    l[27](d);
  }
  let u = {
    selectable: (
      /*_selectable*/
      l[10]
    ),
    root: (
      /*root*/
      l[7]
    ),
    sources: (
      /*sources*/
      l[14]
    ),
    interactive: (
      /*interactive*/
      l[18]
    ),
    showDownloadButton: (
      /*show_download_button*/
      l[15]
    ),
    showShareButton: (
      /*show_share_button*/
      l[16]
    ),
    showClearButton: (
      /*show_clear_button*/
      l[17]
    ),
    i18n: (
      /*gradio*/
      l[23].i18n
    ),
    height: (
      /*height*/
      l[8]
    ),
    width: (
      /*width*/
      l[9]
    ),
    label: (
      /*label*/
      l[5]
    ),
    show_label: (
      /*show_label*/
      l[6]
    ),
    max_file_size: (
      /*gradio*/
      l[23].max_file_size
    ),
    cli_upload: (
      /*gradio*/
      l[23].client.upload
    ),
    stream_handler: (
      /*gradio*/
      l[23].client.stream
    ),
    imgSize: (
      /*img_size*/
      l[19]
    ),
    patchSize: (
      /*patch_size*/
      l[20]
    ),
    showGrid: (
      /*show_grid*/
      l[21]
    ),
    gridColor: (
      /*grid_color*/
      l[22]
    ),
    $$slots: { default: [I_] },
    $$scope: { ctx: l }
  };
  return (
    /*active_source*/
    l[25] !== void 0 && (u.active_source = /*active_source*/
    l[25]), /*value*/
    l[0] !== void 0 && (u.value = /*value*/
    l[0]), n = new f_({ props: u }), Gi.push(() => Oi(n, "active_source", s)), Gi.push(() => Oi(n, "value", c)), n.$on(
      "change",
      /*change_handler*/
      l[28]
    ), n.$on(
      "edit",
      /*edit_handler*/
      l[29]
    ), n.$on(
      "patch_select",
      /*patch_select_handler*/
      l[30]
    ), n.$on(
      "clear",
      /*clear_handler*/
      l[31]
    ), n.$on(
      "drag",
      /*drag_handler*/
      l[32]
    ), n.$on(
      "upload",
      /*upload_handler*/
      l[33]
    ), n.$on(
      "select",
      /*select_handler*/
      l[34]
    ), n.$on(
      "share",
      /*share_handler*/
      l[35]
    ), n.$on(
      "error",
      /*error_handler*/
      l[36]
    ), {
      c() {
        vt(e.$$.fragment), t = C_(), vt(n.$$.fragment);
      },
      m(d, _) {
        yt(e, d, _), Vo(d, t, _), yt(n, d, _), r = !0;
      },
      p(d, _) {
        const m = _[0] & /*gradio, loading_status*/
        8388610 ? v_(f, [
          _[0] & /*gradio*/
          8388608 && {
            autoscroll: (
              /*gradio*/
              d[23].autoscroll
            )
          },
          _[0] & /*gradio*/
          8388608 && { i18n: (
            /*gradio*/
            d[23].i18n
          ) },
          _[0] & /*loading_status*/
          2 && w_(
            /*loading_status*/
            d[1]
          )
        ]) : {};
        e.$set(m);
        const h = {};
        _[0] & /*_selectable*/
        1024 && (h.selectable = /*_selectable*/
        d[10]), _[0] & /*root*/
        128 && (h.root = /*root*/
        d[7]), _[0] & /*sources*/
        16384 && (h.sources = /*sources*/
        d[14]), _[0] & /*interactive*/
        262144 && (h.interactive = /*interactive*/
        d[18]), _[0] & /*show_download_button*/
        32768 && (h.showDownloadButton = /*show_download_button*/
        d[15]), _[0] & /*show_share_button*/
        65536 && (h.showShareButton = /*show_share_button*/
        d[16]), _[0] & /*show_clear_button*/
        131072 && (h.showClearButton = /*show_clear_button*/
        d[17]), _[0] & /*gradio*/
        8388608 && (h.i18n = /*gradio*/
        d[23].i18n), _[0] & /*height*/
        256 && (h.height = /*height*/
        d[8]), _[0] & /*width*/
        512 && (h.width = /*width*/
        d[9]), _[0] & /*label*/
        32 && (h.label = /*label*/
        d[5]), _[0] & /*show_label*/
        64 && (h.show_label = /*show_label*/
        d[6]), _[0] & /*gradio*/
        8388608 && (h.max_file_size = /*gradio*/
        d[23].max_file_size), _[0] & /*gradio*/
        8388608 && (h.cli_upload = /*gradio*/
        d[23].client.upload), _[0] & /*gradio*/
        8388608 && (h.stream_handler = /*gradio*/
        d[23].client.stream), _[0] & /*img_size*/
        524288 && (h.imgSize = /*img_size*/
        d[19]), _[0] & /*patch_size*/
        1048576 && (h.patchSize = /*patch_size*/
        d[20]), _[0] & /*show_grid*/
        2097152 && (h.showGrid = /*show_grid*/
        d[21]), _[0] & /*grid_color*/
        4194304 && (h.gridColor = /*grid_color*/
        d[22]), _[0] & /*gradio, active_source*/
        41943040 | _[1] & /*$$scope*/
        64 && (h.$$scope = { dirty: _, ctx: d }), !i && _[0] & /*active_source*/
        33554432 && (i = !0, h.active_source = /*active_source*/
        d[25], Ui(() => i = !1)), !o && _[0] & /*value*/
        1 && (o = !0, h.value = /*value*/
        d[0], Ui(() => o = !1)), n.$set(h);
      },
      i(d) {
        r || (Ge(e.$$.fragment, d), Ge(n.$$.fragment, d), r = !0);
      },
      o(d) {
        He(e.$$.fragment, d), He(n.$$.fragment, d), r = !1;
      },
      d(d) {
        d && No(t), kt(e, d), kt(n, d);
      }
    }
  );
}
function B_(l) {
  let e, t;
  return e = new rr({
    props: {
      visible: (
        /*visible*/
        l[4]
      ),
      variant: "solid",
      border_mode: (
        /*dragging*/
        l[24] ? "focus" : "base"
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[2]
      ),
      elem_classes: (
        /*elem_classes*/
        l[3]
      ),
      width: (
        /*width*/
        l[9]
      ),
      allow_overflow: !1,
      container: (
        /*container*/
        l[11]
      ),
      scale: (
        /*scale*/
        l[12]
      ),
      min_width: (
        /*min_width*/
        l[13]
      ),
      $$slots: { default: [D_] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      vt(e.$$.fragment);
    },
    m(n, i) {
      yt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      16 && (o.visible = /*visible*/
      n[4]), i[0] & /*dragging*/
      16777216 && (o.border_mode = /*dragging*/
      n[24] ? "focus" : "base"), i[0] & /*elem_id*/
      4 && (o.elem_id = /*elem_id*/
      n[2]), i[0] & /*elem_classes*/
      8 && (o.elem_classes = /*elem_classes*/
      n[3]), i[0] & /*width*/
      512 && (o.width = /*width*/
      n[9]), i[0] & /*container*/
      2048 && (o.container = /*container*/
      n[11]), i[0] & /*scale*/
      4096 && (o.scale = /*scale*/
      n[12]), i[0] & /*min_width*/
      8192 && (o.min_width = /*min_width*/
      n[13]), i[0] & /*_selectable, root, sources, interactive, show_download_button, show_share_button, show_clear_button, gradio, height, width, label, show_label, img_size, patch_size, show_grid, grid_color, active_source, value, dragging, loading_status*/
      67094499 | i[1] & /*$$scope*/
      64 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      He(e.$$.fragment, n), t = !1;
    },
    d(n) {
      kt(e, n);
    }
  };
}
function L_(l, e, t) {
  let { elem_id: n = "" } = e, { elem_classes: i = [] } = e, { visible: o = !0 } = e, { value: r = null } = e, { label: f } = e, { show_label: a } = e, { root: s } = e, { height: c } = e, { width: u } = e, { _selectable: d = !1 } = e, { container: _ = !0 } = e, { scale: m = null } = e, { min_width: h = void 0 } = e, { loading_status: p } = e, { sources: w = ["upload", "webcam", "clipboard"] } = e, { show_download_button: g } = e, { show_share_button: b } = e, { show_clear_button: S } = e, { interactive: L } = e, { img_size: C = null } = e, { patch_size: M = 16 } = e, { show_grid: q = !0 } = e, { grid_color: D = "rgba(200, 200, 200, 0.5)" } = e, { gradio: v } = e, I, V = null;
  function U(z) {
    V = z, t(25, V);
  }
  function le(z) {
    r = z, t(0, r);
  }
  const j = () => v.dispatch("change"), T = () => v.dispatch("edit"), X = ({ detail: z }) => v.dispatch("patch_select", z), E = () => {
    v.dispatch("clear");
  }, N = ({ detail: z }) => t(24, I = z), G = () => v.dispatch("upload"), O = ({ detail: z }) => v.dispatch("select", z), ie = ({ detail: z }) => v.dispatch("share", z), fe = ({ detail: z }) => {
    t(1, p = p || {}), t(1, p.status = "error", p), v.dispatch("error", z);
  };
  return l.$$set = (z) => {
    "elem_id" in z && t(2, n = z.elem_id), "elem_classes" in z && t(3, i = z.elem_classes), "visible" in z && t(4, o = z.visible), "value" in z && t(0, r = z.value), "label" in z && t(5, f = z.label), "show_label" in z && t(6, a = z.show_label), "root" in z && t(7, s = z.root), "height" in z && t(8, c = z.height), "width" in z && t(9, u = z.width), "_selectable" in z && t(10, d = z._selectable), "container" in z && t(11, _ = z.container), "scale" in z && t(12, m = z.scale), "min_width" in z && t(13, h = z.min_width), "loading_status" in z && t(1, p = z.loading_status), "sources" in z && t(14, w = z.sources), "show_download_button" in z && t(15, g = z.show_download_button), "show_share_button" in z && t(16, b = z.show_share_button), "show_clear_button" in z && t(17, S = z.show_clear_button), "interactive" in z && t(18, L = z.interactive), "img_size" in z && t(19, C = z.img_size), "patch_size" in z && t(20, M = z.patch_size), "show_grid" in z && t(21, q = z.show_grid), "grid_color" in z && t(22, D = z.grid_color), "gradio" in z && t(23, v = z.gradio);
  }, [
    r,
    p,
    n,
    i,
    o,
    f,
    a,
    s,
    c,
    u,
    d,
    _,
    m,
    h,
    w,
    g,
    b,
    S,
    L,
    C,
    M,
    q,
    D,
    v,
    I,
    V,
    U,
    le,
    j,
    T,
    X,
    E,
    N,
    G,
    O,
    ie,
    fe
  ];
}
class P_ extends h_ {
  constructor(e) {
    super(), y_(
      this,
      e,
      L_,
      B_,
      S_,
      {
        elem_id: 2,
        elem_classes: 3,
        visible: 4,
        value: 0,
        label: 5,
        show_label: 6,
        root: 7,
        height: 8,
        width: 9,
        _selectable: 10,
        container: 11,
        scale: 12,
        min_width: 13,
        loading_status: 1,
        sources: 14,
        show_download_button: 15,
        show_share_button: 16,
        show_clear_button: 17,
        interactive: 18,
        img_size: 19,
        patch_size: 20,
        show_grid: 21,
        grid_color: 22,
        gradio: 23
      },
      null,
      [-1, -1]
    );
  }
  get elem_id() {
    return this.$$.ctx[2];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), H();
  }
  get elem_classes() {
    return this.$$.ctx[3];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), H();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({ visible: e }), H();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), H();
  }
  get label() {
    return this.$$.ctx[5];
  }
  set label(e) {
    this.$$set({ label: e }), H();
  }
  get show_label() {
    return this.$$.ctx[6];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), H();
  }
  get root() {
    return this.$$.ctx[7];
  }
  set root(e) {
    this.$$set({ root: e }), H();
  }
  get height() {
    return this.$$.ctx[8];
  }
  set height(e) {
    this.$$set({ height: e }), H();
  }
  get width() {
    return this.$$.ctx[9];
  }
  set width(e) {
    this.$$set({ width: e }), H();
  }
  get _selectable() {
    return this.$$.ctx[10];
  }
  set _selectable(e) {
    this.$$set({ _selectable: e }), H();
  }
  get container() {
    return this.$$.ctx[11];
  }
  set container(e) {
    this.$$set({ container: e }), H();
  }
  get scale() {
    return this.$$.ctx[12];
  }
  set scale(e) {
    this.$$set({ scale: e }), H();
  }
  get min_width() {
    return this.$$.ctx[13];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), H();
  }
  get loading_status() {
    return this.$$.ctx[1];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), H();
  }
  get sources() {
    return this.$$.ctx[14];
  }
  set sources(e) {
    this.$$set({ sources: e }), H();
  }
  get show_download_button() {
    return this.$$.ctx[15];
  }
  set show_download_button(e) {
    this.$$set({ show_download_button: e }), H();
  }
  get show_share_button() {
    return this.$$.ctx[16];
  }
  set show_share_button(e) {
    this.$$set({ show_share_button: e }), H();
  }
  get show_clear_button() {
    return this.$$.ctx[17];
  }
  set show_clear_button(e) {
    this.$$set({ show_clear_button: e }), H();
  }
  get interactive() {
    return this.$$.ctx[18];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), H();
  }
  get img_size() {
    return this.$$.ctx[19];
  }
  set img_size(e) {
    this.$$set({ img_size: e }), H();
  }
  get patch_size() {
    return this.$$.ctx[20];
  }
  set patch_size(e) {
    this.$$set({ patch_size: e }), H();
  }
  get show_grid() {
    return this.$$.ctx[21];
  }
  set show_grid(e) {
    this.$$set({ show_grid: e }), H();
  }
  get grid_color() {
    return this.$$.ctx[22];
  }
  set grid_color(e) {
    this.$$set({ grid_color: e }), H();
  }
  get gradio() {
    return this.$$.ctx[23];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), H();
  }
}
export {
  W_ as BaseExample,
  P_ as default
};
