/* Size this same-origin lab to its content, rather than leaving a fixed blank area. */
(() => {
 const frame=document.querySelector('.lesson-lab iframe');
 if(!frame)return;
 window.addEventListener('message',event=>{
  if(event.origin!==location.origin||event.source!==frame.contentWindow||event.data?.kind!=='parcel-lab-height')return;
  const height=event.data.height;
  if(Number.isFinite(height)&&height>=100&&height<=2500)frame.style.height=`${height}px`;
 });
})();
