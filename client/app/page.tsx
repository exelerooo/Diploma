"use client";

import { useState } from "react";

const sentimentPics = new Map([
  ["positive", "😁"],
  ["neutral", "😌"],
  ["negative", "😡"]
]);

export default function HomePage() {
  const [prompt, setPrompt] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setSentiment("");
    setExplanation("");

    try {
      const res = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      const jsonResult = JSON.parse(data);
      const sentimentResult = jsonResult.sentiment;
      const explanationResult = jsonResult.explanation;
      setSentiment(sentimentResult + " " + sentimentPics.get(sentimentResult));
      setExplanation("Explanation:" + explanationResult);
    } catch (err) {
      console.error(err);
      setSentiment("Ошибка запроса к серверу");
      setExplanation("");
    } finally {
      setLoading(false);
    }
  };

  return (
      <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-100">
        <div className="w-full max-w-xl bg-white p-6 rounded-xl shadow-lg">
          <h1 className="text-2xl font-bold mb-4 text-center">🔮 Оценка тональности </h1>
          <textarea
              className="w-full border rounded-md p-3 mb-4 resize-none h-32"
              placeholder="Введите ваш запрос (промпт)..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
          />
          <button
              onClick={handleSubmit}
              className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
              disabled={loading}
          >
            {loading ? "Обработка..." : "Сгенерировать"}
          </button>

          {sentiment && (
              <div className="mt-6">
                <h2 className="text-lg font-semibold mb-2">📜 Ответ:</h2>
                <div className="bg-gray-100 p-3 rounded-md text-gray-800 whitespace-pre-wrap">
                  {sentiment}
                </div>
                <div className="bg-gray-100 p-3 rounded-md text-gray-800 whitespace-pre-wrap">
                  {explanation}
                </div>
              </div>
          )}
        </div>
      </main>
  );
}
