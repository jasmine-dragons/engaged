# 🌲 TreeHacks 2025: Teacher Teacher - AI-Powered Classroom Simulation for Smarter Teacher Training

## Inspiration
Every day, teachers step into classrooms filled with students who have different personalities, learning styles, and challenges. Some students are eager to participate, others are easily distracted, and a few might resist authority altogether. A teacher's ability to navigate these interactions can mean the difference between an engaging classroom and a chaotic one.

Yet, there are few opportunities for educators to practice classroom management in a realistic, risk-free setting. So, we asked ourselves: What if teachers could train for the classroom the way pilots train in flight simulators? Could we create an AI-powered environment where educators could interact with dynamic student personalities, receive real-time feedback, and refine their teaching techniques so that they can accel in the classroom?

That’s how we built Teacher Teacher—an interactive classroom simulation that prepares educators for real-world teaching challenges. By leveraging AI-bots that simulate student behaviors and a performance analytics dashboard, Teacher Teacher helps teachers develop strong communication skills, manage classroom dynamics, and build confidence—all in a safe, controlled environment.

We believe that if Teacher Teacher is implemented in teacher training programs and professional development workshops, it could revolutionize how educators prepare for the modern classroom—leading to more engaged students, less burnout, and stronger learning outcomes across the board. 

## What it does


## How we built it

## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for Teacher Teacher

_Training Teachers to Teach using AI._

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
