---
name: fm-homework
description: Turns a photo of school material into a lesson plan or extra exercises for a specific child. Use when the user sends a photo together with words like "dever", "aula", "escola", "atividade", or otherwise asks for help with a kid's schoolwork.
---

# Homework Helper — skeleton

This is the thin-skeleton version: acknowledge the photo and return one
generic exercise, proving the image reaches the model and the chat round
trip works. Reading the photo's real content and adapting it per child
lands later (US-14).

## Post

Reply confirming the photo was received, then include at least one
generic, age-neutral exercise (e.g. "Write 3 sentences using today's new
word"). Do not attempt to identify the subject or grade from the photo yet.

Always include the generic exercise, even if the photo looks unclear,
low quality, or hard to read — do not stop to ask for a better photo or
for details instead. Legibility handling is out of scope for this
skeleton; it lands with the real image-reading logic later.
