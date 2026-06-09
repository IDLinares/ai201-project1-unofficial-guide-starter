# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Domain: Activities to do at/around the University of Florida
This knowledge is valuable cause it lets students know what kind of activities and experiences they can do in their free-time when attending the University of Florida and for who and when these activities are appropriate. Although you can find some events happening on campus through official channels, knowing all of the possible activites to do around Gainesville can be useful to know the full extent of what Gainesville has to offer. Many people consider Gainesville to just be the University of Florida, but there are a lot of different things to do on and around campus.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source                        | Description/Type                                                                               | URL or Location                                                                                                 |
| --- | ----------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1   | URL - The Village Gainesville | Blog providing accessible activities around Gainesville for Seniors.                           | https://thevillagegainesville.com/blog/day-trips-for-seniors/                                                   |
| 2   | GNV Subreddit                 | Reddit post providing a list of a best of different kinds of food in Gainesville.              | https://www.reddit.com/r/GNV/comments/1ldgqxr/best_food_and_locations_in_gainesville_2025/                      |
| 3   | URL - The Mayfair Gainesville | Blog describing the best local food in Gainesville.                                            | https://www.themayfairgainesvillefl.com/blog/2026/gainesville-food-guide-best-local-eats-for-new-residents.html |
| 4   | GNV Subreddit                 | Reddit post with comments for budget options for things to do around Gainesville.              | https://www.reddit.com/r/GNV/comments/171j93p/fun_hidden_gems_in_gnv_that_are_cheapfree/                        |
| 5   | GNV Subreddit                 | Reddit post with most budget options of activities around Gainesville.                         | https://www.reddit.com/r/GNV/comments/1etmfsi/ideas_for_fun_things_to_do_in_gainesville_that/                   |
| 6   | URL - Stay Gainesville        | Blog prodiving options of outdoor activites to do near the University of Florida.              | https://www.staygainesville.com/best-outdoor-things-to-do-near-uf-a-freshmans-guide                             |
| 7   | URL - Visit Gainesville       | Blog with Live Music and Performing Arts activities at and around UF.                          | https://www.visitgainesville.com/things-to-do/live-music-performing-arts/                                       |
| 8   | URL/FAQ - Visit Florida       | General blog with all kinds of activities and descriptions of things to do around Gainesville. | https://www.visitflorida.com/places-to-go/north-central/gainesville/                                            |
| 9   | TripAdvisor Reviews           | List of indoor activities to do around the University of Florida.                              | https://www.tripadvisor.com/Attractions-g34242-Activities-zft11295-Gainesville_Florida.html                     |
| 10  | URL - Sweetwater Gainesville  | Blog describing things to do with your parents/the family when visiting UF.                    | https://sweetwatergainesville.com/resources/things-to-do-with-parents-uf/                                       |
| 11  | URL - Sweetwater Inn          | Blog describing activities to do with kids around the University of Florida.                   | https://sweetwaterinn.com/blog/things-to-do-in-gainesville-fl-with-kids/                                        |
| 12  | URL - Sweetwater Inn          | Blog describing activities to do in downtown Gainesville.                                      | https://sweetwaterinn.com/blog/gainesville-fl-downtown/                                                         |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
600 characters
**Overlap:**
100 characters
**Why these choices fit your documents:**
Most of the documents are lists with small paragraph descriptions of the specific activity or kinds of activities, so I kept the chunk size moderate, so each chunk stays focused on a single activity. I added a small overlap for some of the longer descriptions and FAQS in the blogs just in case and to follow the standard 10-20% rule for overlap. For the actual chunking strategy, I believe a recursive strategy would be best since sometimes many of the documents are broken up into sections of lists for the different activities with their descriptions inside these sections. It would follow the natural structure of the document for the majority of my sources.

For most of the sources, I needed to clean the texts to remove extra URLS, decode "&amps", and especially remove any promotional sections for blogs, such as promoting a stay at a certain hotel as that introduces bias not relevant to my domain. I also standardized the headers since I am using a recursive structure and the headers are important to the context of much of the information.

After an initial test, I decided to drop the chunk count just a little more. Most of the chunks had just a bit too much information than necessary since the descriptions under most headers across Reddit posts and blogs were a bit more brief than 700 characters. To match queries a bit more specifically, I dropped the chunk size 100 characters and the overlap by 50 to keep a 10-20% overlap of the chunk size.

The strategy will go as follows: Paragraph breaks (\n\n) -> Line breaks (\n) -> Sentences -> Characters.
**Final chunk count:**
175 Chunks

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
sentence-transformers (all-MiniLM-L6-v2) - The local embedding model we are using for class since it runs locally with no rate limits.

For structuring my embeddings, I will do one embedding per chunk, the standard. Then, to account for the structure of most of my sources, I will prepend the section or source context to the chunk before embedding.
**Production tradeoff reflection:**
If deploying a RAG system regarding activities to do around UF for real users without a cost constraint, here are tradeoffs I would consider:

- Context Length: Considering most of the information comes in smaller chunks as it is short descriptions of activities to do around UF, I would lean towards a smaller, lightweight model, such as all-MiniLM-L6-v2, as the chunks would be nowhere near the maximum context window. Context length would not be a limiting factor.
- Multilingual Support: For the scope of this kind of project, I would lean towards a single language English model since it would most likely be accessible to the majority of students at UF. However, taking into account the large number of international students at UF, without a cost constraint, a multilingual model would further my accessibility. International students would be most likely to query in another language, so it could be something to factor in if I want to maximize the RAG system's reach.
- Accuracy on domain-specific text: Although the activities themselves, such as food, hikes, etc., might not be super specific or technical, many of the locations around Gainesville can have local place names. Also, posts from students can use local slang or informal talk, so a larger model, such as OpenAI text-embedding-3-large, would be considered to ensure any casual query can match a hyper specific location. For this particular situation, MiniLM is most likely sufficient, but a larger model could guarantee better coverage.
- Latency: For these kinds of queries, we would like faster processing times to quickly provide information on the activities in Gainvesville, so a lightweight and fast model like we are using is preferred.
- Local vs API-hosted: Even without a cost-constraint, this is a very small and domain specific RAG system, so a local model would still suffice. Context windows would not need to be very large and no super demanding computations would be required to answer the majority of queries, so they should still answer relatively quicky. An API-hosted model could be considered only in the case if it is needed to understand specific local slang and location data.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | -------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   |          |                 |                              |                   |                   |
| 2   |          |                 |                              |                   |                   |
| 3   |          |                 |                              |                   |                   |
| 4   |          |                 |                              |                   |                   |
| 5   |          |                 |                              |                   |                   |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_

**Instance 2**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_
