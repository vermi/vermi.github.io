---
layout: post
title: "Building the Future: Developing an Applied Cybersecurity Curriculum with Labtainers"
date: 2025-03-29
categories: [education, cybersecurity, tutorials]
---

# Building the Future: Developing an Applied Cybersecurity Curriculum with Labtainers

Last month, I wrapped up development on a new Applied Cybersecurity curriculum that I'm pretty excited about. I wanted to share my experience aligning this course with CompTIA Security+ objectives while leveraging the excellent Labtainers platform. If you're an educator in the cybersecurity space (or adjacent to it), hopefully this post gives you some ideas and motivation to develop your own hands-on curriculum.

## The Why: More Than Just Another Tech Course

My advisor, Dr. Lorie Liebrock (Director of the New Mexico Cybersecurity Center of Excellence), and I had discussed this curriculum for several years. Our motivation was simple but powerful: help students—particularly those from underprivileged backgrounds here in New Mexico—gain practical cybersecurity skills that can lead to meaningful careers.

The reality is that these skills open doors. Cybersecurity positions remain unfilled across the country, and certifications like Security+ can help students get their foot in the door. For many of our students, this could be the opportunity that helps break cycles of economic hardship while also establishing New Mexico as a hub for cybersecurity education and talent.

## Discovering Labtainers: A Game-Changer for Hands-on Learning

A colleague first pointed me toward [Labtainers](https://nps.edu/web/c3o/labtainers), developed by the Naval Postgraduate School's Center for Cybersecurity and Cyber Operations. After exploring the platform, it was honestly a no-brainer to build our curriculum around it.

What makes Labtainers stand out?

1. **Pre-built, focused lab environments** that isolate specific cybersecurity concepts
2. **Consistent execution environments** that just work (if you've ever tried to get 30 different student environments functioning identically, you know what a miracle this is)
3. **Automated assessment capabilities** for certain labs
4. **Easy deployment as a virtual appliance** that can be run on various host operating systems
5. **Comprehensive coverage** of key security domains from network security to cryptography

Best of all, it's **free** and **regularly updated**. The quality and thought that went into these lab environments is immediately apparent.

## Aligning Labs with Security+ Objectives: The Hard Part

With Labtainers selected as our platform, the next challenge was mapping specific labs to the CompTIA Security+ (SY0-701) exam objectives. This was genuinely the most time-consuming part of curriculum development.

Have you seen the Security+ exam objectives document? It's comprehensive (to put it mildly). We went through each section methodically:

- 1.0 General Security Concepts (12%)
- 2.0 Threats, Vulnerabilities, and Mitigations (22%)
- 3.0 Security Architecture (18%)
- 4.0 Security Operations (28%)
- 5.0 Security Program Management and Oversight (20%)

For each objective, we asked: "Which Labtainer lab best demonstrates this concept?" Sometimes the answer was obvious — the `onewayhash` lab clearly aligns with cryptographic objectives. Other times we had to get creative, combining labs or supplementing with CyberCIEGE scenarios (another excellent platform with more scenario-based learning).

## Theory Meets Practice: Why Hands-on Labs Matter

You can teach theory all day long, but there's nothing like getting your hands dirty with practical exercises. As I designed this curriculum, I kept coming back to this truth: failure in a controlled environment is one of the most powerful learning tools we have.

We've done our students a disservice by creating educational environments where failure is avoided at all costs. The reality is that all of us fail, constantly, especially in cybersecurity where you're often working with incomplete information against adversaries who only need to succeed once.

Labtainers creates that safe space for experimentation. Students can break things, fix them, and develop the troubleshooting mindset that's essential in this field. When a student misconfigures a firewall in the `iptables2` lab and suddenly can't access services they need, that lesson sticks with them far more effectively than reading about proper firewall configuration in a textbook.

## Beyond the Certification: Advanced Topics

While preparing students for Security+ certification was a primary goal, we didn't stop there. The curriculum also introduces students to advanced topics like:

- **Industrial Control System (ICS) security** using specialized Labtainer environments
- **Security automation and orchestration** concepts
- **Advanced forensics** techniques
- **Security architecture design**

These topics give students exposure to specialized areas they might want to pursue further, while still building on the solid foundation that Security+ provides.

## Moving Forward and Advice for Others

I'll be testing this curriculum live in the Fall semester, and I'm genuinely excited to see how students respond. I'll definitely post again with updates on what works and what needs refinement.

For other educators considering a similar path, here's my advice:

1. **Just start.** Don't wait for the perfect lab platform or perfect curriculum alignment. Begin with what you have, test it, and iterate.

2. **Leverage existing resources.** Platforms like Labtainers save you from reinventing the wheel. My colleague who uses them in professional certification bootcamps raves about their effectiveness.

3. **Balance theory and practice.** Make sure students understand why they're performing specific tasks in the labs, not just how to complete them.

4. **Create space for failure.** Some of the best learning happens when students have to troubleshoot problems they've created themselves.

5. **Keep the end goal in mind.** For us, it's helping students build skills that lead to opportunities. Every lab and lecture should contribute to that mission.

I'll be back in the fall with an update on how the first cohort does with this curriculum. Until then, happy hacking (ethically, of course)!
