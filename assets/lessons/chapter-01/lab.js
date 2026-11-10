(() => {
const $=id=>document.getElementById(id);let scene='evidence';
const box='<svg viewBox="0 0 100 80" aria-hidden="true"><path d="M10 22 50 5l40 17v40L50 78 10 62Z M10 22l40 18 40-18M50 40v38M30 14l40 18v17" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/></svg>';
function parcels(six){const states=six?['On time','On time','Late','Late','Unfinished','Unfinished']:['On time','On time','Late','Unfinished'];if($('parcels').children.length!==states.length)$('parcels').innerHTML=states.map((s,i)=>`<div class="parcel ${s==='Late'?'late':s==='Unfinished'?'waiting':''}" data-index="${i}">${box}<span>${s}</span></div>`).join('');return states;}
const content={
 task:['The operations meeting','Which deliveries count?','Of all parcels due by noon, how many arrived on time?','?','?','Choose the population before calculating.'],
 evidence:['The evidence','Four parcels. All due.','At 13:00: two on time, one late, one unfinished.','?','?','The records are complete at this moment.'],
 demonstration:['Worked example','Count completed deliveries','Keep the late arrival. Leave the unfinished parcel outside.','3','66.7%','2 on time out of 3 completed.'],
 guided:['Your turn','Count all deliveries due','Which parcels belong in the denominator? Pause and explain.','?','?','The numerator is still two. What changes?'],
 explanation:['The operations answer','The unfinished parcel counts','All four were due by noon. The numerator stays the same.','4','50.0%','2 on time out of all 4 due.'],
 independent:['A separate example','Six parcels. Your calculation.','All six were due. Assume complete records at measurement time.','?','?','What percentage of all parcels due arrived on time?'],
 feedback:['Check your reasoning','Two out of all six due','The unfinished parcels still belong in this population.','6','33.3%','Using 4 as the denominator would answer a different question.'],
 application:['Use the definition','Make the rule inspectable','Population. Measurement time. Responsible team.','4','50.0%','Then check that the calculation follows the recorded rule.']};
window.showScene=(id)=>{if(!content[id])throw Error(id);scene=id;document.body.dataset.scene=id;document.body.classList.remove('show-calculation');const c=content[id],six=['independent','feedback'].includes(id);document.body.classList.toggle('six',six);parcels(six);['context','title','description','denominator','percentage','reason'].forEach((key,i)=>$(key).textContent=c[i]);$('population').textContent=six?'Six parcels due by noon':'Four parcels due by noon';$('group').textContent=id==='demonstration'?'3 completed deliveries':c[3]==='?'?'Which parcels belong?':`${c[3]} deliveries due`;$('parcels').querySelectorAll('.parcel').forEach((p,i)=>p.classList.toggle('excluded',['demonstration','guided'].includes(id)&&i===3));document.querySelector('.group-line').style.width=['demonstration','guided'].includes(id)?'625px':'';$('feedback').textContent='';document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scene===id)));$('reveal').hidden=!['guided','independent'].includes(id);$('answer-input').hidden=$('reveal').hidden;$('answer').value='';};
document.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>showScene(b.dataset.scene)));
$('reveal').addEventListener('click',()=>{const independent=scene==='independent';const answer=Number($('answer').value);showScene(independent?'feedback':'explanation');$('feedback').textContent=(answer ? answer===(independent?6:4)?'Yes. ':answer===4&&independent?'Four counts only completed deliveries. Include the unfinished parcels too. ':'Count every parcel due, including unfinished ones. ':'Compare with your explanation: ')+(independent?'Two on time ÷ six due = 33.3%. Four is the completed-delivery denominator.':'The unfinished parcel was due too. Two on time ÷ four due = 50.0%.');});
if(new URLSearchParams(location.search).has('record'))document.body.classList.add('record');
if(new URLSearchParams(location.search).has('embed')){
 document.body.classList.add('embed');
 const resize=()=>parent.postMessage({kind:'parcel-lab-height',height:Math.ceil(document.body.getBoundingClientRect().height)},location.origin);
 new ResizeObserver(resize).observe(document.body);document.fonts.ready.then(resize);
}
window.setRecordingScene=(id,heading)=>{showScene(id);$('title').textContent=heading;};
window.revealCalculation=()=>document.body.classList.add('show-calculation');
showScene('evidence');
})();
