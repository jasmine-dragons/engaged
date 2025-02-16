import { HistoryItem } from "@/components/HistoryItem";
import { Analysis } from "@/lib/types";

const history: Analysis[] = [
  {
    transcript: [
      {
        what: "Alright class, settle down, settle down! Today, we're exploring the wonders of the Amazon rainforest.  It's the largest rainforest on Earth, a vast and incredibly diverse ecosystem. (Pause) Can anyone tell me what comes to mind when you think of the Amazon?",
      },
      { who: "Maria", what: "Um, lots of trees?" },
      {
        what: "Absolutely, Maria!  A *lot* of trees.  But it's so much more than just trees.  It's home to countless species of plants and animals, many of which are found nowhere else on the planet.  Think jaguars, sloths, colorful macaws… (Gestures)  It's a biodiversity hotspot.  And it plays a crucial role in regulating the Earth's climate.  So, it's really important that we protect it.  Any questions so far?",
      },
      { who: "David", what: "Yeah, what about deforestation?" },
      {
        what: "That's a very important question, David. Deforestation is a huge problem.  Trees are being cut down at an alarming rate, primarily for agriculture and cattle ranching.  This not only destroys habitats but also releases large amounts of carbon dioxide into the atmosphere, contributing to climate change. So, it's a complex issue, but one that we need to address.  We'll be discussing this more next week.",
      },
    ],
    summary:
      "The teacher introduces the Amazon rainforest, highlighting its size, biodiversity, and importance to the Earth's climate.  They discuss the issue of deforestation and its impact on the environment.",
    ratings: {
      talkSpeed: 130,
      emotion: 3,
      talkTimeRatio: 85,
      fillerWords: 7,
    },
    time: new Date("2024-10-27T09:15:00"),
  },
  {
    transcript: [
      {
        what: "Okay, so, today we're gonna talk about… (pause) …Shakespeare.  Specifically, Hamlet.  It's, like, one of the most famous plays ever written.  (Shrugs)  So, Hamlet, right? He's, um, the Prince of Denmark, and his dad, the king, gets, like, killed.  And, uh, Hamlet's, like, really upset about it, obviously.  So, he's, like, trying to figure out what happened, and, um, there's this ghost, right?  The ghost of his dad.  And the ghost tells him that, uh, his uncle, Claudius, killed him.  So, Hamlet's, like, gotta get revenge, but he's, like, really indecisive.  So, the whole play is about him trying to, like, decide what to do.  Get it?",
      },
      { who: "Sarah", what: "Kind of…" },
      {
        what: "Yeah, it's kinda complicated. We'll read it in class and it will make more sense, okay?",
      },
    ],
    summary:
      "The teacher provides a very basic and somewhat disorganized summary of the plot of Hamlet, focusing on the main characters and the central conflict of revenge.",
    ratings: {
      talkSpeed: 100,
      emotion: 2,
      talkTimeRatio: 75,
      fillerWords: 20,
    },
    time: new Date("2024-10-27T11:00:00"),
  },
  {
    transcript: [
      {
        what: "Good morning, everyone! Today, we're embarking on a journey through the fascinating world of quantum physics!  (Enthusiastically)  Now, I know what some of you might be thinking: 'Quantum physics?  That sounds complicated!'  And, well, it can be. But don't worry, we'll take it one step at a time.  We're going to explore some of the fundamental concepts, like wave-particle duality, superposition, and entanglement.  These ideas might seem a little strange at first, but they're absolutely essential to understanding how the universe works at the smallest scales.  (Slight pause)  Think about light, for example.  Sometimes it behaves like a wave, and sometimes it behaves like a particle.  That's wave-particle duality!  It's mind-blowing, isn't it?  (Chuckles)  And then there's superposition, which basically means that a quantum system can exist in multiple states at the same time.  It's like a coin spinning in the air – it's both heads and tails until it lands.  We'll delve into these concepts and many more, and I promise you'll leave here with a newfound appreciation for the weird and wonderful world of quantum mechanics!",
      },
      { who: "Michael", what: "So, like, is this stuff actually real?" },
      {
        what: "Absolutely, Michael!  It's not just theoretical.  Quantum physics has real-world applications that we use every day, from lasers to MRI machines.  It's the foundation of modern technology. So, yes, it's very real, and it's incredibly important.",
      },
    ],
    summary:
      "The teacher introduces quantum physics, emphasizing its importance and highlighting key concepts like wave-particle duality and superposition. They aim to make the topic accessible and engaging for students, connecting it to real-world applications.",
    ratings: {
      talkSpeed: 140,
      emotion: 4,
      talkTimeRatio: 80,
      fillerWords: 3,
    },
    time: new Date("2024-10-27T14:00:00"),
  },
];

export default function History() {
  return (
    <div className="container">
      <h1 className="heading">Past Sessions</h1>
      {history.map((anal) => (
        <HistoryItem analysis={anal} key={anal.time.toISOString()} />
      ))}
    </div>
  );
}
