import{k as t,d as g,q as V,h as d,w as o,c as s,e as w,M as x,K as m,L as A,D as c,E as D}from"./index.414cfc81.js";import{f as B,B as L,C as v,R as y}from"./index.00266534.js";import{a as C,b as R,R as j,F as I}from"./index.99517337.js";import{a as N}from"./axios.91e25212.js";import{s as z}from"./store.374d1e7a.js";import{a as M,N as p}from"./index.db5edbd9.js";const U=M("arrow-right",!0,function(a){return t("svg",{width:a.size,height:a.size,viewBox:"0 0 48 48",fill:"none"},[t("path",{d:"M41.9999 24H5.99994",stroke:a.colors[0],"stroke-width":a.strokeWidth,"stroke-linecap":a.strokeLinecap,"stroke-linejoin":a.strokeLinejoin},null),t("path",{d:"M30 12L42 24L30 36",stroke:a.colors[0],"stroke-width":a.strokeWidth,"stroke-linecap":a.strokeLinecap,"stroke-linejoin":a.strokeLinejoin},null)])}),T=g({__name:"Index",setup(a){const e=V({tb_name:"\u996D\u6876\u8BBE\u8BA1",dst_path:"",ori_path:""});function f(){p.info({title:"\u5408\u5E76\u7D20\u6750",content:"\u628A\u7D20\u6750\u76EE\u5F55\uFF1A"+e.dst_path+"\u5408\u5E76\u5230\u76EE\u5F55\uFF1A"+e.ori_path,closable:!0,duration:0}),N.post("http://127.0.0.1:22702/material_merge",{tb_name:e.tb_name,ori_path:e.ori_path,dst_path:e.dst_path}).then(function(i){console.log(i),p.success({title:"\u5408\u5E76\u7D20\u6750\u6210\u529F",content:"\u628A\u7D20\u6750\u76EE\u5F55\uFF1A"+e.dst_path+"\u5408\u5E76\u5230\u76EE\u5F55\uFF1A"+e.ori_path,closable:!0,duration:0})})}return(i,n)=>{const E=C,h=j,r=I,l=v,_=B,k=L,F=y,b=R;return s(),d(b,{layout:"vertical",size:"large"},{default:o(()=>[t(F,{gutter:[24,24],justify:"start",align:"center"},{default:o(()=>[t(l,{span:3},{default:o(()=>[t(r,{label:"\u5E97\u94FA\u9009\u62E9"},{default:o(()=>[t(h,{type:"button",modelValue:e.tb_name,"onUpdate:modelValue":n[0]||(n[0]=u=>e.tb_name=u)},{default:o(()=>[(s(!0),w(A,null,x(m(z).tb_name,u=>(s(),d(E,{value:u},{default:o(()=>[c(D(u),1)]),_:2},1032,["value"]))),256))]),_:1},8,["modelValue"])]),_:1})]),_:1}),t(l,{span:9},{default:o(()=>[t(r,{label:"\u6E90\u76EE\u5F55"},{default:o(()=>[t(_,{modelValue:e.ori_path,"onUpdate:modelValue":n[1]||(n[1]=u=>e.ori_path=u)},null,8,["modelValue"])]),_:1})]),_:1}),t(l,{span:1,class:"text-center text-3xl"},{default:o(()=>[t(m(U))]),_:1}),t(l,{span:9},{default:o(()=>[t(r,{label:"\u76EE\u6807\u76EE\u5F55"},{default:o(()=>[t(_,{modelValue:e.dst_path,"onUpdate:modelValue":n[2]||(n[2]=u=>e.dst_path=u)},null,8,["modelValue"])]),_:1})]),_:1}),t(l,{span:24},{default:o(()=>[t(k,{type:"primary",onClick:f},{default:o(()=>[c("\u63D0\u4EA4")]),_:1},8,["onClick"])]),_:1})]),_:1})]),_:1})}}});export{T as default};
