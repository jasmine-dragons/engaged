export type StudentTemplate = {
  name: string;
  description: string;
  /** For API only; not user-facing */
  personality: string;
};

export type ClassroomTemplate = {
  name: string;
  /** List of personalities. */
  students: string[];
};

export type Analysis = {
  transcript: { who?: string; what: string }[];
  summary: string;
  ratings: {
    talkSpeed: number;
    emotion: number;
    talkTimeRatio: number;
    fillerWords: number;
  };
};
