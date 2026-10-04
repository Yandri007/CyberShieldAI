(() => {
  const config = JSON.parse(document.getElementById("assessment-config").textContent);
  const home = document.getElementById("home");
  const assessment = document.getElementById("assessment");
  const results = document.getElementById("results");
  const panels = Array.from(document.querySelectorAll(".question-panel"));
  const answers = Object.create(null);
  let activeIndex = 0;
  let lastAssessment = null;

  const get = (id) => document.getElementById(id);
  const screens = [home, assessment, results];

  function showScreen(screen) {
    screens.forEach((item) => { item.hidden = item !== screen; });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function answerFor(panel) {
    return answers[panel.dataset.questionId];
  }

  function paintQuestion() {
    panels.forEach((panel, index) => { panel.hidden = index !== activeIndex; });
    const current = panels[activeIndex];
    get("question-area").textContent = current.dataset.group;
    get("question-step").textContent = `Question ${activeIndex + 1} of ${panels.length}`;
    get("progress-count").textContent = `Question ${activeIndex + 1} of ${panels.length}`;
    const progress = ((activeIndex + 1) / panels.length) * 100;
    get("progress-percent").textContent = `${Math.round(progress)}%`;
    get("progress-fill").style.width = `${progress}%`;
    get("back-button").disabled = activeIndex === 0;
    get("next-button").hidden = activeIndex === panels.length - 1;
    get("analyze-button").hidden = activeIndex !== panels.length - 1;
    const saved = answerFor(current);
    current.querySelectorAll('input[type="radio"]').forEach((input) => {
      input.checked = input.value === saved;
    });
  }

  function moveToFirstMissing() {
    const missingIndex = panels.findIndex((panel) => !answerFor(panel));
    if (missingIndex !== -1) {
      activeIndex = missingIndex;
      showScreen(assessment);
      paintQuestion();
      showQuestionError(panels[missingIndex]);
      return false;
    }
    return true;
  }

  function showQuestionError(panel) {
    const error = get(`error-${panel.dataset.questionId}`);
    error.hidden = false;
    panel.classList.add("question-panel-invalid");
    panel.querySelectorAll("input[type=radio]").forEach((input) => input.setAttribute("aria-invalid", "true"));
    panel.querySelector("input[type=radio]").focus();
  }

  function hideQuestionError(panel) {
    get(`error-${panel.dataset.questionId}`).hidden = true;
    panel.classList.remove("question-panel-invalid");
    panel.querySelectorAll("input[type=radio]").forEach((input) => input.removeAttribute("aria-invalid"));
  }

  function makeElement(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function renderRisk(finding, index) {
    const card = makeElement("article", `risk-card risk-${finding.priority}`);
    const top = makeElement("div", "risk-card-top");
    const number = makeElement("span", "risk-number", String(index + 1).padStart(2, "0"));
    const tags = makeElement("div", "risk-tags");
    tags.append(
      makeElement("span", `priority-tag priority-${finding.priority}`, `${finding.priority_label} priority`),
      makeElement("span", `certainty-tag certainty-${finding.certainty}`, finding.certainty_label),
    );
    top.append(number, tags);
    const title = makeElement("h3", "risk-title", finding.area);
    const reason = makeElement("p", "risk-reason", finding.reason);
    card.append(top, title, reason);
    return card;
  }

  function renderAssessment(result) {
    lastAssessment = result;
    get("score-value").textContent = Number.isInteger(result.score) ? String(result.score) : result.score.toFixed(2).replace(/0+$/, "").replace(/\.$/, "");
    get("status-label").textContent = result.status;
    get("status-description").textContent = result.status_description;
    get("finding-count").textContent = result.findings.length;
    get("score-visual").dataset.status = result.status_id;
    get("score-visual").style.setProperty("--score-angle", `${result.score * 3.6}deg`);
    get("status-dot").dataset.status = result.status_id;

    const riskList = get("risk-list");
    riskList.replaceChildren();
    const topRisks = result.findings.slice(0, 3);
    topRisks.forEach((finding, index) => riskList.append(renderRisk(finding, index)));
    const otherRisks = get("other-risks");
    const otherRiskList = get("other-risk-list");
    otherRiskList.replaceChildren();
    result.findings.slice(3).forEach((finding) => {
      const row = makeElement("article", "other-risk-row");
      const copy = makeElement("div", "other-risk-copy");
      copy.append(makeElement("strong", "", finding.area), makeElement("span", "", finding.reason));
      const labels = makeElement("div", "risk-tags");
      labels.append(
        makeElement("span", `priority-tag priority-${finding.priority}`, `${finding.priority_label} priority`),
        makeElement("span", `certainty-tag certainty-${finding.certainty}`, finding.certainty_label),
      );
      row.append(copy, labels);
      otherRiskList.append(row);
    });
    otherRisks.hidden = result.findings.length <= 3;
    get("risk-count").textContent = result.findings.length ? `${result.findings.length} ${result.findings.length === 1 ? "finding" : "findings"}` : "Clear overview";

    const positive = get("positive-note");
    const noMore = get("no-more-risks");
    const riskIntro = get("risk-intro");
    positive.hidden = result.findings.length !== 0;
    noMore.hidden = result.findings.length === 0 || result.findings.length > 3;
    if (result.findings.length === 0) {
      riskIntro.textContent = "Your answers did not identify any significant gaps that need attention right now.";
    } else if (result.findings.length === 1) {
      riskIntro.textContent = "This is the main finding from your answers. The certainty label shows whether it is a confirmed gap or something to verify.";
    } else {
      riskIntro.textContent = "These findings are ordered by potential impact and your answer. “Needs verification” means the control should be checked; it does not confirm that it is missing.";
    }

    const areaList = get("area-list");
    areaList.replaceChildren();
    result.areas.forEach((area) => {
      const row = makeElement("div", `area-row area-${area.signal}`);
      const marker = makeElement("span", "area-marker", area.signal === "in_place" ? "✓" : area.signal === "confirmed_gap" ? "!" : "?");
      marker.setAttribute("aria-hidden", "true");
      const text = makeElement("div", "area-row-copy");
      text.append(makeElement("strong", "", area.name), makeElement("span", "", area.signal_label));
      const answer = makeElement("span", "area-answer", area.answer_label);
      row.append(marker, text, answer);
      areaList.append(row);
    });
    showScreen(results);
    get("results-title").focus({ preventScroll: true });
  }

  function renderAction(action, index) {
    const card = makeElement("article", `plan-card plan-${action.kind}`);
    const top = makeElement("div", "plan-card-top");
    const number = makeElement("span", "plan-number", String(index + 1).padStart(2, "0"));
    const tags = makeElement("div", "plan-tags");
    tags.append(makeElement("span", `action-kind kind-${action.kind}`, action.kind_label));
    if (action.priority_label) {
      tags.append(makeElement("span", `priority-tag priority-${action.priority}`, `${action.priority_label} priority`));
      tags.append(makeElement("span", `certainty-tag certainty-${action.certainty}`, action.certainty_label));
    }
    top.append(number, tags);

    const addressed = makeElement(
      "p",
      action.risk_id ? "action-risk-linked" : "action-risk-preventive",
      action.risk_id ? `Risk addressed: ${action.risk_addressed}` : `Preventive guidance: ${action.risk_addressed}`,
    );
    const title = makeElement("h3", "plan-what-title", "What to do");
    const what = makeElement("p", "plan-what", action.what_to_do);
    const details = makeElement("div", "plan-detail-grid");
    const why = makeElement("div", "plan-detail");
    why.append(makeElement("strong", "", "Why it matters"), makeElement("p", "", action.why_it_matters));
    const how = makeElement("div", "plan-detail");
    how.append(makeElement("strong", "", "How to get started"), makeElement("p", "", action.how_to_start));
    details.append(why, how);
    card.append(top, addressed, title, what, details);
    return card;
  }

  function renderGuidance(guidance) {
    const planList = get("plan-list");
    planList.replaceChildren();
    guidance.actions.forEach((action, index) => planList.append(renderAction(action, index)));
    get("guidance-summary").textContent = guidance.summary;
    get("guidance-notice-text").textContent = guidance.notice || "";
    get("guidance-notice").hidden = !guidance.notice;
    get("plan-mode").textContent = guidance.mode === "ai" ? "AI explanations · fixed priorities" : "Rules-based action plan";
    get("retry-guidance").hidden = !guidance.can_retry;
    get("plan-footer").textContent = guidance.mode === "ai"
      ? "Your score, findings, priorities, and action mapping remain fixed by the assessment rules."
      : "These actions were selected from your answers using fixed rules. Preventive items are labeled and do not represent additional findings.";
    get("guidance-plan").hidden = false;
    get("guidance-entry").hidden = true;
    window.setTimeout(() => {
      get("guidance-title").focus({ preventScroll: true });
      get("guidance-plan").scrollIntoView({ behavior: "smooth", block: "start" });
    }, 0);
  }

  async function requestGuidance(trigger) {
    if (!lastAssessment) return;
    const button = trigger || get("get-guidance");
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    try {
      const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      const response = await fetch(config.guidanceUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify({ answers }),
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "We could not prepare your action plan. Please try again.");
      }
      renderGuidance(payload);
    } catch (error) {
      window.alert(error.message || "We could not reach the guidance service. Please try again.");
    } finally {
      button.disabled = false;
      button.removeAttribute("aria-busy");
    }
  }

  async function analyze() {
    if (!moveToFirstMissing()) return;
    const button = get("analyze-button");
    button.disabled = true;
    button.classList.add("button-loading");
    button.setAttribute("aria-busy", "true");
    try {
      const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      const response = await fetch(config.analyzeUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify({ answers }),
      });
      const payload = await response.json();
      if (!response.ok) {
        if (payload.question_id) {
          const index = panels.findIndex((panel) => panel.dataset.questionId === payload.question_id);
          if (index !== -1) {
            activeIndex = index;
            showScreen(assessment);
            paintQuestion();
            showQuestionError(panels[index]);
            return;
          }
        }
        throw new Error(payload.error || "We could not analyze these answers. Please try again.");
      }
      renderAssessment(payload);
    } catch (error) {
      window.alert(error.message || "We could not reach the assessment. Please try again.");
    } finally {
      button.disabled = false;
      button.classList.remove("button-loading");
      button.removeAttribute("aria-busy");
    }
  }

  get("start-assessment").addEventListener("click", () => {
    showScreen(assessment);
    paintQuestion();
    get("assessment-title").focus({ preventScroll: true });
  });
  get("back-button").addEventListener("click", () => {
    if (activeIndex > 0) {
      activeIndex -= 1;
      paintQuestion();
    }
  });
  get("next-button").addEventListener("click", () => {
    const panel = panels[activeIndex];
    if (!answerFor(panel)) {
      showQuestionError(panel);
      return;
    }
    hideQuestionError(panel);
    activeIndex += 1;
    paintQuestion();
  });
  get("analyze-button").addEventListener("click", analyze);
  get("get-guidance").addEventListener("click", () => requestGuidance());
  get("retry-guidance").addEventListener("click", (event) => requestGuidance(event.currentTarget));
  get("retake-assessment").addEventListener("click", () => {
    Object.keys(answers).forEach((key) => { delete answers[key]; });
    panels.forEach((panel) => {
      panel.querySelectorAll('input[type="radio"]').forEach((input) => { input.checked = false; });
      hideQuestionError(panel);
    });
    activeIndex = 0;
    lastAssessment = null;
    get("guidance-plan").hidden = true;
    get("guidance-entry").hidden = false;
    get("plan-list").replaceChildren();
    paintQuestion();
    showScreen(home);
    get("start-assessment").focus({ preventScroll: true });
  });

  panels.forEach((panel) => {
    panel.addEventListener("change", (event) => {
      if (event.target.matches('input[type="radio"]')) {
        answers[panel.dataset.questionId] = event.target.value;
        hideQuestionError(panel);
      }
    });
  });

  paintQuestion();
})();
