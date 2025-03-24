import { useEffect, useState } from "react";
import GuessGrid from "./GuessGrid";
import LetterPad from "./LetterPad";
import { snakeToCamel } from "caseparser";
import { Game, User } from "../types";

type ErrorMessage = {
  message: string;
};

const baseEndpoint = "http://localhost:8000/game-engine";

const loadGame = async (): Promise<Game> => {
  const userId: string | null = window.localStorage.getItem("userId");
  if (!userId) {
    const response = await fetch(`${baseEndpoint}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const user: User = await response.json();
    window.localStorage.setItem("userId", user.id);
    return snakeToCamel(user.games[0]);
  }

  let response = await fetch(`${baseEndpoint}/users/${userId}/active-game`);
  if (response.status === 404) {
    response = await fetch(`${baseEndpoint}/users/${userId}/active-game`, {
      method: "POST",
    });
  }

  const game: Game = await response.json();
  return snakeToCamel(game);
};

export default function MainGame() {
  const [game, setGame] = useState<Game | null>(null);
  const [currentGuess, setCurrentGuess] = useState<string>("");
  const [warningMessage, setWarningMessage] = useState<string>("");

  useEffect(() => {
    loadGame().then((data) => {
      setGame(data);
    });
  }, []);

  useEffect(() => {
    setWarningMessage("");
  }, [currentGuess]);

  const handleSubmit = async () => {
    const userId = window.localStorage.getItem("userId");
    const response = await fetch(
      `${baseEndpoint}/users/${userId}/active-game`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ guessed_word: currentGuess }),
      }
    );
    if (response.status === 400) {
      const errorResponse: ErrorMessage = await response.json();
      setWarningMessage(errorResponse.message);
      return;
    }
    const game: Game = await response.json();
    setGame(snakeToCamel(game));
    setCurrentGuess("");
  };

  if (!game) {
    return <div>Loading...</div>;
  }
  return (
    <>
      <h2>Elixir Tech Assessment - Charlie Maunder</h2>
      <GuessGrid game={game} currentGuess={currentGuess} />
      {warningMessage && <h3 style={{ color: "red" }}>{warningMessage}</h3>}
      <LetterPad
        game={game}
        setCurrentGuess={setCurrentGuess}
        handleSubmit={handleSubmit}
      />
      {/* TODO - DRY this up below */}

      {game.gameStatus === "complete" && (
        <>
          <h3>
            Congratulations!
            <p
              onClick={() => window.location.reload()}
              style={{ cursor: "pointer" }}
            >
              Click here to play again.
            </p>
          </h3>
        </>
      )}
      {game.gameStatus === "failed" && (
        <>
          <h3 style={{ color: "red" }}>
            You failed!
            <p
              onClick={() => window.location.reload()}
              style={{ cursor: "pointer" }}
            >
              Click here to play again.
            </p>
          </h3>
        </>
      )}
    </>
  );
}
