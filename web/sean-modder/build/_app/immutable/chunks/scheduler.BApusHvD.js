function N(){}function P(t,e){for(const n in e)t[n]=e[n];return t}function T(t){return t()}function et(){return Object.create(null)}function D(t){t.forEach(T)}function B(t){return typeof t=="function"}function nt(t,e){return t!=t?e==e:t!==e||t&&typeof t=="object"||typeof t=="function"}function it(t){return Object.keys(t).length===0}function L(t,...e){if(t==null){for(const i of e)i(void 0);return N}const n=t.subscribe(...e);return n.unsubscribe?()=>n.unsubscribe():n}function ct(t,e,n){t.$$.on_destroy.push(L(e,n))}function rt(t,e,n,i){if(t){const c=j(t,e,n,i);return t[0](c)}}function j(t,e,n,i){return t[1]&&i?P(n.ctx.slice(),t[1](i(e))):n.ctx}function st(t,e,n,i){if(t[2]&&i){const c=t[2](i(n));if(e.dirty===void 0)return c;if(typeof c=="object"){const o=[],r=Math.max(e.dirty.length,c.length);for(let l=0;l<r;l+=1)o[l]=e.dirty[l]|c[l];return o}return e.dirty|c}return e.dirty}function lt(t,e,n,i,c,o){if(c){const r=j(e,n,i,o);t.p(r,c)}}function ot(t){if(t.ctx.length>32){const e=[],n=t.ctx.length/32;for(let i=0;i<n;i++)e[i]=-1;return e}return-1}function ut(t){const e={};for(const n in t)n[0]!=="$"&&(e[n]=t[n]);return e}function at(t,e){const n={};e=new Set(e);for(const i in t)!e.has(i)&&i[0]!=="$"&&(n[i]=t[i]);return n}function ft(t){const e={};for(const n in t)e[n]=!0;return e}function _t(t,e,n){return t.set(n),e}function dt(t){return t&&B(t.destroy)?t.destroy:N}const M=["",!0,1,"true","contenteditable"];let p=!1;function ht(){p=!0}function mt(){p=!1}function q(t,e,n,i){for(;t<e;){const c=t+(e-t>>1);n(c)<=i?t=c+1:e=c}return t}function H(t){if(t.hydrate_init)return;t.hydrate_init=!0;let e=t.childNodes;if(t.nodeName==="HEAD"){const s=[];for(let u=0;u<e.length;u++){const a=e[u];a.claim_order!==void 0&&s.push(a)}e=s}const n=new Int32Array(e.length+1),i=new Int32Array(e.length);n[0]=-1;let c=0;for(let s=0;s<e.length;s++){const u=e[s].claim_order,a=(c>0&&e[n[c]].claim_order<=u?c+1:q(1,c,S=>e[n[S]].claim_order,u))-1;i[s]=n[a]+1;const k=a+1;n[k]=s,c=Math.max(k,c)}const o=[],r=[];let l=e.length-1;for(let s=n[c]+1;s!=0;s=i[s-1]){for(o.push(e[s-1]);l>=s;l--)r.push(e[l]);l--}for(;l>=0;l--)r.push(e[l]);o.reverse(),r.sort((s,u)=>s.claim_order-u.claim_order);for(let s=0,u=0;s<r.length;s++){for(;u<o.length&&r[s].claim_order>=o[u].claim_order;)u++;const a=u<o.length?o[u]:null;t.insertBefore(r[s],a)}}function I(t,e){if(p){for(H(t),(t.actual_end_child===void 0||t.actual_end_child!==null&&t.actual_end_child.parentNode!==t)&&(t.actual_end_child=t.firstChild);t.actual_end_child!==null&&t.actual_end_child.claim_order===void 0;)t.actual_end_child=t.actual_end_child.nextSibling;e!==t.actual_end_child?(e.claim_order!==void 0||e.parentNode!==t)&&t.insertBefore(e,t.actual_end_child):t.actual_end_child=e.nextSibling}else(e.parentNode!==t||e.nextSibling!==null)&&t.appendChild(e)}function pt(t,e,n){p&&!n?I(t,e):(e.parentNode!==t||e.nextSibling!=n)&&t.insertBefore(e,n||null)}function yt(t){t.parentNode&&t.parentNode.removeChild(t)}function bt(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function z(t){return document.createElement(t)}function F(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function w(t){return document.createTextNode(t)}function gt(){return w(" ")}function xt(){return w("")}function wt(t,e,n,i){return t.addEventListener(e,n,i),()=>t.removeEventListener(e,n,i)}function v(t,e,n){n==null?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}const U=["width","height"];function W(t,e){const n=Object.getOwnPropertyDescriptors(t.__proto__);for(const i in e)e[i]==null?t.removeAttribute(i):i==="style"?t.style.cssText=e[i]:i==="__value"?t.value=t[i]=e[i]:n[i]&&n[i].set&&U.indexOf(i)===-1?t[i]=e[i]:v(t,i,e[i])}function vt(t,e){for(const n in e)v(t,n,e[n])}function G(t,e){Object.keys(e).forEach(n=>{J(t,n,e[n])})}function J(t,e,n){const i=e.toLowerCase();i in t?t[i]=typeof t[i]=="boolean"&&n===""?!0:n:e in t?t[e]=typeof t[e]=="boolean"&&n===""?!0:n:v(t,e,n)}function kt(t){return/-/.test(t)?G:W}function Et(t){return t.dataset.svelteH}function Nt(t){return t===""?null:+t}function jt(t){return Array.from(t.childNodes)}function K(t){t.claim_info===void 0&&(t.claim_info={last_index:0,total_claimed:0})}function A(t,e,n,i,c=!1){K(t);const o=(()=>{for(let r=t.claim_info.last_index;r<t.length;r++){const l=t[r];if(e(l)){const s=n(l);return s===void 0?t.splice(r,1):t[r]=s,c||(t.claim_info.last_index=r),l}}for(let r=t.claim_info.last_index-1;r>=0;r--){const l=t[r];if(e(l)){const s=n(l);return s===void 0?t.splice(r,1):t[r]=s,c?s===void 0&&t.claim_info.last_index--:t.claim_info.last_index=r,l}}return i()})();return o.claim_order=t.claim_info.total_claimed,t.claim_info.total_claimed+=1,o}function O(t,e,n,i){return A(t,c=>c.nodeName===e,c=>{const o=[];for(let r=0;r<c.attributes.length;r++){const l=c.attributes[r];n[l.name]||o.push(l.name)}o.forEach(r=>c.removeAttribute(r))},()=>i(e))}function At(t,e,n){return O(t,e,n,z)}function Ot(t,e,n){return O(t,e,n,F)}function Q(t,e){return A(t,n=>n.nodeType===3,n=>{const i=""+e;if(n.data.startsWith(i)){if(n.data.length!==i.length)return n.splitText(i.length)}else n.data=i},()=>w(e),!0)}function Ct(t){return Q(t," ")}function R(t,e){e=""+e,t.data!==e&&(t.data=e)}function V(t,e){e=""+e,t.wholeText!==e&&(t.data=e)}function St(t,e,n){~M.indexOf(n)?V(t,e):R(t,e)}function Pt(t,e){t.value=e??""}function Tt(t,e,n,i){n==null?t.style.removeProperty(e):t.style.setProperty(e,n,"")}function X(t,e,{bubbles:n=!1,cancelable:i=!1}={}){return new CustomEvent(t,{detail:e,bubbles:n,cancelable:i})}function Dt(t,e){return new t(e)}let m;function y(t){m=t}function d(){if(!m)throw new Error("Function called outside component initialization");return m}function Bt(t){d().$$.on_mount.push(t)}function Lt(t){d().$$.after_update.push(t)}function Mt(t){d().$$.on_destroy.push(t)}function qt(){const t=d();return(e,n,{cancelable:i=!1}={})=>{const c=t.$$.callbacks[e];if(c){const o=X(e,n,{cancelable:i});return c.slice().forEach(r=>{r.call(t,o)}),!o.defaultPrevented}return!0}}function Ht(t,e){return d().$$.context.set(t,e),e}function It(t){return d().$$.context.get(t)}function zt(t,e){const n=t.$$.callbacks[e.type];n&&n.slice().forEach(i=>i.call(this,e))}const h=[],E=[];let _=[];const g=[],C=Promise.resolve();let x=!1;function Y(){x||(x=!0,C.then($))}function Ft(){return Y(),C}function Z(t){_.push(t)}function Ut(t){g.push(t)}const b=new Set;let f=0;function $(){if(f!==0)return;const t=m;do{try{for(;f<h.length;){const e=h[f];f++,y(e),tt(e.$$)}}catch(e){throw h.length=0,f=0,e}for(y(null),h.length=0,f=0;E.length;)E.pop()();for(let e=0;e<_.length;e+=1){const n=_[e];b.has(n)||(b.add(n),n())}_.length=0}while(h.length);for(;g.length;)g.pop()();x=!1,b.clear(),y(t)}function tt(t){if(t.fragment!==null){t.update(),D(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(Z)}}function Wt(t){const e=[],n=[];_.forEach(i=>t.indexOf(i)===-1?e.push(i):n.push(i)),n.forEach(i=>i()),_=e}export{_t as $,D as A,et as B,$ as C,B as D,it as E,Z as F,Wt as G,m as H,y as I,T as J,h as K,Y as L,ht as M,mt as N,P as O,W as P,dt as Q,at as R,d as S,ut as T,It as U,F as V,Ot as W,vt as X,kt as Y,Ht as Z,Mt as _,st as a,wt as a0,zt as a1,Pt as a2,ft as a3,Ut as a4,St as a5,bt as a6,Nt as a7,qt as a8,Et as a9,gt as b,rt as c,At as d,z as e,jt as f,ot as g,Q as h,yt as i,Ct as j,pt as k,I as l,R as m,N as n,ct as o,xt as p,Lt as q,Bt as r,nt as s,w as t,lt as u,v,Tt as w,E as x,Dt as y,Ft as z};
