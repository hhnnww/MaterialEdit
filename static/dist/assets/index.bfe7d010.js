import{y as s,q as D,Y as i,$ as d,A as F,p as B}from"./index.39e660c6.js";const a={formatYear:"YYYY \u5E74",formatMonth:"YYYY \u5E74 MM \u6708",today:"\u4ECA\u5929",view:{month:"\u6708",year:"\u5E74",week:"\u5468",day:"\u65E5"},month:{long:{January:"\u4E00\u6708",February:"\u4E8C\u6708",March:"\u4E09\u6708",April:"\u56DB\u6708",May:"\u4E94\u6708",June:"\u516D\u6708",July:"\u4E03\u6708",August:"\u516B\u6708",September:"\u4E5D\u6708",October:"\u5341\u6708",November:"\u5341\u4E00\u6708",December:"\u5341\u4E8C\u6708"},short:{January:"\u4E00\u6708",February:"\u4E8C\u6708",March:"\u4E09\u6708",April:"\u56DB\u6708",May:"\u4E94\u6708",June:"\u516D\u6708",July:"\u4E03\u6708",August:"\u516B\u6708",September:"\u4E5D\u6708",October:"\u5341\u6708",November:"\u5341\u4E00\u6708",December:"\u5341\u4E8C\u6708"}},week:{long:{self:"\u5468",monday:"\u5468\u4E00",tuesday:"\u5468\u4E8C",wednesday:"\u5468\u4E09",thursday:"\u5468\u56DB",friday:"\u5468\u4E94",saturday:"\u5468\u516D",sunday:"\u5468\u65E5"},short:{self:"\u5468",monday:"\u4E00",tuesday:"\u4E8C",wednesday:"\u4E09",thursday:"\u56DB",friday:"\u4E94",saturday:"\u516D",sunday:"\u65E5"}}},y={locale:"zh-CN",empty:{description:"\u6682\u65E0\u6570\u636E"},drawer:{okText:"\u786E\u5B9A",cancelText:"\u53D6\u6D88"},popconfirm:{okText:"\u786E\u5B9A",cancelText:"\u53D6\u6D88"},modal:{okText:"\u786E\u5B9A",cancelText:"\u53D6\u6D88"},pagination:{goto:"\u524D\u5F80",page:"\u9875",countPerPage:"\u6761/\u9875",total:"\u5171 {0} \u6761"},table:{okText:"\u786E\u5B9A",resetText:"\u91CD\u7F6E"},upload:{start:"\u5F00\u59CB",cancel:"\u53D6\u6D88",delete:"\u5220\u9664",retry:"\u70B9\u51FB\u91CD\u8BD5",buttonText:"\u70B9\u51FB\u4E0A\u4F20",preview:"\u9884\u89C8",drag:"\u70B9\u51FB\u6216\u62D6\u62FD\u6587\u4EF6\u5230\u6B64\u5904\u4E0A\u4F20",dragHover:"\u91CA\u653E\u6587\u4EF6\u5E76\u5F00\u59CB\u4E0A\u4F20",error:"\u4E0A\u4F20\u5931\u8D25"},datePicker:{view:a.view,month:a.month,week:a.week,placeholder:{date:"\u8BF7\u9009\u62E9\u65E5\u671F",week:"\u8BF7\u9009\u62E9\u5468",month:"\u8BF7\u9009\u62E9\u6708\u4EFD",year:"\u8BF7\u9009\u62E9\u5E74\u4EFD",quarter:"\u8BF7\u9009\u62E9\u5B63\u5EA6",time:"\u8BF7\u9009\u62E9\u65F6\u95F4"},rangePlaceholder:{date:["\u5F00\u59CB\u65E5\u671F","\u7ED3\u675F\u65E5\u671F"],week:["\u5F00\u59CB\u5468","\u7ED3\u675F\u5468"],month:["\u5F00\u59CB\u6708\u4EFD","\u7ED3\u675F\u6708\u4EFD"],year:["\u5F00\u59CB\u5E74\u4EFD","\u7ED3\u675F\u5E74\u4EFD"],quarter:["\u5F00\u59CB\u5B63\u5EA6","\u7ED3\u675F\u5B63\u5EA6"],time:["\u5F00\u59CB\u65F6\u95F4","\u7ED3\u675F\u65F6\u95F4"]},selectTime:"\u9009\u62E9\u65F6\u95F4",today:"\u4ECA\u5929",now:"\u6B64\u523B",ok:"\u786E\u5B9A"},image:{loading:"\u52A0\u8F7D\u4E2D"},imagePreview:{fullScreen:"\u5168\u5C4F",rotateRight:"\u5411\u53F3\u65CB\u8F6C",rotateLeft:"\u5411\u5DE6\u65CB\u8F6C",zoomIn:"\u653E\u5927",zoomOut:"\u7F29\u5C0F",originalSize:"\u539F\u59CB\u5C3A\u5BF8"},typography:{copied:"\u5DF2\u590D\u5236",copy:"\u590D\u5236",expand:"\u5C55\u5F00",collapse:"\u6298\u53E0",edit:"\u7F16\u8F91"}},m=s("zh-CN"),C=D({"zh-CN":y}),h=()=>{const r=i(d,void 0),o=F(()=>{var e;return(e=r==null?void 0:r.locale)!=null?e:C[m.value]});return{locale:F(()=>o.value.locale),t:(e,...E)=>{const l=e.split(".");let u=o.value;for(const t of l){if(!u[t])return e;u=u[t]}return B(u)&&E.length>0?u.replace(/{(\d+)}/g,(t,c)=>{var n;return(n=E[c])!=null?n:t}):u}}};export{h as u};
