# 📘 PRD — NeonRelay Agents
Multi-Agent System for Intelligent Email Automation for **ONG Amazonia**

## 1. 🎯 Purpose & Vision

**Context:**  
**ONG Amazonia** needs to scale email communication with donors, volunteers, and community members. Today, the process is fully manual, slow, and impossible to measure. The team spends valuable time responding to repetitive messages, limiting the organization’s impact.

**Vision:**  
Build an orchestrated multi-agent system that generates, validates, and delivers emails aligned with the mission of ONG Amazonia — fully observable, fully measurable, and operationally efficient.

**Mission:**  
Use Google ADK + Gemini to automate communication flows without losing empathy, accuracy, or institutional consistency.

---

## 2. ⚠ Problem Statement

**Context:**  
**ONG Amazonia** faces operational and digital engagement challenges. The growing volume of questions from volunteers, donors, and community members consumes the team’s time and reduces overall efficiency. Even with strong motivation and commitment, the team can’t keep up with the increasing demand at the speed users expect.

**Current Situation:**  
Team members spend hours every week answering repetitive questions — from how to join an expedition, to how donations work, to details about ongoing campaigns. This manual workload delays responses and negatively impacts people who want to contribute, donate, or get involved with the organization’s activities.

**Impact:**  
This operational bottleneck decreases donor and volunteer conversion rates, disrupts communication flow, and weakens the perception of agility and empathy that **ONG Amazonia** aims to convey. The lack of standardized messaging also creates inconsistencies and prevents the organization from understanding what works and what needs improvement.

**Proposed Solution:**  
Deploy a system of **autonomous agents** capable of automating frequent responses and full email workflows in an empathetic, contextualized, and mission-aligned way. The system delivers fast, high-quality communication supported by complete observability — eliminating guesswork and enabling data-driven optimization.

**Hypothesis:**  
If the system automates **70% of frequent interactions**, conversion rates could increase by **30%**, and response time could be reduced by **50%**, significantly strengthening engagement with the community, volunteers, and donors.

---

## 3. 👥 Target Audience

**Donors:** seek transparency and clear impact.  
**Volunteers:** require instructions, reminders, and onboarding.  
**Community:** expects updated information in their preferred language.

---

## 4. 💡 User Needs

Different groups require timely, trustworthy, personalized, and empathetic communication aligned with ONG Amazonia’s mission and values.

---

## 4.1 The Build — How It Was Created & Technologies Used

NeonRelay Agents was designed and built with a modular, production-ready approach using Google’s AI ecosystem.

**Key Technologies:**
- Google ADK (Agents Development Kit)
- Gemini
- Custom ADK Tools (CRM DB + Email API)
- InMemorySessionService
- Memory Bank
- Agent-to-Agent Protocol
- Observability stack (logs, traces, metrics)

---

## 4.2 Overall Architecture

**1. Orchestrator Agent**  
Receives events, selects the correct pipeline, manages sequence, parallel execution, and retries.

**2. Segmentation Agent**  
Classifies the contact as donor, volunteer, or community.  
Detects language and interests using CRM data.

**3. Content Agent (Gemini)**  
Generates personalized subject lines, body text, and CTAs aligned with ONG Amazonia’s mission.

**4. Compliance & Tone Agent**  
Validates tone, clarity, factual correctness, and alignment with organizational values.

**5. Delivery & Scheduling Agent**  
Interfaces with the Email API. Sends or schedules emails.

Supporting infrastructure includes CRM DB, Observability, Email APIs, and Memory Bank.

---

## 5. 💎 Value Proposition

**For ONG Amazonia:**  
Reliable automation, consistent messaging, operational efficiency, and real data to drive improvements.

**For users:**  
Clear, timely, empathetic communication tailored to their needs and language.

---

## 6. 📊 Success Metrics

**Technical Metrics:**  
- End-to-end latency < 3 seconds  
- Validation loops < 2  
- Email tool errors < 2%  
- Agent latency < 1 second

**Impact Metrics:**  
- +30% open rate  
- +15% CTA clicks  
- +20% volunteer engagement  
- –50% manual workload

