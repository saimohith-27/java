const rd = window.__RESULT_DATA__;
new Chart(document.getElementById('statusChart'), {
  type:'doughnut',
  data:{labels:Object.keys(rd.status), datasets:[{data:Object.values(rd.status)}]}
});
new Chart(document.getElementById('categoryChart'), {
  type:'bar',
  data:{labels:Object.keys(rd.category), datasets:[{label:'% Score', data:Object.values(rd.category)}]}
});
new Chart(document.getElementById('timeChart'), {
  type:'scatter',
  data:{datasets:[{label:'Time per question (sec)', data:rd.timePoints.map((p,i)=>({x:i+1,y:p[1]}))}]},
  options:{scales:{x:{title:{display:true,text:'Question Number'}},y:{title:{display:true,text:'Time (s)'}}}}
});
