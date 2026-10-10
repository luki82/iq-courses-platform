/*
 * Lesson page helpers for English learners:
 *  - Read-aloud: speaker buttons, tap-any-word, and "play the conversation",
 *    using the browser's built-in voices (Web Speech API), woman or man,
 *    normal or slow.
 *  - Fill-in-the-gap exercises: drag a word (or tap it, then tap a gap).
 *    A wrong word turns red and shakes, then goes back; a right word turns
 *    green and the full sentence is read out.
 */
(function () {
  "use strict";

  var body = document.querySelector("[data-lesson-body]");
  if (!body) return;

  // ---------------------------------------------------------------------
  // Settings (remembered per browser where storage is available)
  // ---------------------------------------------------------------------
  function load(key, fallback) {
    try { return window.localStorage.getItem(key) || fallback; } catch (e) { return fallback; }
  }
  function save(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* storage blocked */ }
  }

  var settings = {
    gender: load("iq-voice-gender", "female"),
    speed: load("iq-voice-speed", "normal"),
  };

  // ---------------------------------------------------------------------
  // Voices
  // ---------------------------------------------------------------------
  var synth = window.speechSynthesis;
  var canSpeak = !!(synth && window.SpeechSynthesisUtterance);

  // Browsers don't say whether a voice is male or female, so we guess from
  // the voice name. "female" is checked first because it contains "male".
  var FEMALE = /female|woman|samantha|karen|moira|tessa|fiona|victoria|zira|susan|hazel|catherine|serena|allison|\bava\b|\bkate\b|libby|sonia|natasha|\baria\b|jenny|emma|\bamy\b|joanna|salli|kimberly|\bivy\b|nicole|olivia|martha|kathy|vicki|google us english|google uk english female/i;
  var MALE = /\bmale\b|\bman\b|daniel|\balex\b|\bfred\b|david|\bmark\b|george|james|ryan|\bguy\b|william|thomas|oliver|rishi|\blee\b|aaron|arthur|gordon|\btom\b|matthew|brian|russell|joey|justin|ralph|bruce|google uk english male/i;
  var LOCALE_RANK = ["en-au", "en-gb", "en-nz", "en-us", "en-ie", "en-ca", "en-za", "en-in"];

  var voices = [];
  function refreshVoices() {
    voices = synth.getVoices().filter(function (v) { return /^en([-_]|$)/i.test(v.lang); });
  }

  function guessGender(voice) {
    if (FEMALE.test(voice.name)) return "female";
    if (MALE.test(voice.name)) return "male";
    return "";
  }

  function rank(voice) {
    var lang = voice.lang.toLowerCase().replace("_", "-");
    var i = LOCALE_RANK.indexOf(lang);
    return (i === -1 ? LOCALE_RANK.length : i) * 2 + (voice.localService ? 0 : 1);
  }

  // Returns {voice, pitch}. If no voice of the wanted gender exists, use the
  // best English voice and shift its pitch so "man" and "woman" still differ.
  function pickVoice(gender) {
    if (!voices.length) refreshVoices();
    var sorted = voices.slice().sort(function (a, b) { return rank(a) - rank(b); });
    var match = sorted.filter(function (v) { return guessGender(v) === gender; })[0];
    if (match) return { voice: match, pitch: 1 };
    var fallback = sorted[0] || null;
    return { voice: fallback, pitch: gender === "male" ? 0.75 : 1.2 };
  }

  function otherGender(gender) { return gender === "male" ? "female" : "male"; }

  // Make text sound natural: "/" becomes a pause, gaps are read as "blank",
  // arrows are read as a pause.
  function cleanForSpeech(text) {
    return text
      .replace(/_{2,}/g, " blank ")
      .replace(/\s*->\s*/g, ", ")
      .replace(/\s+\/\s+/g, ", ")
      .replace(/\.\.\.|…/g, ", ")
      .replace(/\s+/g, " ")
      .trim();
  }

  var speakingEl = null;
  function markSpeaking(el) {
    if (speakingEl) speakingEl.classList.remove("is-speaking");
    speakingEl = el || null;
    if (speakingEl) speakingEl.classList.add("is-speaking");
  }

  // Speak one or more pieces of text in order. Each piece:
  // {text, gender, el} -- el is highlighted while it's being read.
  var queueToken = 0;
  function speakQueue(pieces, onDone) {
    if (!canSpeak) return;
    synth.cancel();
    var token = ++queueToken;
    var i = 0;
    function next() {
      if (token !== queueToken) return;
      if (i >= pieces.length) {
        markSpeaking(null);
        if (onDone) onDone();
        return;
      }
      var piece = pieces[i++];
      var text = cleanForSpeech(piece.text || "");
      if (!text) { next(); return; }
      var chosen = pickVoice(piece.gender || settings.gender);
      var u = new SpeechSynthesisUtterance(text);
      if (chosen.voice) { u.voice = chosen.voice; u.lang = chosen.voice.lang; } else { u.lang = "en-AU"; }
      u.pitch = chosen.pitch;
      u.rate = settings.speed === "slow" ? 0.6 : 0.9;
      u.onstart = function () { if (token === queueToken) markSpeaking(piece.el); };
      u.onend = next;
      u.onerror = next;
      synth.speak(u);
    }
    next();
  }

  function speak(text, el) { speakQueue([{ text: text, el: el }]); }

  function stopSpeaking() {
    queueToken++;
    if (canSpeak) synth.cancel();
    markSpeaking(null);
    resetDialogueButtons();
  }

  // ---------------------------------------------------------------------
  // Voice bar
  // ---------------------------------------------------------------------
  var bar = document.querySelector("[data-voice-bar]");
  if (canSpeak) {
    refreshVoices();
    if ("onvoiceschanged" in synth) synth.addEventListener("voiceschanged", refreshVoices);
    if (bar) {
      bar.hidden = false;
      var g = bar.querySelector('input[name="voice-gender"][value="' + settings.gender + '"]');
      var s = bar.querySelector('input[name="voice-speed"][value="' + settings.speed + '"]');
      if (g) g.checked = true;
      if (s) s.checked = true;
      bar.addEventListener("change", function (e) {
        if (e.target.name === "voice-gender") {
          settings.gender = e.target.value;
          save("iq-voice-gender", settings.gender);
          speak(settings.gender === "male" ? "Hello. This is my voice." : "Hello. This is my voice.");
        } else if (e.target.name === "voice-speed") {
          settings.speed = e.target.value;
          save("iq-voice-speed", settings.speed);
          speak(settings.speed === "slow" ? "I will speak slowly." : "I will speak at normal speed.");
        }
      });
    }
  } else {
    var note = document.querySelector("[data-voice-unsupported]");
    if (note) note.hidden = false;
    document.documentElement.classList.add("no-speech");
  }

  // ---------------------------------------------------------------------
  // Tap any word to hear it
  // ---------------------------------------------------------------------
  function wrapWords(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      if (!node.nodeValue.trim()) return;
      var frag = document.createDocumentFragment();
      node.nodeValue.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part) || !/[A-Za-z0-9]/.test(part)) {
          frag.appendChild(document.createTextNode(part));
        } else {
          var span = document.createElement("span");
          span.className = "w";
          span.textContent = part;
          frag.appendChild(span);
        }
      });
      node.parentNode.replaceChild(frag, node);
    });
  }

  if (canSpeak) {
    body.querySelectorAll(".say-text").forEach(wrapWords);
  }

  function rowText(row) {
    // Read a row's own words, plus a correctly filled gap if there is one.
    var parts = [];
    row.querySelectorAll(".say-text, .blank").forEach(function (el) {
      if (el.classList.contains("blank")) {
        parts.push(el.classList.contains("is-correct") || el.classList.contains("is-revealed") ? el.textContent : "blank");
      } else {
        parts.push(el.textContent);
      }
    });
    return parts.join(" ").replace(/\s+([.,!?])/g, "$1");
  }

  body.addEventListener("click", function (e) {
    var btn = e.target.closest(".say-btn");
    if (btn && canSpeak) {
      var row = btn.closest(".say-row");
      speak(rowText(row), row);
      return;
    }
    var word = e.target.closest(".w");
    if (word && canSpeak) {
      var clean = word.textContent.replace(/^[^A-Za-z0-9$]+|[^A-Za-z0-9%]+$/g, "");
      if (clean) speak(clean, word);
    }
  });

  // ---------------------------------------------------------------------
  // Play a whole conversation, one voice per speaker
  // ---------------------------------------------------------------------
  function resetDialogueButtons() {
    body.querySelectorAll("[data-dialogue-play]").forEach(function (b) {
      b.classList.remove("is-playing");
      b.innerHTML = "&#9654; Play the conversation";
    });
  }

  body.querySelectorAll("[data-dialogue]").forEach(function (dialogue) {
    var button = dialogue.querySelector("[data-dialogue-play]");
    if (!button) return;
    if (!canSpeak) { button.hidden = true; return; }
    button.addEventListener("click", function () {
      if (button.classList.contains("is-playing")) { stopSpeaking(); return; }
      var speakers = [];
      var pieces = [];
      dialogue.querySelectorAll(".dialogue-turn").forEach(function (turn) {
        var who = turn.getAttribute("data-speaker");
        if (speakers.indexOf(who) === -1) speakers.push(who);
        var gender = speakers.indexOf(who) % 2 === 0 ? settings.gender : otherGender(settings.gender);
        pieces.push({ text: rowText(turn), gender: gender, el: turn });
      });
      resetDialogueButtons();
      button.classList.add("is-playing");
      button.innerHTML = "&#9632; Stop";
      speakQueue(pieces, resetDialogueButtons);
    });
  });

  // ---------------------------------------------------------------------
  // Fill-in-the-gap exercises
  // ---------------------------------------------------------------------
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  body.querySelectorAll("[data-exercise]").forEach(function (exercise) {
    var bank = exercise.querySelector("[data-word-bank]");
    var blanks = Array.prototype.slice.call(exercise.querySelectorAll(".blank"));
    var feedback = exercise.querySelector("[data-feedback]");
    var originalChips = Array.prototype.slice.call(bank.querySelectorAll(".word-chip"));
    var selected = null;
    var mistakes = 0;

    function chips() { return Array.prototype.slice.call(bank.querySelectorAll(".word-chip:not(.is-used)")); }

    function select(chip) {
      if (selected) selected.classList.remove("is-selected");
      selected = chip && chip !== selected ? chip : null;
      if (selected) {
        selected.classList.add("is-selected");
        blanks.forEach(function (b) { if (!b.classList.contains("is-correct")) b.classList.add("is-target"); });
      } else {
        blanks.forEach(function (b) { b.classList.remove("is-target"); });
      }
    }

    function setFeedback(text, kind) {
      feedback.textContent = text;
      feedback.className = "exercise-feedback" + (kind ? " is-" + kind : "");
    }

    function blankNumber(blank) { return blanks.indexOf(blank) + 1; }

    function place(chip, blank) {
      if (!chip || !blank || blank.classList.contains("is-correct") || blank.classList.contains("is-revealed")) return;
      var word = chip.getAttribute("data-word");
      var answer = blank.getAttribute("data-answer");
      select(null);

      if (word.toLowerCase() === answer.toLowerCase()) {
        blank.textContent = word;
        blank.classList.remove("is-wrong");
        blank.classList.add("is-correct");
        blank.setAttribute("aria-label", "Gap " + blankNumber(blank) + ": " + word + ", correct");
        chip.classList.add("is-used");
        chip.disabled = true;
        bank.classList.toggle("is-empty", chips().length === 0);
        var row = blank.closest(".say-row");
        if (blanks.every(function (b) { return b.classList.contains("is-correct"); })) {
          var msg = mistakes === 0 ? "Excellent! All correct on the first try." : "Well done! All correct.";
          setFeedback(msg, "done");
          speakQueue([{ text: rowText(row), el: row }, { text: "Well done!" }]);
        } else {
          setFeedback("Correct!", "correct");
          speak(rowText(row), row);
        }
      } else {
        mistakes++;
        blank.textContent = word;
        blank.classList.remove("is-wrong");
        void blank.offsetWidth; // restart the shake animation
        blank.classList.add("is-wrong");
        setFeedback("Not quite. Try another word.", "wrong");
        setTimeout(function () {
          if (blank.classList.contains("is-wrong")) {
            blank.classList.remove("is-wrong");
            blank.textContent = "";
          }
        }, reduceMotion ? 1200 : 900);
      }
    }

    // Tap a word to pick it (and hear it), then tap a gap.
    bank.addEventListener("click", function (e) {
      var chip = e.target.closest(".word-chip");
      if (!chip || chip.disabled) return;
      if (suppressClick) { suppressClick = false; return; }
      select(chip);
      if (selected && canSpeak) speak(chip.getAttribute("data-word"), chip);
    });

    exercise.addEventListener("click", function (e) {
      var blank = e.target.closest(".blank");
      if (blank && selected) place(selected, blank);
    });

    // Drag with mouse, finger or pen.
    var drag = null;
    var suppressClick = false;

    bank.addEventListener("pointerdown", function (e) {
      var chip = e.target.closest(".word-chip");
      if (!chip || chip.disabled || (e.pointerType === "mouse" && e.button !== 0)) return;
      drag = { chip: chip, x: e.clientX, y: e.clientY, ghost: null, over: null, id: e.pointerId };
    });

    function blankAt(x, y) {
      var el = document.elementFromPoint(x, y);
      var blank = el && el.closest ? el.closest(".blank") : null;
      return blank && exercise.contains(blank) ? blank : null;
    }

    window.addEventListener("pointermove", function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.ghost) {
        if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) < 6) return;
        select(null);
        var rect = drag.chip.getBoundingClientRect();
        drag.offsetX = drag.x - rect.left;
        drag.offsetY = drag.y - rect.top;
        drag.ghost = drag.chip.cloneNode(true);
        drag.ghost.className = "word-chip word-chip--ghost";
        drag.ghost.style.width = rect.width + "px";
        document.body.appendChild(drag.ghost);
        drag.chip.classList.add("is-dragging");
        blanks.forEach(function (b) { if (!b.classList.contains("is-correct")) b.classList.add("is-target"); });
        if (canSpeak) speak(drag.chip.getAttribute("data-word"), null);
      }
      e.preventDefault();
      drag.ghost.style.transform =
        "translate(" + (e.clientX - drag.offsetX) + "px," + (e.clientY - drag.offsetY) + "px)";
      var over = blankAt(e.clientX, e.clientY);
      if (over !== drag.over) {
        if (drag.over) drag.over.classList.remove("is-over");
        if (over) over.classList.add("is-over");
        drag.over = over;
      }
    }, { passive: false });

    function endDrag(e, cancelled) {
      if (!drag || e.pointerId !== drag.id) return;
      var d = drag;
      drag = null;
      if (!d.ghost) return; // it was a tap; the click handler deals with it
      suppressClick = true;
      setTimeout(function () { suppressClick = false; }, 0);
      d.ghost.remove();
      d.chip.classList.remove("is-dragging");
      if (d.over) d.over.classList.remove("is-over");
      blanks.forEach(function (b) { b.classList.remove("is-target"); });
      if (!cancelled) place(d.chip, blankAt(e.clientX, e.clientY));
    }
    window.addEventListener("pointerup", function (e) { endDrag(e, false); });
    window.addEventListener("pointercancel", function (e) { endDrag(e, true); });

    // Desktop drag and drop with the mouse also works through the handlers
    // above; stop the browser's own image/text drag from interfering.
    bank.addEventListener("dragstart", function (e) { e.preventDefault(); });

    exercise.querySelector("[data-show-answers]").addEventListener("click", function () {
      select(null);
      blanks.forEach(function (b) {
        if (!b.classList.contains("is-correct")) {
          b.textContent = b.getAttribute("data-answer");
          b.classList.remove("is-wrong");
          b.classList.add("is-revealed");
        }
      });
      chips().forEach(function (c) { c.classList.add("is-used"); c.disabled = true; });
      bank.classList.add("is-empty");
      setFeedback("Here are the answers. Press the speaker buttons to hear each sentence.", "");
    });

    exercise.querySelector("[data-reset]").addEventListener("click", function () {
      stopSpeaking();
      select(null);
      mistakes = 0;
      blanks.forEach(function (b, i) {
        b.textContent = "";
        b.className = "blank";
        b.setAttribute("aria-label", "Gap " + (i + 1) + ", empty");
      });
      // Shuffle the words again.
      var order = originalChips.slice();
      for (var i = order.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = order[i]; order[i] = order[j]; order[j] = t;
      }
      order.forEach(function (c) {
        c.classList.remove("is-used", "is-selected", "is-dragging");
        c.disabled = false;
        bank.appendChild(c);
      });
      bank.classList.remove("is-empty");
      setFeedback("", "");
    });
  });
})();
