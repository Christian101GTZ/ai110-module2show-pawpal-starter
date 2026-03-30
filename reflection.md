# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design waS TO create four classes whihc are Owner,Pet, Task and Scheduler. I made sure to mapped the attirbute methods and show how they connect.  
- What classes did you include, and what responsibilities did you assign to each?
I included four classes. Owner is responsible for storing the person's name and available time per day. Pet is responsible for holding the animal's information and its list of care tasks. Task is responsible for representing a single care activity with a name, duration, priority, and category. Scheduler is responsible for taking the Owner and Pet and generating a prioritized daily plan that fits within the owner's available time.

**b. Design changes**

- Did your design change during implementation? Yes I did make modifications.
- If yes, describe at least one change and why you made it.
I chnaged the scheduler to accept a list of pets instead of a single one. The original design only accpeted one pet a time but many ownser can have multiple pets.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The conflict detector only flags tasks with the exact same start time. It does not catch overlapping durations, so a 30-minute task at 08:00 and a task at 08:15 would not trigger a warning.

- Why is that tradeoff reasonable for this scenario?
For a simple pet care planner, exact-time matching is easy to understand and covers the most common mistakes. Duration-aware overlap detection would add complexity that is not needed at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
