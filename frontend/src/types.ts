export type LetterStatus = {
  status: string;
  locations: number[];
};

export type Game = {
  correctWord: string;
  gameStatus: string;
  guessCount: number;
  guessedWords: string[];
  id: string;
  letterStatus: Record<string, LetterStatus>;
  user: string;
};

export type User = {
  id: string;
  games: Game[];
};
