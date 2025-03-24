import { Dispatch, SetStateAction } from "react";
import { Game, LetterStatus } from "../types";
import "./LetterPad.css";

type LetterPadProps = {
  game: Game;
  setCurrentGuess: Dispatch<SetStateAction<string>>;
  handleSubmit: () => void;
};

type LetterProps = {
  letter: string;
  status: LetterStatus;
  setCurrentGuess: Dispatch<SetStateAction<string>>;
};

function LetterButton({ letter, status, setCurrentGuess }: LetterProps) {
  return (
    <button
      key={letter}
      className={"btn " + status.status}
      onClick={() =>
        setCurrentGuess((prevGuess) =>
          prevGuess.length >= 5 ? prevGuess : prevGuess + letter
        )
      }
    >
      {letter}
    </button>
  );
}

export default function LetterPad({
  game,
  setCurrentGuess,
  handleSubmit,
}: LetterPadProps) {
  return (
    <div className={"container"}>
      {["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"].map((row, rowIndex) => (
        <div key={rowIndex} className="keyboard-row">
          {row.split("").map((letter) => (
            <LetterButton
              key={letter}
              letter={letter}
              status={game.letterStatus[letter] || "default"}
              setCurrentGuess={setCurrentGuess}
            />
          ))}
        </div>
      ))}
      <br />

      <button
        className="btn"
        onClick={() => setCurrentGuess((prevGuess) => prevGuess.slice(0, -1))}
      >
        Backspace
      </button>
      <button className="btn enter" onClick={handleSubmit}>
        Enter
      </button>
    </div>
  );
}
