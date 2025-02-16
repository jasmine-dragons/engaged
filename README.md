# _engagED_ - AI-Powered Classroom Simulation for Smarter Teacher Training 👩‍🎓👩🏾‍🎓👨🏻‍🎓

🌲 Made for TreeHacks 2025. [Devpost](https://devpost.com/software/teacher-teacher) · [GitHub](https://github.com/jasmine-dragons/treehacks-2025/)

## Inspiration

Every day, teachers step into classrooms filled with students who have different personalities, learning styles, and challenges. Some students are eager to participate, others are easily distracted, and a few might resist authority altogether. A teacher's ability to navigate these interactions can mean the difference between an engaging classroom and a chaotic one.

Yet, there are few opportunities for educators to practice classroom management in a realistic, risk-free setting. So, we asked ourselves: What if teachers could train for the classroom the way pilots train in flight simulators? Could we create an AI-powered environment where educators could interact with dynamic student personalities, receive real-time feedback, and refine their teaching techniques so that they can accel in the classroom?

That’s how we built _engagED_—an interactive classroom simulation that prepares educators for real-world teaching challenges. By leveraging AI-bots that simulate student behaviors and a performance analytics dashboard, _engagED_ helps teachers develop strong communication skills, manage classroom dynamics, and build confidence—all in a safe, controlled environment.

We believe that if _engagED_ is implemented in teacher training programs and professional development workshops, it could revolutionize how educators prepare for the modern classroom—leading to more engaged students, less burnout, and stronger learning outcomes across the board.

## What it does

_engagED_ simulates a classroom environment where teachers interact with AI-powered student personalities, each with unique behaviors, engagement levels, and challenges. The platform allows educators to practice managing real-world classroom dynamics—whether it’s handling a disruptive student, encouraging a quiet learner to participate, or maintaining engagement during a lesson.

_engagED_ responds to natural teacher interactions in a virtual classroom setting, adjusting student behaviors based on teaching strategies. Just like in a real class, students may ask unexpected questions, lose focus, or react differently depending on the teacher’s approach. At the end of each session, _engagED_ provides a performance dashboard, offering insights into key performance metrics and providing feedback for improvement.

## How we built it
_engaged_ was built by a mix of haxers from various backgrounds in frontend and backend roles. We began by wireframing and designing our user workflows, and then iterated upon these designs to create a seamless experience. We used a variety of cutting-edge technologies in this platform, which are outlined below. 

### Design and Wireframing
![image](https://github.com/user-attachments/assets/dc7576bc-e58f-4868-b769-94d4d9266c97)
![image](https://github.com/user-attachments/assets/6c10abff-5699-42a9-800c-e3b1f50f03ae)
![image](https://github.com/user-attachments/assets/53af2792-a776-4cf8-9a06-de68f87da23d)
![image](https://github.com/user-attachments/assets/f597a2bd-fd5a-44c1-b101-8c8d948f9edc)

### Engineering

![image](https://github.com/user-attachments/assets/e406cdbf-61e2-4f4f-95de-2e75e09ab974)
_Our tech flow_

![image](https://github.com/user-attachments/assets/678ddf3b-1be3-4b51-9f38-f948ea1f00a8)
_Client Logic flow_

![image](https://github.com/user-attachments/assets/1756c555-4835-47e7-bdb4-fc44dc4b5589)
__



## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for _engagED_

---

### Setup

![home page](./docs/thubmnail.png)

![results page animation](docs/output.gif)

![results page](docs/results.png)

![new classroom selection page](docs/select-better-draft.png)

![classroom selection page](docs/select-draft.png)

Idea: Simulated environment for teachers to pilot lesson plans / teach different types of students

User flow:

On main dashboard:

1. Specify size of class

1. Specify personality / behavior of students (unengaged, disruptive, not understanding content, etc…)

1. Open up Sim environment

   - Say a zoom meeting with canvas and/or uploaded teacher slides

   - Teacher starts presenting, AI students act on their own and interact with teacher

     - Teacher has to adjust on the fly and figure out how to handle groups of students

   Cap total Video to like 5 minutes

1. On dashboard give feedback on how teacher handled students, how engaging presentation was, etc…can use perplexity

Tech Stack:

- Next.js/React.js Frontend -> Dashboard + Class Session Form
- CrewAI/Langraph Agents -> AI Students
- Deepgram/Google Cloud -> Speech to Text
- ElevenLabs/Cartesia -> Text to Speech
- Groq -> Fast LLM Inference (for AI Agents)
- Evaluation System
  - Transcript of meeting/script -> feed into OpenAI or Perplexity and get qualitative feedback
  - Voice Performance APIs -> get quantitative metrics (https://www.voicebase.com/developer-api-for-speech-analytics/)

## Development

For the backend:

1. Setup `.env`.

1. Install dependencies.

   ```sh
   $ cd backend/
   $ pip install -r requirements.txt
   ```

1. Then start the backend server:

   ```sh
   $ uvicorn main:app --reload
   ```

For the frontend:

1. Install dependencies.

   ```sh
   $ cd client/
   $ npm install
   ```

1. Start the Next.js development server:

   ```sh
   $ npm run dev
   ```
