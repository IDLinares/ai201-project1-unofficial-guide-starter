# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Domain: Activities to do at/around the University of Florida
This knowledge is valuable cause it lets students know what kind of activities and experiences they can do in their free-time when attending the University of Florida and for who and when these activities are appropriate. Although you can find some events happening on campus through official channels, knowing all of the possible activites to do around Gainesville can be useful to know the full extent of what Gainesville has to offer. Many people consider Gainesville to just be the University of Florida, but there are a lot of different things to do on and around campus.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source              | Description                                                                                    | URL or location                                                                                                 |
| --- | ------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1   | URL                 | Blog providing accessible activities around Gainesville for Seniors.                           | https://thevillagegainesville.com/blog/day-trips-for-seniors/                                                   |
| 2   | GNV Subreddit       | Reddit post providing a list of a best of different kinds of food in Gainesville.              | https://www.reddit.com/r/GNV/comments/1ldgqxr/best_food_and_locations_in_gainesville_2025/                      |
| 3   | URL                 | Blog describing the best local food in Gainesville.                                            | https://www.themayfairgainesvillefl.com/blog/2026/gainesville-food-guide-best-local-eats-for-new-residents.html |
| 4   | GNV Subreddit       | Reddit post with comments for budget options for things to do around Gainesville.              | https://www.reddit.com/r/GNV/comments/171j93p/fun_hidden_gems_in_gnv_that_are_cheapfree/                        |
| 5   | GNV Subreddit       | Another Reddit post with most budget options of activities around Gainesville.                 | https://www.reddit.com/r/GNV/comments/1etmfsi/ideas_for_fun_things_to_do_in_gainesville_that/                   |
| 6   | URL                 | Blog prodiving options of outdoor activites to do near the University of Florida.              | https://www.staygainesville.com/best-outdoor-things-to-do-near-uf-a-freshmans-guide                             |
| 7   | Forum               | A Quora forums with people describing activities to do on the weekends as a student at UF.     | https://www.quora.com/What-are-the-best-things-to-do-on-weekends-as-a-student-at-the-University-of-Florida      |
| 8   | URL                 | Blog with Live Music and Performing Arts activities at and around UF.                          | https://www.visitgainesville.com/things-to-do/live-music-performing-arts/                                       |
| 9   | URL/FAQ             | General blog with all kinds of activities and descriptions of things to do around Gainesville. | https://www.visitflorida.com/places-to-go/north-central/gainesville/                                            |
| 10  | TripAdvisor Reviews | List of indoor activities to do around the University of Florida.                              | https://www.tripadvisor.com/Attractions-g34242-Activities-zft11295-Gainesville_Florida.html                     |
| 11  | URL                 | Blog describing things to do with your parents/the family when visiting UF.                    | https://sweetwatergainesville.com/resources/things-to-do-with-parents-uf/                                       |
| 12  | URL                 | Blog describing activities to do with kids around the University of Florida.                   | https://sweetwaterinn.com/blog/things-to-do-in-gainesville-fl-with-kids/                                        |
| 13  | URL                 | Blog describing activities to do in downtown Gainesville.                                      | https://sweetwaterinn.com/blog/gainesville-fl-downtown/                                                         |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
