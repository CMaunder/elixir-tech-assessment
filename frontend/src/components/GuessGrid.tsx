import { Game } from "../types";
import "./GuessGrid.css";
import "./LetterPad.css";

type GuessGridProps = {
  game: Game;
  currentGuess: string;
};

type LetterWithStatus = {
  letter: string;
  status: string;
};

export default function GuessGrid({ game, currentGuess }: GuessGridProps) {
  const rows = 6;
  const columns = 5;

  const getLetterWithStatus = (index: number) => {
    const letters: LetterWithStatus[] = [];
    game.guessedWords.forEach((word) => {
      word.split("").forEach((letter, _) => {
        const letterStatus = game.letterStatus[letter];
        if (letterStatus?.status === "correct") {
          letters.push({
            letter,
            status: letterStatus.locations.includes(index % columns)
              ? "correct"
              : "contains",
          });
        } else {
          letters.push({
            letter,
            status: letterStatus?.status || "",
          });
        }
      });
    });
    currentGuess.split("").map((letter) => {
      letters.push({
        letter,
        status: "",
      });
    });
    return letters[index];
  };

  return (
    <div className="grid">
      {Array.from({ length: rows * columns }).map((_, index) => {
        const letterWithStatus = getLetterWithStatus(index);
        return (
          <b key={index} className={"box " + letterWithStatus?.status}>
            {letterWithStatus?.letter}
          </b>
        );
      })}
    </div>
  );
}
