

cline-d2 = "vars: {
  d2-config: {
    dark-theme-id: 200
  }
}

start: {shape: diamond; label: "Is Cline, Roo Code acting dumb?"}
openApp: {shape: rectangle; label: "Type `aicp` + Enter in VS Code terminal to open the app."}
filesSelected: {shape: rectangle; label: "Code files will be already selected."}
promptBox: {
  shape: rectangle
  label: "Type your problem into the prompt box, add or subtract any extra files you think it might need."
}
clickPreset: {
  shape: rectangle
  label: "Click the Cline/Roo Code prompt preset button ('Write a prompt for Cline, an AI coding agent, to make the necessary changes. Enclose the entire Cline prompt in one single code tag for easy copy and paste.')"
}
clickGenerateContext: {shape: rectangle; label: "Click GENERATE CONTEXT."}
pasteIntoGemini: {
  shape: rectangle
  label: "Paste into Gemini in AI Studio (or Deepseek, o3 on OpenAI Playground, Claude, Grok, etc.)."
}
solutionBack: {
  shape: rectangle
  label: "If it solves your problem, cut & paste it back into Cline set on GPT-4.1 to save."
}
end: {shape: circle; label: "Continue working normally."}

start -> openApp: "Yes" {
  style.stroke-dash: 5
  style.animated: true
}
start -> end: "No" {
  style.stroke-dash: 5
  style.animated: true
}
openApp -> filesSelected: {
  style.stroke-dash: 5
  style.animated: true
}
filesSelected -> promptBox: {
  style.stroke-dash: 5
  style.animated: true
}
promptBox -> clickPreset: {
  style.stroke-dash: 5
  style.animated: true
}
clickPreset -> clickGenerateContext: {
  style.stroke-dash: 5
  style.animated: true
}
clickGenerateContext -> pasteIntoGemini: {
  style.stroke-dash: 5
  style.animated: true
}
pasteIntoGemini -> solutionBack: {
  style.stroke-dash: 5
  style.animated: true
}
```
"
d2-icon-angry = "https://icons.terrastruct.com/emotions%2F001-angry.svg"

d2-icon-smile = "https://icons.terrastruct.com/emotions%2F002-smile.svg"

d2-icon-file ="https://icons.terrastruct.com/essentials%2F257-file.svg"

