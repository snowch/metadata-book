(() => {
  const $ = id => document.getElementById(id);
  const form = $('answer-form');
  const answer = $('answer');
  const feedback = $('feedback');
  const buttons = [...document.querySelectorAll('[data-scene]')];
  const box = '<svg viewBox="0 0 100 80" aria-hidden="true"><path d="M10 22 50 5l40 17v40L50 78 10 62Z M10 22l40 18 40-18M50 40v38M30 14l40 18v17" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/></svg>';
  const content = {
    task: ['The operations meeting', 'Which deliveries count?', 'Of all parcels due by noon, how many arrived on time?', '?', '?', 'Choose the population before calculating.'],
    evidence: ['Parcel records', 'Four parcels due by noon', 'At 13:00, two have arrived on time, one is late and one is unfinished.', '?', '?', 'The records are complete at this time. Select a question to see which parcels it counts.'],
    demonstration: ['Worked example', 'Completed deliveries', 'Count the late arrival and the two on-time arrivals.', '3', '66.7%', 'Two on time out of three completed.'],
    guided: ['Your turn', 'Count all deliveries due', 'Which parcels belong in the denominator? Pause and explain.', '?', '?', 'The numerator is still two. What changes?'],
    explanation: ['Worked example', 'All parcels due', 'All four parcels were due by noon. Two have arrived on time.', '4', '50.0%', 'Two on time out of all four due.'],
    independent: ['Your turn', 'Six parcels due by noon', 'Two are on time, two are late and two are unfinished. The records are complete at 13:00.', '?', '?', 'How many parcels belong in the denominator when you count all parcels due?'],
    feedback: ['Worked result', 'Two out of six', 'Include both unfinished parcels in the denominator.', '6', '33.3%', 'Two on time out of all six due.'],
    application: ['Use the definition', 'Make the rule inspectable', 'Population. Measurement time. Responsible team.', '4', '50.0%', 'Then check that the calculation follows the recorded rule.'],
  };

  function renderParcels(six) {
    const states = six ? ['On time', 'On time', 'Late', 'Late', 'Unfinished', 'Unfinished'] : ['On time', 'On time', 'Late', 'Unfinished'];
    if ($('parcels').children.length !== states.length) {
      $('parcels').innerHTML = states.map((state, index) => {
        const style = state === 'Late' ? 'late' : state === 'Unfinished' ? 'waiting' : '';
        return `<div class="parcel ${style}" role="listitem" data-index="${index}">${box}<span>${state}</span></div>`;
      }).join('');
    }
  }

  function showScene(id) {
    if (!content[id]) throw Error(id);
    document.body.dataset.scene = id;
    document.body.classList.remove('show-calculation');
    const six = id === 'independent' || id === 'feedback';
    document.body.classList.toggle('six', six);
    renderParcels(six);
    ['context', 'title', 'description', 'denominator', 'percentage', 'reason'].forEach((key, index) => {
      $(key).textContent = content[id][index];
    });
    $('population').textContent = six ? 'Six parcels due by noon' : 'Four parcels due by noon';
    $('group').textContent = id === 'demonstration' ? '3 completed deliveries'
      : id === 'explanation' ? '4 deliveries due' : id === 'feedback' ? '6 deliveries due' : 'Which parcels count?';
    const exclude = id === 'demonstration' || id === 'guided';
    $('parcels').querySelectorAll('.parcel').forEach((parcel, index) => {
      const outside = exclude && index === 3;
      parcel.classList.toggle('excluded', outside);
      if (outside) parcel.setAttribute('aria-label', 'Unfinished, outside the completed-delivery count');
      else parcel.removeAttribute('aria-label');
    });
    document.querySelector('.group-line').style.width = exclude ? '625px' : '';
    buttons.forEach(button => {
      const selected = id === 'feedback' ? 'independent' : id;
      button.setAttribute('aria-pressed', String(button.dataset.scene === selected));
    });
    form.hidden = id !== 'independent';
    answer.value = '';
    answer.removeAttribute('aria-invalid');
    feedback.textContent = '';
    feedback.removeAttribute('data-state');
  }

  buttons.forEach(button => button.addEventListener('click', () => {
    showScene(button.dataset.scene);
    if (button.dataset.scene === 'independent') answer.focus();
  }));
  answer.addEventListener('input', () => {
    answer.removeAttribute('aria-invalid');
    feedback.textContent = '';
    feedback.removeAttribute('data-state');
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!answer.validity.valid) {
      answer.setAttribute('aria-invalid', 'true');
      feedback.dataset.state = 'error';
      feedback.textContent = 'Enter a whole number from 1 to 6.';
      answer.focus();
      return;
    }
    if (answer.valueAsNumber !== 6) {
      feedback.textContent = answer.valueAsNumber === 4
        ? 'Four counts only the completed parcels. Include the two unfinished parcels and try again.'
        : 'Count each parcel due at noon, including any unfinished parcels, and try again.';
      answer.focus();
      return;
    }
    showScene('feedback');
    feedback.textContent = 'Correct. All six parcels were due. Two on time out of six gives 33.3%.';
    feedback.focus();
  });

  const options = new URLSearchParams(location.search);
  if (options.has('record')) document.body.classList.add('record');
  if (options.has('embed')) {
    document.body.classList.add('embed');
    const resize = () => parent.postMessage({kind: 'parcel-lab-height', height: Math.ceil(document.body.getBoundingClientRect().height)}, location.origin);
    new ResizeObserver(resize).observe(document.body);
    document.fonts.ready.then(resize);
  }
  window.showScene = showScene;
  window.setRecordingScene = (id, heading) => {
    showScene(id);
    $('title').textContent = heading;
  };
  window.revealCalculation = () => document.body.classList.add('show-calculation');
  showScene('evidence');
  for (const section of document.querySelectorAll('.manifest, .result, section.controls')) {
    section.hidden = false;
  }
})();
